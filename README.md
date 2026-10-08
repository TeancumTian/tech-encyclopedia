# 近现代科技百科全书

> 从工业革命到大模型：17 个领域、997 个关键词，每个词条讲清是什么、为什么行（第一性原理）、怎么工作、谁何时、改变了什么。求全不求深，通俗、双语、多图。
>
> *An Illustrated Encyclopedia of Modern Technology · 1700–2026*

<p align="center"><img src="front/cover.svg" alt="书中插图预览" width="720"></p>

## 这本书里有什么

- **17 个领域、997 个词条**（★ 核心 A 105 条 / 标准 B 244 条 / 短词条 C 648 条）+ **59 条第一性原理**：能源与动力、电与电子、计算与软件、互联网与通信、人工智能、材料与化工、制造、交通、航天、生物医药、农业与食品、建筑与城市、安全与密码、金融科技、环境与气候、媒体与娱乐、前沿科技。
- 每个词条：是什么 → 原理（链接到第一性原理）→ 怎么工作 → 关键年份与人物 → 改变了什么 → 常见误解；中英对照。
- **183 张** SVG 图解（每篇一张知识地图 + 核心词条原理图），全部由 `tools/figs_*.py` 脚本生成。
- 前置：怎么读这本书、全书地图、第一性原理索引；附录：大事年表、资料来源与核实记录、中文拼音索引、English Index。A4 共 549 页。
- 每篇都有核实记录：年份与人物用维基百科正文批量核对，2025–2026 年数据注明时间点。

## 下载 PDF

成书 PDF **不放在 git 里**，在 GitHub **[Releases](../../releases)** 页面下载（每个 `v*` tag 自动生成）。
每次推送到 `main`，Actions 也会把最新 PDF 作为 artifact 上传（Actions → Build PDF → Artifacts）。

## 目录（Table of Contents）

- **[怎么读这本书](front/howto.md)**

- **[全书地图](front/map.md)**

- **[第一性原理索引（导读）](front/principles-intro.md)**
- [第 1 篇　能源与动力（68 条）](domains/01-energy.md)
- [第 2 篇　电与电子（79 条）](domains/02-electronics.md)
- [第 3 篇　计算与软件（124 条）](domains/03-computing.md)
- [第 4 篇　互联网与通信（83 条）](domains/04-internet.md)
- [第 5 篇　人工智能（81 条）](domains/05-ai.md)
- [第 6 篇　材料与化工（54 条）](domains/06-materials.md)
- [第 7 篇　制造与自动化（45 条）](domains/07-manufacturing.md)
- [第 8 篇　交通运输（51 条）](domains/08-transport.md)
- [第 9 篇　航天与空间（39 条）](domains/09-space.md)
- [第 10 篇　生物与医学（107 条）](domains/10-biomed.md)
- [第 11 篇　农业与食品（34 条）](domains/11-agri.md)
- [第 12 篇　建筑与城市（34 条）](domains/12-building.md)
- [第 13 篇　安全与国防（48 条）](domains/13-security.md)
- [第 14 篇　金融与商业科技（37 条）](domains/14-fintech.md)
- [第 15 篇　环境与气候技术（36 条）](domains/15-environment.md)
- [第 16 篇　光学、成像与媒体（47 条）](domains/16-media.md)
- [第 17 篇　量子与前沿（30 条）](domains/17-frontier.md)

## 自己出 PDF（Build）

需要：Python 3.10+、Noto CJK 字体（`Noto Serif CJK SC` + `Noto Sans CJK SC`）、WeasyPrint 的系统库（Pango）。

```bash
# Ubuntu / Debian
sudo apt-get install fonts-noto-cjk fonts-noto-cjk-extra libpango-1.0-0 libpangoft2-1.0-0
# macOS: brew install pango，并安装 Noto Sans CJK / Noto Serif CJK 字体

python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt

make pdf      # 全书 → build/近现代科技百科全书-全书.pdf
make sample   # 样章 → build/样章.pdf
make check    # 检查 SVG、JSON、路径
```

全书参考页数：约 549 页（A4）。字体或 WeasyPrint 版本不同，页数会有几页浮动。

## 怎么维护

改章节、加图、改数据、发版本：见 **[MAINTAINING.md](MAINTAINING.md)**。版本记录见 [CHANGELOG.md](CHANGELOG.md)。

## 版权（Rights）

© 2026 Teancum Tian. **All rights reserved. 保留所有权利。** 本仓库暂未选择开源许可证（no license），
未经许可请勿转载或再发布。书中引用的公司名、产品名和商标归各自所有者；引用的数据和资料以文中标注的来源为准。
