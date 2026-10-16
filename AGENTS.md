# exocortex

研究领域的个人知识库，按 [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 的三层组织。整个仓库就是一个 Obsidian vault。

## 目录

| 路径 | 内容 | 谁写 |
|---|---|---|
| `raw/<source>/` | 各 tracker 的只读快照，保留源内相对目录 | 只由 `python scripts/sync_sources.py` 写 |
| `raw/manifest.md` | 每个源的路径、源 commit、文件数 | 同上 |
| `wiki/index.md` | 每个源一节：是什么、入口、核查日期范围 | agent |
| `wiki/log.md` | 追加日志，最新在下 | agent |

**`raw/` 不手改。** 要改内容，改源仓库里的原文件，再跑同步。源列表在 `scripts/sync_sources.py` 顶部。

## 查询

1. 读 `wiki/index.md` 判断哪些源相关。
2. 在 `raw/` 里 `rg` 关键词，再读命中的文件；`landscape.md` 只是地图，细节在 `works/`。
3. 答案里每条事实引用 `raw/` 下的文件路径。查不到就说查不到，不去原仓库补。
4. 在 `wiki/log.md` 追加 `## [YYYY-MM-DD] query | <问题>`。

## 同步

改了源文件或新增源后跑 `python scripts/sync_sources.py`，`--check` 验证 `raw/` 与源一致；
有变化时在 `wiki/log.md` 追加 `## [YYYY-MM-DD] sync | <哪些源>`，并更新 `wiki/index.md` 里对应一节。
