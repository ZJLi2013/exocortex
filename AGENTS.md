# exocortex

研究领域的个人知识库，按 [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 组织。整个仓库是一个 Obsidian vault。
human 丢链接、提问、批准判断；其余由 agent 按本文件执行。

## 目录

| 路径 | 内容 | 谁写 |
|---|---|---|
| `inbox/links.md` | 待收录的 URL，一行一个 | human |
| `raw/<slug>.md` | 抓取的原文，写一次不改 | agent |
| `wiki/sources/<slug>.md` | 一个来源一页 | agent |
| `wiki/concepts/<name>.md` | 跨来源的概念，≥ 2 个来源提到才建 | agent |
| `wiki/lenses/<name>.md` | human 的研究问题：范围、当前判断、待批准草稿 | 范围与当前判断归 human；草稿归 agent |
| `wiki/index.base` | Bases 视图，从 frontmatter 生成 | 不手改 |
| `wiki/log.md` | 追加日志 | agent |

不按主题建目录。分组靠概念页与 lens，二者都不是预设分类。

## 收录（human 说「收录 inbox」）

对 `inbox/links.md` 里每个 URL：

1. **去重**：`rg "^url: <URL>$" raw/` 命中则跳过，log 记一行。
2. **抓原文**写 `raw/<slug>.md`。slug 用工作名的小写短横线形式（`embodiedevo`、`gemini-4-argon`）。
   arXiv 抓 `https://arxiv.org/html/<id>` 全文，抓不到再退到 abs 页。frontmatter：

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
   published: YYYY-MM-DD      # 原文发布日期；查不到写 unknown
   ingested: YYYY-MM-DD
   concepts: [概念 A, 概念 B]  # 纯文本，含只有本来源提到的
   lenses: ["[[robotrsi]]"]   # keep 的 lens，链接形式；都不 keep 写 []
   ---
   # <工作名>

   <一句话：它做了什么、最重要的结果>

   - **关键数字**：带条件与口径，例「LIBERO-PRO 50.0% → 82.4%（自报，单次）」
   - **评估与接纳**：谁评、在哪个集合上评、谁宣布成功
   - **可信度**：作者自报 / 单次 / 未给评测次数 / 未开源 等
   - **概念**：只链已有页的概念，`[[概念 A]]`
   - **原文**：[[raw/<slug>]]
   ```

   只写原文里有的事实；推断写成「未说明」。正文不超过 40 行。

4. **概念**：对 `concepts` 每一项
   - 先 `rg -l` 查 `wiki/concepts/` 与其它来源页的 `concepts:`，有同义的就复用已有名字；
   - 已有页 → 在该页「来源」下追加 `- [[<slug>]]：<一句话说明这个来源怎样体现该概念>`；
   - 无页且另有来源页的 `concepts:` 含同名 → 建页，链回所有含它的来源，并把这些来源页「概念」行改成链接；
   - 只有本来源提到 → 只留在 frontmatter。

   概念页格式：

   ```markdown
   ---
   type: concept
   ---
   # <概念名>

   <一句话定义>

   ## 来源
   - [[<slug>]]：……
   ```

5. **lens 判定**：逐个读 `wiki/lenses/*.md` 的「范围」，判这条来源 keep 还是 reject。
   - reject：不写 lens 页，log 里记 lens 名与一句理由。
   - keep：在该 lens 的「待批准」下追加草稿，**不改「当前判断」**：

     ```markdown
     > [!draft] <工作名>（YYYY-MM-DD）
     > 支持 / 削弱 / 新增 判断 N：<一句话>。依据 [[<slug>]]
     ```

     与某条当前判断冲突时用 `> [!contradiction]`。

6. **log**：`wiki/log.md` 追加 `## [YYYY-MM-DD] ingest | <工作名>`，下面一行写 lens 判定结果。
7. 处理完的 URL 从 `inbox/links.md` 删除。

全部收录完运行 `python evals/check_wiki.py --sources <来源总数>`。

## 查询

1. `obsidian base:query path=wiki/index.base view=sources format=md` 看有哪些来源；或 `rg` `wiki/`。
2. 先读概念页与 lens 页，再读来源页；细节不够才读 `raw/`。
3. 每条事实引用页面路径（`wiki/sources/<slug>.md`）。查不到就说查不到。
4. log 追加 `## [YYYY-MM-DD] query | <问题>`。

## 批准

human 说「批准 <lens> 的 <工作名> 草稿」时，把草稿内容并入「当前判断」并删除草稿；只有 human 能触发。
