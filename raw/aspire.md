---
url: https://research.nvidia.com/labs/gear/aspire/
fetched: 2026-10-16
title: "ASPIRE: Agentic /Skills Discovery for Robotics"
---

# Auto Discover /skills for Robots

## Abstract (introText, rendered by js/config.js)

Traditional robot programming is notoriously challenging: it requires orchestrating multimodal perception, managing complex physical contact dynamics, and handling diverse environment configurations and execution failures. We introduce ASPIRE (Agentic Skill Programming through Iterative Robot Exploration), a continual learning system for robotics that autonomously writes and refines robot control programs in a code-as-policy paradigm while compounding experience into a reusable skill library. ASPIRE enables automated discovery of reusable skills that persist across multiple tasks, simulation and real-world settings, and different embodiments. Rather than relying on fixed, human-engineered pipelines, ASPIRE operates in an open-ended learning loop, consisting of three key components: (1) a closed-loop robot execution engine that exposes fine-grained multimodal traces (e.g., perception overlays, grasp candidates, motion trajectories, and collision feedback), enabling the agent to autonomously diagnose failures, synthesize repairs, and validate outcomes; (2) a continually expanding skill library that distills validated fixes into reusable, transferable robotic knowledge; and (3) an evolutionary search procedure that generates diverse programs, systematically debugging them to explore beyond single-trajectory refinement. As ASPIRE encounters more tasks, its growing skill library enables increasingly rapid adaptation. Consequently, ASPIRE surpasses prior methods by up to 77% on manipulation tasks under perturbation, 72% on Robosuite’s bimanual handover task, and up to 32% on long-horizon household tasks. The accumulated skill library further enables strong zero-shot generalization: on representative unseen long-horizon tasks, ASPIRE achieves 31% success, substantially outperforming the 4% success rate of prior methods despite their heavy reliance on test-time reasoning and retries. Performance scales with the capabilities of frontier models. With Claude Opus 5.5, ASPIRE nearly saturates these benchmarks, achieving 99% average success across all 80 LIBERO-Pro tasks and 100% success on representative Robosuite and BEHAVIOR-1K tasks. Beyond simulation, skills discovered in simulation reduce real-world robot programming effort across embodiments and robot APIs, while skills acquired through online interaction with physical robots enable ASPIRE to solve a Rubik’s Cube with progressively improving efficiency.

Cross-Embodiment Sim-to-Real: Long Horizon Table Bussing Claude Opus 4.6 (sim), GPT-5.5 (real)

Online Learning in Real: Solve the Rubik’s Cube GPT-6 Astra

Unscrew the bottle cap

Put the pill in the bottle and screw on the cap

Stack all the cups upside-down into a pile

## Method: How ASPIRE Works

ASPIRE is a self-improving continual learning system for robotics that writes and refines code-as-policy robot control programs from execution feedback. It inspects rollout traces, diagnoses failures, repairs programs, validates corrected behaviors, and saves reusable skills for future tasks. ASPIRE operates in an open-ended learning loop with three key components: a closed-loop robot execution engine , a continually expanding skill library , and an evolutionary search procedure.

### Closed-Loop Robot Execution Engine

For each perception, planning, grasping, and control call, the engine records the observations, inputs, outputs, and visual evidence if possible. These rich multimodal traces allow the agent to selectively inspect salient primitive logs, progressively localize failures, and validate repairs through re-execution.

### Continually Expanding Skill Library

ASPIRE maintains a growing skill library that distills validated fixes into modular, transferable robotic knowledge retrievable as in-context guidance for future tasks.

### Evolutionary Search Over Programs

ASPIRE employs an evolutionary search procedure that generates diverse task sequences and control programs, exploring beyond single-trajectory self-improvement through iterative debugging and parallel refinement.

## Task Gallery

Each card shows either a real-robot example of ASPIRE or a CaP-Agent0 baseline or initial task attempt paired with the final behavior after ASPIRE diagnosed the rollout and rewrote the program. Hover over a demo video to view the baseline or initial program and the ASPIRE fix code. Use the filters to narrow the gallery. This is not an exhaustive list of all tasks.

## Skill Library Gallery

Explore the expansive skill library learned by ASPIRE. Each card groups many related skills. This is a representative sample, not an exhaustive list.

## Benchmark Results

## ASPIRE Improves with Stronger Models

We tested ASPIRE across a full suite of recent frontier models, including GPT-6 Astra, Claude Opus 5.5, Claude Sonnet 5.5, Claude Fable 5.1, and open-weight models such as Kimi K3 and Qwen 3.8 Max, while holding the environment, robot programming API, and evaluation protocol fixed.

### Success vs. Cost Frontier

Evaluation is run on 10 LIBERO-Pro tasks.

## Online Skill Learning on a Real Robot

ASPIRE also runs online on a real robot: the coding agent acts as a system-2 that calls executable perception and action tools and records what it learns as text skills.

### Efficiency Across Episodes

Tokens and wall-clock time per completed face turn fall across episodes as context and skills accumulate. Values are full-episode amortized, including failed attempts, recovery, and context compaction.

Example Rubik’s Cube Turns

## Case Study: Five Models Across Four Tasks

