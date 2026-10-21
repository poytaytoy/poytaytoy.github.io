---
title: 'Q4_K and Q6_K Quantization in Llama.cpp'
date: 2026-10-16
draft: false
description: 'Notes on how Q4_K and Q6_K quantization work in llama.cpp.'
tags: ['LLMs', 'Quantization', 'C++', 'llama.cpp', 'inference']
---

When I was working on my inference engine for Qwen3-4B-Q4_K_M, there were little details on Q4_K and Q4_6 quantization. It turns out it was developed within this [PR](https://github.com/ggml-org/llama.cpp/pull/1684). There weren't any formal papers on this as it was a clever idea by someone. While there are `Q2_K`, `Q3_K`, ..., `Q4_K`, and `Q6_K` with each being slightly different, I'm only going to focus on `Q4_K` and `Q6_K`. Hopefully with these two, you could figure out the rest.

## What is quantization? 

Let's start with the basics. By definition, quantization is about taking something a large set and mapping it to a small output set. For example, casting a double to a float could be considered a form of quantization, noting that we constrain doubles within the range of float. The goal is that while we lose the decimal precision of a double, we also use half as much memory. In case of local inferencing, quantization always comes down to using less VRAM(GPU RAM) from models that otherwise would not fit a standard PC's 8-32GB. 

## Q4_K memory layout

With this, let's examine how Q4_K compresses float values. Let's look at an example from Qwen3-4B-Q4_K_M's [gguf](https://huggingface.co/Qwen/Qwen3-4B-GGUF/blob/main/Qwen3-4B-Q4_K_M.gguf). The "blk.0.attn_k.weight" has dimensions of 2560 by 1024 in Q4_K. Let's examine the first 144 bytes of it: 

```
| 0-1 bytes | 2-3 bytes | 4-15 bytes | 16-143 bytes | 
|     d     |   dmin    |   scales   |      qs      | 
```
Source: [https://github.com/ggml-org/llama.cpp/blob/master/ggml/src/ggml-common.h#L323-L338]. 

To start, `d` and `dmin` are two FP16 (or half) values. Meanwhile, `scales` is a group of 16 6-bit numbers. Lastly, `qs` contains 256 of the quantized weights in 4-bits unsigned integer. As you may noticed, each 256 consecutive number within the weights get its own set of quantization. Within every 32 of consecutive of the, they get their own assigned scales. We will focus on the dequantization compute later. For now, we focus on the memory layout of `scales` and `qs`.

For `scales`, it contains 8 minimums and 8 scales. Layout as follows, 

```
               7  6 | 5  4  3  2  1  0
              ------+------------------
scales[0]      S4 H |       S0
scales[1]      S5 H |       S1
scales[2]      S6 H |       S2
scales[3]      S7 H |       S3
              ------+------------------
scales[4]      M4 H |       M0
scales[5]      M5 H |       M1
scales[6]      M6 H |       M2
scales[7]      M7 H |       M3
              ------+------------------

               7  6  5  4 | 3  2  1  0
              ------------+------------
scales[8]        M4 L     |    S4 L
scales[9]        M5 L     |    S5 L
scales[10]       M6 L     |    S6 L
scales[11]       M7 L     |    S7 L
```

Does it feel awkward? This is necessary because each byte holds 8-bits while the values in scales are 6-bits. To get S0-3 and M0-3, cast scales into a `char*`(c) or `std::bytes*`(cpp) pointer and only use the last 6 bits of its index position. For the rest however, we note that we need to assemble them into, for example,

```
      5 4  | 3 2 1 0
M4 =  M4 H    M4 L 
```

We essentially need to take the stray 2 bits from byte 0-7 and assemble them into the appropriate remaining 4 bits in bytes 8-11. Each S# is a scale and each M# is a minimum. We'll define their use later. 

For `weights`, for the 256 4-bit weights, we view them as 8 groups of 32 weights with each group. And each 64 weights have the layout as follows: 

```
            Bits 7–4    | Bits 3–0
           -------------+----------
qs[0]        Weight 32  | Weight 0
qs[1]        Weight 33  | Weight 1
qs[2]        Weight 34  | Weight 2
...                     |
qs[31]       Weight 63  | Weight 31
           -------------+----------
```

It's another weird layout right??? I bet you're wondering why do this for 4-bits?? After all why couldn't they align them consecutively such as: 

```
            Bits 7–4    | Bits 3–0
           -------------+----------
qs[0]        Weight 0   | Weight 1
qs[1]        Weight 2   | Weight 3
...                     |
           -------------+----------
```

It comes does to optimizing the GPU access pattern, more specifically memory coalescense. We will explore this further in our matmul kernels later. For now, just acknowledge this weird layout. That said, code-wise, it is fairly easy to implement. From weights 0-31, use the low 3-0 bits of each byte for 31-63, use the high 7-4 bits of each byte. 

## Dequantization 

Now that we know each value, let us calculate the dequantized value of weight 0 (W0). `0 / 8 = 0`, so we use S0 and M0. Then we calculate: 

```
float w_i = (d * S0) * W0 - (dmin * M0)
```
 
Then tada! We get what the dequantized value for `w_i` is. As you may have noticed, Q4_K lets regions of high value ranges not affect other ranges accuracy! To elaborate, if a value range becomes really really high, we can image `(d * S0)` is stretched much further. In other words, it meant that we lose more precision as the spacing increases. Anyhow, let us make a simple function that gives us this conversion given a 256 block of Q4_K and an index within: 

```cpp
float dequantize_q4k(std::bytes* block, int index){

    // take d and dmin directly by the location. 
    // fp16 is not a supported type on all compiler. I'm using cuda's _half2float here
    // but feel free to substitute it with anything similar
    float d = _half2float(block[0]);
    float dmin = _half2float(block[1]);

    //The calcualte for S# and M#
    std::bytes* scale = block + 4; 
    uint8_t S;
    uint8_t M; 
    int group = index / 32; 

    if (group < 4) {
        // These values are stored contiguously, so you simply access its location 
        S = scales[group] & 0x3F;
        M = scales[group + 4] & 0x3F;
    } else { 
        // Access and perform bit operation to combine the high and low 
        S = (scales[group + 4] & 0x0F) | ((scales[group - 4] >> 6) << 4);
        M = (scales[group + 4] & 0xF0) | ((scales[group] >> 6) << 4);
    }   

    // Gets the weight by accessing its appropriate index location then
    // either shift down if high or cast the first 4 bit to 0
    std::bytes* qs = block + 16;
    int weight_index = (index / 64) * 32 + (index % 32);
    bool high = (index % 64 > 31); 
    uint8_t W; 

    W = high ?  qs[weight_index] >> 4 : qs[weight_idnex] & 0x0F;

    // dequantize formula 
    return (d * S) * W - (dmin * M);
}
```
