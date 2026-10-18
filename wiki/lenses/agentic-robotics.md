---
type: lens
tags: [agentic-robotics]
---
# agentic-robotics

## 范围

冻结的前沿模型当 agent、在模型外写代码技能 / 程序 / harness 来驱动机器人操作的工作，以及评测这类 agent 的 benchmark。

## 总结

6 个系统让 agent 从执行反馈中把经验沉淀成模型外的技能、程序或 harness，2 个 benchmark 评测这类 agent，其中一个同时评 VLA 策略。常见评测是 RoboDojo、LIBERO-Pro、BEHAVIOR-1K。全部是自报，没有第三方复现。

## 工作

- [[rax]]：coding agent 在线探索学任务，再编译成脱离 agent 运行的程序；未见布局平均成功率随探索 4 → 128 回合从 25% 升到 79%，编译后执行快 100× 以上。（自报）
- [[aspire]]：按执行 trace 修 code-as-policy 程序，验证过的修复进技能库；Claude Opus 5.5 下 LIBERO-Pro 平均 99%。（自报）
- [[robodojo]]：42 个仿真加 18 个真机任务的操作策略 benchmark，公开排行榜设 agent 赛道；2026-10-17 仿真榜前两名 WorldScape-R²SI 46.58、EmbodiedEvo 45.08 都在 agent 赛道。（自报）
- [[embodiedevo]]：在 Playground 场景把物理反馈写成代码 Skills 与 Lessons，冻结后在未见场景执行；RoboDojo-Sim 自跑 Score 44.48、SR 37.82%。（自报）
- [[embodiedrsi]]：冻结 VLA 外的 harness 按信息增益与实验成本选下一次物理实验；RoboCasa365 77.0%，真机 SmolVLA 46.0% → 71.3%。（自报）
- [[roboquest]]：10 个需靠物理交互取证的移动操作 benchmark；最好的 GPT-6 Astra 成功率 23.2%，失败主要来自缺证据。（自报）
- [[worldscape-r2si]]：内层 agent 调 Skill 执行，外层 agent 复盘修 Skill 并用执行记录训练动作模型；称 RoboDojo 总榜第一，未给分数。（自报，公司发布稿）
- [[physicalrsi]]：基座改写 harness 生成多个变体、按仿真表现选优继承，π₀.₅ 作为技能之一；RoboDojo-Sim 官方榜 Score 36.27、SR 31.38%。（自报）

## 冲突
