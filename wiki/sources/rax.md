---
type: source
url: https://github.com/robot-agent-exploration/rax
published: 2026
ingested: 2026-10-16
tags: []
concepts: [选出集合与确认集合分离, 人定义评估与验收, 自改进, 经验写成代码技能, 探索预算扩展, 把 agent 编译成程序]
lenses: ["[[agentic-robotics]]"]
---
# RAX

冻结模型的 coding agent（Codex CLI / Claude Code）靠在线探索学任务、再编译成脱离 agent 运行的机器人程序；未见场景平均成功率随探索从 4 到 128 回合由 25% 升到 79%。

- **关键数字**：
  - 未见场景平均成功率 25% → 79%（探索 4 → 128 回合）；最佳先前 SOTA 41.2。
  - 仿真平均比最强基线高 +37.4%；基准为 RoboDojo 与 BEHAVIOR-1K（Isaac Sim 5.1）。
  - 编译程序比 agent 本身快：Air fryer 72 min → 18 s（241×），Bandu tower 17 min → 10 s（103×）。
  - 真机 Franka FR3、Rainbow RB-Y1；无示教数据、无手工动作原语、无价值函数引导。
- **评估与接纳**：仿真正式评测用 held-out layouts，冻结程序或 agent 副本在从未见过的布局上运行；探索在哪些布局上进行、seed 数未说明。
  真机由操作员复位场景后程序端到端运行；操作员 arm / disarm 目录 agent 不可写，recorder 只读。
  agent 沙箱只能经 MCP 工具碰机器人，模型冻结；skill 需两次无人值守成功才标 `verified`。
- **可信度**：作者自报；预印本；评测次数未说明；代码按分支开源。
- **原文**：[[raw/rax]]
