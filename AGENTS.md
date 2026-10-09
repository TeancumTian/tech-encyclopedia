# 项目维护约定

- 本项目同时提供科技百科书稿 / PDF 与「原来如此」互动学习网页；网页面向零基础成年人。
- 用户于 2026-10-09 后续明确授权：仓库改为公有，网页发布到 GitHub Pages，线上进度只保存在浏览器，并保留导入导出。此决定替代此前本机/私有要求；未授权设置额外后台定时任务。
- 数据源是 `data/src/*.txt`；书稿是 `domains/*.md`。不要手改 `data/entries.json`，运行 `make entries` 生成；不要修改 `build/web/` 产物。
- 网页代码在 `web/`，导学在 `web/learning.js`，数学模型在 `web/models.js`；维护细则见 `docs/WEB_MAINTENANCE.md`。
- 更改网页或网页内容后运行 `make web-check`。行为改动还需在浏览器检查对应流程和至少一种窄屏布局。
- 新增事实、历史、数字遵守 `PUBLISHING_STANDARD.md`，核实记录放入 `front/sources-*.md`。实验清楚注明单位、公式和简化假设。
- 线上静态站由 `web/browser-storage.js` 将记录保存到浏览器，按网站路径隔离；不得上传个人笔记。保留导入导出、存储失败提示与旧版兼容。本机学习记录由 `scripts/serve_web.py` 写入 `learning-data/progress.json`，该目录的 JSON 不提交 Git。保持 v1 浏览器进度与 v2 文件格式兼容；不要默默清空用户笔记，浏览器验收使用临时 `--data-dir` 和独立端口。
- 书稿全量覆盖 `front/*.md`、`domains/*.md`、原理、年表与中英文索引；修改构建器需维持 coverage 清单和完整性断言。
- 页面使用语义化控件、可见焦点和文本反馈。
- 不将本网页任务延伸为 iOS / Apple Watch / TestFlight 项目。
