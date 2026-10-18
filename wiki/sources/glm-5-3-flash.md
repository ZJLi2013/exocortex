---
type: source
url: https://z.ai/blog/glm-5.3-flash
published: 2026-08-26
ingested: 2026-10-18
tags: [llm-foundation-models]
concepts: [混合线性与稀疏注意力, IndexPool, KV cache 压缩, 原生视觉理解, 流形约束超连接]
lenses: ["[[llm-foundation-models]]"]
---
# GLM-5.3-Flash

智谱 GLM-5 系列里第一个原生多模态模型。320B 总参数、18B 激活，用线性注意力加稀疏注意力压长上下文成本。

- **关键数字**（自报）：相对 GLM-4.5，总参数 320B 对 355B，激活 18B 对 32B，层数 45 对 92。相对 GLM-5.3，每头每层注意力计算少 3.0×，每层 KV cache（BF16）小 4.4×。Artificial Analysis Intelligence Index v4.1.1 为 57，折扣后 $0.045/任务。DeepSWE v1.1 63.4 对 GLM-5.2 的 46.2；AutomationBench v1.0.6 48.8 对 26.2。Z.ai Code Bench v1.0 最大 effort 29.0，Opus 4.8 为 29.5。同一国产芯片集群上端到端服务比初始基线高 3×。
- **评估与接纳**：发布前以 ox-alpha 在 OpenCode 与 OpenRouter 匿名试用。Toolathlon Verified 为官方服务上 3 次 pass@1 的平均；GDPval-AA v2 由 Artificial Analysis 评；HLE 用 GPT-5.6-luna (medium) 做裁判。DeepSeek-V4-Flash-Base 的基座数字用智谱内部框架重跑。权重在 Hugging Face，推理支持 SGLang、vLLM、TokenSpeed。
- **可信度**：作者自报。多数基准未给次数。「同价十分之一」「与 NVIDIA 每 token 成本相当」未给对方单价。
- **原文**：[[raw/glm-5-3-flash]]
