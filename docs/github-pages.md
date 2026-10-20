# 发布 wiki 到 GitHub Pages

Plan Revision: 1
Plan Review: approved

## Goal

把 `wiki/` 发布成公开网站，合并到 `main` 后自动更新；仓库内容的写法不为网站改变。

## 当前结论

已实现，本地构建满足全部验收；线上部署要等 PR 合并到 `main` 后第一次运行。用 Quartz v4.5.2 生成，只发布 `wiki/`，评测集 / 方法 / 模型节点生成空页面、靠反向链接列出来源。
仓库公开，GitHub Pages 与 Actions 免费；Pages 来源已设为 GitHub Actions。设计见 [issue #16](https://github.com/ZJLi2013/exocortex/issues/16)。

## 下一步决策

human 合并 PR 后，在线上按验收再核对一次；通过即关闭 t11。

## 流程

```text
push 到 main（改动碰 wiki/ 或站点构建文件）
  → workflow：checkout 本仓库 + 固定版本的 Quartz
  → python scripts/build_site.py <Quartz content 目录>   # 只写构建目录，不改仓库文件
  → npx quartz build
  → actions/deploy-pages → https://zjli2013.github.io/exocortex/
```

仓库里不放 Quartz 源码，只多三样：`.github/workflows/pages.yml`、`scripts/build_site.py`、`site/` 下的 Quartz 配置与布局。
配置在 v4.5.2 默认值上改了：站名与 `baseUrl`、中文界面、去掉统计脚本与社交卡片图；去掉 LaTeX（来源页里的美元价格会被当成公式）；日期不读 git（构建目录不在 git 里）；页脚只链本仓库。

本地预览：`git clone --depth 1 --branch v4.5.2 https://github.com/jackyzha0/quartz`，在里面 `npm ci`，复制 `site/quartz.*.ts` 进去，
`python <仓库>/scripts/build_site.py content`，再 `npx quartz build -d content --serve`。

## 构建前的内容准备（`build_site.py`）

复制 `wiki/lenses/`、`wiki/sources/` 到构建目录，在副本上做这几件事：

1. **节点进正文**：来源页 frontmatter 里 `benchmarks` / `methods` / `models_used` / `models_compared` 的链接，在副本正文末尾渲染成一节。
   Quartz 是否从 frontmatter 里抓链接未核实；写进正文后，反向链接与图谱不依赖这一点。
2. **节点空页面**：上述字段里没有来源页的名字（按 Obsidian 规则，大小写不敏感），各生成一页。
3. **raw 链接**：`[[raw/<slug>]]` 改成来源页 `url:` 的外链。`raw/` 不公开，原样留下会是死链。
4. **首页**：生成 `index.md`，列出已批准 lens 的范围句与总结，链到各 lens 页。
5. **链接大小写**：Obsidian 把 `[[RoboDojo]]` 不分大小写地解析到 `robodojo.md`，Quartz 的 URL 保留大小写；指向来源页或 lens 页的链接改成 `[[robodojo|RoboDojo]]`。
6. **标题**：页面的一级标题移进 frontmatter `title`，Quartz 用它作页面标题、反向链接与面包屑，不再显示文件名。

不复制：`inbox/`、`docs/`、`wiki/log.md`、`wiki/*-rejections.yaml`、`raw/`、`.agent-loop/`。

渲染样例（节点空页面，以 LIBERO-Pro 为例）：

```markdown
---
title: LIBERO-Pro
type: benchmark
---
评测集节点。报了它的数字的来源见下方反向链接。
```

来源页副本末尾追加的一节：

```markdown
## 节点

- 评测集：[[RoboDojo]]、[[LIBERO-Pro]]
- 方法：[[harness evolution]]
- 用到的模型：[[π0.5]]
- 直接对照的模型：[[GPT-6 Astra]]
```

首页：

```markdown
---
title: exocortex
---
研究领域的个人知识库，每个 lens 是一个研究方向。

## [[agentic-robotics]]

<范围句>

<总结>
```

## 边界

- 网站内容与仓库 `wiki/` 相同（CC BY 4.0），不新增公开面；`raw/` 全文不上网站。
- `wiki/index.base` 不发布：Bases 支持（BasesPage 插件）只在 Quartz v5，v4.5.2 渲染不了；lens 页已覆盖同样的浏览入口。换 v5 要改配置方式，不在 t11 范围。
- 部署 workflow 在 `.github/` 下，按 CONTRIBUTING 由 human 合并；之后的收录 PR 自动合并后站点自动更新。
- 仓库设置把 Pages 来源改成 GitHub Actions（可逆）。

## 验收（t11）

- `https://zjli2013.github.io/exocortex/` 能打开，首页列出全部 6 个已批准 lens；
- 任一来源页的原文链接指向原 URL，站内没有指向 `raw/` 的链接；
- `LIBERO-Pro` 节点页的反向链接列出 4 个来源（aspire、embodiedrsi、harnesspai、sensenova-roborsi）；
- 站内没有 `inbox/`、`docs/` 的页面；`check_wiki.py` 仍退出 0；workflow 一次部署 ≤ 5 分钟。

失败去向：Quartz 构建报错是集成问题，按报错修配置或换固定版本；反向链接数不对，查节点名解析（大小写、特殊字符如 `π0.5`）；
index.base 不渲染不算失败，按「边界」处理。

## Experiment Log

| Exp | 假设 | 状态 | 关键结果 | 结论 / evidence |
|---|---|---|---|---|
| E1 | Quartz v4.5.2 加构建前准备，本地构建满足验收 | ✅ 本地 | 6 秒构建 151 个文件；首页 6 个 lens；站内 0 条 `raw/` 链接、0 条站内死链、无 inbox/docs 页；LIBERO-Pro 反向链接 aspire、embodiedrsi、harnesspai、sensenova-roborsi；88 个节点页 | 本地预览截图；线上待合并后核对 |
