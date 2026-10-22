# exocortex

研究领域的个人知识库：你丢链接，LLM 整理成 Obsidian wiki，并按研究方向汇总各工作的要点。
你只挑源、定方向、提问，不做分类。

## 准备

无需安装。clone 后用 Cursor 打开，根目录的 [AGENTS.md](AGENTS.md) 会自动加载为 agent 规则；
用 Claude Code、Codex CLI 等则先让它读一遍 `AGENTS.md`。检查脚本只需 Python 3 标准库；[Obsidian](https://obsidian.md) 可选，用来浏览。

## 怎么用

**在线浏览**：[zjli2013.github.io/exocortex](https://zjli2013.github.io/exocortex/)，合并到 `main` 后自动更新，构建方式见 [docs/github-pages.md](docs/github-pages.md)。

**本地浏览与看图谱用 Obsidian**：打开方式、图谱配置和常用看法见 [docs/obsidian.md](docs/obsidian.md)。

其余在 agent 对话里：

| 你想做 | 怎么做 |
|---|---|
| 收录 | 把 URL 写进 `inbox/links.md`，标签先查 [docs/human-tags.md](docs/human-tags.md) 里已有的写法（`<URL> #jev`），说「收录 inbox」 |
| 收录关注网络的新工作 | 说「feed 收录」：[feed/](feed/README.md) 每天从 GitHub feed 与头部团队渠道挑出的工作直接收录，每次最多 5 条 |
| 撤销 | 说「删 <来源>」，以后不再收，也成为 feed 判定的负例 |
| 查询 | 直接提问，答案引用 `wiki/` 里的页面 |
| 处置新 lens | 出现 `status: proposed` 的 lens 时，说「批准 lens <name>」「并入 <已有 lens>」或「否决 lens <name>」 |
| 检查 | `python scripts/check_wiki.py --sources <来源数>` |

## 怎么组织

- **lens**（`wiki/lenses/`）：一个研究方向。一句话范围下是两三句中立总结，和每个工作一行的 highlight。范围归你，其余由 LLM 维护。
- **你的标签**（来源页 `tags:`）：丢链接时打的 `#tag`，先用 [已有写法](docs/human-tags.md)。LLM 照抄，不把近义标签并成一个；它只用来决定先判哪个 lens，归属仍按内容定。
- **新 lens**：两个以上无 lens 的来源共享一个标签时，LLM 起草候选 lens 等你处置。

`wiki/sources/` 一个来源一页，原文只在收录时读、不保存。

现有的 lens 与各自收的工作见 [网页](https://zjli2013.github.io/exocortex/)。设计理由与 token 开销见 [docs/design.md](docs/design.md)，接下来要做什么见 [docs/roadmap.md](docs/roadmap.md)。

## 贡献与许可

改动一律走 pull request，见 [CONTRIBUTING.md](CONTRIBUTING.md)。
代码 MIT（[LICENSE](LICENSE)），wiki 与文档 CC BY 4.0（[LICENSE-CONTENT](LICENSE-CONTENT)）；来源原文版权归原作者，不在仓库分发。
