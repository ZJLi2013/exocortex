# exocortex 设计决策

**一句话：来源平铺、概念自下而上长、研究问题（lens）自上而下由人定，LLM 只写草稿，改变判断的那一步永远归人。**

执行细节（收录步骤、frontmatter 模板、命令）以 [AGENTS.md](../AGENTS.md) 为准；验收结果与进度见 [mvp.md](mvp.md)。
本文只记「为什么这样设计」和「放弃了什么」。

## 三层：raw / wiki / schema

| 层 | 内容 | 谁写 | 规则 |
|---|---|---|---|
| `raw/` | 抓下来的原文 | agent | 写一次不改，是事实的最终出处 |
| `wiki/` | 来源页、概念页、lens、log | agent（lens 的范围与当前判断归人） | 每条事实可追回 `raw/` |
| `AGENTS.md` | 怎么收录、查询、lint、批准 | 人 | agent 的唯一操作手册 |

取自 [Karpathy llm-wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)。

- **raw 只放原始来源，不放综合页。** r2 把两份 tracker 文档（本身是 LLM 写的综合）镜像进 `raw/`，能查但层次错位：
  事实没有出处，wiki 只能复述别人的总结。r3 改为从论文、README、博客原文编译。
- **raw 存之前去站点外壳，存之后不改。** 导航、页脚、营销滚动条不算原文；去掉后的文本就是以后所有引用的基准。

## concept 与 lens 的分工

| | concept（概念页） | lens（研究问题） |
|---|---|---|
| 回答 | 「它是什么」：哪些来源共享同一个想法 | 「它改变我什么」：支持 / 削弱 / 新增哪条判断 |
| 方向 | 自下而上，从来源里长出来 | 自上而下，人定义一句范围 |
| 谁能改 | LLM 全权维护 | 范围与「当前判断」只有人能改；LLM 写待批准草稿 |
| 一条来源可以属于 | 任意多个 | 0 到多个 |

两者都不是分类：概念页描述内容间的关联，lens 描述对决策的影响。

### concept

- **第二个来源提到才建页。** 只被一个来源提到的概念留在该来源的 frontmatter，不成页。避免每条来源都长出一堆孤页。
- **建页前先查同义名，复用已有名字。** 概念名漂移会让聚类断开；t3 合并过「程序进化搜索」与「进化式代码搜索」。
- **建页时回扫旧来源。** 旧来源正文明确体现该概念的，补进它的 `concepts` 并链回；否则早收录的来源永远链不进后长出的概念。

### lens

- **范围是一句话，判定是 keep / reject。** 取自 embodied_radar 的 `domain.yaml`：一句范围足够 LLM 判，也逼人把问题说清。
- **LLM 只写草稿，不改「当前判断」。** 判断是人的结论，LLM 的产出是证据。草稿用 `> [!draft]`，与已有判断冲突用
  `> [!contradiction]`，都等人批准（冲突写法取自 [claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian)）。
- **lens 是问题，不是主题。** 「机器人」不是 lens；「会改变 RoboRSI 选底座、改进方向或评测选择的工作」是。

## 不做人工分类

- **不按主题分文件夹，不手写 index。** 目录只按页面类型分（sources / concepts / lenses），类型是结构不是主题。
- **依据**：3dgen_tracker 手写的 9 个类混用了四个轴，留一法一致性只有 0.42–0.93；分类表一旦手写就要人维护，不可扩展。
- **索引由 Obsidian Bases 从 frontmatter 生成**（`wiki/index.base`）：sources、unowned、concepts、lenses 四个视图。

## lens 之外的来源：提议新 lens

进来的来源很可能不属于任何已有问题（t4 里 6 个新链接 5 个两个 lens 都 reject）。

- **触发**：某个概念页链到 ≥ 2 个 `lenses: []` 的来源 → 成一簇，共享来源的簇合并；在每次收录批次结束后跑 lint lenses。
- **产出**：`status: proposed` 的候选 lens，附范围草案；放宽某个已有 lens 即可覆盖时，写一行「也可并入」。
- **候选 lens 不参与收录判定。** 未批准的问题不吸新来源，避免越长越大。
- **只有人能批准 / 并入 / 否决。** 批准后 agent 对全库补判；否决记进 log，同一簇没有新来源加入就不再提。
- **单个无 lens 来源不提议**，留在 Bases 的 `unowned` 视图里可见。

## 执行与校验

- **整理者是 coding agent，按 `AGENTS.md` 执行。** Cursor 会自动加载根目录的 `AGENTS.md`；换别的 agent 只要先读它。
  t4 / t5 验证了新 agent 只拿一句「收录 inbox」「lint lenses」就能完成，不需要额外指令。
- **校验不依赖 Obsidian 运行。** Obsidian CLI 要求应用开着，无头运行时不可靠；`evals/check_wiki.py` 直接解析文件查断链与字段。
  Obsidian 只用于浏览。
- **查询集作回归**：`evals/check_answers.py` 的 5 题，由无设计上下文的 agent 只读 wiki 作答，≥ 4/5 通过。

## 放弃的方案

| 方案 | 放弃原因 |
|---|---|
| 把现有 tracker 文档镜像进 vault（r2） | 综合页放进 `raw/` 是层次错位，事实无出处 |
| 手写 index / 主题分类 | 不可扩展；手写分类混轴（见上） |
| 一张大图不设 lens，全靠来源自己聚类 | 聚类只能说「它是什么」，说不了「它改变我哪个判断」；lens 让判断有归属 |
| LLM 直接改「当前判断」或自建 lens | 判断与研究问题是人的；LLM 只出证据与提议 |
| 校验走 Obsidian CLI | 要求 Obsidian 开着，无头运行会失败 |
| 现在就上 embedding 聚类 | 来源才十几个，概念页聚类够用；上百后再复用 3dgen_tracker 的近邻图 + Louvain |

## 已知缺口

- 「也可并入」没有判据；放宽一个 lens 的范围会顺带吸入别的来源，规则没要求写出这种副作用。
- 没有概念页的概念不参与 lens 聚类，主题相近但概念名不同的无 lens 来源会被漏掉。
- 收录仍需人在对话里触发；inbox 有新内容时自动收录（无头触发）尚未实现。
