---
type: source
url: https://github.com/WorldOracle-benchmark/WorldOracle/tree/main
published: 2026-10
ingested: 2026-10-21
tags: [un-category]
concepts: [动作条件世界模型对照真机执行, 失败执行也要复现, 隐藏评测器, 公开排行榜]
benchmarks: []
methods: []
models_used: ["[[π0.5-DROID]]", "[[GPT-5.5]]", "[[GPT-5.6 Luna]]", "[[SAM3]]"]
models_compared: ["[[GE-Sim 2.0]]", "[[Cosmos 3 Nano]]", "[[DreamDojo]]", "[[IRASim]]", "[[ctrl-world]]"]
lenses: ["[[interactive-video-world-models]]"]
---
# WorldOracle

评测动作条件世界模型的 benchmark：给同一初始观测与低层动作轨迹，把预测视频和配对的真机执行比，覆盖 AgiBot G2、YAM 与人手，含失败尝试与约两分钟长回合；7 个模型里 GE-Sim 2.0 最好，30 秒内 WorldOracle-SV 73.86、全长 63.33。

- **关键数字**：
  - 评测集 335 条：AgiBot G2 100、YAM 75、人手 100 条人工操作回合，AgiBot G2 策略 rollout 60 条；约 40% 的交互段是失败执行。
  - 30 秒 → 全长 WorldOracle-SV：GE-Sim 2.0 73.86 → 63.33，DreamDojo 50.56 → 27.08，Cosmos 3 53.99 → 26.60。
  - 臂与物体的空间对齐差距：AgiBot 上 IRASim 臂 78.8、物体 29.1；Cosmos 3 89.4、45.4。
  - Ctrl-World 多视角一致性 AgiBot 65.6 → YAM 41.9。
- **评估与接纳**：四个指标：VLM 判物理状态、DINOv3 特征对齐、交互区域 PSNR / LPIPS / V-JEPA 保真、多视角一致性。测试集真值不公开，由官方服务评测；排行榜提交需审批。
- **可信度**：作者自报；论文 arXiv 2610.18826；论文用 GPT-5.5 当 VLM 评审，在线榜单全部改用 GPT-5.6 Luna 重评，两处数值可能不同。
- **模型**：策略 rollout 由 π0.5 产生（从 DROID checkpoint 初始化、在 AgiBot 训练集上微调）；GPT-5.5 / GPT-5.6 Luna 是物理状态评审；SAM3 出掩码。被评的 7 个世界模型：IRASim、Ctrl-World、DreamDojo、Cosmos 3 Nano、GE-Sim 2.0、JointControlVideo、OSCAR。
