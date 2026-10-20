# 搜索候选来源

Plan Revision: 1
Plan Review: approved

## Goal

agent 用 SearXNG 按已批准的 lens 搜新工作，只写候选清单；收不收由 human 决定，`inbox/links.md` 仍只归 human 写。

## 当前结论

已实现，t10 通过：第一次运行的 10 条候选 human 收下 6 条。挑源权不变：搜索只把候选摆到 human 面前，进 inbox、收录、改 lens 都不由搜索触发。
本机网络下只有 arXiv 引擎可用，候选全是论文；GitHub 与网页引擎不通，项目页与仓库搜不到。

## 下一步决策

无进行中的 task。当前只开 arXiv；GitHub 与网页引擎待后续支持（如 GitHub 改走已登录的 `gh api`），或换到不做 TLS 拦截的网络后再开，用来补上项目页与仓库。

## 流程

```text
human 说「搜索候选」
  → 每个已批准 lens 生成查询
  → SearXNG 搜（只读结果摘要，不抓全文）
  → 去重
  → 追加到 inbox/proposals.md
  → human 处置：收下的移进 inbox/links.md，之后照常「收录 inbox」
```

只在 human 说「搜索候选」时跑，不挂在收录批次后自动跑。

## 查询从哪来

- 每个已批准 lens 的范围句改写成 2–3 条英文关键词查询；
- lens 内来源共享的评测集节点（如 RoboDojo、LIBERO-Pro）各一条；
- 每个 lens 最多 5 条；参数 `format=json`。当前只开 `arxiv` 引擎（脚本默认），GitHub 与网页引擎待后续支持，或网络能访问后再开，可用 `--engines` 换。
- 不传 `time_range`：SearXNG 会跳过不支持它的引擎（arXiv 就不支持），近 30 天由脚本按 `publishedDate` 过滤，没有日期的结果保留。

`status: proposed` 的候选 lens 不生成查询。

## 去重

候选 URL 命中下面任一处就丢弃：

- `raw/` 里的 `url:`（同收录第 1 步）；
- `inbox/links.md`、`inbox/proposals.md` 里已有的行；
- `wiki/search-rejections.yaml` 里 human 否决过的 URL。

arXiv 的 `abs/`、`html/`、`pdf/` 同一编号算同一来源。

从仓库或项目页收录的来源，搜索会以它的论文、换一个 URL 返回（RAX 就是这样），所以也按工作名去重：标题以库内来源页的工作名加冒号开头，或摘要写了「introduce(s) <工作名>」，就丢弃。只在评测里提到库内工作名（如「on RoboDojo」）的不丢。

## 候选格式

`inbox/proposals.md`，每次运行追加一节，最多 10 条，按与 lens 范围的相关度排：

```markdown
## [YYYY-MM-DD] search

1. <URL> #<已有标签> — <标题>。<一句：为什么可能属于 [[<lens>]]，依据是搜索摘要>（查询：`<query>`）
```

- 标签只从 [human-tags.md](human-tags.md) 已有写法里选，没有合适的就不写；human 收下时可以改。
- 理由只写搜索摘要里有的内容，不写推断。

## human 处置

| human 说 | agent 做 |
|---|---|
| 「收下 1、3」 | 那几行去掉理由与查询，原样移到 `inbox/links.md` |
| 「不要 2」「其余不要」 | URL 追加进 `wiki/search-rejections.yaml`，从 proposals 删除 |
| 不处置 | 留在 proposals，下次搜索不重复提 |

`wiki/search-rejections.yaml` 与 `lens-rejections.yaml` 同格式：

```yaml
- url: <URL>
  rejected: YYYY-MM-DD
```

## 边界

- agent 不写 `inbox/links.md`，不触发收录，不改 lens 与来源页。
- SearXNG 在本机 WSL 的 Docker 里跑，不需要另一台服务器；镜像 265 MB，空闲内存约 100 MB。实例地址放本地环境变量 `SEARXNG_URL`，不进仓库。部署：

 ```bash
 mkdir -p ~/searxng/config   # 写入下面的 settings.yml
 docker run -d --name searxng --restart unless-stopped -p 127.0.0.1:8888:8080 \
   -v ~/searxng/config:/etc/searxng searxng/searxng:latest
 ```

 ```yaml
 use_default_settings: true
 server:
   secret_key: "<openssl rand -hex 32>"
   limiter: false
 search:
   formats: [html, json]   # 默认只有 html，请求 JSON 返回 403
 outgoing:
   request_timeout: 10.0
 ```

 容器启动后会把配置目录改成容器用户所有，之后改配置用 `docker exec -i searxng sh -c 'cat >> /etc/searxng/settings.yml'`。
 网络做 TLS 拦截时，网页引擎报证书错误，要把拦截根证书拼进 CA 包，再设 `outgoing.verify`。
- 搜索请求与去重由脚本做，查询改写、相关度排序与一句理由由 agent 写。

## 验收（t10）

- 一次运行写出 ≤ 10 条候选，每条链到一个已批准 lens；
- 没有一条与 `raw/`、`inbox/links.md`、`wiki/search-rejections.yaml` 重复；
- `inbox/links.md` 与 `raw/` 未被改动；
- human 逐条判断，至少一半值得收。

失败去向：SearXNG 连不上或返回 403 是环境问题，按上面的部署说明修；出现重复就改去重；值得收的不到一半，改查询生成，例如改用 lens 内来源的标题与「关联」里的工作名做查询。

## Experiment Log

| Exp | 假设 | 状态 | 关键结果 | 结论 / evidence |
|---|---|---|---|---|
| E1 | 18 条查询覆盖 6 个 lens，能搜出 ≥ 一半值得收的候选 | ✅ 6/10 收下 | 只有 arXiv 引擎能用。去重和 30 天过滤后剩 21 条（RAX 的论文靠工作名去重丢掉），挑 10 条写进 proposals：agentic-robotics 6、agent-loop 3、jev 1；agentic-3d、robotics-rl、llm-foundation-models 没有贴范围的结果。GitHub 引擎超时（API 10 秒后返回 403），网页引擎被 TLS 拦截；调大超时、补公司根证书两次自修都没修好。human 收下 agentic-robotics 4 条、agent-loop 2 条；否决 HexaShell、Encore、HarnessNet、OmniMed-Jev | `inbox/links.md`、`wiki/search-rejections.yaml` |
