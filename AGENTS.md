# 项目维护约定

- 本项目同时提供科技百科书稿 / PDF 与「原来如此」互动学习网页；网页面向零基础成年人。
- 用户于 2026-10-09 选择先在本机使用。不要推断已获公开部署、修改仓库可见性或设置后台维护任务的授权。
- 数据源是 `data/src/*.txt`；书稿是 `domains/*.md`。不要手改 `data/entries.json`，运行 `make entries` 生成；不要修改 `build/web/` 产物。
- 网页代码在 `web/`，导学在 `web/learning.js`，数学模型在 `web/models.js`；维护细则见 `docs/WEB_MAINTENANCE.md`。
- 更改网页或网页内容后运行 `make web-check`。行为改动还需在浏览器检查对应流程和至少一种窄屏布局。
- 新增事实、历史、数字遵守 `PUBLISHING_STANDARD.md`，核实记录放入 `front/sources-*.md`。实验清楚注明单位、公式和简化假设。
- 保持现有学习进度格式兼容；不要默默清空用户笔记。页面使用语义化控件、可见焦点和文本反馈。
- 不将本网页任务延伸为 iOS / Apple Watch / TestFlight 项目。
