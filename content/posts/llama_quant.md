---
title: 'Q4_K and Q6_K Quantization in Llama.cpp'
date: 2026-10-16
draft: true
description: 'Notes on how Q4_K and Q6_K quantization work in llama.cpp.'
tags: ['LLMs', 'Quantization', 'C++', 'llama.cpp', 'inference']
---

When I was working on my inference engine for Qwen3-4B-Q4_K_M, there was absolutely no blog or documentation on what on earth is Q4_K and Q4_6 quantization. The best I found was some github PR 3 years ago that basically summarize to someone saying I made it up. That said, it was an ingenious strategy than regular quantization, so I'm going to go over indepth, so any poor soul out there won't have to go through the same mess I did. 

