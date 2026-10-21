---
type: source
url: https://developers.googleblog.com/gemini-4-argon-for-robotics/
published: 2026-10-13
ingested: 2026-10-16
tags: []
concepts: [人定义评估与验收, 自改进, 仿真孪生造数据, 基座接管人做的环节, 验证 agent]
benchmarks: ["[[ERQA]]"]
methods: []
models_used: []
models_compared: []
lenses: ["[[llm-foundation-models]]"]
---
# Gemini 4 Argon

Google 面向物理推理的基座模型，博客展示它覆盖机器人控制、Real2Sim、物理理解、仿真造数据与硬件自改进。

- **关键数字**：
  - ERQA 87%（纯推理，不是任务成功率）。
  - 仿真造数据：一张真机照片建 MuJoCo 孪生、定义 77 个任务、生成 4,500+ 条 `reward == 1.0` 的轨迹微调 VLA；真机成功率 56% → 75%，完成时间 35 s → 24 s。
  - SO-101 硬件自改进三轮耗时 58.9 s、22.9 s（擦到盒沿）、17.4 s。
  - 零样本控制按 2–4 / 4–7 / 8–20 次 VLM 调用分档，未给成功率。
- **评估与接纳**：仿真数据按 `reward == 1.0` 过滤；硬件自改进分三个阶段由人写，安全规则来自 `AGENTS.md`，提速超过 2× 需人授权。
  Spot 演示用 2 个验证 agent（foot / hand）确认后才释放。
- **可信度**：只有博客与 prompt 演示；56% → 75% 未给评测次数；模型闭源，经付费 Gemini API / AI Studio 提供。
