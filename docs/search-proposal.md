# 搜索候选来源

agent 用 alphaXiv 公开检索按已批准的 lens 搜新工作，只写候选清单；收不收由 human 决定，`inbox/links.md` 仍只归 human 写。

检索只覆盖 arXiv，候选全是论文，项目页与仓库搜不到。

## 流程

```text
human 说「搜索候选」
  → 每个已批准 lens 生成查询
  → alphaXiv 检索（只读标题与摘要，不抓全文）
  → 去重
  → 追加到 inbox/proposals.md
  → human 处置：收下的移进 inbox/links.md，之后照常「收录 inbox」
```

只在 human 说「搜索候选」时跑，不挂在收录批次后自动跑。

## 查询从哪来

- 每个已批准 lens 的范围句改写成 2–3 条 `embedding` 查询：一句短问题，在标题与摘要上做语义检索；
- lens 内来源共享的评测集名（如 RoboDojo、LIBERO-Pro）各一条 `keyword` 查询：在标题、摘要与全文里精确匹配；
- 每个 lens 最多 5 条；`--days`（默认 30）作为发表日期下限传给检索，`--days 0` 不设下限。

`status: proposed` 的候选 lens 不生成查询。

检索接口是 `https://api.alphaxiv.org/search/v2/paper/discover/{keyword|embedding}`（OpenResearch CLI 用的同一组），不需要 key，每条查询返回 15–25 篇；按 IP 限流，429 时脚本按 `Retry-After` 退避。使用条款未核实，只做每次几条查询的轻量调用。

## 去重

候选 URL 命中下面任一处就丢弃：

- 来源页的 `url:`（同收录第 1 步）；
- `inbox/links.md`、`inbox/proposals.md` 里已有的行；
- `wiki/search-rejections.yaml` 里 human 否决过的 URL。

arXiv 的 `abs/`、`html/`、`pdf/` 同一编号算同一来源。

从仓库或项目页收录的来源，搜索会以它的论文、换一个 URL 返回（RAX 就是这样），所以也按工作名去重：标题以库内来源页的工作名加冒号开头，或摘要写了「introduce(s) <工作名>」，就丢弃。只在评测里提到库内工作名（如「on RoboDojo」）的不丢。

insight 查新要看到已知工作，用 `--include-known`：已知的不丢，`known` 字段标出它在哪。

## 候选格式

`inbox/proposals.md`，每次运行追加一节，最多 10 条，按与 lens 范围的相关度排：

```markdown
## [YYYY-MM-DD] search

1. <URL> #<已有标签> — <标题>。<一句：为什么可能属于 [[<lens>]]，依据是搜索摘要>（查询：`<query>`）
```

- 标签只从 [human-tags.md](human-tags.md) 已有写法里选，没有合适的就不写；human 收下时可以改。
- 理由只写搜索摘要里有的内容，不写推断。

## human 处置

| human 说 | agent 做 |
|---|---|
| 「收下 1、3」 | 那几行去掉理由与查询，原样移到 `inbox/links.md` |
| 「不要 2」「其余不要」 | URL 追加进 `wiki/search-rejections.yaml`，从 proposals 删除 |
| 不处置 | 留在 proposals，下次搜索不重复提 |

`wiki/search-rejections.yaml` 与 `lens-rejections.yaml` 同格式：

```yaml
- url: <URL>
  rejected: YYYY-MM-DD
```

## 边界

- agent 不写 `inbox/links.md`，不触发收录，不改 lens 与来源页。
- 检索请求与去重由脚本做，查询改写、相关度排序与一句理由由 agent 写。
- 已知重叠工作的召回不稳（2026-10-23 在 agentic-robotics 三条方向上两轮只召回 0–1/4），适合找新来源，不适合当「没人做过」的依据。