Each video compares the human teleoperation demonstration from the original LIBERO dataset with a held-out evaluation episode of the ASPIRE program written by each model: Claude Opus 4.6, Claude Opus 5, Claude Opus 5.5, and GPT-6 Astra.

## Main Evaluation Results

We show ASPIRE with Claude Opus 4.6, GPT-6 Astra, and Claude Opus 5.5 (Opus 5.5 was not evaluated on BEHAVIOR-1K). ASPIRE learns on a small debug split and reports success on disjoint held-out evaluation seeds, while CaP-Agent0 regenerates a program for each seed with test-time reasoning and retries.

### LIBERO-PRO

LIBERO-Pro Object / Goal / Spatial under position perturbations (shifted object positions) and task perturbations (perturbed instructions): 160 tasks, each evaluated on 50 held-out seeds.

### Robosuite

ASPIRE handles contact-heavy tabletop manipulation tasks. Each task is evaluated on 100 held-out seeds.

### BEHAVIOR-1K

BEHAVIOR-1K tests long-horizon mobile manipulation. Each task is evaluated on 25 held-out seeds.

## Zero-Shot Transfer of Skill Library

### Scaling with Skill-Library Size · LIBERO-Pro Long

Skills learned across LIBERO-90 carry over to held-out long-horizon tasks. As the skill library grows, coding agents achieve higher success rate on LIBERO-Long.

### Real-Robot Cross-Embodiment Skill Transfer

For each task, we compare real-robot debugging with and without retrieving a corresponding simulation-discovered skill from ASPIRE’s library. Token counts are measured until the first successful real-robot program. Success Rate reports held-out evaluation trials of the code that achieved that first success. When equipped with ASPIRE skills, the coding agent reaches its first success with fewer tokens, and the generated code achieves a higher success rate.

Output tokens (M)

Total tokens (M)

Held-out success rate (%)

## Model Ablation

### Model Ablation · LIBERO-Pro

LIBERO-Pro Goal / Spatial / Object / Long under task and position perturbations: 160 tasks, each evaluated on 50 held-out seeds.

## Limitations

- Not yet a fully autonomous real-world learner. Real-world deployment still needs robust success detection, safe resets, safety monitoring, and calibration.

- Dependence on a frozen frontier LLM. ASPIRE relies on a frontier model (Claude Opus 4.6); we have not verified that smaller or weaker LLMs can sustain the debugging loop.

- Bounded by a predefined primitive API. The fixed set of perception, planning, and control primitives keeps debugging safe but limits expressible behaviors.

- Incomplete long-term memory management. The skill library currently prioritizes validated reusable repairs but does not fully solve long-term memory management. As the library grows, some entries may become stale, overly specific, redundant, or misleading for a new task.

- Compute-intensive search loop. The debug and evolutionary-search loop costs many LLM calls and rollouts per task, so scaling up will require cheaper inference or more sample-efficient search.

## Conclusion

We present ASPIRE, a self-improving continual learning robotic system that autonomously writes and refines robot control programs while compounding experience into a reusable skill library. ASPIRE operates in an open-ended learning loop with three components: a closed-loop robot execution engine that exposes fine-grained multimodal traces, a continually expanding skill library that distills validated fixes into transferable knowledge, and an evolutionary search procedure that explores diverse task sequences and control programs. Across diverse benchmarks, ASPIRE substantially outperforms existing VLA and coding-agent baselines, demonstrates strong zero-shot transfer to unseen long-horizon tasks, and provides initial evidence that the skills discovered in sim can transfer across embodiment to significantly reduce real-robot programming token cost despite different robot embodiments and APIs.

## Team

Runyu Lu *†

Yubo Wu *

Ethan Kou *

Haotian Lin *

Max Fu

Wenli Xiao

Ajay Mandlekar

Yinzhen Xu

Guanya Shi

Ken Goldberg

Ang Chen

Mosharaf Chowdhury

Jan Kautz

Yuke Zhu †

Linxi “Jim” Fan †

Guanzhi Wang †

* Equal contribution · † Project leads

## BibTeX

@article{lu2026aspire, title = {ASPIRE: Agentic /Skills Discovery for Robotics}, author = {Runyu Lu and Yubo Wu and Ethan Kou and Haotian Lin and Letian Fu and Wenli Xiao and Ajay Mandlekar and Yinzhen Xu and Guanya Shi and Ken Goldberg and Ang Chen and Mosharaf Chowdhury and Jan Kautz and Yuke Zhu and Linxi "Jim" Fan and Guanzhi Wang}, year = {2026}, journal = {arXiv preprint arXiv:2607.00272}, url = {https://arxiv.org/abs/2607.00272} }

## Acknowledgments

We thank Nadun Ranawaka, Jimmy Wu, Matin Furutan, Abhi Maddukuri, Yulu Gan, Matin Nikoui, and Yuqi Xie for their help with open-source support, real robot infrastructure, advice and guidance on the paper, website release, and experimental equipment. We are also grateful to the members of NVIDIA GEAR, UMich SymbioticLab, UsesysLab, UC Berkeley AUTOLab, CMU LeCAR Lab for their kind support.
