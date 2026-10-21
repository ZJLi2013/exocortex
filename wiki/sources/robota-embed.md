---
type: source
url: https://robota-ai.github.io/robota-embed/
published: 2026-10
ingested: 2026-10-20
tags: [agentic-robotics]
concepts: [动作参与检索的 VLA 嵌入, 检索未来片段作上下文, 机器人上下文学习, 选出集合与确认集合分离]
benchmarks: ["[[ManiSkill]]", "[[Robota-Embed-Bench]]", "[[DROID-Sim]]", "[[LIBERO]]"]
methods: []
models_used: ["[[GPT-6 Astra]]", "[[DreamZero]]", "[[Fast-WAM]]", "[[SAM3]]", "[[Qwen3-VL]]"]
models_compared: ["[[Gemini Embedding 2]]", "[[CLIP ViT-L/14]]", "[[Omni-Embed-Nemotron-3B]]"]
lenses: ["[[agentic-robotics]]"]
---
# Robota-Embed

把视觉、语言和原生动作编码进同一个检索空间，按当前交互检索未来 4 秒的经验片段作上下文；冻结的 GPT-6 Astra 配上演化出的任务内记忆，ManiSkill 五任务成功率 24% → 68%。

- **关键数字**：
  - Embed2Evolve（ManiSkill 5 个选定任务，每任务每条件 20 个新初始化）：成功率 Direct 24% → 68%，同协议演化的 Omni-Embed-Nemotron-3B 为 33%；每回合策略 token 0.921M → 0.518M（−43.7%）。
  - 检索（Robota-Embed-Bench，4 源 4,000 查询、8,000 窗口共享库）：片段级 R@1 47.33%，Gemini Embedding 2 25.2%、CLIP ViT-L/14 1.2%；回合级 81.77%。查询去掉动作降到 20.08%，去掉视觉 23.00%。
  - Embed2ICL：DROID-Sim 三任务 47.0% → 56.3%（免训练，DreamZero）；LIBERO 难子集五任务 86.4% → 92.8%（Fast-WAM）；真机 Split Cup 进度 66.67% → 87.50%（每条件 12 回合）。
- **评估与接纳**：Embed2Evolve 先在开发回合里演化记忆与上下文配方并选出最优，再冻结，在新初始化上测试；GPT 与嵌入权重全程不变。谁执行演化未说明。成功判定由各仿真任务给出。
- **可信度**：作者自报（NVIDIA 技术报告）；ManiSkill 任务为作者选定的 5 个；去掉某模态是对训练好的模型做推理时缺失输入，不是重训消融；代码、模型与 benchmark 标注 coming soon。
- **模型**：GPT-6 Astra 是 Embed2Evolve 中的冻结策略；DreamZero（冻结）与 Fast-WAM（微调）是 Embed2ICL 的两个策略；SAM3 裁剪物体，Qwen3-VL 做训练数据质量门；Gemini Embedding 2、CLIP ViT-L/14 是检索基线，Omni-Embed-Nemotron-3B 是演化对照的嵌入。
