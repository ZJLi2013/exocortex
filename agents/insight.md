# insight agent

读 [collector](collector.md) 维护的证据层，为每个已批准 lens 写一页判断：下一个值得做的方向与未解决的问题。读者是这个方向的 researcher。

## insight 页

`wiki/insights/<lens>.md`，文件名与 lens 同名，正文用英文：

```markdown
---
type: insight
lens: "[[agentic-robotics]]"
updated: YYYY-MM-DD
---
# agentic-robotics: insight

## Directions

### <一句：下一个值得做什么>

- **Why**: <跨工作的观察，链 [[slug]]>
- **Gap**: <现有工作都没测过的条件或问题>
- **First experiment**: <一个能检验它的具体实验>

## Open problems

- **<问题>**: <为什么现有工作没解决，链 [[slug]]>
```

- 方向最多 3 条，问题最多 3 条；正文不超过 80 行。
- 每条方向、问题都链到支撑它的来源页；链的是 lens 外的库内来源也可以。

## 写 insight（human 说「写 insight <lens>」）

1. 读 lens 页与它「工作」里的全部来源页；某条判断要靠的细节，回来源页的 `url` 读原文，不落盘。
2. 找跨工作的东西：几项工作共同依赖的前提、共同回避的条件、彼此不一致的数字、一项工作的局限恰好是另一项的贡献、评测集是否已经饱和或只有自报。
3. 起草后、自检前逐条**查新**：在 3dgen_tracker 的论文库里查是否已有人做（`scripts/query_papers.py prior`，用法见该仓库 readme「论文图谱」）。
   种子取这条方向链到、且在那个库里的来源，加 2–4 个 title / summary 关键词；读候选摘要，逐篇判已做 / 部分重叠 / 无关：
   - 已做 → 改写 Gap 或删掉这条方向；
   - 部分重叠 → 重叠工作有来源页的，在 Why 或 Gap 里链上；没有的，URL 追加进 `inbox/proposals.md`（`## [YYYY-MM-DD] novelty <lens>` 一节）等 human 处置，方向里不引用；
   - 只读了摘要的比较写「摘要未说明」，不写成「没人做」。那个库只含 tracker 入选与本库导入的论文，查不到不等于没人做。
   - 全 arXiv 检索（`scripts/search_candidates.py --days 0 --include-known`）只作线索：命中的相关工作照上面进 proposals，不作「未见」的依据——已知重叠工作它两轮只召回 0–1/4。
4. 逐条过自检，过不了的删掉，不改写到勉强通过：
   - 只复述某一项工作的摘要或贡献 → 删；
   - 放到任何领域都成立（「需要更多数据」「提升泛化」「走向真实部署」）→ 删；
   - 没有链接，或链到的来源支撑不了它 → 删；
   - 只靠自报数字却没写明是自报 → 补上或删；
   - 方向给不出具体的第一个实验 → 删。
5. 高质量指带来新的研究 idea 或方向；实验细节多不等于高质量，不为凑细节堆数字。
6. 已有 insight 页时在原页上改：human 写的或改过的行不改回。
7. `python scripts/check_wiki.py --sources <来源总数>`，开 PR，等 human 合并。PR 描述每条方向一行，写它依据哪几个来源，再附一段查新：种子、关键词、读了多少篇，判为已做 / 部分重叠的论文。

## 边界

- 判断只写进 `wiki/insights/`；不往来源页、lens 页搬判断，lens 总结保持中立。
- 证据层撑不住某条判断时，在 PR 描述里写缺哪类来源，交给 collector，不在 insight 页里补事实。
