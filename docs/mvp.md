# exocortex MVP

Plan Revision: 2
Plan Review: approved

## Goal

把散在各仓库、手工维护的研究追踪聚到一个 Obsidian vault，在一处就能查到、并跨 tracker 回答问题。

### 长期目标与边界

**研究领域的个人知识层：采集、沉淀、insight 三步里，human 只负责挑源、提问、批准结论。**
知识层是 markdown + git，以后的 personal assistant 直接读写它，不另建存储。

| 做 | 现在不做 |
|---|---|
| 聚拢手工维护的 tracker，统一查看与查询 | 个人日常管理（日程、待办、邮件） |
| 随手丢进来的链接自动路由到相关主题页（第 2 步） | 已有自动管线的 tracker（3dgen_tracker、embodied_radar）：它们自成闭环，规模也大，需要时再接 |
| agent 起草 insight，human 批准后写入（第 3 步） | 自建 UI；Obsidian 只当阅读器 |
| | embedding / RAG；规模到数千页之前用 `index.md` + `rg` |

### 借鉴

| 来源 | 取 | 不取 |
|---|---|---|
| [Karpathy llm-wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) | `raw/` 只读 + `wiki/` agent 写 + schema 文件三层；`index.md` 目录、`log.md` 追加日志；ingest / query / lint 三个操作 | — |
| [claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian) | 页面 YAML frontmatter；新来源与旧页冲突时写 `> [!contradiction]` callout 而不是覆盖；lint 查死链、孤页、过期索引 | `entities/concepts/domains/...` 七类固定目录、`hot.md` 会话缓存、Obsidian REST API；等真遇到问题再加 |
| [LinkVault](https://github.com/calghar/LinkVault) / [engram](https://github.com/tomashrdlicka/engram) | 第 2 步的 inbox：链接先进队列，去重后路由到已有页，没有合适的才新建 | — |

## 当前结论

未验证。

## 下一步决策

先做 t1 聚拢、t2 验证可用。t2 的结果决定第 2 步做什么：

- **t2 通过** → 第 2 步做 inbox 路由（每个追踪页声明范围规则，丢进来的链接按范围分发）。
  开工前要先定：手工 tracker 的 owner 是留在原仓库（exocortex 起草改动、回写原仓库），还是迁进 exocortex。
- **t2 因「找不到跨 tracker 的相关内容」失败** → 第 2 步先建 `wiki/topics/` 跨 tracker 主题页，再做 inbox。

## 系统

```text
exocortex/               # = Obsidian vault 根
├── AGENTS.md            # schema：目录约定、query 先读 index 再 rg、raw 只读
├── scripts/sync_sources.py   # 源列表写在脚本顶部
├── raw/                 # 脚本写的快照，agent 与 human 都不手改
│   ├── manifest.md      # 每个源：路径、源 commit、文件数、源是否有未提交改动
│   └── <source>/
└── wiki/
    ├── index.md         # 每个源一节：它是什么、入口文件、核查日期范围
    └── log.md           # ## [YYYY-MM-DD] sync | query | ingest | lint …
```

**复制而不是 symlink / junction**：原仓库仍是这些文件的 owner，exocortex 只读快照；
Windows junction 在 Obsidian 与 git 下行为不一致。同步是镜像：源里删掉的文件 raw 里也删。
保留源内相对目录，`landscape.md` → `works/*.md` 的链接在 vault 里照常可点。

### 第 1 步聚拢的源

| 源 | 路径 | 内容 | 量 |
|---|---|---|---|
| `robotrsi` | `robotRSI/doc/landscape.md`、`doc/works/` | agent × 具身工作地图与逐篇笔记 | 7 个 |
| `agent_loop` | `agent-loop/docs/study/research-rsi-track.md` | Research / RSI 工作追踪表 | 1 个 |

两份文件链到的项目内文档（`direction.md`、`exploration-mode/*`、`industry-practices.md`）不聚拢，在 vault 里显示为未解析链接。

### 渲染样例

`raw/manifest.md` 一行：

```markdown
| robotrsi | ji_qi_ren/…/robotRSI/doc | 1a2b3c4 | 7 | 有未提交改动 |
```

不写同步时间：重跑无变化时 manifest 也不变，`git status` 才能干净。

`wiki/index.md` 一节：

```markdown
## robotrsi：agent × 具身相关工作地图
四个比较轴、评测场地、方法与框架三张表，逐篇笔记在 works/。核查日期 2026-09-29 至 2026-10-16。
入口：[[raw/robotrsi/landscape]]
```

## t2 验收：查询集

agent 只读 `exocortex/`（`AGENTS.md` → `wiki/index.md` → `rg raw/`），不打开原仓库。每题答案要引用 raw 路径。
「应命中」是设计时在原文件里查到的位置；命中指答案引用了该来源。Q1、Q3、Q4、Q5 需要同时用到两个源。

| # | 问题 | 应命中 |
|---|---|---|
| Q1 | 哪些工作把「选出候选的集合」和「确认胜出的集合」分开？ | rsi-track 的 RSIGym 自改进（6 题选、37 题全集降分）；landscape 的 EmbodiedRSI、EmbodiedEvo、ASPIRE、RAX |
| Q2 | Gemini 4 Argon 的公开状态和已知读数是什么？ | landscape 主表与 `works/gemini-argon.md`（56% → 75%、未给评测次数、模型闭源） |
| Q3 | 哪些系统由 human 写评估器、任务定义或验收，agent 只在其内搜索？ | rsi-track 的 AlphaEvolve、RSIGym；landscape 的 Gemini 4 Argon（硬件上由人写阶段与验收） |
| Q4 | 2026-10-13 及以后读过或核过的工作有哪些？ | rsi-track 的 RSIGym、ScienceDiscovery；landscape 的 EmbodiedEvo、Gemini 4 Argon、RAX |
| Q5 | 哪些地方记录了自改进没迁移、或被当作反例？ | rsi-track 的 Qwen3.8 自改进（56.66% → 56.26%）、autoresearch 贪心接受规则、Agent Laboratory「难以引导」；landscape 的 RSIAgent 具身迁移性未验证 |

## Experiment Log

（尚无）

## Revision 记录

- r2（2026-10-16，human）：3dgen_tracker 与 embodied_radar 已有自动管线，不进第 1 步；只聚拢 robotrsi 与 agent_loop 两个手工 tracker，查询集随之重写。
