# exocortex

研究领域的个人知识库：你丢链接，LLM 把它整理进一个 Obsidian wiki，并判断它会改变你哪个研究问题的哪条判断。
你不做分类，只挑源、提问、批准结论。

## 准备

不用安装，没有依赖包：

1. `git clone` 本仓库。
2. 用一个能读写文件、能联网抓网页的 coding agent 打开它。默认用 Cursor：仓库根目录的 [AGENTS.md](AGENTS.md) 会被 Cursor 自动加载为规则，
   直接在 Cursor 的 agent 对话里说话即可。Claude Code、Codex CLI 等也可以，开头先让它读一遍 `AGENTS.md`。
3. 有 Python 3 就能跑 `evals/` 里的检查脚本（只用标准库）。
4. 可选：用 [Obsidian](https://obsidian.md) 把本目录打开为 vault 来浏览、看图谱和 Bases 视图。agent 收录不依赖 Obsidian。

## 怎么用

下表的「说」都是在上面那个 agent 对话里说。

| 你想做 | 怎么做 |
|---|---|
| 收录新来源 | 把 URL 一行一个写进 `inbox/links.md`，说「收录 inbox」 |
| 查东西 | 直接提问，答案会引用 `wiki/` 里的页面 |
| 采纳一条判断 | 打开 `wiki/lenses/<lens>.md` 看「待批准」，说「批准 <lens> 的 <工作名> 草稿」 |
| 处置新研究问题 | 有 `status: proposed` 的 lens 出现时，说「批准 lens <name>」「并入 <已有 lens>」或「否决 lens <name>」 |
| 检查 wiki 完整性 | `python evals/check_wiki.py --sources <来源数>` |

## wiki 怎么组织

不按主题建目录，靠两种会自己长出来的结构：

- **概念页**（`wiki/concepts/`）：同一个概念被第二个来源提到时自动建页，链回所有来源。
- **lens**（`wiki/lenses/`）：你的研究问题，一句话范围加一组「当前判断」。每收一条来源，LLM 逐个 lens 判 keep / reject；
  keep 的写成待批准草稿，「当前判断」只在你批准后才改。
- **新 lens 的提议**：两个以上不属于任何 lens 的来源共享一个概念页时，LLM 起草一个候选 lens 等你处置。

| 路径 | 内容 |
|---|---|
| `inbox/links.md` | 待收录的 URL |
| `raw/` | 抓下来的原文，写一次不改；只存在本地，不进仓库 |
| `wiki/sources/` | 一个来源一页：关键数字、谁评估、可信度 |
| `wiki/concepts/` | 跨来源概念 |
| `wiki/lenses/` | 研究问题与待批准草稿 |
| `wiki/index.base` | Obsidian Bases 视图：来源、概念、lens、无 lens 来源（`unowned`） |
| `wiki/log.md` | 每次收录、查询、lens 判定的日志 |

## 现状

18 个来源、13 个概念页、4 个 lens（`robotrsi`、`agent-loop`、`demo-free-rl`、`system1-decision`）。
为什么这样设计见 [docs/design.md](docs/design.md)；验收结果与下一步见 [docs/mvp.md](docs/mvp.md)。

## 贡献与许可

所有改动走 pull request，见 [CONTRIBUTING.md](CONTRIBUTING.md)。
代码 MIT（[LICENSE](LICENSE)），wiki 与文档文字 CC BY 4.0（[LICENSE-CONTENT](LICENSE-CONTENT)）；来源原文版权归原作者，不在仓库里分发。
