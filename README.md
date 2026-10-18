# exocortex

研究领域的个人知识库：你丢链接，LLM 整理成 Obsidian wiki，并判断它会改变你哪个研究问题的哪条判断。
你只挑源、提问、批准结论，不做分类。

## 准备

无需安装。clone 后用 Cursor 打开，根目录的 [AGENTS.md](AGENTS.md) 会自动加载为 agent 规则；
用 Claude Code、Codex CLI 等则先让它读一遍 `AGENTS.md`。检查脚本只需 Python 3 标准库；[Obsidian](https://obsidian.md) 可选，用来浏览。

## 怎么用

在 agent 对话里：

| 你想做 | 怎么做 |
|---|---|
| 收录 | 把 URL 写进 `inbox/links.md`，可顺手打标签（`<URL> #jev #kernel`），说「收录 inbox」 |
| 查询 | 直接提问，答案引用 `wiki/` 里的页面 |
| 采纳判断 | 看 `wiki/lenses/<lens>.md` 的「待批准」，说「批准 <lens> 的 <工作名> 草稿」 |
| 处置新 lens | 出现 `status: proposed` 的 lens 时，说「批准 lens <name>」「并入 <已有 lens>」或「否决 lens <name>」 |
| 检查 | `python evals/check_wiki.py --sources <来源数>` |

## 怎么组织

- **lens**（`wiki/lenses/`）：你的研究问题，一句话范围加「当前判断」。每条来源逐个 lens 判 keep / reject，keep 的写成草稿，你批准后才进「当前判断」。
- **你的标签**（来源页 `tags:`）：丢链接时打的 `#tag`，LLM 用它决定先判哪个 lens，归属仍按内容定。
- **新 lens**：两个以上无 lens 的来源共享一个标签时，LLM 起草候选 lens 等你处置。

`raw/` 存原文，只在本地；`wiki/sources/` 一个来源一页；`wiki/log.md` 记每次操作。

现有 18 个来源、4 个 lens：`agentic-robotics`、`agent-loop`、`robotics-rl`、`jev`。
设计理由见 [docs/design.md](docs/design.md)。

## 贡献与许可

改动一律走 pull request，见 [CONTRIBUTING.md](CONTRIBUTING.md)。
代码 MIT（[LICENSE](LICENSE)），wiki 与文档 CC BY 4.0（[LICENSE-CONTENT](LICENSE-CONTENT)）；来源原文版权归原作者，不在仓库分发。
