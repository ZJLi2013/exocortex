---
type: source
url: https://www.deepseek.com/en/news/deepseek-v4-1-flash/
published: 2026-09-10
ingested: 2026-10-18
tags: [llm-foundation-models]
concepts: [因果编码器-解码器, 非对称激活参数, KV cache 压缩, 原生视觉理解, 大规模强化学习后训练]
benchmarks: []
lenses: ["[[llm-foundation-models]]"]
---
# DeepSeek-V4.1-Flash

DeepSeek 新架构族里最小的模型，552B MoE、原生视觉理解，API 模型名 `deepseek-flash`。

- **关键数字**：输入 8B、输出 16B 激活参数；KV cache 相对上一代只需 1/4 HBM、1/8 SSD。非高峰价为高峰价的 50%（2026-09-10 04:00 UTC 起）。2026-09-14 04:00 UTC 起 `deepseek-v4-pro` 请求按 V4.1-Flash 价格转到本模型，直到 V4.1-Pro 上线。
- **评估与接纳**：称新预训练与更大规模 RL 后训练的基准结果超过包括 V4-Pro 在内的旗舰；「多方测试」在性能、成本、速度与总时长上优于 V4-Pro。未给出基准名、分数与测试方。技术报告为 Hugging Face 上的 PDF。
- **可信度**：作者自报；对比的「上一代」未点名；基准数字未公布。
- **原文**：[[raw/deepseek-v4-1-flash]]
