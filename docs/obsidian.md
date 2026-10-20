# 用 Obsidian 看图谱

整个仓库就是一个 Obsidian vault。全局图谱与 [网页](https://zjli2013.github.io/exocortex/) 的关系图一致：只画已批准的 lens 和它们收的来源，看每个方向有哪些工作、工作之间怎么关联。

## 打开

1. 装 [Obsidian](https://obsidian.md)，「Open folder as vault」选仓库根目录。
2. `Ctrl+G` 开全局图谱。
3. 仓库自带 vault 级排除规则，`raw/` 不会进入搜索、反向链接或图谱。图谱的显示范围和颜色仍需按下节配置一次。

## 配置图谱（一次）

在图谱右上角齿轮里：

- **Filters → Search files** 粘贴（批准新 lens 后在末尾加一个 `OR [lenses:<name>]`）：

  ```text
  (path:wiki/lenses -[status:proposed]) OR [lenses:agentic-robotics] OR [lenses:agent-loop] OR [lenses:agentic-3d] OR [lenses:robotics-rl] OR [lenses:jev] OR [lenses:llm-foundation-models]
  ```

- **Filters**：勾「Existing files only」，不勾「Orphans」。评测集、模型、方法没有页面，这样就不进全局图谱。
- **Groups**：第一组 `path:wiki/lenses` 给 lens 节点一个深色，之后每个 lens 一组，按 lens 给来源上色：

  ```text
  [lenses:agentic-robotics]
  [lenses:agent-loop]
  [lenses:agentic-3d]
  [lenses:llm-foundation-models]
  [lenses:robotics-rl]
  [lenses:jev]
  ```

## 图里有什么

| 节点 / 边 | 来自 |
|---|---|
| lens 节点 | `wiki/lenses/` 里已批准的 lens 页 |
| 来源节点，按 lens 上色 | `lenses` 不为空的来源页；`lenses: []` 的来源不画 |
| lens ↔ 来源 | lens 页「工作」行与来源页 `lenses` 字段 |
| 来源 → 来源 | 正文「关联」一节（基于 / 对照 / 相悖），以及模型字段里链到库内来源页的模型（如 RSIGym 用了 [[deepseek-v4-1-flash]]） |

Obsidian 不按边的类型上色；关系类型要打开来源页看「关联」。

## 操作

| 操作 | 效果 |
|---|---|
| 鼠标悬停在节点上 | 高亮它和直接相连的节点，其余变淡 |
| 滚轮 | 缩放；缩小时标签会隐藏，放大才显示 |
| 拖空白处 / 拖节点 | 平移画布 / 把节点拉开看清连线 |
| 点节点 | 打开那个 lens 页或来源页 |

齿轮里的 **Forces** 调布局：图挤成一团时调大 Repel force 和 Link distance。

## 常用看法

| 想看 | 做法 |
|---|---|
| 某个工作经评测集、模型、方法和谁相连 | 打开来源页，命令面板（`Ctrl+P`）运行「Graph view: Open local graph」，Depth 调到 2。local graph 的过滤独立于全局图谱，默认画出评测集、模型、方法这些无页面的灰点；别点灰点，点了 Obsidian 会在仓库根目录新建同名空页，误点就删掉 |
| 哪些工作用了 / 对照了某个模型 | 搜索面板（`Ctrl+Shift+F`）搜 `"[[GPT-6 Astra]]"`，命中的来源页再看是在 `models_used` 还是 `models_compared` |
| 某个方向的全貌 | 打开 `wiki/lenses/<lens>.md`：总结加每个工作一行 highlight |
| 按日期或 lens 列表浏览 | 打开 `wiki/index.base`：`sources` 全部来源，`unowned` 没有 lens 的来源，`lenses` 各方向 |

## 改动在 agent 对话里做

来源页、lens 页由 agent 按 [AGENTS.md](../AGENTS.md) 维护。在 Obsidian 里能直接改的只有 lens 的范围、总结和工作行，agent 不改回；其余改动在 agent 对话里说。
