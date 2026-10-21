---
type: lens
tags: [agentic-robotics]
---
# agentic-robotics

## 范围

冻结的前沿模型当 agent、在模型外写代码技能 / 程序 / harness 来驱动机器人操作的工作，以及评测这类 agent 的 benchmark。

## 总结

11 个系统让 agent 从执行反馈中把经验沉淀成模型外的技能、程序、记忆或 harness，4 个 benchmark 评测这类 agent，其中一个同时评 VLA 策略，另有一个把 LLM agent、code-as-policy 与 VLA 接到同一套真机与仿真接口上的评测框架；另有一项实证研究比较前沿模型直接出动作、在 agent 会话里出动作、监督学习策略三种用法。常见评测是 RoboDojo、LIBERO-Pro、BEHAVIOR-1K、RoboCasa。只有一个系统的分数由 benchmark 方在隐藏种子上复评，其余都是自报。

## 工作

- [[rax]]：coding agent 在线探索学任务，再编译成脱离 agent 运行的程序；未见布局平均成功率随探索 4 → 128 回合从 25% 升到 79%，编译后执行快 100× 以上。（自报）
- [[aspire]]：按执行 trace 修 code-as-policy 程序，验证过的修复进技能库；Claude Opus 5.5 下 LIBERO-Pro 平均 99%。（自报）
- [[harnesspai]]：一次 rollout 内程序固定，多次 rollout 之间改代码；不重训时 LIBERO-PRO 比 π0.5 高 61.6 个点，并报 96.5%。（自报）
- [[robodojo]]：42 个仿真加 18 个真机任务的操作策略 benchmark，公开排行榜设 agent 赛道；2026-10-17 仿真榜前两名 WorldScape-R²SI 46.58、EmbodiedEvo 45.08 都在 agent 赛道。（自报）
- [[embodiedevo]]：在 Playground 场景把物理反馈写成代码 Skills 与 Lessons，冻结后在未见场景执行；RoboDojo-Sim 自跑 Score 44.48、SR 37.82%。（自报）
- [[embodiedrsi]]：冻结 VLA 外的 harness 按信息增益与实验成本选下一次物理实验；RoboCasa365 77.0%，真机 SmolVLA 46.0% → 71.3%。（自报）
- [[roboquest]]：10 个需靠物理交互取证的移动操作 benchmark；最好的 GPT-6 Astra 成功率 23.2%，失败主要来自缺证据。（自报）
- [[robotworld]]：多模态 agent 只用公开的观测与动作工具，在仿真里控制 18 种具身完成 84 个任务，成功由 agent 看不见的评测器判定；项目页未给总分。（自报）
- [[robota-embed]]：视觉、语言、动作统一嵌入，检索未来经验片段作上下文；冻结 GPT-6 Astra 加演化出的任务内记忆，ManiSkill 五任务成功率 24% → 68%，策略 token −43.7%。（自报）
- [[sensenova-roborsi]]：冻结权重，用执行反馈改 Harness；RoboDojo-Sim 平均分 60.08、成功率 54.17%，称正在提交官方榜。（自报）
- [[worldscape-r2si]]：内层 agent 调 Skill 执行，外层 agent 复盘修 Skill 并用执行记录训练动作模型；称 RoboDojo 总榜第一，未给分数。（自报，公司发布稿）
- [[embodied-first-exam]]：coding agent 写代码控制仿真机器人的 benchmark，31 个 suite、1,090 个任务；核心 449 题上 Codex + GPT-6 Astra 32.7%，privileged 75.5% 而 standard 33.8%。（自报）
- [[physicalrsi]]：基座改写 harness 生成多个变体、按仿真表现选优继承，π₀.₅ 作为技能之一；RoboDojo-Sim 官方榜 Score 36.27、SR 31.38%。（自报）
- [[hexashell]]：coding agent 只用一条命令行与三路 RGB 驱动机器人，失败后由第二个 agent 写或修工具；RoboDojo 隐藏种子官方评测 SR 46.9%、进度分 53.2。（第三方，RoboDojo 官方评测）
- [[astranomy]]：GPT-6 Astra 当原生机器人策略的三种用法；RoboLab-120 上 Codex 会话里的 Agentic Policy 74.8%，每个成功回合约 $36.40。（自报）
- [[robodoctor]]：agent 审查、修正或接管冻结 PrismWAM 的动作，按 Warmup 分数选控制方式，再更新干预经验；RoboDojo 54 个任务本地 Refinement 57.10 / 49.44%。（自报）
- [[inspect-robots]]：把前沿 LLM agent、code-as-policy 与 VLA 接到同一套真机与仿真接口上评测，每次运行留可离线重打分的日志；alpha 阶段，未报评测结果。（自报）
