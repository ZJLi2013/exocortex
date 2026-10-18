---
type: source
url: https://arxiv.org/html/2609.15364v1
published: 2026-09
ingested: 2026-10-16
tags: []
concepts: [选出集合与确认集合分离, 人定义评估与验收, 自改进, 验证 agent, 课程式探索]
benchmarks: ["[[OSWorld]]", "[[ALE]]", "[[GameCraft-Bench]]"]
methods: []
models_used: ["[[GLM-5.3]]", "[[Kimi-K3]]", "[[Kimi-K2.6]]", "[[glm-5-3-flash]]", "[[Qwen3.8-27B]]", "[[GPT-5.4]]", "[[GPT-4o]]"]
models_compared: ["[[Kimi-K2.6]]", "[[MiMo-V2.5]]", "[[DeepSeek-V4-Pro]]", "[[Qwen3.8-Max]]", "[[Kimi-K3]]", "[[Claude Opus 4.8]]", "[[Gemini 3.8 Flash]]", "[[GPT-5.6 Sol]]", "[[muse-spark]]", "[[Claude Fable 5]]", "[[Claude Opus 5]]", "[[GPT-6 Astra]]"]
lenses: ["[[agent-loop]]"]
---
# RSIAgent

curriculum / actor / verifier 三个 agent 在新软件环境里先广（BRS）后深（DRS）地自主练习，经验写进 actor 自管的 memory，冻结后用于目标任务，不改权重；GLM-5.3 + Kimi-K3 在 OSWorld 2.0 partial 78.98%、ALE 84.82%。

- **关键数字**：
  - OSWorld 2.0（0808 offline，82 题）：无 RSI 71.97 / binary 37.80 → RSI 78.98 / 42.68。
  - ALE Near-term（67 题）：83.75 / 49.25 → 84.82 / 50.75；binary 低于 GPT-6 Astra 的 52.24。
  - RSI 行只有部分题真有 RSI 结果：OSWorld 41 题、ALE 19 题，其余沿用 baseline 分。
  - 四题阶段消融：完整 RSI 74.54%，只 BRS 65.52%，只 DRS 56.50%；只 DRS 在 T085、T089 低于 baseline。
  - GameCraft-Bench 随机 40 题：四个生成器下都提升 overall（如 Kimi-K2.6 31.28 → 46.37）；Play2Code 在最强生成器上降分（52.77 → 51.05）。
- **评估与接纳**：
  - 练习结果由 verifier agent（Kimi-K3，独立上下文，看不到 actor 的推理与 memory）判 PASS / FAIL，决定经验是否写入 memory；何时停止探索由 curriculum agent 决定。
  - 最终分由 benchmark 官方评估器给（需模型评分处用 GPT-5.4），在全部 agent 循环之后调用，不向 agent 回传分数或隐藏检查。
  - 选出与确认是同一任务：curriculum agent 以目标 query 为参照出练习题，DRS 从尝试目标任务开始，练习后在 reset 的环境里再试；最终评测也在同一目标任务上，只是环境 reset、memory 冻结。
  - 选题：额外探索只给 baseline 未满分的题；四题消融取自「相对 baseline 有提升」的探索 cohort，完整 RSI 取两次历史评测均值。
  - 跨系统对比用各自 leaderboard 报告值，非同一评测协议；ALE 含本地修正分。
  - 人工介入：探索期无 gold label 与人监督；选题规则与报告口径由作者定。
  - 失败模式：verifier 在官方 rubric 下仍有错时返回 PASS；未充分验证的决定被写成规则（如把缺失数据标记当有效答案）并在后续复用；练习没覆盖目标的真正弱点（未测试获取不可得的用户信息）。
- **可信度**：作者自报；OSWorld 结果标为 provisional，各次运行的预算与评测范围未完全对齐；代码开源。
- **模型**：主系统 GLM-5.3 + Kimi-K3（verifier）；GameCraft-Bench 生成器含 Kimi-K2.6、GLM-5.3-Flash、Qwen3.8-27B；官方评估器用 GPT-5.4 评分、GPT-4o 模拟用户；OSWorld 对照表用各家 leaderboard 报告值。
- **原文**：[[raw/rsiagent]]
