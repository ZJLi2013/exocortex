# exocortex

研究领域的个人知识库，按 [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 组织。整个仓库是一个 Obsidian vault。
human 丢链接、提问、批准判断；其余由 agent 按本文件执行。

## 目录

| 路径 | 内容 | 谁写 |
|---|---|---|
| `inbox/links.md` | 待收录的 URL，一行一个，可跟 human 标签：`<URL> #jev #kernel` | human |
| `raw/<slug>.md` | 抓取的原文，写一次不改 | agent |
| `wiki/sources/<slug>.md` | 一个来源一页 | agent |
| `wiki/lenses/<name>.md` | human 的研究问题：范围、当前判断、待批准草稿 | 范围与当前判断归 human；草稿与 `status: proposed` 的候选归 agent |
| `wiki/index.base` | Bases 视图，从 frontmatter 生成 | 不手改 |
| `wiki/lens-rejections.yaml` | human 否决过的候选 lens 与当时的簇内来源 | agent |
| `wiki/log.md` | 审计日志，只追加；按事件类型或来源名搜索，不整份读 | agent |

不按主题建目录。分组靠 lens 与两种标签，都不是预设分类：

- `tags`：human 丢链接时打的标签，带着 human 的意图（「大概是 jev 相关」），agent 照抄不改；
- `concepts`：agent 读原文后打的标签，写方法或主张。

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
   lenses: ["[[agentic-robotics]]"]   # keep 的 lens，链接形式；都不 keep 写 []
   ---
   # <工作名>

   <一句话：它做了什么、最重要的结果>

   - **关键数字**：带条件与口径，例「LIBERO-PRO 50.0% → 82.4%（自报，单次）」
   - **评估与接纳**：谁评、在哪个集合上评、谁宣布成功
   - **可信度**：作者自报 / 单次 / 未给评测次数 / 未开源 等
   - **原文**：[[raw/<slug>]]
   ```

   只写原文里有的事实；推断写成「未说明」。正文不超过 40 行。

4. **concepts 标签**：3–6 个，写这个来源的方法或主张，不写泛主题（「机器人」「LLM」不算）。
   先搜其它来源页的 `concepts:`，有同义的就用已有写法，不另起新名；确实没有才起新标签。不建概念页。

5. **lens 判定**：逐个读 `wiki/lenses/*.md` 的「范围」，判这条来源 keep 还是 reject。跳过 `status: proposed` 的候选 lens。
   human 标签是线索不是归属：lens frontmatter `tags` 含来源某个标签时先判这个 lens，但仍按内容判；
   标签指向的 lens 被 reject 时，log 里写「标签 <tag> 与内容不符」。
   - reject：不写 lens 页，log 里记 lens 名与一句理由。
   - keep：把来源的 human 标签补进该 lens 的 `tags`（已有则不加）；在该 lens 的「待批准」下追加草稿，**不改「当前判断」**：

     ```markdown
     > [!draft] <工作名>（YYYY-MM-DD）
     > 支持 / 削弱 判断 N：<一句话>。依据 [[<slug>]]
     ```

     不对应任何已有判断时写 `> 新增：<一句话>`；与某条当前判断冲突时用 `> [!contradiction]`。

6. **log**：`wiki/log.md` 追加 `## [YYYY-MM-DD] ingest | <工作名>`，下面一行写 lens 判定结果。
7. 处理完的 URL 从 `inbox/links.md` 删除。

全部收录完做一遍下面的 lint lenses，再运行 `python scripts/check_wiki.py --sources <来源总数>`。

## lint lenses（收录批次结束后，或 human 说「lint lenses」）

lens 外的来源成簇时，提议一个新研究问题，由 human 决定要不要。

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

   <一句话草案：会改变什么判断的什么工作>

   ## 为何提议

   - 来源：[[<slug>]]、[[<slug>]]
   - 共享标签：<标签>
   - 也可并入 [[<已有 lens>]]：<改后的范围句>   ← 只在放宽某个已有 lens 的范围句就能覆盖时写

   ## 当前判断

   ## 待批准
   ```

   候选 lens 不改任何来源页的 `lenses`。
4. **log**：`## [YYYY-MM-DD] lint | lenses`，每个候选一行（名字与来源）；没有候选也记一行。

## 查询

1. 列 `wiki/sources/` 看有哪些来源，或全文搜 `wiki/`。
2. 先读 lens 页，再按 `tags:` / `concepts:` 标签或全文搜索找来源页；细节不够才读 `raw/`。
3. 每条事实引用页面路径（`wiki/sources/<slug>.md`）。查不到就说查不到。

## 批准

human 说「批准 <lens> 的 <工作名> 草稿」时，把草稿内容并入「当前判断」并删除草稿；只有 human 能触发。

候选 lens 同样只由 human 处置：

- 「批准 lens <name>」：删掉 `status` 与「为何提议」，对 `wiki/sources/` 全部来源做一遍收录第 5 步（只判这个 lens），keep 的同时把它加进来源页 `lenses`。
- 「并入 <已有 lens>」：human 先改该 lens 的范围句；agent 删候选文件，对全部来源补判该 lens。
- 「否决 lens <name>」：先在 `wiki/lens-rejections.yaml` 追加一条（文件不存在就新建），再删候选文件，log 记 `## [YYYY-MM-DD] reject lens | <name>`：

  ```yaml
  - name: <name>
    rejected: YYYY-MM-DD
    sources: [<簇内来源 slug，按字母序>]
  ```
