# GitHub Pages 站点

[zjli2013.github.io/exocortex](https://zjli2013.github.io/exocortex/) 只有一个 `index.html`：上方是关系图，下方按 lens 列出工作。页面数不随来源增长。
来源页细节（关键数字、可信度）、评测集 / 方法 / 模型节点、全文搜索只在仓库与本地 Obsidian 里看。设计讨论见 [issue #16](https://github.com/ZJLi2013/exocortex/issues/16)。

## 构建

```text
push 到 main（改动碰 wiki/ 或站点构建文件）
  → python scripts/build_site.py _site    # 只写 _site/index.html，不改仓库文件
  → actions/deploy-pages → https://zjli2013.github.io/exocortex/
```

构建文件只有 `.github/workflows/pages.yml` 与 `scripts/build_site.py`，只需 Python 标准库；部署约 25 秒。本地预览：`python scripts/build_site.py _site`，用浏览器打开 `_site/index.html`。

## 页面内容

- **工作列表**：每个已批准 lens 一节，写范围句、总结，下面照抄「工作」列表；行首工作名链到来源原 URL，wikilink 渲染成纯文本。
- **关系图**：节点是已批准 lens 与它们收的来源（`lenses: []` 的来源不画）；边有两类：lens → 它收的来源，来源之间的「关联」（基于 / 对照 / 相悖，按颜色区分）。
  点来源节点打开原 URL，点 lens 节点跳到它那一节。节点名用来源页的一级标题。图用 [vis-network](https://visjs.github.io/vis-network/) 固定版本，从 CDN 加载。

不发布：来源页正文、`inbox/`、`docs/`、`wiki/*-rejections.yaml`、`wiki/index.base`。

## 边界

- 网页内容是仓库 `wiki/` 的子集（CC BY 4.0），不新增公开面。
- 关系图依赖 CDN 上的 vis-network；CDN 不可用时图不显示，工作列表照常可读。
- 部署 workflow 在 `.github/` 下，改它按 CONTRIBUTING 由 human 合并；收录 PR 自动合并后站点自动更新。
- 仓库设置里 Pages 来源是 GitHub Actions。
