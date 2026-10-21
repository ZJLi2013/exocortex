---
type: source
url: https://dev.meta.ai/models/muse-spark
published: 2026-09-02
ingested: 2026-10-18
tags: [llm-foundation-models]
concepts: [原生视觉理解, 长程 agent 工作流, 真实执行环境中的视觉推理]
benchmarks: ["[[GDPval-AA]]", "[[DeepSWE]]", "[[Terminal-Bench]]", "[[MRCR]]"]
methods: []
models_used: []
models_compared: ["[[Muse Spark 1.2]]", "[[GPT-5.6 Sol]]", "[[Claude Opus 5]]"]
lenses: ["[[llm-foundation-models]]"]
---
# Muse Spark 1.3

Meta 面向长程 agent 与编码的模型，有 max 推理档，视觉推理走真实执行环境。模型页未写参数量。

- **关键数字**（页面表，max 档，自报）：GDPVal-AA v2 为 1754，对照 Muse Spark 1.2（xhigh）1615、GPT 5.6 Sol 1710、Opus 5 1824。DeepSWE v1.1 为 75.4，对照 55.0 / 73.0 / 74.0。Terminal-Bench 2.1 为 88.8，对照 82.9 / 88.8 / 86.7。MRCR 512K–1M 为 98.1，Opus 5 一栏为空。上下文 1M。`muse-spark-1.3` 输入 $1.25、缓存输入 $0.15、输出 $4.25 / 百万 token；contributor 档为 $0.10 / $0.002 / $0.20，并写明会用来改进 Meta 的产品。
- **评估与接纳**：未说明谁跑的表、跑了几次。Agentic IF Index 标明 Internal。页面链到 2026-09-02 的公告，模型页本身没写日期。
- **可信度**：作者自报；参数量未说明。
- **模型**：发布表对照 Muse Spark 1.2（xhigh）、GPT-5.6 Sol（max）、Opus 5（max）。
