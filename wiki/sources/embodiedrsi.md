---
type: source
url: https://arxiv.org/abs/2610.10498
published: 2026-10
ingested: 2026-10-16
tags: []
concepts: [选出集合与确认集合分离, 人定义评估与验收, 自改进, 按信息价值选实验]
benchmarks: ["[[RoboCasa365]]", "[[LIBERO-Pro]]"]
methods: ["[[harness evolution]]", "[[code skills from experience]]"]
models_used: ["[[SmolVLA]]", "[[Qwen3.5-122B-A10B]]", "[[Qwen3-Embedding-0.6B]]"]
models_compared: ["[[OpenVLA]]", "[[π0]]", "[[π0.5]]"]
lenses: ["[[agentic-robotics]]"]
---
# EmbodiedRSI

冻结 VLA 外的 agentic harness 用 Hypothesis Graph 维护代码 / 技能假设，按「信息增益 / 实验成本」选下一次物理实验，代码与技能联合演化；RoboCasa365 总成功率 77.0%。

- **关键数字**：
  - RoboCasa365：总体 77.0%，Composite-Unseen 71.3%；最强基线 Harness VLA 为 63.6% / 40.1%。
  - LIBERO-Pro（T / S 扰动 8 格）：86.8%，Harness VLA 72.1%。
  - 真机 SO-101 + SmolVLA，5 个任务各 30 次：SmolVLA 单独 46.0% → 加 harness 71.3%；harness 全在仿真里演化后零样本部署。Glasses Bridge Grasp 一项下降（60.0% → 56.7%）。
  - 50 个物理 episode 后：72.9% vs 随机探索 27.1%，learning AUC 0.635 vs 0.309。
  - 记忆消融（Composite-Unseen）：检索式 61.7%、PPO 只用任务奖励 65.2%、完整方法 71.3%。
- **评估与接纳**：
  - 每个任务演化用 10 个 seed，所有方法在另外 10 个互不相交的 seed 上评测，每 seed 10 次试验。
  - 成功为 benchmark 的二值任务结果；判定器由谁实现未说明。真机成功由谁判定未说明。
  - agent 不能改机器人基座模型：VLA 全程冻结，只改代码、技能与记忆。真机 SmolVLA 先用每任务 50 条遥操作示范全量微调 20,000 步，再冻结。
  - 假设靠 matched trial 判定：同一初始状态、其余调用及顺序不变，比较成功率差；消融时 VLA、任务集、物理实验预算与评估协议固定。
- **可信度**：作者自报；未给多次运行或方差；基线数字是否复现未说明；代码是否开源未说明。
- **模型**：真机底座 SmolVLA；冻结 Qwen3.5-122B-A10B 做更新算子，Qwen3-Embedding-0.6B 做编码；LIBERO-Pro 对照冻结 VLA OpenVLA、π0、π0.5。
- **原文**：[[raw/embodiedrsi]]
