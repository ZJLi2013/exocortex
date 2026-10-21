---
type: source
url: https://github.com/HexaFuture/HexaShell
published: 2026-10-16
ingested: 2026-10-21
tags: [agentic-robotics]
concepts: [薄 harness 命令行控制机器人, 双视角三角测量定位, 失败归因]
benchmarks: ["[[RoboDojo]]"]
methods: ["[[code skills from experience]]"]
models_used: ["[[GPT-6 Astra]]", "[[Codex]]"]
models_compared: []
lenses: ["[[agentic-robotics]]"]
---
# HexaShell

coding agent 只用一条 `robo` 命令行、三路 RGB 相机与一页手册驱动 RoboDojo 双臂机器人，失败后由第二个 agent 读回合、写或修 Python 工具；RoboDojo 官方在隐藏种子上复评 SR 46.9%、进度分 53.2。

- **关键数字**：
  - RoboDojo 官方评测（隐藏种子，42 个任务各 50 回合）：SR 46.9%、进度分 53.2；Memory 81.0%、Precision 32.0%、Open 55.3%。
  - 杂物场景（桌上多 13–18 个物体）：标准 38.0%、杂物 31.0%，保留 82% 的成功率。
  - 自测（冻结工具，每布局 1 回合）：新布局 39.7% / 48.0，开发布局 38.3% / 43.6。
  - 34 个非 Open 任务共 196 个工具，启用 137 个、270 条命令；一轮修复中位 6.3 分钟。
- **评估与接纳**：官方分由 RoboDojo 在自己的机器上跑冻结系统、用自家检查器判定；自测也用 RoboDojo 检查器。工具修好后在同一布局重试。
- **可信度**：官方分是第三方复评；自测每布局一回合。只开源冻结工具与接口，harness（服务器、执行器、agent 容器、演化循环）与工具测试未发布。论文 arXiv 2610.23479。
- **模型**：执行 agent 与修复 agent 都是 Codex + GPT-6 Astra；任务笔记由模型从开发布局运行中写出，具体模型未说明。
