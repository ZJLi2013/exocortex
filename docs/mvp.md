# exocortex MVP

Plan Revision: 6
Plan Review: approved

## Goal

随手丢进来的研究链接由 LLM 整理成一个 Obsidian wiki：判断它影响我哪个研究问题，人不做分类。
来源落在所有研究问题之外时，由 LLM 提议新的研究问题（lens），human 批准后生效。

**长期**：研究领域的个人知识层，markdown + git，以后的 personal assistant 直接读写它。

## 当前结论

**MVP 可用：新 agent 只凭 `AGENTS.md` 就能收录、回答查询、提议新 lens，三步各自在预登记判据上通过。**

- 收录：新 agent 只拿「收录 inbox」处理 6 个新链接，3 条预登记 lens 判定全中（t4）。
- 查询：无上下文 agent 只读 wiki 作答 5/5（t7）。
- 新 lens：lint 恰好提出预登记的两个候选（t5），批准后全库补判完成（t6）。

## 下一步

**t8：human 标签**（规则已实现，设计见 [design.md](design.md#标签人打的是线索llm-打的只作检索)）。验收：human 给 ≥ 5 个带标签的新链接，新 agent 只拿「收录 inbox」：

- 带 `#jev` 的来源按内容判进 `jev` lens，且 `jev` 出现在该 lens 的 `tags`；
- ≥ 2 个共享某个未被覆盖标签的无 lens 来源，lint 提出以该标签命名的候选 lens；
- `check_wiki.py --sources <N>` 退出 0。

不通过：内容不符仍 keep → 改判定规则；该成簇没成簇 → 改 lint 规则。

之后的候选：无头触发（inbox 有新内容自动收录）；批准四个 lens 积压的草稿。

## 边界

不做人工主题分类与手写 index；LLM 不改「当前判断」、不自建 lens；已有自动管线的 tracker（3dgen_tracker、embodied_radar）不进来。

## 查询集

`evals/check_answers.py` 的判据，≥ 4/5 通过。

| # | 问题 | 应提到 |
|---|---|---|
| Q1 | 哪些工作把「选出候选的集合」和「确认胜出的集合」分开？ | RSIGym、EmbodiedRSI、EmbodiedEvo、ASPIRE、RAX |
| Q2 | Gemini 4 Argon 的公开状态和已知读数是什么？ | 56%、75% |
| Q3 | 哪些系统由 human 写评估器、任务定义或验收，agent 只在其内搜索？ | AlphaEvolve、RSIGym、Argon |
| Q4 | 收录的来源里，哪些是 2026-10 发布的？ | EmbodiedRSI、EmbodiedEvo、RoboQuest、Argon |
| Q5 | 哪些地方记录了自改进没迁移、或被当作反例？ | 56.26、autoresearch、Agent Laboratory、RSIAgent |

## Experiment Log

| Exp | 假设 | 结果 | evidence |
|---|---|---|---|
| t1–t2（r2） | tracker 文档镜像进 vault 就能查 | superseded：能查，但综合页放进 `raw/` 是层次错位 | commit `df3a910` |
| t3（r3） | 12 个原始来源冷启动编译的 wiki 能答查询集 | pass，4/5 | verify `20261016T095843Z-36c55293` |
| t4（r3） | `AGENTS.md` 单独能驱动收录 | pass，3 条预登记判定全中 | commit `65995be` |
| t5（r4） | 无 lens 来源成簇即可提议新 lens | pass，恰好两个候选 | verify `20261016T144423Z-849f37d5` |
| t6（r4） | 批准后能补判全库 | pass，robotics-rl keep SGS / AlphaNIST；jev keep JevAny / openjev | verify `20261017T031812Z-af96c6cb` |
| t7（r5） | 删掉概念页、只留标签，查询仍 ≥ 4/5 | pass，5/5 | verify `20261017T041330Z-5c6f34c7` |

## Revision 记录

- r2：已有自动管线的 tracker 不进第 1 步。
- r3：改为 llm-wiki：来源平铺、LLM 判 lens、Bases 索引。
- r4：来源多半不属于已有 lens，加 lint lenses 提议候选。
- r5：概念页冗余难维护，降级为来源页标签。
- r6：human 丢链接时打标签，作 lens 判定线索与成簇依据。
