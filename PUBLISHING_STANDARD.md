# 《近现代科技百科全书》出版与写作标准

> 本书定位、词条格式、篇幅、第一性原理、事实纪律、图解、交叉引用与排版 QA。
> 工具链继承自姊妹仓库 `b2b-zero-to-one`（WeasyPrint + markdown-it + Noto CJK）。

## 1. 定位

| 项 | 约定 |
|---|---|
| 书名 | 近现代科技百科全书 |
| 英文副题 | An Illustrated Encyclopedia of Modern Technology · 1700–2026 |
| 范围 | 工业革命前后至今（约 1700–2026）的关键技术关键词 |
| 深度 | **广度优先、不求深**：每个词条说清"是什么、为什么行、怎么工作、谁何时、改变了什么"即可 |
| 读者 | 以计算机专业本科生为主，兼顾对科技好奇的普通读者；假定有 ADHD → **结论先行、词条短、图多、双语** |
| 语言 | 中文正文；关键术语、人名、产品名附英文；年份用阿拉伯数字 |
| 规模 | 17 个领域、约 900–1500 个词条、59 条第一性原理 |

## 2. 领域与文件布局

```
tech-encyclopedia/
├── PUBLISHING_STANDARD.md          ← 本文件
├── data/src/00-principles.txt      ← 第一性原理
├── data/src/01-energy.txt … 17-frontier.txt  ← 词条总表（管道分隔）
├── data/entries.json               ← compile_entries.py 生成
├── data/index_keys.json            ← make_index_keys.py 生成（拼音索引排序键）
├── domains/NN-<id>.md              ← 正文（17 篇全部完成）
├── front/{howto,map,principles-intro,sources-<id>,cover}.md|.svg
├── assets/figs/<domain>/           ← SVG 图
├── tools/{compile_entries,build_pdf,svgkit,figs_*,factcheck,preview_figs}.py
└── build/近现代科技百科全书-全书.pdf（构建产物，约 8 MB；不进 git，见 GitHub Releases）
```

## 3. 词条总表格式（data/src）

```
# id | 中文 | English | tagline
## 子类名
entry-id | 中文名 | English name | 年份或空 | A|B|C | 一句话定义 | related-id,related-id | principle-id,principle-id
```

- `id`：小写英文短横线，全书唯一。
- `related` / `principles`：只引用本表已有的 id；`compile_entries.py` 会校验并生成反向链接 `cited_by`。
- 年份：该技术的**关键起点**（发明、首次演示或首次商用），不确定则留空，写正文时再补。

## 4. 正文格式（domains/*.md）

```
@intro
……导读与 ```svg map path``` ……

@entry <id>
原理：……（可含 [[p:principleid|标签]]）
怎么工作：……
年份人物：……
改变了：……
注意：……          ← 可选，渲染为「常见误解」
图注：……          ← 紧挨着下一张图
```svg
figs/<domain>/<id>.svg
```
```svg small
figs/.../small.svg
```

@outro
……可选收尾……
```

字段还可写 `是什么：` 覆盖总表中的一句话定义。交叉引用：`[[id]]`、`[[id|显示文字]]`、`[[p:principleid|标签]]`。

## 5. 篇幅级别（字数 = 汉字/标点 + 英文词/数字）

| 级别 | 用途 | 字数 | 图 |
|---|---|---|---|
| A ★ | 核心 | 360–750 | **必须 1 张** |
| B | 标准 | 220–480 | 可选 |
| C | 短 | 120–320 | 一般无 |

`tools/build_pdf.py` 在构建时打印越界与 A 级缺图警告。

## 6. 第一性原理规则

- 每个词条**至少挂 1 条**原理（总表中的 `principles` 列）。
- 正文「原理」字段用一两句白话落到该原理上，不要堆术语。
- 全书原理控制在 **30–60 条**；新增前先看是否已有可复用的。
- 原理分组固定为：力、能量与热｜电磁与光｜量子与原子｜化学与材料｜生命｜数学、信息与计算｜经济与系统。

