---
type: source
url: https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017
published: unknown
ingested: 2026-10-18
tags: [llm-foundation-models]
concepts: [原生视觉理解, 更短输出降本, prompt 编码参考实现]
benchmarks: ["[[HLE]]", "[[Terminal-Bench]]", "[[DeepSWE]]"]
lenses: ["[[llm-foundation-models]]"]
---
# DeepSeek-V4.1-Flash-1017

DeepSeek-V4.1-Flash 的小版本更新，推理、编码、agent 与视觉基准上升，同时缩短任务时间和输出长度。

- **关键数字**（对照上一版，自报）：HLE 无工具 36.8 → 42.6（纯文本子集 39.1† → 44.0†）；Terminal-Bench 4.0 31.2 → 42.3（Claude Code harness）；DeepSWE v1.1 74.2 → 77.0（Mini-SWE-V2）。上下文 1M，temperature 1.0，top_p 1.0。
- **评估与接纳**：表内还有 K3、GLM-5.3、GPT-5.6 Sol、Opus 5。未说明评测次数。技术报告沿用 V4.1-Flash 的 PDF，本卡未单列新报告。
- **可信度**：作者自报。卡面未写发布日期；Hugging Face 仓库创建于 2026-10-17。权重 MIT。
- **原文**：[[raw/deepseek-v4-1-flash-1017]]

## 关联

- 基于 [[deepseek-v4-1-flash]]：同一模型的小版本更新，沿用其技术报告
