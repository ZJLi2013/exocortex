# 用 Obsidian 看图谱

整个仓库就是一个 Obsidian vault。图谱用来看工作之间怎么关联：两个来源连到同一个评测集、模型或方法，就说明它们在这一点上可以放在一起看。

## 打开

1. 装 [Obsidian](https://obsidian.md)，「Open folder as vault」选仓库根目录。
2. `Ctrl+G` 开全局图谱。
3. 仓库自带 vault 级排除规则，`raw/` 不会进入搜索、反向链接或图谱。图谱的显示范围和颜色仍需按下节配置一次。

## 配置图谱（一次）

在图谱右上角齿轮里：

- **Filters → Search files** 粘贴：

  ```text
  -path:inbox -path:docs -path:scripts -path:wiki/lenses -file:log -file:README -file:AGENTS -file:CONTRIBUTING -file:LICENSE -file:index
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

## 第一次用：图谱怎么操作

| 操作 | 效果 |
|---|---|
| 鼠标悬停在节点上 | 高亮它和直接相连的节点，其余变淡。看一个模型或方法连着哪些工作，最快就是悬停 |
| 滚轮 | 缩放；缩小时标签会隐藏，放大才显示 |
| 拖空白处 | 平移画布 |
| 拖节点 | 把它拉开看清连线，松手后会弹回布局 |
| 点**彩色**节点 | 打开那个来源页 |
| 点**灰色**节点 | 不要点，见「别点灰色节点」 |

齿轮里的 **Display** 可以调显示：Arrows 开关箭头，Text fade threshold 调标签在多大缩放下出现，Node size / Link thickness 调点和线的粗细。
**Forces** 调布局：Repel force 调大，节点散得更开；Link distance 调大，连线更长。图挤成一团时调这两项。

## 图里有什么

| 节点 | 样子 | 来自来源页的 |
|---|---|---|
| 来源 | 按 lens 上色；没有 lens 的是默认色 | 文件本身 |
| 评测集，如 RoboDojo | 灰色，无页面 | `benchmarks` |
| 模型，如 GPT-6 Astra、π0.5 | 灰色，无页面 | `models_used`、`models_compared` |
| 方法，如 harness evolution、code skills from experience、evolutionary code search | 灰色，无页面 | `methods` |

箭头从来源指向它链接的节点。灰点没有页面，是故意的：它们只用来把引用同一个评测集、模型或方法的来源连起来。

来源与来源之间的直连边来自正文「关联」一节（基于 / 对照 / 相悖），以及模型字段里链到库内来源页的模型（如 RSIGym 用了 [[deepseek-v4-1-flash]]）。

- **边不带类型**：Obsidian 不按边的类型上色。「用了」还是「对照了」某个模型，要打开来源页看 frontmatter 和正文「模型」一行。
- **连了很多边的灰点**（GPT-6 Astra、Kimi-K3）是被很多工作用到或拿来对照的模型，跨 lens 的边主要经过它们。
- `raw/` 里的 README 常有指向子目录 README、图片和示例文件的相对链接。vault 级排除规则会连同这些出边一起隐藏，避免 `README` / `SKILL` 灰点和同名 raw/source 双节点。

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
