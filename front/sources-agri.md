# 本篇资料来源与核实记录

**一句话：本篇的年份、人物和关键数字都至少对照过一个公开来源；袁隆平、冷冻精液和农业无人机等维基百科写得不全的条目，改用新华社、学术期刊和企业官网核对。**

## 一、按原始来源核对的最新数据

| 正文中的说法 | 来源（访问于 2026 年 10 月） |
|---|---|
| 2020 年新加坡首次批准培养鸡肉上市；2023 年 6 月 21 日美国农业部食品安全检验局向 UPSIDE Foods、GOOD Meat 发放检验许可（此前 FDA 已完成安全咨询） | 新加坡食品局；美国农业部 FSIS 2023 年 6 月公告；Reuters 2023-06-21（终校时核对） |
| 2023 年 AeroFarms（6 月）等室内农场公司申请破产保护，2024 年 11 月 Bowery Farming 关停 | AeroFarms 2023 年公告（同年 9 月重组后退出破产）；TechCrunch 2024-11-04；PitchBook。终校更正：初稿把 AppHarvest 列为垂直农场，它其实是高科技温室公司（2023 年 7 月申请破产后清算），正文改举 Bowery |
| 斯瓦尔巴全球种子库 2008 年启用 | en.wikipedia.org/wiki/Svalbard_Global_Seed_Vault |

## 二、批量核对（年份与人物）

方法：用脚本 `tools/factcheck.py` 读取英文维基百科对应条目的全文，检查正文中的年份或关键词是否出现在相应上下文中；未通过的换用其他条目复核，或查找机构官网、原始论文和权威媒体，逐条人工处理。本篇共核对 50 项（含复核项），脚本通过 44 项；其余均已人工处理，见下。原始结果保存在 `research/factcheck/` 下的 `agri.result.tsv` 及共享复核文件中。

**未通过项的处理：**

- 袁隆平 1964 年开始杂交水稻研究、1970 年发现"野败"、1973 年三系配套、1976 年大面积推广：维基百科正文年份不全 → 对照新华社报道和《Engineering》期刊纪念文章确认，保留
- Polge 1949 年甘油冷冻精液：维基百科 Christopher Polge 条目提到 1950 年冷冻精液孵出小鸡；1949 年发表于《自然》的论文（Polge、Smith、Parkes）为公认出处，保留
- 雅马哈 R-50 1987 年：维基百科无单独条目 → 雅马哈官网确认 1987 年研制成功、1989 年正式销售，保留

**已核对通过的说法（括号内为维基百科条目名）：**

Tull seed drill 1701（Jethro Tull (agriculturist)）；Tull book 1731（Jethro Tull (agriculturist)）；McCormick reaper 1831（Cyrus McCormick）；McCormick patent 1834（Cyrus McCormick）；Glidden barbed wire 1874（Barbed wire）；Froelich tractor 1892（Tractor）；Fordson 1917（Fordson）；Lawes superphosphate 1842（John Bennet Lawes）；Liebig 1840 agricultural chemistry（Justus von Liebig）；Müller DDT 1939（DDT）；Müller Nobel 1948（Paul Hermann Müller）；Silent Spring 1962（Silent Spring）；DDT US ban 1972（DDT）；Shull hybrid corn 1908（George Harrison Shull）；Wallace Pioneer 1926（Henry A. Wallace）；Borlaug Nobel 1970（Norman Borlaug）；IR8 1966（IR8）；Green revolution term Gaud 1968（Green Revolution）；Yuan 1964 male sterile（Yuan Longping）；Flavr Savr 1994（Flavr Savr）；GABA tomato 2021 Japan（Genetically modified tomato）；Netafim 1965（Netafim）；Gericke hydroponics 1929（Hydroponics）；Gericke 1937 term（Hydroponics）；Birdseye frozen 1925（Clarence Birdseye）；Birdseye frozen sale 1930（Clarence Birdseye）；Ando instant noodles 1958（Momofuku Ando）；Cup noodles 1971（Cup Noodles）；Post cultured burger 2013（Mark Post）；Singapore cultured meat 2020（Cultured meat）；US cultured meat approval 2023（Cultured meat）；Fahlberg saccharin 1879（Saccharin）；Chymosin FDA 1990（Chymosin）；Seed vault 2008（Svalbard Global Seed Vault）；HACCP NASA Pillsbury（Hazard analysis and critical control points）；Appert canning（Nicolas Appert）；Pasteur pasteurization 1864（Pasteurization）；Haber-Bosch（Haber process）；Swift refrigerated rail car（Gustavus Franklin Swift）；EU antibiotic growth promoter ban 2006（Antibiotic use in livestock）；Aquaculture exceeds capture 2022（Aquaculture）；Svalbard seed vault 2008（Svalbard Global Seed Vault）；HACCP Pillsbury NASA（Hazard analysis and critical control points）；artificial insemination cattle 1930s（Artificial insemination）。

## 三、收词范围的对照来源

- 维基百科"重要条目"（Vital Articles）第 4 级"技术"与第 5 级"技术"下各子页面（共 3306 个条目名），逐条与本书词条清单比对，补入 3 个遗漏词条：人工授精与家畜育种、种子库、食品安全体系 HACCP。
- 维基百科"历史发明年表"（Timeline of historic inventions）1700 年以后的条目。
- 联合国粮农组织（FAO）农业技术专题目录。

## 四、延伸阅读（未作为核对依据）

- 瓦茨拉夫·斯米尔，《能源与文明》《养活世界》——化肥、能源与粮食的关系讲得最透。
- 查尔斯·曼恩，《巫师与先知》——博洛格与绿色革命的人物史。
- 汤姆·斯坦迪奇，《舌尖上的历史》。
- Dan Koeppel，《香蕉：改变世界的水果》——单一品种与育种风险。
