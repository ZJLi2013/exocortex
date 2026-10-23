---
type: source
url: https://github.com/Junchao-cs/SolarWM
published: 2026-09-02
ingested: 2026-10-22
tags: []
concepts: [交互式视频世界模型, 因果视频生成, 统一数据引擎, 相机轨迹条件控制]
benchmarks: []
methods: []
models_used: ["[[Wan2.2-5B]]", "[[Wan2.2-14B]]", "[[LTX-2.5]]", "[[MiniMax-H3]]", "[[Kimi-K2.6]]"]
models_compared: []
lenses: ["[[interactive-video-world-models]]"]
---
# SolarWM

开放的视频世界模型框架：把多源视频统一成 143 万段帧对齐训练片段，在四种 5B–33B 视频骨干上套同一套三阶段训练配方，蒸馏出可交互的长程因果模型。

- **关键数字**：1.43M clips、约 25 TB 数据；四个模型 5B–33B（Wan2.2-5B、Wan2.2-14B、LTX-2.5-22B、MiniMax-H3-33B）；因果生成 16 fps、4 步采样，训练只用 5 秒片段，最长连续生成到 60 分钟。
- **评估与接纳**：论文只给 10 秒、分钟级、小时级的定性 rollout，没有报 FID/FVD 等定量指标；成功与否由作者目视判定，未说明独立评测。
- **可信度**：作者自报；代码与权重开源，完整 raw-WDS 数据需申请访问。
- **模型**：Wan2.2-5B/14B、LTX-2.5-22B、MiniMax-H3-33B 是四条骨干路线，各自保留原生表示与训练目标；Kimi-K2.6 用于生成数据 caption。
