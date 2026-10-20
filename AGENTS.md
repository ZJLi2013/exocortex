# exocortex

研究领域的个人知识库，按 [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 组织。整个仓库是一个 Obsidian vault。
human 丢链接、提问、定 lens 范围、裁决冲突；其余由 agent 按本文件执行。

## 目录

| 路径 | 内容 | 谁写 |
|---|---|---|
| `inbox/links.md` | 待收录的 URL，一行一个，可跟 human 标签：`<URL> #jev #kernel` | human |
| `inbox/proposals.md` | 搜索出的候选来源，等 human 处置 | agent |
| `raw/<slug>.md` | 抓取的原文，写一次不改 | agent |
| `wiki/sources/<slug>.md` | 一个来源一页 | agent |
| `wiki/lenses/<name>.md` | 一个研究方向：范围、总结、工作、冲突（格式见下节） | 范围归 human；总结与工作由 agent 维护；冲突由 human 裁决 |
| `wiki/index.base` | Bases 视图，从 frontmatter 生成 | 不手改 |
| `wiki/lens-rejections.yaml` | human 否决过的候选 lens 与当时的簇内来源 | agent |
| `wiki/search-rejections.yaml` | human 否决过的搜索候选 URL | agent |
| `wiki/log.md` | 审计日志，只追加，只在本地；按事件类型或来源名搜索，不整份读 | agent |

不按主题建目录。分组靠 lens 与两种标签，都不是预设分类：

- `tags`：human 丢链接时打的标签，带着 human 的意图（「大概是 jev 相关」），agent 照抄不改；
- `concepts`：agent 读原文后打的标签，写方法或主张。

## lens 页

```markdown
---
type: lens
tags: [jev]
---
# <name>

## 范围

<一句话：这个方向包含哪类工作>

## 总结

<2–3 句高层概述：方向里有哪几类工作、证据共有的局限>

## 工作

- [[<slug>]]：<一两句 highlight：做了什么、最重要的结果（带评测集）>（自报）

## 冲突
```

- 范围只描述方向，不写用途。
- 总结中立：不逐个点名工作，不排高下，不写建议。
- 「工作」每个 keep 的来源一行，按 `published` 排序。只写这个工作自己的事实，不与其它工作比较。
  句末括号标自报或第三方：作者评自己的工作是自报，用了外部数据集不算第三方。

## 收录（human 说「收录 inbox」）

对 `inbox/links.md` 里每个 URL：

1. **去重**：在 `raw/` 里搜 `url: <URL>`（`rg` 或文件搜索工具），命中则跳过，log 记一行。
2. **抓原文**写 `raw/<slug>.md`。slug 用工作名的小写短横线形式（`embodiedevo`、`gemini-4-argon`）。
   arXiv 抓 `https://arxiv.org/html/<id>` 全文，抓不到再退到 abs 页。
   GitHub 仓库页只返回导航壳，改抓 `https://raw.githubusercontent.com/<owner>/<repo>/<branch>/README.md`；
   文件名可能是 `readme.md`，分支可能是 `master`。
   正文靠 JavaScript 填充的页面，下载 HTML 抽文本。存之前去掉导航、页脚、营销滚动条等站点外壳；存之后不改。
   README / 项目页没有数字但链了自己的论文时，把论文全文接在同一个 raw 文件后面。存原文用 `python scripts/save_raw.py --url <URL> --slug <slug> --title <标题> --from <抓到的文件>`。frontmatter：

   ```yaml
   url: <原 URL>
   fetched: YYYY-MM-DD
   title: <标题>
   ```

3. **写来源页** `wiki/sources/<slug>.md`：

   ```markdown
   ---
   type: source
   url: <原 URL>
   published: YYYY-MM-DD      # 首发日期（不取修订日）；没写日期但链了自己的 arXiv 编号就按编号写 YYYY-MM；都没有写 unknown
   ingested: YYYY-MM-DD
   tags: [jev]                # inbox 行里的 human 标签，去掉 #；没打写 []
   concepts: [概念 A, 概念 B]  # agent 标签，纯文本；见第 4 步
   benchmarks: ["[[RoboDojo]]"]   # 报了数字的评测集，链接形式；见第 4 步；没有写 []
   methods: ["[[evolutionary code search]]"]     # 方法节点；见第 4 步；没有写 []
   models_used: ["[[π0.5]]"]        # 用到的模型；见第 4 步；没有写 []
   models_compared: ["[[GPT-6 Astra]]"]   # 直接对照的模型；见第 4 步；没有写 []
   lenses: ["[[agentic-robotics]]"]   # keep 的 lens，链接形式；都不 keep 写 []
   ---
   # <工作名>

   <一句话：它做了什么、最重要的结果>

   - **关键数字**：带条件与口径，例「LIBERO-PRO 50.0% → 82.4%（自报，单次）」
   - **评估与接纳**：谁评、在哪个集合上评、谁宣布成功
   - **可信度**：作者自报 / 单次 / 未给评测次数 / 未开源 等
   - **模型**：每个模型的角色与版本，例「π0.5 是 harness 中的一个技能」；两个模型字段都空时不写
   - **原文**：[[raw/<slug>]]

   ## 关联

   - 对照 [[<slug>]]：<一句，带数字>
   ```

   只写原文里有的事实；推断写成「未说明」。正文不超过 40 行。

4. **concepts、图谱节点与关联**：
   - concepts 与 methods 合计 3–6 个，写这个来源的方法或主张，不写泛主题（「机器人」「LLM」不算）。
     先搜其它来源页的 `concepts:`，有同义的就用已有写法，不另起新名；确实没有才起新标签。不建概念页。
   - benchmarks 只列原文报了自己数字的评测集，写评测集族名、不带版本号（`DeepSWE`，不写 `DeepSWE v1.1`）；先搜其它来源页的写法。不建评测集页，它们在 Obsidian 图谱里是共享节点。
   - models_used 列这个工作用到的模型：底座、技能、裁判、被研究的对象。models_compared 只列它自己直接对照的模型；转载整张榜单不算，只取它点名比较的几个。
     同一模型可同时出现在两个字段。名字只用 [docs/model-names.md](docs/model-names.md) 左列的规范名，保留有意义的版本差别（Base / Instruct、π0.5 / π0.5-DROID）；
     原文写法是别名就换成规范名，表里没有就追加一行；模型有库内来源页时写来源页链接。角色写进正文「模型」一行，原文没说的写「未说明」。
   - methods 只用至少两个来源共有、且原文能核实的方法：`harness evolution`（agent 改写调用模型的外层代码，权重不变）、`code skills from experience`、`evolutionary code search`。
     方法节点名用英文，与模型、评测集节点一致。
     新来源让某个 concepts 标签第一次被两个来源共有、且它是可核实的方法时，才新增方法节点。方法写进 methods 后不再重复写进 concepts。
   - 关联只连库内来源，关系三选一：`基于`（用了对方的方法、组件或是它的新版本）、`对照`（拿对方当基线或在同一张表里比）、
     `相悖`（同一件事两边的数字或说法不一致）。相关工作里顺带一提的不连；对方是模型、已写进 models_compared 的不再写对照。写在主动方的页面上，一对来源一种关系一行；没有就不写这一节。
     双向查：新来源原文提到的库内工作，以及已有来源原文里提到新来源的（`rg` 搜 `raw/`，命中就给那个来源页补一行）。

5. **lens 判定**：逐个读 `wiki/lenses/*.md` 的「范围」，判这条来源 keep 还是 reject。跳过 `status: proposed` 的候选 lens。
   human 标签是线索不是归属：lens frontmatter `tags` 含来源某个标签时先判这个 lens，但仍按内容判。
   - reject：不写 lens 页，log 里记 lens 名与一句理由。标签指向这个 lens 却被 reject 时，在该 lens 的「冲突」下写：

     ```markdown
     > [!mismatch] <工作名>（YYYY-MM-DD）
     > 标签 #<tag> 指向本 lens，按内容 reject：<一句理由>。依据 [[<slug>]]
     ```

   - keep：把 lens 加进来源页 `lenses`，把来源的 human 标签补进该 lens 的 `tags`（已有则不加），在「工作」加一行。
     来源带来新的一类工作或新的共同局限时，改「总结」里对应的那一句；否则总结不动。

6. **log**：`wiki/log.md` 追加 `## [YYYY-MM-DD] ingest | <工作名>`，下面一行写 lens 判定结果。
7. 处理完的 URL 从 `inbox/links.md` 删除。human 标签若还不在 [docs/human-tags.md](docs/human-tags.md)，追加一行。不改已有写法，不把近义标签合并。

全部收录完做一遍下面的 lint lenses，再运行 `python scripts/check_wiki.py --sources <来源总数>`。

## lint lenses（收录批次结束后，或 human 说「lint lenses」）

lens 外的来源成簇时，提议一个新研究方向，由 human 决定要不要。

1. **找簇**：只看 `lenses: []` 的来源页。先比 `tags:`，≥ 2 个来源共享同一个 human 标签 → 成一簇；
   再比 `concepts:`，≥ 2 个来源共享同一个（或同义的）标签 → 成一簇。
   两簇共享任一来源就合并。不与任何其它无 lens 来源共享标签的来源不成簇。
2. **跳过**：已有候选 lens 覆盖同一簇时只追加新来源；簇内来源全部出现在 `wiki/lens-rejections.yaml` 某条记录的 `sources` 里时不提，有新来源加入才重提。
3. **提议**：每簇写 `wiki/lenses/<name>.md`（name 小写短横线；簇由 human 标签成簇时默认用该标签）：

   ```markdown
   ---
   type: lens
   status: proposed
   tags: [<簇内来源的 human 标签>]   # 没有写 []
   ---
   # <name>

   ## 范围

   <一句话草案：这个方向包含哪类工作>

   ## 为何提议

   - 来源：[[<slug>]]、[[<slug>]]
   - 共享标签：<标签>
   - 也可并入 [[<已有 lens>]]：<改后的范围句>   ← 只在放宽某个已有 lens 的范围句就能覆盖时写
   ```

   候选 lens 不改任何来源页的 `lenses`。
4. **log**：`## [YYYY-MM-DD] lint | lenses`，每个候选一行（名字与来源）；没有候选也记一行。

## 搜索候选（human 说「搜索候选」）

只把候选摆到 human 面前：agent 不写 `inbox/links.md`，不触发收录，不改 lens 与来源页。SearXNG 部署见 [docs/search-proposal.md](docs/search-proposal.md)。

1. **查询**：每个已批准 lens（跳过 `status: proposed`）写 2–5 条英文查询：范围句改写 2–3 条，lens 内来源共享的评测集各一条。
 写成临时文件，一行 `<lens> | <query>`。
2. **搜索与去重**：`python scripts/search_candidates.py <查询文件>`（需环境变量 `SEARXNG_URL`）。
 脚本丢掉近 30 天以外的结果，以及 URL 已在 `raw/`、来源页、`inbox/links.md`、`inbox/proposals.md`、`wiki/search-rejections.yaml` 里的结果
 （arXiv 同编号算同一来源），以及标题或摘要点名库内工作的结果。
3. **写候选**：只读脚本给的标题与摘要，不抓全文。按与 lens 范围的相关度挑最多 10 条，在 `inbox/proposals.md` 末尾追加：

 ```markdown
 ## [YYYY-MM-DD] search

 1. <URL> #<已有标签> — <标题>。<一句：为什么可能属于 [[<lens>]]，依据是搜索摘要>（查询：`<query>`）
 ```

 标签只从 [docs/human-tags.md](docs/human-tags.md) 已有写法里选，没有合适的不写。理由只写摘要里有的内容。
4. 运行 `python scripts/check_wiki.py --sources <来源总数>`，它校验候选不重复、每条链到已批准 lens、最新一节不超过 10 条。

human 处置：

- 「收下 1、3」：那几行去掉标题、理由与查询，`<URL> #<标签>` 移到 `inbox/links.md`；
- 「不要 2」「其余不要」：URL 追加进 `wiki/search-rejections.yaml`（`- url: <URL>` 下一行 `  rejected: YYYY-MM-DD`），从 proposals 删除；
- 不处置的留在 proposals，下次不重复提。

## 查询

1. 列 `wiki/sources/` 看有哪些来源，或全文搜 `wiki/`。
2. 先读 lens 页：「总结」给方向概貌，「工作」给每个来源的 highlight；再按 `tags:` / `concepts:` 标签或全文搜索找来源页；细节不够才读 `raw/`。
3. 每条事实引用页面路径（`wiki/sources/<slug>.md`）。查不到就说查不到。

## 裁决

「冲突」里只有 `[!mismatch]` 块，只由 human 处置：「<lens> 收下 <工作名>」把 lens 加进来源页 `lenses`，删除该块，再按收录第 5 步加一行；
「<lens> 不收 <工作名>」删除该块。

human 直接改总结或工作时，agent 不改回。human 改范围句后，agent 对全部来源补判该 lens：新 keep 的加行，不再 keep 的删行并从来源页 `lenses` 去掉，再重写总结。

候选 lens 同样只由 human 处置：

- 「批准 lens <name>」：删掉 `status` 与「为何提议」，补上「总结」「工作」「冲突」三节；
  再对 `wiki/sources/` 全部来源做一遍收录第 5 步（只判这个 lens），keep 的同时把它加进来源页 `lenses`。
- 「并入 <已有 lens>」：human 先改该 lens 的范围句；agent 删候选文件，对全部来源补判该 lens。
- 「否决 lens <name>」：先在 `wiki/lens-rejections.yaml` 追加一条（文件不存在就新建），再删候选文件，log 记 `## [YYYY-MM-DD] reject lens | <name>`：

  ```yaml
  - name: <name>
    rejected: YYYY-MM-DD
    sources: [<簇内来源 slug，按字母序>]
  ```