## 7. 事实纪律

1. **年份、人物、关键数字必须可核。** 不确定就查（维基百科全文、机构官网、TOP500、IEA、Unicode 等），写进 `front/sources-<domain>.md`。
2. 可用 `tools/factcheck.py` 批量对照维基百科提取文本；未通过项必须人工处理后再定稿。
3. 正文中只写核对过的 URL 与说法；预测性内容（如技术奇点）必须标明「推测」。
4. 2025–2026 年的最新进展要注明时间点。

## 8. 文风（ADHD 友好）

- **结论先行**：第一句说清是什么；黄色框说清为什么行。
- 段落 ≤ 4 行；少用从句套从句。
- 数字用「能感受到的量级」（「快一千倍」优于「提升 99.9%」）。
- 中英对照：术语首次出现写「中文（English）」。
- 不用恐吓式或营销式语言。

## 9. 图解标准

- 调色板固定：`svgkit.C`（blue / amber / green / red / purple / slate / teal / pink）。
- 字体：Noto Sans CJK SC；标题加粗，说明用 muted 灰。
- 每张图有一句脚注（`图注：`），说明「图在说什么」。
- 概念地图用 ` ```svg map `，整页；小图用 ` ```svg small `。
- 生成脚本：`tools/figs_<domain>.py`，输出到 `assets/figs/<domain>/`。
- 预览：`tools/preview_figs.py <domain>` → `build/preview/*.png`，人工目视后再入 PDF。

## 10. 构建与 QA

```bash
python3 tools/compile_entries.py                      # 或 make entries
python3 tools/build_pdf.py --sample computing         # → build/样章.pdf（或 make sample）
python3 tools/make_index_keys.py                      # 增删/改名词条后重跑（需 pypinyin；或 make index-keys）
python3 tools/build_pdf.py                            # → build/近现代科技百科全书-全书.pdf（约 5 分钟；或 make pdf）
# 若 PDF 超过 25 MB：gs -sDEVICE=pdfwrite -dPDFSETTINGS=/ebook -dNOPAUSE -dBATCH -sOutputFile=build/压缩版.pdf build/近现代科技百科全书-全书.pdf（很慢，CJK 字体下可能超过 15 分钟）
```

全书结构：封面 → 目录 → 怎么读这本书 → 全书地图 → 第一性原理索引 → 17 篇正文（每篇：导读 + 知识地图 + 词条）→ 附录一 大事年表 → 附录二 资料来源与核实记录（合并 front/sources-*.md）→ 附录三 中文关键词索引（拼音）→ 附录四 English Index。
`front/howto.md` 中的 `@@STATS@@`、`front/map.md` 中的 `@@DOMAIN_TABLE@@` 由构建脚本按 entries.json 自动填写。

构建时检查：未知交叉引用、长度越界、A 级缺图、缺失正文。样章结构：封面 → 目录 → 怎么读 → 全书地图 → 第一性原理索引 → 样章篇全文 → 资料来源 → 全书词条总表。

## 11. 本阶段完成标准（样章）

- [x] 词条总表 ≥ 800（实际 934）并对照 Vital Articles / 发明年表
- [x] 59 条第一性原理
- [x] 第 3 篇「计算与软件」124 条全部写完 + 概念地图 + 核心图
- [x] `PUBLISHING_STANDARD.md`、front 导读与来源
- [x] `样章.pdf` 可打开、事实已核对

## 12. 全书终校（2026 年 10 月）

- [x] 997 个词条（A 105 / B 244 / C 648）全部有正文，长度全部在硬限内；无未知交叉引用、无重复 id
- [x] 写手凭记忆引用的说法逐条联网核对，更正写入正文与 `front/sources-*.md`（标"终校时核对"）
- [x] 跨篇事实统一（电动车销量、升温数字、星舰、AI 模型）；年份区间统一用"–"；时效标注统一为"截至 2026 年 10 月"
- [x] SVG 文字溢出检查（headless Chrome）；全书 PDF 构建与抽页目检
