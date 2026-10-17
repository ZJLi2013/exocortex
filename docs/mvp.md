# exocortex MVP

Plan Revision: 6
Plan Review: approved

## Goal

随手丢进来的研究链接由 LLM 整理成一个 Obsidian wiki：判断它影响我哪个研究问题，人不做分类。
来源落在所有研究问题之外时，由 LLM 提议新的研究问题（lens），human 批准后生效。

**长期**：研究领域的个人知识层。采集、沉淀、insight 三步里，human 只挑源、提问、批准结论。
知识层是 markdown + git，以后的 personal assistant 直接读写它，不另建存储。

## 当前结论

**MVP 可用：新 agent 只凭 `AGENTS.md` 就能收录、回答查询、提议新 lens，三步各自在预登记判据上通过。**

- **冷启动能查**：12 个原始来源编译的 wiki，无设计上下文的 agent 只读 wiki 作答 4/5（t3）。
- **收录不靠人写指令**：新 agent 只拿「收录 inbox」处理 6 个新链接，3 条预登记 lens 判定全中（t4）。
- **概念页不必要**：13 个概念页降级为来源页标签后，作答 5/5（t7，删页前 4/5）；概念页太宽或太碎，且维护成本随来源数增长。
- **lens 外的来源能长出新问题**：lint lenses 恰好提出预登记的两个候选，没有多提（t5）；human 批准后全库补判完成（t6）。
- **校验不依赖 Obsidian 运行**：`check_wiki.py` 直接解析文件；Obsidian CLI 要求应用开着，无头运行时不可靠。

## 下一步决策

下一步 t8：human 标签（设计见下节）。规则已实现，验收等 human 给一批带标签的新链接。

其余候选：

- **无头触发**：inbox 有新内容时自动跑收录（Cursor SDK / agent CLI）。
- **批准草稿**：四个 lens 的「待批准」里积压了草稿，并入「当前判断」后 lens 才开始积累判断。

