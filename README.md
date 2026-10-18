# exocortex

研究领域的个人知识库：你丢链接，LLM 整理成 Obsidian wiki，并按研究方向汇总各工作的要点。
你只挑源、定方向、提问，不做分类。

## 准备

无需安装。clone 后用 Cursor 打开，根目录的 [AGENTS.md](AGENTS.md) 会自动加载为 agent 规则；
用 Claude Code、Codex CLI 等则先让它读一遍 `AGENTS.md`。检查脚本只需 Python 3 标准库；[Obsidian](https://obsidian.md) 可选，用来浏览。

## 怎么用

在 agent 对话里：

| 你想做 | 怎么做 |
|---|---|
| 收录 | 把 URL 写进 `inbox/links.md`，标签先查 [docs/human-tags.md](docs/human-tags.md) 里已有的写法（`<URL> #jev`），说「收录 inbox」 |
| 查询 | 直接提问，答案引用 `wiki/` 里的页面 |
| 看关联 | 用 Obsidian 打开仓库，`Ctrl+G` 开图谱：来源之间的边来自评测集节点和来源页的「关联」（基于 / 对照 / 相悖） |
| 裁决冲突 | `wiki/lenses/<lens>.md` 的「冲突」里是你的标签指向它、LLM 却按内容 reject 的来源。说「<lens> 收下 / 不收 <工作名>」 |
| 处置新 lens | 出现 `status: proposed` 的 lens 时，说「批准 lens <name>」「并入 <已有 lens>」或「否决 lens <name>」 |
| 检查 | `python scripts/check_wiki.py --sources <来源数>` |

## 怎么组织

- **lens**（`wiki/lenses/`）：一个研究方向。一句话范围下是两三句中立总结，和每个工作一行的 highlight。范围归你，其余由 LLM 维护。
- **你的标签**（来源页 `tags:`）：丢链接时打的 `#tag`，先用 [已有写法](docs/human-tags.md)。LLM 照抄，不把近义标签并成一个；它只用来决定先判哪个 lens，归属仍按内容定。
- **新 lens**：两个以上无 lens 的来源共享一个标签时，LLM 起草候选 lens 等你处置。

`wiki/sources/` 一个来源一页；`raw/` 存原文、`wiki/log.md` 记每次操作，这两样只在本地。

现有 25 个来源、5 个 lens：`agentic-robotics`、`agent-loop`、`robotics-rl`、`jev`、`llm-foundation-models`。
设计理由见 [docs/design.md](docs/design.md)。

## 贡献与许可

改动一律走 pull request，见 [CONTRIBUTING.md](CONTRIBUTING.md)。
代码 MIT（[LICENSE](LICENSE)），wiki 与文档 CC BY 4.0（[LICENSE-CONTENT](LICENSE-CONTENT)）；来源原文版权归原作者，不在仓库分发。
