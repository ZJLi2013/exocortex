---
type: source
url: https://arxiv.org/abs/2609.29166
published: 2026-09-24
ingested: 2026-10-19
tags: [agentic-robotics]
concepts: [开环执行闭环改程序, VLA 当技能调用, 成功轨迹反哺微调]
benchmarks: ["[[LIBERO-Pro]]", "[[RoboCasa]]", "[[BEHAVIOR-1K]]", "[[Robosuite]]"]
methods: ["[[harness evolution]]", "[[code skills from experience]]"]
models_used: ["[[π0.5]]"]
models_compared: ["[[OpenVLA]]", "[[WorldDreamer]]"]
lenses: ["[[agentic-robotics]]"]
---
# HarnessPAI

一次 rollout 内程序固定，多次 rollout 之间用执行反馈改代码；不重训底层模型时，LIBERO-PRO 比 π0.5 高 61.6 个点。

- **关键数字**：
  - LIBERO-PRO 相对 π0.5 +61.6 个点，并报保持 96.5%（Object / Goal / Spatial，Swap 与 Task，每套 10 个任务、每任务 50 个 layout seed；程序在前 15 个 seed 上演化，再原样跑满 50 个）。
  - RoboCasa Atomic-Seen：WorldDreamer 65.0% → 套上闭环代码后 92.2%（+27.2；18 个任务，20 个 seed）。
  - 用收集的轨迹微调 π0.5，LIBERO-PRO 从 34.9% 到 73.7%（摘要写 +38.8 个点）。
  - robosuite 七任务平均 96.3%，高于论文所引 ASPIRE 的 81.0%。
- **评估与接纳**：作者自报。LIBERO / LIBERO-PRO 的 50-seed 评测含演化用过的 15 个 seed。
- **可信度**：arXiv:2609.29166v1，2026-09-24；作者自报。编码 agent 的底座未说明。
- **模型**：π0.5 是被程序调用的动作模型，也是对照基线。WorldDreamer 是另一被包裹的动作模型。

## 关联

- 对照 [[aspire]]：同文写 ASPIRE 在 LIBERO-PRO 上到 72%，HarnessPAI 报 96.5%；robosuite 上写 ASPIRE 81.0%、HarnessPAI 96.3%。
