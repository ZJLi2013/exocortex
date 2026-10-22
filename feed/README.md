# feed

替 human 读他的关注网络：GitHub feed 与一份头部团队清单的官方渠道。两个源的信号按「工作」（规范化 URL）合在一起，每个工作用同一个偏好判定判一次，结果写进一个候选文件，由 [AGENTS.md](../AGENTS.md) 的「feed 收录」读取。

## 每天的流程

1. **GitHub feed**（`radar/daily.py`）：读 human 的 github.com/feed，记下关注者 star / 新建 / 转公开的仓库与 GitHub trending，以及 human 自己 star 了哪些。
2. **公司渠道**（`radar/collect.py --signals`）：对 [`domains/embodied/entities.yaml`](domains/embodied/entities.yaml) 中每个团队的渠道取新条目，按工作键累计进 `company/signals.jsonl`：
   - `rss`：公司级 feed 或团队论文 feed；
   - `page`：博客 / 团队列表页的链接快照比对；
   - `github`：组织下新建的仓库；
   - `hf`：Hugging Face 组织下新建的模型与数据集。
3. **判定**（`radar/feed_judge.py`）：
   - 过滤：GitHub 推荐卡与 fork 副本不算信号；创建或发布超过 180 天的不收；既无简介又无正文的不收。
   - 每个新工作调一次 DeepSeek，依据 human 最近 star 的仓库、他最近 90 天推送过的自己的仓库（非 fork，最多 15 个）和他标过 yes / no 的工作判 yes / no；材料是仓库简介与 README，或网页正文。
   - `wiki/search-rejections.yaml` 里的每个 URL 记一次 no 标注，标题取一次缓存；取不到内容的不进例子。
   - `candidates.json`：判 yes 的工作；≥ 2 位关注者或 trending 的排前面，其余按置信度。只有公司信号的工作，发布（没有日期时取首次采到）后 14 天内才进候选。
   - `judge_runs.jsonl` 每次记「以后 star 命中率」：判定之后才被 human star 的工作数，与其中当时判 yes 的数。
   - `cost.jsonl` 每次记一行开销：缓存命中 / 未命中 / 输出 token，按调用时段的 DeepSeek 单价折成人民币（`radar/cost.py`）。收录的运行也记进这里。
4. **收录**：「feed 收录」读 `candidates.json`，把还没见过的前 5 条直接收录；human 「删 X」撤销，撤销的 URL 进 `wiki/search-rejections.yaml`。

判定、正文快照与标注都留在运行者自己的私有目录，不进本仓库。

## 运行

```bash
cd feed
pip install ".[test]" ./LLMProvider
pytest
python -m radar.collect --domain embodied --out <store>/company/latest --state <store>/company/state --signals <store>/company/signals.jsonl
DEEPSEEK_API_KEY=... GITHUB_TOKEN=... python -m radar.feed_judge <store> --rejections ../wiki/search-rejections.yaml
python -m radar.verify feed-judge <store> ../wiki/search-rejections.yaml
python -m radar.cost <store> month      # 本月开销（人民币）
python -m radar.cost <store> balance    # 把 DeepSeek 余额记进 cost.jsonl，对账用
```

GitHub feed 需要浏览器登录 cookie，见 `radar/daily.py`。

## 新增领域

复制 `domains/embodied/` 为 `domains/<domain>/`，改写 `entities.yaml`（团队清单与渠道）与 `domain.yaml`（页面日期抓取预算），运行时传 `--domain <domain>`。

## 已知局限

- 公司渠道只看官方渠道，不收 X、公众号；国内团队主要在公众号发布，目前覆盖不到。
- 前端渲染的页面取不到链接（如 Meta 的 `/research/`），只能改用能直接解析的列表页。
- GitHub 渠道只看新建仓库，不跟踪 release；Hugging Face 只看新建的模型与数据集。
- GitHub feed 带浏览器登录 cookie 读 github.com 的非公开接口：cookie 过期后该次运行记为错误、要人工换 cookie；GitHub 改版也可能让解析失效。feed 只保留约两天，连续停跑超过两天会漏掉中间的信号。
- 偏好判定没有评测门：human 的标注少且有噪声，判得好不好靠撤销的比例与以后的 star 观察。
