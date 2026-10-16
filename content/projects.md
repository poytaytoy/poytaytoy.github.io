---
title: Projects
description: Software, tools, and experiments I've built.
ShowToc: false
ShowReadingTime: false
hideMeta: true
---

A list of stuff I've built. I like tinkering around with hardware, systems programming, and lately, I've been really getting into GPU programming! 
<br>

Feel free to [browse my GitHub](https://github.com/poytaytoy?tab=repositories).

{{< project-row >}}

{{< project-copy >}}

*October 2026*

## Qwen inference engine

A C++20 and CUDA inference engine for the quantized Qwen3-4B model. The implementation includes GGUF model loading, tokenization, GPU kernels, and cached decoding, with tests and benchmarks for individual components. I made some custom kernels that let me reach around 63 token/s, around *91%* of llama.cpp. 

[Source on GitHub](https://github.com/poytaytoy/Qwen3-4B-Q4_K_M-Inference-Engine)

{{< project-tags "C++" "CUDA" "LLM inference" "GPU computing" >}}

{{< /project-copy >}}

{{< /project-row >}}

{{< project-row >}}

{{< project-image src="/images/projects/blimpy.jpg" alt="Blimpy balloon robot with its suspended electronics and propellers at Hack the North" kind="screenshot" >}}

{{< project-copy >}}

*September 2026*

## Blimpy

A floating robot companion built at Hack the North 2026, combining ESP32 motor control, computer vision, and voice interaction. I primarily worked on the ESP32 controls. We didn't win, but its still super cool to make a big balloon move.

[Project on Devpost](https://devpost.com/software/blimpy)

{{< project-tags "Robotics" "ESP32" "Computer vision" "Voice AI" >}}

{{< /project-copy >}}

{{< /project-row >}}


{{< project-row >}}

{{< project-image src="/images/projects/buzzkill-product.jpg" alt="Buzzkill hackathon prototype with camera, turret, wiring, and Raspberry Pi" kind="screenshot" >}}

{{< project-copy >}}

*July 2026*

## Buzzkill

A Hack the 6ix 2026 team project exploring mosquito detection and tracking with computer vision and a pan-and-tilt foam-dart turret. The prototype combines OpenCV, a Raspberry Pi running QNX, and ESP32-based control. We made a 3am mosquitto shooter idea into reality.

**Award:** QNX: Best Use of QNX.

[Project on Devpost](https://devpost.com/software/buzzkill-ig3p0b)

{{< project-tags "Robotics" "Computer vision" "QNX" "ESP32" >}}

{{< /project-copy >}}

{{< /project-row >}}

{{< project-row >}}

{{< project-image src="/images/projects/mathphic-demo.jpg" alt="Mathphic interface showing the prompt input, settings, and graph canvas" kind="screenshot" >}}

{{< project-copy >}}

*March 2026*

## Mathphic

A Hack Canada 2026 team project that turns natural-language questions into narrated mathematical visualizations. Built with Next.js, FastAPI, Desmos, and a small scripting language called Desq, with Gemini and Claude generating the explanations and visual scripts.

**Award:** Most technically complex AI hack.

[Project on Devpost](https://devpost.com/software/mathphic)

{{< project-tags "AI" "Math visualization" "Next.js" "FastAPI" >}}

{{< /project-copy >}}

{{< /project-row >}}

{{< project-row >}}

{{< project-image src="/images/projects/pid.png" alt="PID simulator showing controller tuning, robot position, and camera view" kind="screenshot" >}}

{{< project-copy >}}

*January 2026*

## PID simulator

An interactive C++ and OpenGL simulator for exploring PID control. A simulated robot uses translational and rotational controllers to follow a target, making it easier to see how tuning affects movement. I used it for swerve drive simulation way back. 

[Source on GitHub](https://github.com/poytaytoy/pid_sim)

{{< project-tags "C++" "OpenGL" "Control systems" "Robotics" >}}

{{< /project-copy >}}

{{< /project-row >}}

{{< project-row >}}

{{< project-copy >}}

*December 2025*

## DingleBob

A small programming language I made in Rust. I was trying to learn all about programming languages. I also made a small web IDE so anyone can run some stuff on it. 

[Language source](https://github.com/poytaytoy/DingleBob) · [Playground source](https://github.com/poytaytoy/dinglebob_playground)

{{< project-tags "Rust" "Programming languages" "Interpreter" "Web IDE" >}}

{{< /project-copy >}}

{{< /project-row >}}

{{< project-row >}}

{{< project-copy >}}

*June 2025*

## Devvy

A SpurrHacks 2025 team project built around project-based coding challenges and GitHub repositories. The stack combines React, FastAPI, Supabase, and Docker.

[Source on GitHub](https://github.com/poytaytoy/devvy)

{{< project-tags "React" "FastAPI" "Docker" "Developer tools" >}}

{{< /project-copy >}}

{{< /project-row >}}

{{< project-row >}}

{{< project-image src="/images/projects/spacey.png" alt="Spacey3D displaying a plane, line, and vector in three dimensions" kind="screenshot" >}}

{{< project-copy >}}

*September 2024*

## Spacey3D

A JavaFX application for visualizing linear algebra in three dimensions: vectors, spans, planes, and linear transformations. Made it when I was obsessed with learning linear algebra in grade 11. 

[Source on GitHub](https://github.com/poytaytoy/Spacey3D)

{{< project-tags "Java" "JavaFX" "Linear algebra" "3D visualization" >}}

{{< /project-copy >}}

{{< /project-row >}}

{{< project-row >}}

{{< project-image src="/images/projects/faris-demo.jpg" alt="Faris chatbot interface from the original YouTube demo" kind="screenshot" >}}

{{< project-copy >}}

*June 2023*

## Faris chatbot

A conversational web app with an animated Live2D character. It combines a React and TypeScript frontend with a Python backend; the updated backend uses FastAPI and Groq-hosted language models. Heavily inspired by Neuro-sama at the time. I even configured the same Azure voice to her. 

[Source on GitHub](https://github.com/poytaytoy/Project-Faris-Chatbot-)

{{< project-tags "React" "TypeScript" "Live2D" "Conversational AI" >}}

{{< /project-copy >}}

{{< /project-row >}}

{{< project-row >}}


{{< project-copy >}}

*April 2023*

## FRC scouting website

A scouting web app built for team 2198 during the 2023 Charged Up season. It uses Python and Flask with Google Sheets to collect and organize scouting data.

[Source on GitHub](https://github.com/poytaytoy/Scouting-Website-2198---Charged-Up-2023)

{{< project-tags "Python" "Flask" "FRC robotics" "Google Sheets" >}}

{{< /project-copy >}}

{{< /project-row >}}

---

This notebook is also [open source](https://github.com/poytaytoy/poytaytoy.github.io), built with Hugo and PaperMod.
