# exocortex

研究领域的个人知识库：你丢链接，LLM 整理成 Obsidian wiki，并判断它会改变你哪个研究问题的哪条判断。
你只挑源、提问、裁决冲突，不做分类。

## 准备

无需安装。clone 后用 Cursor 打开，根目录的 [AGENTS.md](AGENTS.md) 会自动加载为 agent 规则；
用 Claude Code、Codex CLI 等则先让它读一遍 `AGENTS.md`。检查脚本只需 Python 3 标准库；[Obsidian](https://obsidian.md) 可选，用来浏览。

## 怎么用

在 agent 对话里：

| 你想做 | 怎么做 |
|---|---|
| 收录 | 把 URL 写进 `inbox/links.md`，标签先查 [docs/human-tags.md](docs/human-tags.md) 里已有的写法（`<URL> #jev`），说「收录 inbox」 |
| 查询 | 直接提问，答案引用 `wiki/` 里的页面 |
| 裁决冲突 | `wiki/lenses/<lens>.md` 的「冲突」里只有在相同条件下反驳已有判断的来源，和与你标签不一致的来源。说「<lens> 采纳 / 不采纳 C<N>」或「<lens> 收下 / 不收 <工作名>」 |
| 处置新 lens | 出现 `status: proposed` 的 lens 时，说「批准 lens <name>」「并入 <已有 lens>」或「否决 lens <name>」 |
| 检查 | `python scripts/check_wiki.py --sources <来源数>` |

## 怎么组织

- **lens**（`wiki/lenses/`）：你的研究问题。一句话范围下拆成几个决策问题，每个问题有一句「当前答案」；答案依据的判断各带支持 / 限定 / 反驳证据和推翻条件。归属与判断由 LLM 维护，只有冲突才等你。
- **你的标签**（来源页 `tags:`）：丢链接时打的 `#tag`，先用 [已有写法](docs/human-tags.md)。LLM 照抄，不把近义标签并成一个；它只用来决定先判哪个 lens，归属仍按内容定。
- **新 lens**：两个以上无 lens 的来源共享一个标签时，LLM 起草候选 lens 等你处置。

`wiki/sources/` 一个来源一页；`raw/` 存原文、`wiki/log.md` 记每次操作，这两样只在本地。

现有 23 个来源、5 个 lens：`agentic-robotics`、`agent-loop`、`robotics-rl`、`jev`、`llm-foundation-models`。
设计理由见 [docs/design.md](docs/design.md)。

## 贡献与许可

改动一律走 pull request，见 [CONTRIBUTING.md](CONTRIBUTING.md)。
代码 MIT（[LICENSE](LICENSE)），wiki 与文档 CC BY 4.0（[LICENSE-CONTENT](LICENSE-CONTENT)）；来源原文版权归原作者，不在仓库分发。
