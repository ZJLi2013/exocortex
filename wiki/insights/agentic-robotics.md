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

### Choose physical experiments by information value

- **Why**: In [[rax]], success on unseen layouts rises from 25% to 79% as exploration grows from 4 to 128 episodes. [[embodiedrsi]] picks the next physical experiment by information gain per unit cost and reaches 72.9% after 50 episodes, against 27.1% with random exploration. Both self-reported.
- **Gap**: RAX's exploration is untargeted and EmbodiedRSI's curve stops at 50 episodes; nobody has shown whether targeted selection changes the slope of the budget curve or only its starting point.
- **First experiment**: Rerun RAX's 4–128 episode sweep with EmbodiedRSI-style hypothesis selection on the same tasks and compare the two curves.

### Hand contact-rich steps to a learned policy

- **Why**: Agents are weakest where contact precision matters: [[hexashell]] scores 32.0% on RoboDojo Precision against 81.0% on Memory (official), and [[embodiedevo]] reports fine insertion and liquid handling as still hard. Hybrids already call VLAs as skills ([[harnesspai]], [[physicalrsi]], [[sensenova-roborsi]]) or let the agent supervise a policy, but [[robodoctor]] picks the controller per task from a fixed warmup threshold, and [[astranomy]]'s Orchestrated mode (66.5%) trails pure Agentic (74.8%).
- **Gap**: No work reports per-capability results showing where a handoff helps; routing happens per task, not per step.
- **First experiment**: On RoboDojo, compare agent-only against agent-plus-VLA-skill per capability dimension (Precision, Long-horizon, Memory), same agent and seeds.

## Open problems

- **Held-out discipline in self-improving loops**: [[harnesspai]]'s 50-seed LIBERO-PRO score includes the 15 seeds its programs evolved on; [[physicalrsi]] does not say whether its select-on-eval set is disjoint from the leaderboard; [[worldscape-r2si]] revises skills on the same layout; [[robodoctor]] keeps the best of several runs. Of the 17 works, only [[hexashell]] was re-evaluated by the benchmark owner on hidden seeds.
- **Knowing whether the task is done**: [[roboquest]] agents decide when to submit, and 23–31% of their failures are wrong decisions; [[aspire]] names success detection and safe reset as what still blocks autonomous real-robot learning; [[embodied-first-exam]] probes its verifiers with an agent trying to pass without doing the task. One capability blocks both evaluation and real-world improvement loops.
- **Memorization in ported benchmarks**: [[embodied-first-exam]] saw Opus 5.5 reproduce a deleted reference solution (26 of 28 lines) and states that single attempts cannot separate model differences from luck; [[roboquest]] also runs each instance once.
- **LIBERO-Pro no longer separates agentic methods**: self-reported 99% ([[aspire]]), 96.5% ([[harnesspai]]) and 94.5% ([[sensenova-roborsi]]), and SenseNova notes its Task/Swap subset differs from the official five-perturbation total, so the numbers are not comparable either.
- **Real-robot evidence is thin**: [[embodiedrsi]] evolves in simulation and deploys zero-shot on five SO-101 tasks; [[rax]] relies on operator resets; [[sensenova-roborsi]] shows real-robot demos without success rates; [[robodojo]]'s real-robot leaderboard has one visible entry.

## Predictions

| Prediction | Due | Basis | Result |
|---|---|---|---|
| SenseNova-RoboRSI's official RoboDojo-Sim success rate comes in at least 5 points below its self-reported 54.17% | 2027-01-31 | [[sensenova-roborsi]] | pending |
| An official RoboDojo-Sim entry reaches a 60% success rate | 2027-06-30 | [[robodojo]], [[hexashell]] | pending |
| A RoboLab-120 result at ≥ 70% success reports ≤ $5 per successful episode | 2027-06-30 | [[astranomy]] | pending |
| The best Embodied First Exam standard-mode score reaches 50% | 2027-07-31 | [[embodied-first-exam]] | pending |
| The best RoboQuest success rate reaches 40% | 2027-10-15 | [[roboquest]] | pending |
