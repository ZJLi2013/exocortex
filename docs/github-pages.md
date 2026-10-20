# 发布 wiki 到 GitHub Pages

Plan Revision: 3
Plan Review: approved

## Goal

把各 lens 的工作与工作之间的关系发布成一个公开网页，合并到 `main` 后自动更新；页面数不随来源增长，仓库内容的写法不为网站改变。

## 当前结论

已上线（t11 完成）：[zjli2013.github.io/exocortex](https://zjli2013.github.io/exocortex/) 只有一个 `index.html`，上方是关系图，下方按 lens 列出工作。不用静态站生成器，`scripts/build_site.py` 直接写出这一页，部署约 25 秒。
来源页细节（关键数字、可信度）、评测集 / 方法 / 模型节点、全文搜索只在仓库与本地 Obsidian 里看。
仓库公开，GitHub Pages 与 Actions 免费；Pages 来源已设为 GitHub Actions。设计讨论见 [issue #16](https://github.com/ZJLi2013/exocortex/issues/16)。

## 下一步决策

无进行中的 task。之后的收录 PR 合并后站点自动更新，不需要单独动作。

## 流程

```text
push 到 main（改动碰 wiki/ 或站点构建文件）
  → python scripts/build_site.py _site    # 只写 _site/index.html，不改仓库文件
  → actions/deploy-pages → https://zjli2013.github.io/exocortex/
```

仓库里只多 `.github/workflows/pages.yml` 与 `scripts/build_site.py`；构建只需 Python 标准库。本地预览：`python scripts/build_site.py _site`，用浏览器打开 `_site/index.html`。

## 页面内容

- **工作列表**：每个已批准 lens 一节，写范围句、总结，下面照抄「工作」列表；行首工作名链到来源原 URL，wikilink 渲染成纯文本。
- **关系图**：节点是已批准 lens 与它们收的来源（`lenses: []` 的来源不画）；边有两类：lens → 它收的来源，来源之间的「关联」（基于 / 对照 / 相悖，按颜色区分）。
  点来源节点打开原 URL，点 lens 节点跳到它那一节。图用 [vis-network](https://visjs.github.io/vis-network/) 固定版本，从 CDN 加载。
- 图上节点名用来源页的一级标题（工作名），不用文件名。

不发布：来源页正文、`raw/`、`inbox/`、`docs/`、`wiki/log.md`、`wiki/*-rejections.yaml`、`wiki/index.base`、`.agent-loop/`。

## 边界

- 网页内容是仓库 `wiki/` 的子集（CC BY 4.0），不新增公开面；`raw/` 全文不上网站。
- 关系图依赖 CDN 上的 vis-network；CDN 不可用时图不显示，工作列表照常可读。
- 部署 workflow 在 `.github/` 下，按 CONTRIBUTING 由 human 合并；之后的收录 PR 自动合并后站点自动更新。
- 仓库设置把 Pages 来源改成 GitHub Actions（可逆）。

## 验收（t11）

- 站点只有一个 HTML 页面；
- 6 个已批准 lens 各一节，每节工作行数与对应 lens 页「工作」一致，工作名链到来源页 `url:`；
- 关系图节点数 = 6 + 被 lens 收的来源数，边数 = lens 工作行数之和 + 两端都在图里的「关联」行数；
- 页面里没有指向 `raw/` 或仓库内 `.md` 的链接；`check_wiki.py` 仍退出 0；workflow 一次部署 ≤ 5 分钟。

失败去向：行数或节点 / 边数不对，查 `build_site.py` 对「工作」与「关联」行的解析。

## Experiment Log

| Exp | 假设 | 状态 | 关键结果 | 结论 / evidence |
|---|---|---|---|---|
| E1 | r1：Quartz 多页站点（含 88 个节点页） | superseded by r2 | 151 个文件；human 认为页面太多，只关心各 lens 的工作与工作间关系 | PR #17 初版 |
| E2 | r2：Quartz 只留首页、lens 页、来源页 | superseded by r3 | 未构建完；human 指出来源页会随时间增长，不要每个工作一页 | — |