未处理的已知缺口见 [design.md](design.md#已知缺口)。

## r6：human 丢链接时顺手打标签

human 没细看，但知道大概方向（「jev 相关」「kernel 优化」）。这个意图 LLM 从原文推不出来，成本却只有一个词。

- **inbox**：`<URL> #jev #kernel`，标签可选，小写短横线。
- **来源页**：frontmatter `tags: [jev, kernel]` 存 human 标签，与 LLM 的 `concepts` 分开；没打写 `[]`。`tags` 是 Obsidian 原生属性，标签面板直接可用。
- **lens 判定**：标签是线索，不是归属；仍按内容逐个 lens 判。lens 页 frontmatter `tags` 列出与它对应的 human 标签：
  带这些标签的来源优先判这个 lens；keep 时 agent 把来源的新标签追加进去；标签与内容不符时 log 里注明。
- **lint lenses**：先看 human 标签，≥ 2 个无 lens 来源共享同一 human 标签即成簇，候选 lens 默认以该标签命名；再看 `concepts`。

t8 验收：human 给 ≥ 5 个带标签的新链接，新 agent 只拿「收录 inbox」+ `AGENTS.md`：

- 带 `jev` 的来源按内容判 `system1-decision`，该 lens 的 `tags` 出现 `jev`；
- ≥ 2 个共享某个未被覆盖标签的无 lens 来源，lint 提出以该标签命名的候选 lens；
- `check_wiki.py --sources <N>` 退出 0。

不通过 → 标签被当成归属（内容不符仍 keep）就改判定规则；该成簇没成簇就改 lint 规则。

## 边界

| 做 | 不做 |
|---|---|
| LLM 收录来源、维护来源页与概念标签（[llm-wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)） | 人工主题分类；按主题分文件夹；手写 index |
| LLM 按 lens 起草判断改动，human 批准 | LLM 直接改 lens 的「当前判断」或自建 lens |
| 索引由 Obsidian Bases 从 frontmatter 生成 | embedding 聚类：来源上百后再复用 3dgen_tracker 的近邻图 + Louvain |
| | 已有自动管线的 tracker（3dgen_tracker、embodied_radar）、个人日常管理 |

## 系统

执行规则以 [AGENTS.md](../AGENTS.md) 为准；concept 与 lens 的分工、各项设计理由与放弃的方案见 [design.md](design.md)。

```text
exocortex/                    # = Obsidian vault 根
├── AGENTS.md                 # agent 执行规则与 frontmatter schema
├── inbox/links.md            # 一行一个 URL
├── raw/<slug>.md             # 抓取的原文，写一次不改；只在本地
├── evals/                    # check_wiki.py（结构）、check_answers.py（查询集）
└── wiki/
    ├── sources/<slug>.md     # frontmatter 带 concepts 标签
    ├── lenses/<name>.md      # 范围（human）+ 当前判断 + 待批准草稿
    ├── index.base            # Bases 视图：sources / unowned / lenses
    └── log.md
```

## 查询集

`evals/check_answers.py` 的判据；新 agent 只读 `AGENTS.md`、`wiki/`、`raw/` 作答，≥ 4/5 通过。

| # | 问题 | 应提到 |
|---|---|---|
| Q1 | 哪些工作把「选出候选的集合」和「确认胜出的集合」分开？ | RSIGym、EmbodiedRSI、EmbodiedEvo、ASPIRE、RAX |
| Q2 | Gemini 4 Argon 的公开状态和已知读数是什么？ | 56%、75% |
| Q3 | 哪些系统由 human 写评估器、任务定义或验收，agent 只在其内搜索？ | AlphaEvolve、RSIGym、Argon |
| Q4 | 收录的来源里，哪些是 2026-10 发布的？ | EmbodiedRSI、EmbodiedEvo、RoboQuest、Argon |
| Q5 | 哪些地方记录了自改进没迁移、或被当作反例？ | 56.26、autoresearch、Agent Laboratory、RSIAgent |

## Experiment Log

| Exp | 假设 | 状态 | 关键结果 | 结论 / evidence |
|---|---|---|---|---|
| t1–t2（r2） | 两份 tracker 文档镜像进 vault 就能查 | superseded | 5/5 | 能查，但文档本身是 LLM 综合页，放进 `raw/` 是层次错位；r3 改为从原始来源编译。commit `df3a910` |
| t3（r3） | 从 12 个原始来源冷启动编译的 wiki 能回答查询集 | pass | 8 概念页（最大链 11 来源）；作答 4/5 | 冷启动可用。verify `20261016T095843Z-36c55293`，`evals/answers.md` |
| t4（r3） | `AGENTS.md` 单独能驱动收录，lens 判定合理 | pass | 18 来源 / 13 概念页；3 条预登记判定全中 | 收录可交给新 agent。收录方反馈的抓取 / 日期 / 概念补链缺口已改进 `AGENTS.md`（commit `65995be`） |
| t5（r4） | 无 lens 来源经概念页成簇即可提议新 lens | pass | 恰好两个预登记候选，无多提 | 机制成立。verify `20261016T144423Z-849f37d5` |
| t6（r4） | 批准后能按规则补判全库 | pass | demo-free-rl keep SGS / AlphaNIST；system1-decision keep JevAny / openjev | 新 lens 生效。verify `20261017T031812Z-af96c6cb` |
| t7（r5） | 删掉概念页、只留来源页标签，查询仍 ≥ 4/5 | pass | 作答 5/5；18 来源 44 个标签，13 个被 ≥ 2 个来源共享 | 概念页不必要。verify `20261017T041330Z-5c6f34c7`；作答方发现 RSIGym 发布日应为 2026-10，已改 |

## Revision 记录

- r2（2026-10-16，human）：3dgen_tracker 与 embodied_radar 已有自动管线，不进第 1 步。
- r3（2026-10-16，human）：手工 index 不可扩展、`raw/` 放的是综合页、没有 LLM 整理层。改为 llm-wiki：来源平铺、
  LLM 长概念页、lens 由 LLM 判定、索引用 Bases；整理者先用 coding agent。
- r4（2026-10-16，human）：进来的来源很可能完全不属于已有 lens（t4 里 5/6 双 reject）。加 lint lenses：
  无 lens 来源经概念页成簇时提议候选 lens，human 批准后补判全库。
- r5（2026-10-17，human）：概念页冗余且难维护。降级为来源页 `concepts` 标签，lens 提议改看共享标签。
- r6（2026-10-17，human）：human 丢链接时顺手打标签，比 LLM 标签更稳、带着 human 的意图；用于 lens 判定线索与 lens 提议。
