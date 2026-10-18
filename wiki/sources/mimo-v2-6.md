---
type: source
url: https://mimo.xiaomi.com/mimo-v2-6
published: 2026-09-22
ingested: 2026-10-18
tags: [llm-foundation-models]
concepts: [大规模强化学习后训练, 选出集合与确认集合分离, 原生视觉理解, 开源训练环境与 RL 代码]
benchmarks: ["[[Artificial Analysis Intelligence Index]]", "[[DeepSWE]]"]
methods: []
models_used: []
models_compared: ["[[Kimi-K3]]", "[[Qwen3.8-Max]]"]
lenses: ["[[llm-foundation-models]]"]
---
# MiMo-V2.6

小米开源的全模态系列：Pro 与 Flash，另有最高约 20× 输出速度的 Pro-UltraSpeed。作者把它写成 RSI 路径上的一步，在可验证任务上加大 RL 算力。

- **关键数字**（自报）：Artificial Analysis Intelligence Index v4.3 上 Pro 46.32，称当时最强开源。不到 6 天、各 30 步 RL、约 75 万条轨迹；Flash / Pro 花费约 $0.85M / $2.62M，训练任务相对通过率 +25% / +12%。held-out 的 DeepSWE v1.1：Flash 48.8 → 65.68，Pro 58.4 → 72.57。每步更新 1,568 条样本，上下文最长 1M，每步 3.5–3.7B tokens。API 价格与 V2.5 相同。
- **评估与接纳**：DeepSWE 称为 held-out。机械臂一段是多视角闭环抓取演示，未给成功率。技术报告、训练环境与 RL 代码称已开源。
- **可信度**：作者自报；参数量未说明；Intelligence Index 未给评测次数。
- **模型**：AA Index 上称超过 Kimi K3 与 Qwen3.8 Max。
- **原文**：[[raw/mimo-v2-6]]
