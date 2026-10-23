# GitHub Pages 站点

[zjli2013.github.io/exocortex](https://zjli2013.github.io/exocortex/) 固定两页：`index.html` 按 lens 列出工作，每节带该 lens 的关系图；`insights.html` 放各方向的 insight。页面数不随来源增长。
来源页细节（关键数字、可信度）、评测集 / 方法 / 模型节点、全文搜索只在仓库与本地 Obsidian 里看。设计讨论见 [issue #16](https://github.com/ZJLi2013/exocortex/issues/16)。

## 构建

```text
push 到 main（改动碰 wiki/ 或站点构建文件）
  → python scripts/build_site.py _site    # 只写 _site/index.html 与 insights.html，不改仓库文件
  → actions/deploy-pages → https://zjli2013.github.io/exocortex/
```

构建文件只有 `.github/workflows/pages.yml` 与 `scripts/build_site.py`，只需 Python 标准库；部署约 25 秒。本地预览：`python scripts/build_site.py _site`，在 `_site` 下起 `python -m http.server`，浏览器打开 `index.html`。

## 页面内容

- **工作列表**（`index.html`）：每个已批准 lens 一节，写范围句、总结，下面照抄「工作」列表；行首工作名链到来源原 URL，wikilink 渲染成纯文本。有 insight 的 lens 在节内链到 `insights.html`。
- **关系图**：每个 lens 一张，节点是该 lens 收的来源，边是这些来源之间的「关联」（基于 / 对照 / 相悖，按颜色区分）；一条关联都没有的 lens 不画图。跨 lens 的关联不画。
  点节点打开原 URL；节点名用来源页的一级标题。图用 [vis-network](https://visjs.github.io/vis-network/) 固定版本，从 CDN 加载。
- **Insights**（`insights.html`）：`wiki/insights/` 各页，按 lens 分节，页首说明它们是判断、证据在工作列表。

不发布：来源页正文、`inbox/`、`docs/`、`wiki/*-rejections.yaml`、`wiki/index.base`。

## 边界

- 网页内容是仓库 `wiki/` 的子集（CC BY 4.0），不新增公开面。
- 关系图依赖 CDN 上的 vis-network；CDN 不可用时图不显示，工作列表照常可读。
- 部署 workflow 在 `.github/` 下，改它按 CONTRIBUTING 由 human 合并；收录 PR 自动合并后站点自动更新。
- 仓库设置里 Pages 来源是 GitHub Actions。
