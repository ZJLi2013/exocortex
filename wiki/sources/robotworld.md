---
type: source
url: https://robotworldai.github.io/
published: 2026-10
ingested: 2026-10-19
tags: [agentic-robotics]
concepts: [多具身工具接口, 隐藏评测器, 动作工具调用]
benchmarks: []
methods: []
models_used: []
models_compared: []
lenses: ["[[agentic-robotics]]"]
---
# RobotWorld

一个多模态 agent 通过公开的观测和动作工具，在仿真里控制机械臂、灵巧手、人形、四足、车和无人机；84 个任务，成功由 agent 看不见的评测器判定。

- **关键数字**：84 个任务、18 种具身、20 个控制配置。README 写默认批协议每个任务 3 次 rollout，并关闭环境侧代码控制。抓到的项目页未给出总分。
- **评估与接纳**：隐藏的原生检查器或 world-state-v1。项目页未写谁宣布排行榜名次。
- **可信度**：项目页，2026-10；作者自报。仿真在 agent 推理时暂停。页面有 Astra 仿真录像，默认协议下的具体模型未说明。
