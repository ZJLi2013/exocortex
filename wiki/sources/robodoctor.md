---
type: source
url: https://robodoctor-rsi.github.io/
published: unknown
ingested: 2026-10-21
tags: [agentic-robotics]
concepts: [自改进, 策略主导与 agent 主导控制切换, 干预经验记忆]
benchmarks: ["[[RoboDojo]]"]
methods: []
models_used: ["[[prismwam]]"]
models_compared: []
lenses: ["[[agentic-robotics]]"]
---
# RoboDoctor

冻结的 PrismWAM 出动作块，agent（Doctor）审查、修正或接管；先跑 3 回合 Warmup，均分 ≥ 30 留在策略主导，否则转 agent 主导，之后靠回合间更新的干预与操作经验改进。RoboDojo 54 个任务本地 Refinement 平均分 57.10、成功率 49.44%。

- **关键数字**：
  - RoboDojo 54 个任务（本地）：Warmup 49.74 / 40.83%，Refinement 57.10 / 49.44%；Open 维度 29.17 → 50.52。
  - 页面同图引官方榜（2026-10-20 快照）：HexaShell-Preview 53.18 / 46.85%，EmbodiedEvo 45.08 / 38.95%。
- **评估与接纳**：每回合由 RoboDojo 自带评测器打分；同一任务连续跑 9 回合（Warmup 0–2、Refinement 3–8）；每个任务每轮取多次运行里最高的有效分。
- **可信度**：作者自报；页面自承本地结果与官方全量分口径不同、回合数不等，Refinement 计划 324 回合只得到 301 回合，不能当同口径排名；没有消融。harness 修订在报告的实验里只是两种预设 harness 按固定 Warmup 阈值二选一。页面未写日期。
- **模型**：PrismWAM 是冻结的低层策略；Doctor 的模型未说明，权重不变。

## 关联

- 对照 [[hexashell]]：同图引 RoboDojo 官方榜 HexaShell-Preview 53.18 / 46.85%，RoboDoctor 本地 Refinement 57.10 / 49.44%。
- 对照 [[embodiedevo]]：同图引官方榜 EmbodiedEvo 45.08 / 38.95%。
