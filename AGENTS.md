# exocortex

研究领域的个人知识库，按 [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 组织。整个仓库是一个 Obsidian vault。
目标是给领域 researcher 方向 insight：下一个值得做的方向、未解决的问题与可证伪的预测。
human 丢链接、提问、定 lens 范围、处置候选 lens；其余由两个 agent 执行，规则各在一个文件里。

## 两个 agent

| agent | 做什么 | human 说 | 规则 |
|---|---|---|---|
| collector | 持续收录新工作，维护中立的证据层（来源页、lens 页、否决记录） | 「收录 inbox」「feed 收录」「lint lenses」「搜索候选」「删 X」、处置候选 lens | [agents/collector.md](agents/collector.md) |
| insight | 读证据层，为每个方向写判断，到期核对预测 | 「写 insight <lens>」「核对预测」 | [agents/insight.md](agents/insight.md) |

接到上面任一句话，先读对应的规则文件再动手。证据层只记事实，判断只写进 `wiki/insights/`；两边不互相搬运。

## 目录

| 路径 | 内容 | 谁写 |
|---|---|---|
| `inbox/links.md` | 待收录的 URL，一行一个，可跟 human 标签：`<URL> #jev #kernel` | human |
| `inbox/proposals.md` | 搜索出的候选来源，等 human 处置 | collector |
| `wiki/sources/<slug>.md` | 一个来源一页 | collector |
| `wiki/lenses/<name>.md` | 一个研究方向：范围、总结、工作 | 范围归 human；总结与工作由 collector 维护 |
| `wiki/insights/<lens>.md` | 一个方向的判断：方向、未解决问题、预测 | insight agent 起草，human 改 |
| `wiki/index.base` | Bases 视图，从 frontmatter 生成 | 不手改 |
| `wiki/lens-rejections.yaml` | human 否决过的候选 lens 与当时的簇内来源 | collector |
| `wiki/search-rejections.yaml` | human 否决过的搜索候选与撤销的来源 URL；`feed/` 的判定每天读作负例 | collector |
| `feed/` | 感知与判定代码：读 GitHub feed 与公司渠道，产出「feed 收录」读的候选文件（见 [feed/README.md](feed/README.md)） | collector |
| `agents/` | 两个 agent 的规则 | human 合并 |

不按主题建目录。分组靠 lens 与两种标签，都不是预设分类：

- `tags`：human 丢链接时打的标签，带着 human 的意图（「大概是 jev 相关」），agent 照抄不改；
- `concepts`：agent 读原文后打的标签，写方法或主张。

## 合并

所有改动走 PR。只碰 [CONTRIBUTING.md](CONTRIBUTING.md) 列出的收录类路径的 PR 由 agent 开 auto-merge；insight 页、规则、脚本的改动等 human 合并。

## 查询

1. 列 `wiki/sources/` 看有哪些来源，或全文搜 `wiki/`。
2. 问方向、问下一步做什么，先读 `wiki/insights/<lens>.md`，引用时说明那是判断；问事实先读 lens 页：「总结」给方向概貌，「工作」给每个来源的 highlight；再按 `tags:` / `concepts:` 标签或全文搜索找来源页；细节不够才打开来源页的 `url`。
3. 每条事实引用页面路径（`wiki/sources/<slug>.md`）。查不到就说查不到。
