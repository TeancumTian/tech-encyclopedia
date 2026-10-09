# 更新记录（CHANGELOG）

格式：最新版本在最上面。每个版本对应一个 git tag，PDF 在 GitHub Releases。

## 未发布 — 2026-10-09

- 新增「原来如此」互动学习网站，面向零基础成年人。
- 4 条路线、20 节导学与解释型小测；逻辑门、二进制、电流、高压输电、梯度下降和数据包 6 个互动实验。
- 全部 997 词条、59 原理从原书稿构建，包含搜索、领域筛选、图解、相关词条与原理跳转。
- 浏览器本地进度、收藏、笔记和记录导入导出；适配移动屏幕和键盘操作。
- 零依赖 Python 构建、Node 内置测试、GitHub Actions 检查与构建包；补充网页维护说明。未配置公开部署。

## v1.0 — 2026-10-08

首个公开源码版本（initial book source），与已交付的 PDF 内容一致。

- 17 篇正文（`domains/`）+ 前置与各篇资料来源（`front/`）；997 个词条全部有正文，长度在硬限内，无未知交叉引用。
- `data/src/*.txt`（词条总表，管道分隔）→ `tools/compile_entries.py` → `data/entries.json`（可逐字节重现）；`data/index_keys.json` 拼音排序键（`tools/make_index_keys.py`，需 pypinyin）。
- 183 张 SVG（`assets/figs/<领域>/`）与全部生成脚本 `tools/figs_*.py`、`svgkit.py`。
- `tools/build_pdf.py`（`--sample <领域>` / `--list` / `--html-only`）；全书 A4 549 页。
- 未收入：`research/factcheck/`（核对缓存与结果，47 MB）和 `build/` 中间文件；`tools/factcheck.py` 仍在，可重新生成核对结果。
- GitHub Actions：推送 main 自动出 PDF，打 `v*` tag 自动挂到 Release。
