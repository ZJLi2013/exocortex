---
type: source
url: https://github.com/robocurve/inspect-robots
published: unknown
ingested: 2026-10-21
tags: []
concepts: [统一策略接口, 前沿模型直接当策略, 仿真与真机统一评测, 结果溯源]
benchmarks: []
methods: []
models_used: ["[[Claude Opus 5]]", "[[Claude Fable 5]]"]
models_compared: []
lenses: ["[[agentic-robotics]]"]
---
# Inspect Robots

机器人版 Inspect AI：一次定义 benchmark，把任意策略（VLA、前沿 LLM agent、code-as-policy）接到任意真机或仿真具身上评测，每次运行产出可复读、可离线重打分的评测日志。

- **关键数字**：未报评测分数；README 列出 7 种真机具身（YAM、Franka、AgiBot A2、Unitree G1、SO-ARM、WidowX、任意 ROS 机械臂）与 Isaac Lab 仿真。
- **评估与接纳**：
  - 框架本身不判成败，由每个 benchmark 的 scorer 打分；具体 benchmark 放在另一个仓库 WorldEvals。
  - 运行前检查策略与具身的动作空间、控制频率是否匹配，不匹配不开跑；默认开启边界与单步变化量护栏。
  - `agent` 策略让前沿 LLM 用工具调用逐块驱动机器人；`capx` 插件评测 LLM 写 Python 控制机器人的 code-as-policy；失败日志可总结成笔记交给下一次运行。
- **可信度**：alpha 阶段，API 会变；开源（MIT）；README 无论文、无评测结果。
- **模型**：Claude Opus 5 与 Claude Fable 5 出现在 README 的 agent 策略示例里；其余策略经插件接入，版本未说明。
