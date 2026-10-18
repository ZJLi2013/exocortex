# 用 Obsidian 看图谱

整个仓库就是一个 Obsidian vault。图谱用来看工作之间怎么关联：两个来源连到同一个评测集、模型或方法，就说明它们在这一点上可以放在一起看。

## 打开

1. 装 [Obsidian](https://obsidian.md)，「Open folder as vault」选仓库根目录。
2. `Ctrl+G` 开全局图谱。
3. `.obsidian/` 不进仓库，新 clone 要自己配一次图谱（见下节）；不配也能用，只是 `raw/`、文档也会混进图里。

## 配置图谱（一次）

在图谱右上角齿轮里：

- **Filters → Search files** 粘贴：

  ```text
  -path:raw -path:inbox -path:docs -path:scripts -path:wiki/lenses -file:log -file:README -file:AGENTS -file:CONTRIBUTING -file:LICENSE
  ```

- **Filters**：不勾「Existing files only」。评测集、模型、方法都没有页面，勾上它们就消失了。
- **Groups**：每个 lens 加一组，按 lens 给来源上色：

  ```text
  [lenses:agentic-robotics]
  [lenses:agent-loop]
  [lenses:llm-foundation-models]
  [lenses:robotics-rl]
  [lenses:jev]
  ```

## 图里有什么

| 节点 | 样子 | 来自来源页的 |
|---|---|---|
| 来源 | 按 lens 上色；没有 lens 的是默认色 | 文件本身 |
| 评测集 | 灰色，无页面 | `benchmarks` |
| 模型 | 灰色，无页面 | `models_used`、`models_compared` |
| 方法 | 灰色，无页面 | `methods` |

来源与来源之间的直连边来自正文「关联」一节（基于 / 对照 / 相悖），以及模型字段里链到库内来源页的模型（如 RSIGym 用了 [[deepseek-v4-1-flash]]）。

- **边不带类型**：Obsidian 不按边的类型上色。「用了」还是「对照了」某个模型，要打开来源页看 frontmatter 和正文「模型」一行。
- **连了很多边的灰点**（GPT-6 Astra、Kimi-K3）是被很多工作用到或拿来对照的模型，跨 lens 的边主要经过它们。

## 常用看法

| 想看 | 做法 |
|---|---|
| 某个工作和谁相关 | 打开来源页，命令面板（`Ctrl+P`）运行「Graph view: Open local graph」，Depth 调到 2：经共享节点相连的来源都会出现 |
| 哪些工作用了 / 对照了某个模型 | 搜索面板（`Ctrl+Shift+F`）搜 `"[[GPT-6 Astra]]"`，命中的来源页再看是在 `models_used` 还是 `models_compared` |
| 某个方向的全貌 | 打开 `wiki/lenses/<lens>.md`：总结加每个工作一行 highlight |
| 按日期或 lens 列表浏览 | 打开 `wiki/index.base`：`sources` 全部来源，`unowned` 没有 lens 的来源，`lenses` 各方向 |

## 别点灰色节点

在图谱里点评测集、模型、方法这类灰点，Obsidian 会在仓库根目录新建一个同名空页，这个点也就变成了「有页面」的普通节点。误点了就删掉那个空文件。要看谁连着它，用 local graph 或上面的搜索。

## 改动在 agent 对话里做

来源页、lens 页由 agent 按 [AGENTS.md](../AGENTS.md) 维护。在 Obsidian 里能直接改的只有 lens 的范围、总结和工作行，agent 不改回；其余改动在 agent 对话里说。
