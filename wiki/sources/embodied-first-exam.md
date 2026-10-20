---
type: source
url: https://www.embodied-first-exam.ai/
published: 2026-10-19
ingested: 2026-10-20
tags: [agentic-robotics]
concepts: [隐藏评测器, 公开排行榜, 特权模式与标准模式对照, 实时时钟评测]
benchmarks: []
methods: []
models_used: ["[[GPT-6 Luna]]"]
models_compared: ["[[GPT-6 Astra]]", "[[Claude Opus 5.5]]", "[[gemini-4-argon]]", "[[Gemini 3.8 Flash]]", "[[glm-5-3-flash]]", "[[deepseek-v4-1-flash]]"]
lenses: ["[[agentic-robotics]]"]
---
# Embodied First Exam

coding agent 只拿到文字目标、命令行和机器人接口，写代码控制仿真机器人的 benchmark：31 个 suite、1,090 个任务；核心 449 题上最好的 Codex + GPT-6 Astra 解出 32.7%。

- **关键数字**（2026-10-02 至 10-19 批量评测，每题一次尝试）：
  - Core（449 题，各取默认模式）：GPT-6 Astra 32.7%、Claude Opus 5.5 22.5%、Gemini 4 Argon 18.0%、Gemini 3.8 Flash 5.6%、GLM 5.3 Flash 与 DeepSeek V4.1 Flash 各 2.4%。
  - 前三名分模式：privileged（372 题）75.5 / 55.4 / 39.2%；standard（432 题）33.8 / 23.8 / 19.0%；standard-realtime（59 题）33.9 / 13.6 / 8.5%。
  - 规模：2,128 个任务目录、44 种机器人、20 个仿真器；9 个 suite 为本工作新建，其余移植自 BEHAVIOR-1K、RoboCasa、LIBERO、RoboDojo 等。
- **评估与接纳**：
  - 三种模式：privileged 在仿真器内读全状态、可无限重置，提交轨迹后重放判分；standard 只经机器人 API 看 RGB、深度和关节，默认不能重置，按现场 episode 判分；standard-realtime 同 standard 但时钟不停。
  - verifier 在无网络沙箱里只看录下的状态，判 1 或 0；核心集用人工判断和一次 GPT-6 Luna 预跑筛掉简单题，因此成功率低于全集。
  - 上线前让 agent 尝试不做任务就通过，成功则先修 verifier。
- **可信度**：作者自报，每题一次尝试，报告称尚不能区分模型差异与单次运气。观察到模型凭记忆复现已删除的参考解（Opus 5.5 重写的 RoboTwin 参考解 28 行中 26 行相同），公开 benchmark 移植题的结果可能含记忆成分。Finding 5 的控制方式标签由 agent 读日志标注，未经人工核对。代码 MIT 开源，每次运行的 trace 与回放公开。
- **模型**：六个被评 agent 均为模型 + 自家 harness（Codex、Claude Code、Antigravity、DeepSeek harness），reasoning high；GPT-6 Luna 用于筛核心集。
- **原文**：[[raw/embodied-first-exam]]

## 关联

- 基于 [[robodojo]]：RoboDojo 移植为考试的一个 suite，核心集 12 题。
