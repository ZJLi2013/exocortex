---
type: source
url: https://github.com/RoboValue-Benchmark/RoboValue
published: 2026-10-19
ingested: 2026-10-21
tags: []
concepts: [价值模型评测, 仿真与真机统一评测, 隐藏评测器, 公开排行榜]
benchmarks: []
methods: []
models_used: ["[[LIV]]", "[[ProcVLM]]", "[[Robo-Dopamine]]", "[[RoboFAC]]", "[[Robometer]]", "[[RoboReward]]", "[[RynnValue]]", "[[TOPReward]]", "[[VLAC]]"]
models_compared: []
lenses: []
---
# RoboValue

评测机器人价值模型（从观测与指令判断任务成功与进度的模型）的仿真加真机 benchmark：15 个仿真任务、20 个真机任务，按任务状态理解、时序进度跟踪、失败与恢复判断、价值一致性四个维度评测。

- **关键数字**：
  - Overall（四个能力分的均值）：Zero-Shot 12 个变体中 RoboMeter-4B 60.05 第一、VLAC-2B 29.95 最低；One-Shot 7 个变体中 Robo-Dopamine-8B 58.33 第一（自报，排行榜数据取自 2026-10-19 版论文表格）。
  - RoboReward-4B / 8B 的价值一致性得分为 0（自报）。
  - 作者称结果与前进进度分高的模型，仍在指令对应、执行记忆、恢复判断、子任务计分一致性上出错。
- **评估与接纳**：
  - 参评方只提供推理服务与适配器；测试集不公开，查询与打分由 RoboValue 团队计算并上排行榜。
  - 报 Zero-Shot 与 One-Shot 两个赛道，分开排名；Full-Shot 训练集已公开，本次未报结果。
  - 仿真任务改编自 RoboDojo；另设跨具身、跨环境两个设定。
- **可信度**：作者自报，参评模型由 RoboValue 团队自己跑；论文 arXiv 2610.26663 的 HTML 版读不到；评测代码开源，测试集私有。
- **模型**：LIV、ProcVLM、Robo-Dopamine、RoboFAC、Robometer、RoboReward、RynnValue、TOPReward、VLAC 是被评测的价值模型，版本未说明。

## 关联

- 基于 [[robodojo]]：15 个仿真任务改编自 RoboDojo。
