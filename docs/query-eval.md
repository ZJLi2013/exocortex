# 查询评测

**5 个模型在决策题上全对；差别只出在跨来源的枚举题，小模型漏项更多。** 决策题的答案已经编译进 lens 的「当前答案」，模型只需定位，不需要综合。

## 结果（2026-10-18）

| 模型 | 运行方式 | 决策 D1–D5 | 检索 Q1–Q5 | 耗时 | tokens | 成本 |
|---|---|---|---|---|---|---|
| GPT-6 Astra | `codex exec`，只读沙箱 | 5/5 | 4/5 | 94 s | 输入 127,791（缓存命中 89,856），输出 3,623 | 待填单价 |
| Claude Opus 5.5（medium） | Cursor 子 agent | 5/5 | 4/5 | 66 s | 未取到 | 未取到 |
| Claude Sonnet 5.5（high） | Cursor 子 agent | 5/5 | 4/5 | 71 s | 未取到 | 未取到 |
| GPT-5.6 Luna（medium） | Cursor 子 agent | 5/5 | 3/5 | 69 s | 未取到 | 未取到 |
| Composer 2.5 fast | Cursor 子 agent | 5/5 | 2/5 | 73 s | 未取到 | 未取到 |

- 决策题人工评分，判据见下表；检索题用 `scripts/check_answers.py` 按关键词自动评分。
- Astra 的 tokens 与耗时取自 codex 会话日志；Cursor 子 agent 不返回 token 用量，耗时由 agent 自己在首尾记时间。Cursor 那 4 次在 14:37–14:38 并行运行，tokens 与成本要到 Cursor 用量页查。
- 唯一的事实错误：Composer 在 D1 把 EmbodiedRSI 的扰动子集说成「同一设定」，它实际是冻结 VLA 设定。

## 检索题的关键词分不可靠

金标准写于 lens 结构化之前，有两处已经和库内事实不符：

- Q1 要求出现 RSIGym，但它的来源页写明 final evaluation 复用开发期任务，不算分离。Composer 因此被判漏项，Astra 和 Sonnet 则是把它列为「不算」才过的。
- Q5 要求出现 autoresearch，它作为反例没有证据，已从 lens 删除。Opus 和 Sonnet 在这题的「漏项」主要来自这一条。

确实漏掉的：Composer 和 Luna 在 Q3 都没提到 Gemini 4 Argon，它的硬件自改进阶段由人写、提速超过 2× 需人授权。

## 各模型的使用反馈

- **顺**：先读「当前答案」，再顺着 C 编号下钻到来源页，5 个模型都提到这一点。
- **卡：没有 lens 的来源**。只读 lens 会漏掉它们，D5 的 Batch-Invariant VLAs 要靠全文搜索才能发现（Astra、Opus、Sonnet、Composer）。
- **卡：concepts 与正文不符**。AlphaNIST 打了「选出集合与确认集合分离」，正文却写未给独立评测集（Astra、Composer）。
- **卡：`published: unknown`**。按月份筛选时答不全（Astra、Opus、Sonnet、Composer）。

## 题目与判据

运行方式：每个模型开一个新会话，只读仓库，只按 `AGENTS.md`「查询」一节作答；每题 ≤ 8 行，必须引用 `wiki/` 路径。

| 题 | 问题 | 判据 |
|---|---|---|
| Q1 | 哪些工作把「选出候选的集合」和「确认胜出的集合」分开？ | 关键词，见 `check_answers.py` |
| Q2 | Gemini 4 Argon 的公开状态和已知读数是什么？ | 同上 |
| Q3 | 哪些系统由 human 写评估器、任务定义或验收，agent 只在其内搜索？ | 同上 |
| Q4 | 收录的来源里，哪些是 2026-10 发布的？ | 同上 |
| Q5 | 哪些地方记录了自改进没迁移、或被当作反例？ | 同上 |
| D1 | RoboRSI 评测还该不该用 LIBERO-Pro？证据有多强？ | 整体平均 99% 已饱和；扰动子集仍有 86.8% 对 72.1%；两条都是自报 |
| D2 | agent-loop 现在要不要做自改进或进化搜索？为什么？ | 不做；没有程序化评估器、没有固定 benchmark |
| D3 | agent 跑长上下文任务，现在该选哪个基座？ | 未定、不能横比；成本上 Flash 档可作默认 |
| D4 | 无示教 RL 里，reset 到哪个任务配置怎么采样？证据有多强？ | 按成功率加权；0.73 / 0.70 对约 0；单组自报、评测配置是否另取未说明 |
| D5 | VLA 推理时 batch size 会不会改变动作输出？库里有相关工作吗？ | 会；引用 batch-invariant-vlas；单次试验、未测机器人行为 |
