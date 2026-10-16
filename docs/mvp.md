# exocortex MVP

Plan Revision: 3
Plan Review: approved

## Goal

随手丢进来的研究链接由 LLM 整理成一个 Obsidian wiki：自动长出概念页、判断它影响我哪个研究问题，人不做分类。

### 长期目标与边界

**研究领域的个人知识层：采集、沉淀、insight 三步里，human 只负责挑源、提问、批准结论。**
知识层是 markdown + git，以后的 personal assistant 直接读写它，不另建存储。

| 做 | 现在不做 |
|---|---|
| LLM 收录来源、维护来源页与概念页（[llm-wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)） | 人工主题分类；按主题分文件夹 |
| LLM 按 lens 判断一条来源会改变哪个判断，起草改动，human 批准 | LLM 直接改 lens 的「当前判断」 |
| 索引由 Obsidian Bases 从 frontmatter 生成 | 手写 index |
| | embedding 聚类：来源上百后复用 3dgen 的近邻图 + Louvain 管线 |
| | 已有自动管线的 tracker（3dgen_tracker、embodied_radar）、个人日常管理 |
| | 改原仓库的 `landscape.md` / `research-rsi-track.md`；它们的 owner 迁不迁，等本 MVP 通过再定 |

### 两种组织，都不是分类

- **概念页（下而上）**：LLM 从来源里抽概念；同一概念被第二个来源提到时建页，链回所有来源。概念名先查已有页再起新名。
- **lens（上而下）**：我的研究问题，每个由 human 写一句范围。LLM 对每条来源逐个 lens 判 keep / reject 与影响哪条判断。
  lens 回答「它改变我哪个判断」，不回答「它是什么」；一条来源可以命中 0 到多个 lens。

页面按类型分目录（来源 / 概念 / lens），类型是页面的结构，不是主题。

### 借鉴

| 来源 | 取 |
|---|---|
| [Karpathy llm-wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) | `raw/` 只读、`wiki/` LLM 写、schema 文件；ingest / query / lint；`log.md` |
| [claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian) | frontmatter 约定；冲突写 `> [!contradiction]` 不覆盖；lint 查死链与孤页 |
| embodied_radar `domain.yaml` | 一句话范围 + LLM keep / reject，用在 lens 判定 |
| 3dgen_tracker `docs/paper_graph.md` | 手写 9 类混用四个轴、留一法 0.42–0.93，是不做人工分类的依据；聚类留到规模够时 |

## 当前结论

- r2 证明「聚到一处能查」：无设计上下文的 agent 只读两份 tracker 文档的快照，5/5 题命中（commit `df3a910`）。
  那两份文档本身是 LLM 写的综合页，放进 `raw/` 是层次错位；r3 改为从原始来源编译。
- r3 未验证。

## 下一步决策

先做 t3：12 个种子来源冷启动编译 wiki，用原查询集验收。

- **t3 通过** → t4：丢 5 条新链接（含与两个 lens 都无关的），验 lens 判定；再用 Cursor SDK / agent CLI 让 inbox 有新内容时无头触发。
- **t3 不通过** → 按失败位置改 `AGENTS.md`：缺事实改来源页规则，缺跨来源串联改概念页规则，缺判断改 lens 种子。

## 系统

```text
exocortex/                    # = Obsidian vault 根
├── AGENTS.md                 # 收录 / 查询 / lint 规则与 frontmatter schema；coding agent 按它执行
├── inbox/links.md            # 一行一个 URL，或 Web Clipper 剪下的 .md
├── raw/<slug>.md             # 抓取的原文，写一次不改
└── wiki/
    ├── sources/<slug>.md     # 一个来源一页
    ├── concepts/<name>.md    # ≥ 2 个来源提到时建
    ├── lenses/<name>.md      # 范围（human）+ 当前判断 + 待批准草稿
    ├── index.base            # Bases 视图：来源按日期、概念按来源数、lens
    └── log.md
```

整理者是 coding agent（Cursor 里说「按 AGENTS.md 收录 inbox」）。Obsidian CLI 做 lint 与 Bases 查询，需要 Obsidian 开着且已打开本 vault。

r2 的 `scripts/sync_sources.py`、`raw/robotrsi/`、`raw/agent_loop/`、`raw/manifest.md`、`wiki/index.md` 在 t3 中删除。

### 收录一条来源

1. URL 已在某个 `raw/*.md` 的 `url:` 里 → 跳过并在 log 记一行。
2. 抓取原文写 `raw/<slug>.md`（frontmatter：`url`、`fetched`、`title`）。
3. 写 `wiki/sources/<slug>.md`，样例：

```markdown
---
type: source
url: https://arxiv.org/abs/2610.18867
published: 2026-10-13
ingested: 2026-10-16
concepts: [选出集合与确认集合分离, 技能库写回]
lenses: [robotrsi]
---
# EmbodiedEvo

一个 Playground 场景学技能与 lessons，冻结后才抽 Test 场景；RoboDojo 上 37.82%。

- 关键数字：……
- 可信度：……
- 概念：[[选出集合与确认集合分离]]
- 原文：[[raw/embodiedevo]]
```

4. 概念：`concepts` 里每项先 `rg` 已有概念页；已有则在该页「来源」下追加一行；
   第二个来源提到且无页 → 建页并链回两个来源。只有一个来源的概念只留在 frontmatter，不写 wikilink。
