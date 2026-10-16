# 探索编译成程序，探索预算越大泛化越好：RAX

**冻结模型的编码 agent（Codex CLI / Claude Code）不用示范、不用手写动作原语，在线探索学会任务，再把成功的决策序列编译成一个不需要 agent 的程序。
未见过的场景上，探索预算从 4 个 episode 加到 128 个，平均成功率从 25% 升到 79%；编译后的程序最多比 agent 快 241 倍。**
分级 L3（agent 经感知与控制工具出动作），写回是代码与 memory，不碰权重。[代码](https://github.com/robot-agent-exploration/rax)，[项目页](https://robot-agent-exploration.com/)（Harvard / NVIDIA / Berkeley / MIT / Stanford）。

三个阶段：

- **Explore**：agent 看观测、一步步调机器人工具解任务，把有效的前置条件、动作与效果记进 `memory/`；
- **Compile**：把成功的决策序列写成 `code/<project>/controller.py:main(ctx)`，由一组「先检查观测再动作」的步骤函数组成，并在无人值守下测试；
- **Evaluate**：仿真里由冻结的程序（或 agent 的一个活副本）跑留出布局；真机上由操作员复位场景，程序端到端执行。

| 任务 | agent | 编译后的程序 | 加速 |
|---|---|---|---|
| Air fryer | 72 min | 18 s | 241× |
| Bandu tower | 17 min | 10 s | 103× |

- **harness 与机器人解耦**：harness 不 import 任何机器人或仿真包，每个仿真器或机器人是同一工具接口后面的 backend；真机上 agent 的沙箱只能经 MCP 工具碰机器人。
- **技能库跨 session 增长**：[skills-lib](https://github.com/robot-agent-exploration/skills-lib) 按构型分支存真机上写出的任务技能，每条带代码、前置条件、检查、失败模式与运行记录，两次无人值守成功才标 `verified`。
- **场地**：RoboDojo 与 BEHAVIOR-1K（Isaac Sim 5.1、cuRobo），真机 Franka FR3 与 Rainbow RB-Y1。仿真上平均比最好的基线高 37.4 个百分点，最好的已有方法是 41.2。

对 RobotRSI 判断的影响：

- 支持开头的判断，并补上了 HarnessPAI 缺的公开代码：「演化期用 agent，部署期把 agent 编译掉」有了可运行的实现。
- 「随探索量递增」的曲线就是 RoboRSI 在本目录没复现出来的那种增长。区别在横轴：RAX 是单任务的探索 episode 数，评测在留出布局上；RoboRSI 是跨 release 的进化轮数。
- 「不用手写动作原语」与本目录「接触靠解析代码是短板、接触原语换 VLA」的判断方向相反。RAX 的控制工具具体到哪一层（cuRobo 规划、末端位姿、关节）README 没写，要读分支代码才能判断它是否绕开了精密接触。
- 场地依赖 Isaac Sim，与 RoboProbe 一样在 MI300 上基本跑不了；作方法参照，不作底座。

## 可信度

- 数字只来自仓库 README（核于 2026-10-16）；论文标注为 Preprint，未读正文。25% → 79% 的任务集、每点评测次数、基线名单未核实。
