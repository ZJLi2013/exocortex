# Contributing

所有改动都走 pull request，`main` 受保护，任何人（包括维护者和本地 agent）都不能直接 push。

## 流程

1. Fork 或在本仓库开分支，分支名写改动内容（`fix-check-wiki-links`、`agents-md-fetch-rules`）。
2. 提交前跑 `python scripts/check_wiki.py --sources <来源数>`，退出 0。
3. 开 PR，按模板填写；CI 跑 `check-wiki`，通过才能合并。维护者 review 后 squash merge。

例外：维护者本地 agent 的收录类 PR 由 agent 开启 auto-merge，CI 通过即 squash merge，维护者事后看。
收录类指 diff 只碰 `wiki/sources/`、`wiki/lenses/`、`inbox/`、`wiki/*-rejections.yaml`、`docs/human-tags.md`、`docs/model-names.md`；
碰到 `AGENTS.md`、`scripts/`、`.github/` 或其它文件的仍由维护者合并。

## 欢迎的改动

- `AGENTS.md` 的规则：收录、lint lenses、查询哪里不够用，最好附上 agent 实际卡住的例子。
- `scripts/` 的修复与改进。
- 来源页的事实错误：指出原文出处（URL 与段落）。
- 想推荐收录的链接：开 issue，不用 PR。

## 不接受的改动

- **lens 的「范围」**：这是维护者自己选的研究方向。不同意，开 issue 讨论。
- **第三方全文**：`raw/` 只在本地保留，不进仓库；来源页只摘关键数字与短引用。
- 按主题建目录或手写分类索引，设计理由见 [docs/design.md](docs/design.md)。

## AI 辅助

本仓库本身由 LLM 整理，用 AI 写贡献完全可以，但 PR 里要写明：

- 用了哪个工具（Cursor、Claude Code、Codex 等）；
- AI 参与到什么程度（起草后人改、整段生成未改等）；
- 你能脱离 AI 讲清这次改动做了什么。讲不清的 PR 会被关掉。

不接受 AI 生成的图片、视频、音频。

## 许可

提交即表示同意：代码以 MIT（[LICENSE](LICENSE)）、文字以 CC BY 4.0（[LICENSE-CONTENT](LICENSE-CONTENT)）发布。
