---
type: insight
lens: "[[agentic-robotics]]"
updated: 2026-10-22
---
# agentic-robotics: insight

## Directions

### Give the agent state estimation, not more reasoning

- **Why**: The top agent in [[embodied-first-exam]] solves 75.5% with privileged simulator state but 33.8% through the robot API. In [[roboquest]], 43–46% of failures are missing evidence, while the execution skills pass 72–81% once the hidden information is given. [[astranomy]] lifts Direct control from 19.3% to 72.7% by writing gripper and camera geometry into the prompt, and [[hexashell]] builds its own dual-view triangulation tool. All self-reported except HexaShell's official score.
- **Gap**: No work isolates a perception layer: nobody gives the same agent estimated object poses as a tool and measures how much of the privileged–standard gap closes.
- **First experiment**: On the Embodied First Exam standard split, add a pose-estimation and multi-view triangulation tool to the agent's API; report, per suite, the fraction of the 75.5% → 33.8% gap recovered.

### Treat the agent loop as a data engine for a cheap policy

- **Why**: Agent control is expensive: [[astranomy]] spends 30.9M tokens ($36.40) per successful Agentic episode against $1.96 for Direct. Works that amortize the agent report large gains: [[rax]] compiles exploration into programs that run 103–241× faster; [[harnesspai]] fine-tunes π0.5 on its collected trajectories, 34.9% → 73.7% on LIBERO-PRO; [[sensenova-roborsi]] trains a 27B model on verified traces (RoboCasa365 26.0% → 46.5%, output tokens −73.3%); [[worldscape-r2si]] trains its action model on execution records. All self-reported.
- **Gap**: No work compares the three amortization targets (compiled program, fine-tuned VLA, distilled VLM) under one trace budget on held-out layouts, with cost per success reported.
- **First experiment**: From one agent run's verified traces, build all three and evaluate them on the same held-out RoboDojo layouts; report success rate and dollars per success.

### Hand contact-rich steps to a learned policy

- **Why**: Agents are weakest where contact precision matters: [[hexashell]] scores 32.0% on RoboDojo Precision against 81.0% on Memory (official), and [[embodiedevo]] reports fine insertion and liquid handling as still hard. Hybrids already call VLAs as skills ([[harnesspai]], [[physicalrsi]], [[sensenova-roborsi]]) or let the agent supervise a policy, but [[robodoctor]] picks the controller per task from a fixed warmup threshold, and [[astranomy]]'s Orchestrated mode (66.5%) trails pure Agentic (74.8%).
- **Gap**: No work reports per-capability results showing where a handoff helps; routing happens per task, not per step.
- **First experiment**: On RoboDojo, compare agent-only against agent-plus-VLA-skill per capability dimension (Precision, Long-horizon, Memory), same agent and seeds.

## Open problems

- **Held-out discipline in self-improving loops**: [[harnesspai]]'s 50-seed LIBERO-PRO score includes the 15 seeds its programs evolved on; [[physicalrsi]] does not say whether its select-on-eval set is disjoint from the leaderboard; [[worldscape-r2si]] revises skills on the same layout; [[robodoctor]] keeps the best of several runs. Of the 17 works, only [[hexashell]] was re-evaluated by the benchmark owner on hidden seeds.
- **Knowing whether the task is done**: [[roboquest]] agents decide when to submit, and 23–31% of their failures are wrong decisions; [[aspire]] names success detection and safe reset as what still blocks autonomous real-robot learning; [[embodied-first-exam]] probes its verifiers with an agent trying to pass without doing the task. One capability blocks both evaluation and real-world improvement loops.
- **Real-robot evidence is thin**: [[embodiedrsi]] evolves in simulation and deploys zero-shot on five SO-101 tasks; [[rax]] relies on operator resets; [[sensenova-roborsi]] shows real-robot demos without success rates; [[robodojo]]'s real-robot leaderboard has one visible entry.
