---
type: source
url: https://arxiv.org/abs/2610.18867
published: 2026-10
ingested: 2026-10-16
tags: []
concepts: [选出集合与确认集合分离, 人定义评估与验收, harness 演化, 自改进, 经验写成代码技能, 跨模型迁移]
lenses: ["[[agentic-robotics]]", "[[agent-loop]]"]
---
# EmbodiedEvo

coding agent 在每个任务的一个 Playground 场景里把物理反馈蒸馏成代码 Skills 与诊断 Lessons，冻结后交给新 agent 在未见场景执行，不改模型权重。

- **关键数字**：
  - RoboDojo-Sim 全量：Average Score 44.48、成功率 37.82%（Astra/xhigh，任务描述 + wiki，每任务 50 个 Test 场景）；官方 Astra 结果 22.48%。
  - 配对实验（只给任务描述）：8.50% → 30.17%。
  - 跨模型：Astra 的 Skills / Lessons 让 Sol、Luna 成功率各升 8.86、5.50 个百分点。
  - Skills + Lessons 与原始交互历史性能相当，Test 执行成本低 53.0%。精细插入与液体操作仍难。
- **评估与接纳**：Playground 布局与 Test 布局不同；Playground 可 reset、可写 `skills/` `lessons/`，Test 只读、不能 reset、不回写经验。
  协议文件与执行记录对 agent 只读。
- **可信度**：作者自报；对比用 2026-10-09 排行榜快照；需 RoboDojo / Isaac Sim。
- **原文**：[[raw/embodiedevo]]