5. lens：逐个读 `wiki/lenses/*.md` 的范围，判 keep / reject。keep 时在该 lens 的「待批准」下追加：

```markdown
> [!draft] EmbodiedEvo（2026-10-16）
> 影响判断 2：……；依据 [[embodiedevo]]
```

   与「当前判断」冲突时改用 `> [!contradiction]`。不改「当前判断」本身。
6. `wiki/log.md` 追加 `## [YYYY-MM-DD] ingest | <title>`。
7. 全部收录完跑 `obsidian unresolved total` 与 `obsidian orphans`。

### lens 种子

范围句由 human 定稿；「当前判断」从原 tracker 的判断句搬入（不含事实表），作为起点。

| lens | 范围（草案） | 当前判断来源 |
|---|---|---|
| `robotrsi` | 会改变 RoboRSI 选底座、改进方向或评测选择的 agent × 机器人工作 | `landscape.md` 开头判断、比较轴 |
| `agent-loop` | 会改变 agent-loop 探索模式、评估 / 预算 / 人工介入设计的 research agent 与自改进系统 | `research-rsi-track.md`「当前判断」与「对 agent-loop」列 |

### 冷启动种子（12 个）

覆盖查询集需要的工作，全部取自两份 tracker 的原始链接：

| 工作 | URL |
|---|---|
| RSIGym | https://github.com/evolvent-ai/RSIGym |
| ScienceDiscovery | https://github.com/openJiuwen-ai/sciencediscovery |
| AlphaEvolve | https://arxiv.org/abs/2506.13131 |
| autoresearch | https://github.com/karpathy/autoresearch |
| Agent Laboratory | https://arxiv.org/abs/2501.04227 |
| EmbodiedRSI | https://arxiv.org/abs/2610.10498 |
| EmbodiedEvo | https://arxiv.org/abs/2610.18867 |
| ASPIRE | https://research.nvidia.com/labs/gear/aspire/ |
| RAX | https://github.com/robot-agent-exploration/rax |
| Gemini 4 Argon | https://developers.googleblog.com/gemini-4-argon-for-robotics/ |
| RoboQuest | https://arxiv.org/abs/2610.10388 |
| RSIAgent | https://arxiv.org/html/2609.15364v1 |

## t3 验收

1. 无设计上下文的 agent 只读 `AGENTS.md`、`wiki/`、`raw/` 作答，`python evals/check_answers.py evals/answers.md` ≥ 4/5。
   答案须引用 `wiki/` 页；两份原 tracker 文档不在 vault 里。
2. `obsidian unresolved total` 为 0；`obsidian base:query` 列出 12 个来源。
3. 至少一个概念页链到 ≥ 3 个来源（Q1 的「选出集合与确认集合分离」应自然长出）。

查询集：Q1–Q3、Q5 同 r2；Q4 的「读过或核过」是 tracker 自己的记录，来源里没有，改为发布日期。

| # | 问题 | 应提到 |
|---|---|---|
| Q1 | 哪些工作把「选出候选的集合」和「确认胜出的集合」分开？ | RSIGym、EmbodiedRSI、EmbodiedEvo、ASPIRE、RAX |
| Q2 | Gemini 4 Argon 的公开状态和已知读数是什么？ | 56%、75% |
| Q3 | 哪些系统由 human 写评估器、任务定义或验收，agent 只在其内搜索？ | AlphaEvolve、RSIGym、Argon |
| Q4 | 收录的来源里，哪些是 2026-10 发布的？ | EmbodiedRSI、EmbodiedEvo、RoboQuest、Argon |
| Q5 | 哪些地方记录了自改进没迁移、或被当作反例？ | 56.26、autoresearch、Agent Laboratory、RSIAgent |

分两段跑，合计上限 1 小时，超了停下报告：

- **t3a**：先收录 RSIGym、EmbodiedEvo、Gemini 4 Argon，human 在 Obsidian 里看来源页、概念页、lens 草稿，按意见改 `AGENTS.md`。
  这 3 个来源预期长出「选出集合与确认集合分离」概念页（RSIGym 的 6 题选 / 37 题确认、EmbodiedEvo 的 Playground / Test）。
- **t3b**：收录其余 9 个，跑上面的 t3 验收。

估算（未实测）：12 个来源有效阅读 30 万–50 万 token，输出约 5 万；agent 每次工具调用重发上下文，累计计费输入约 100 万–300 万，多数命中缓存。

## Experiment Log

| task | 做法 | 结果 | 证据 |
|---|---|---|---|
| t1（r2） | 镜像两份 tracker 文档进 `raw/`，`--check` 作 verifier | pass | verify `20261016T091210Z-c1be5484` |
| t2（r2） | 无设计上下文的 subagent 只读快照作答 | 5/5；作答方报告概念措辞不一、日期口径不一，只能通读 | commit `df3a910` 的 `evals/answers.md` |

## Revision 记录

- r2（2026-10-16，human）：3dgen_tracker 与 embodied_radar 已有自动管线，不进第 1 步。
- r3（2026-10-16，human）：手工 index 不可扩展、`raw/` 放的是综合页、没有 LLM 整理层。改为 llm-wiki：来源平铺、
  LLM 长概念页、lens 由 LLM 判定、索引用 Bases；整理者先用 coding agent。
