---
type: source
url: https://prism-wam.github.io/
published: 2026-10-19
ingested: 2026-10-21
tags: [wam]
concepts: [语义与物理状态解耦, 深度空间预测未来, 无具身动作预训练]
benchmarks: ["[[RoboTwin]]", "[[RoboDojo]]", "[[LIBERO]]", "[[LIBERO-Plus]]", "[[LIBERO-Pro]]"]
methods: []
models_used: ["[[Wan2.1-14B]]", "[[LingBot-Depth]]"]
models_compared: ["[[OpenWAM-α]]", "[[π0.5]]", "[[Fast-WAM]]"]
lenses: []
---
# PrismWAM

世界动作模型把状态拆成两路：RGB 预测目标帧做语义规划，深度预测未来轨迹，动作从深度 rollout 读出；不做具身动作预训练，RoboTwin clean → random 平均 83.67%（15B 变体）。

- **关键数字**：
  - RoboTwin clean → random：PrismWAM* 83.67%、PrismWAM（5B）70.57%；OpenWAM-α 69.05%、π0.5 58.35%。
  - RoboDojo（不含 agent 赛道排第二）：PrismWAM* 36.23 / 29.3%，5B 25.10 / 18.55%；第一 VPP2 39.26。
  - LIBERO 99.35%；LIBERO-Plus 79.44%（π0.5 84.76%）；LIBERO-Pro 54.48%（π0.5 57.16%）。
  - 真机三任务对 OpenWAM：分布外 24/35 对 17/35（+20.0 点），分布内 24/27 对 20/27。
  - 仿真深度加最强一档传感器噪声：RoboTwin 平均 68.30%，比干净深度低 2.45 点。
- **评估与接纳**：仿真用各 benchmark 自带评测；真机同任务同试次数对照 OpenWAM。谁判定真机成功未说明。
- **可信度**：作者自报；论文 arXiv 2610.26564，代码在 GitHub；评测次数除真机外未说明。
- **模型**：PrismWAM* 是 15B 探索变体，从 Wan2.1-14B 初始化并加做纯视频预训练；5B 主模型的视频骨干未说明。真机深度先经 LingBot-Depth 细化。对照 OpenWAM-α、π0.5、Fast-WAM 等。
