---
type: source
url: https://github.com/kyutai-labs/cadre-autoencoders-and-world-models
published: 2026-10-07
ingested: 2026-10-22
tags: []
concepts: [交互式视频世界模型, 因果视频生成, 因果视频自编码器, 单步扩散解码, 动作跟随评测]
benchmarks: []
methods: []
models_used: ["[[DINOv3]]"]
models_compared: []
lenses: ["[[interactive-video-world-models]]"]
---
# CADRE

面向交互式世界模型的因果视频自编码器族：在冻结 DINOv3 特征上训瓶颈，再用一到两步的因果扩散解码器重建；基于其 latent 的世界模型在单张 H100 上 20 fps、响应低于 230 ms，覆盖机器人操作、人手操作、驾驶与室内导航。

- **关键数字**：单用户 20 FPS、输入 p95 162 ms；两用户共享时 14 FPS/人、p95 207–212 ms（H100，不含网络与浏览器渲染；两用户未达 19 FPS / 200 ms 目标）。
- **评估与接纳**：世界模型 rollout 用 FID、FVD、PSNR、LPIPS 与动作探针 ARR 评，自编码器在 OpenVid-HD 上评重建；成功口径未说明。
- **可信度**：作者自报；代码 MIT，权重 CC-BY-NC 4.0，冻结的 DINOv3 编码器受 Meta 许可限制；论文尚未上 arXiv（README 标 coming soon）。
- **模型**：DINOv3 是冻结特征编码器；四个环境的世界模型与动作探针分别训练，发布 7 个自编码器与 4 个多分辨率变体。
