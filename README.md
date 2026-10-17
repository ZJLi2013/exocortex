# exocortex

研究领域的个人知识库：你丢链接，LLM 把它整理进一个 Obsidian wiki，并判断它会改变你哪个研究问题的哪条判断。
你不做分类，只挑源、提问、批准结论。

## 怎么用

| 你想做 | 怎么做 |
|---|---|
| 收录新来源 | 把 URL 一行一个写进 `inbox/links.md`，对 agent 说「收录 inbox」 |
| 查东西 | 直接问 agent，答案会引用 `wiki/` 里的页面 |
| 采纳一条判断 | 打开 `wiki/lenses/<lens>.md` 看「待批准」，说「批准 <lens> 的 <工作名> 草稿」 |
| 处置新研究问题 | 有 `status: proposed` 的 lens 出现时，说「批准 lens <name>」「并入 <已有 lens>」或「否决 lens <name>」 |
| 检查 wiki 完整性 | `python evals/check_wiki.py --sources <来源数>` |

agent 按 [AGENTS.md](AGENTS.md) 执行，在 Cursor 里打开本仓库即可。浏览用 Obsidian 打开本目录作为 vault。

## wiki 怎么组织

不按主题建目录，靠两种会自己长出来的结构：

- **概念页**（`wiki/concepts/`）：同一个概念被第二个来源提到时自动建页，链回所有来源。
- **lens**（`wiki/lenses/`）：你的研究问题，一句话范围加一组「当前判断」。每收一条来源，LLM 逐个 lens 判 keep / reject；
  keep 的写成待批准草稿，「当前判断」只在你批准后才改。
- **新 lens 的提议**：两个以上不属于任何 lens 的来源共享一个概念页时，LLM 起草一个候选 lens 等你处置。

| 路径 | 内容 |
|---|---|
| `inbox/links.md` | 待收录的 URL |
| `raw/` | 抓下来的原文，写一次不改 |
| `wiki/sources/` | 一个来源一页：关键数字、谁评估、可信度 |
| `wiki/concepts/` | 跨来源概念 |
| `wiki/lenses/` | 研究问题与待批准草稿 |
| `wiki/index.base` | Obsidian Bases 视图：来源、概念、lens、无 lens 来源（`unowned`） |
| `wiki/log.md` | 每次收录、查询、lens 判定的日志 |

## 现状

18 个来源、13 个概念页、4 个 lens（`robotrsi`、`agent-loop`、`demo-free-rl`、`system1-decision`）。
设计、验收结果与下一步见 [docs/mvp.md](docs/mvp.md)。
