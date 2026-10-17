---
type: source
url: https://github.com/razorback16/openjev
published: unknown
ingested: 2026-10-16
concepts: [System 1 决策模型, 选项概率读出, 概率校准, 扩散模型读出答案, 兼容第三方决策 API]
lenses: ["[[system1-decision]]"]
---
# OpenJev

开源的 System One 决策服务器：在 DiffusionGemma 26B-A4B 的扩散画布上只遮住答案槽，一次只读前向直接读出每个选项的概率，答案不会越出 schema；兼容 TypeSafe Jev 与 OpenAI Decisions API。README 不给它自己的准确率。

- **关键数字**：
  - RTX PRO 6000 Blackwell、三问请求、每次完整 prefill（最坏情况）：49 token 状态单请求 p50 30 ms、64 并发 130 req/s；2,047 token 83 ms；63,999 token 4.8 s。
  - 64K token 状态时，32 并发 32 个请求有 4 个、64 并发 64 个有 37 个等待超 120 s 返回 503。
  - 转接的小编码器：laya-1.0 16 问短状态 10 ms，verdict-1.4 7 ms。
  - 转接 JevK5：JevBench 公开 231 题上与原作 v0.3 有 230 题 top answer 相同，OpenJev 87.4% vs 原作 87.9%。
- **评估与接纳**：
  - openjev-0.1 本身没有准确率评测；README 写明答案质量就是 DiffusionGemma 26B-A4B 在此模式下的质量，要求用户在自己任务上先评。
  - 转接模型的准确率多是原作者数字；OpenJev 只自测与原实现的一致性（如 Clef 17 问全部同一 top answer）。
  - 某个槽熵 > 0.1 时自动再读 3 次取平均。
- **可信度**：性能为作者自测；无质量评测；Apache-2.0 开源；声明与 TypeSafe 无关联。
- **概念**：[[System 1 决策模型]]、[[选项概率读出]]、[[概率校准]]、扩散模型读出答案、兼容第三方决策 API
- **原文**：[[raw/openjev]]
