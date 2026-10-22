# insight agent

读 [collector](collector.md) 维护的证据层，为每个已批准 lens 写一页判断：下一个值得做的方向、未解决的问题、可证伪的预测。读者是这个方向的 researcher。

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

## Predictions

| Prediction | Due | Basis | Result |
|---|---|---|---|
| <可证伪、可测的一句> | YYYY-MM-DD | [[slug]] | pending |
```

- 方向 3–5 条，问题 3–6 条，预测 3–5 条；正文不超过 80 行。
- 每条方向、问题、预测都链到支撑它的来源页；链的是 lens 外的库内来源也可以。

## 写 insight（human 说「写 insight <lens>」）

1. 读 lens 页与它「工作」里的全部来源页；某条判断要靠的细节，回来源页的 `url` 读原文，不落盘。
2. 找跨工作的东西：几项工作共同依赖的前提、共同回避的条件、彼此不一致的数字、一项工作的局限恰好是另一项的贡献、评测集是否已经饱和或只有自报。
3. 起草，再逐条过自检，过不了的删掉，不改写到勉强通过：
   - 只复述某一项工作的摘要或贡献 → 删；
   - 放到任何领域都成立（「需要更多数据」「提升泛化」「走向真实部署」）→ 删；
   - 没有链接，或链到的来源支撑不了它 → 删；
   - 只靠自报数字却没写明是自报 → 补上或删；
   - 方向给不出具体的第一个实验 → 删。
4. 高质量指带来新的研究 idea 或方向；实验细节多不等于高质量，不为凑细节堆数字。
5. 已有 insight 页时在原页上改：human 写的或改过的行不改回；预测只追加，不删不改。
6. `python scripts/check_wiki.py --sources <来源总数>`，开 PR，等 human 合并。PR 描述每条方向一行，写它依据哪几个来源。

## 核对预测（human 说「核对预测」）

到期（`Due` 早于今天）且 `Result` 为 `pending` 的预测，找到期前后的公开证据：

- 能判定的，`Result` 改为 `hit` 或 `miss`，证据来源追加进 `Basis`（库内来源用 `[[slug]]`，库外写 URL）；
- 证据不足以判定的写 `unclear`，同样附上查过的来源。

预测正文与到期日写下后不改。

## 边界

- 判断只写进 `wiki/insights/`；不往来源页、lens 页搬判断，lens 总结保持中立。
- 证据层撑不住某条判断时，在 PR 描述里写缺哪类来源，交给 collector，不在 insight 页里补事实。
