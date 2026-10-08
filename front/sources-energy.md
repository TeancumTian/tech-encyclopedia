# 本篇资料来源与核实记录

**一句话：本篇所有年份、人物和关键数字都至少对照过一个公开来源；最新数据（2024–2026 年）直接引用发布机构的原始报告或公告。**

## 一、按原始来源核对的最新数据

| 正文中的说法 | 来源（访问于 2026 年 10 月） |
|---|---|
| 2025 年全球新增光伏约 6.9 亿千瓦、累计约 29.6 亿千瓦，中国约占新增的六成 | 国际能源署光伏系统项目（IEA PVPS）《Trends in Photovoltaic Applications 2026》及《Snapshot of Global PV Markets 2026》（后者给出 698 GW / 2.973 TW，正文取约数）：iea-pvps.org |
| 2025 年煤电占全球发电量 33.0%，首次被可再生能源（33.8%）超过；光伏 8.7%、风电 8.5%、核电约 9% | Ember《Global Electricity Review 2026》：ember-energy.org |
| 2025 年新增风电约 1.65 亿千瓦，累计约 13 亿千瓦 | 全球风能理事会（GWEC）《Global Wind Report 2026》：gwec.net |
| 东方电气 26 兆瓦风机，叶轮直径约 310 米，2025 年 10 月完成吊装并网测试 | 东方电气集团公告及行业媒体报道（2025 年 10 月） |
| 2024 年新建光伏加权平均度电成本约 0.043 美元/千瓦时，陆上风电约 0.034 美元；91% 新建可再生项目比化石替代方案便宜 | 国际可再生能源署（IRENA）《Renewable Power Generation Costs in 2024》：irena.org |
| 2025 年全球平均电池包价格 108 美元/千瓦时，比 2010 年下降约 93% | 彭博新能源财经（BNEF）2025 年电池价格调查（2025 年 12 月）：about.bnef.com |
| 2025 年新增电池储能 1.08 亿千瓦（+40%），中国约六成，磷酸铁锂约九成 | 国际能源署《Global Energy Review 2026》：iea.org |
| 2025 年底抽水蓄能约 2 亿千瓦（新增 1170 万千瓦），常规水电约 12.7 亿千瓦 | 国际水电协会（IHA）《2026 World Hydropower Outlook》：hydropower.org |
| 2025 年底全球约 410 多座核电机组在运行 | 国际原子能机构动力堆信息系统（IAEA PRIS）：pris.iaea.org（不同统计日给出 413–417 座，正文取"410 多座"） |
| NIF 2022 年 12 月聚变输出 3.15 兆焦、激光输入 2.05 兆焦；2025 年 4 月达 8.6 兆焦 | 劳伦斯利弗莫尔国家实验室新闻稿：llnl.gov |
| ITER 2034 年开始科研运行、2039 年开始氘—氚实验 | ITER 组织 2024 年公布的新基线计划：iter.org |
| EAST 2025 年 1 月 1066 秒高约束运行；WEST 2025 年 2 月 1337 秒 | 中国科学院等离子体物理研究所公告；法国原子能委员会（CEA）公告：cea.fr |
| 隆基钙钛矿/晶硅叠层电池效率 35.5%（2026 年 7 月，欧洲太阳能测试机构 ESTI 认证） | 隆基公告与 pv magazine 报道（2026 年 7 月）：pv-magazine.com |
| 2024 年全球氢需求接近 1 亿吨，低排放氢不到 1% | 国际能源署《Global Hydrogen Review 2025》：iea.org |
| "玲龙一号"截至 2026 年 10 月处于热态功能试验阶段，尚未商运 | 中国核工业集团公告及行业报道（2026 年） |
| 翁加洛乏燃料处置库：芬兰核安全机构 STUK 2026 年 8 月 4 日给出支持运营许可的安全评估，政府许可待批 | STUK 公告：stuk.fi；Posiva 公告：posiva.fi |
| 昌吉—古泉 ±1100 千伏直流工程 2019 年投运，全长约 3300 公里 | 国家电网与设备厂商公开资料（2019 年 9 月 26 日投运，3293 公里） |

## 二、批量核对（年份与人物）

方法：用脚本 `tools/factcheck.py` 读取英文维基百科对应条目的全文，检查正文中的年份或关键词是否出现在相应上下文中；未通过的逐条人工复核（换条目或查原始资料）并修改正文。共核对 120 项（含对首轮未通过项的复核），结果文件见 `research/factcheck/energy*.result.tsv`。

**首轮未通过项及处理：**

- 里廷格 1856 年造出热泵：维基百科写作 1855–1857 年 → 正文改为"1855–1857 年"
- 拉德瑞罗 1913 年建成第一座商业地热电站：维基百科 Geothermal power 写作 1911 年 → 正文改为"1911 年起"
- 弗朗西斯 1849 年水轮机：Francis turbine 条目未写年份 → 改用 James B. Francis 条目核对通过
- 1807 年蓓尔美尔街煤气路灯：改用 Pall Mall, London 条目核对通过
- 石岛湾高温气冷堆 2023 年商运：改用 HTR-PM 条目核对通过
- 昌吉—古泉特高压直流：维基百科无对应英文条目 → 以国家电网与设备厂商公开资料核对（见上表）
- 切尔诺贝利、福岛为 7 级事故：维基百科纯文本摘录不含 INES 表格 → 以 ENSI、IAEA 资料核对（两者是迄今仅有的 7 级事故）
- 磷酸铁锂：维基百科称 1996 年由古迪纳夫团队提出，论文正式发表于 1997 年 → 正文"1997 年发表论文"保留

**已核对通过的说法（括号内为维基百科条目名）：**

纽科门 1712 第一台实用蒸汽机（Newcomen atmospheric engine）；瓦特 1769 分离冷凝器专利（James Watt）；博尔顿 1775 合作（James Watt）；特里维西克 高压蒸汽（Richard Trevithick）；帕森斯 1884 汽轮机（Charles Algernon Parsons）；透平尼亚号 1897 34 节（Turbinia）；勒努瓦 1860 内燃机（Étienne Lenoir）；奥托 1876 四冲程（Nicolaus Otto）；本茨 1885–1886 汽车（Carl Benz）；狄塞尔 1892 专利（Rudolf Diesel）；狄塞尔 1897 样机（Rudolf Diesel）；1939 布朗勃法瑞 纳沙泰尔 燃气轮机 4 兆瓦（Gas turbine）；He 178 1939 首飞（Heinkel He 178）；斯特林 1816 专利（Robert Stirling）；开尔文 1852 热泵（Heat pump）；里廷格 1856 热泵（Heat pump）；珀金斯 1834 蒸气压缩制冷（Jacob Perkins）；林德 1870 年代 氨制冷（Carl von Linde）；开利 1902 空调（Willis Carrier）；珍珠街电站 1882（Pearl Street Station）；霍尔本高架桥 1882（Holborn Viaduct power station）；德雷克 1859 泰特斯维尔（Drake Well）；伯顿 1913 热裂化（Cracking (chemistry)）；胡德利 1937 催化裂化（Eugene Houdry）；水力压裂 1947 堪萨斯（Fracking in the United States）；哈里伯顿 1949 商业化（Hydraulic fracturing）；米切尔 巴尼特页岩（George P. Mitchell）；弗雷多尼亚 1821 天然气井（Natural gas）；甲烷先锋号 1959（Liquefied natural gas）；阿尔及利亚 1964 LNG（Liquefied natural gas）；特斯拉 1888 交流电动机专利（War of the currents）；1893 芝加哥世博会 西屋（War of the currents）；1896 尼亚加拉 布法罗（Adams Power Plant Transformer House）；1954 哥得兰 HVDC（HVDC Gotland）；拉姆 Uno Lamm（Uno Lamm）；晋东南—南阳—荆门 1000 千伏 2009（Ultra-high-voltage electricity transmission in China）；2007 能源独立与安全法 智能电网（Smart grid）；智利 1982 电力市场化（Electricity market）；霍尔 EROI（Energy return on investment）；哈恩 施特拉斯曼 1938 裂变（Nuclear fission）；迈特纳 弗里施 解释（Nuclear fission）；CP-1 1942 12 月 2 日（Chicago Pile-1）；鹦鹉螺号 1954（USS Nautilus (SSN-571)）；希平港 1957（Shippingport Atomic Power Station）；EBR-I 1951 四只灯泡（Experimental Breeder Reactor I）；BN-800 运行（BN-800 reactor）；MSRE 1965–1969（Molten-Salt Reactor Experiment）；武威 2 兆瓦钍基熔盐堆 2023 临界（TMSR-LF1）；罗蒙诺索夫院士号 2020 商运（Akademik Lomonosov）；玲龙一号 ACP100（ACP100）；拉阿格 后处理（La Hague site）；翁加洛 400 多米（Onkalo spent nuclear fuel repository）；曼哈顿 橡树岭 1945（Oak Ridge, Tennessee）；齐佩 气体离心机（Gernot Zippe）；三里岛 1979（Three Mile Island accident）；切尔诺贝利 1986 4 月（Chernobyl disaster）；福岛 2011 3 月（Fukushima nuclear accident）；切尔诺贝利 福岛 7 级（International Nuclear Event Scale）；NIF 2022 12 月 3.15 MJ 2.05 MJ（National Ignition Facility）；ITER 2034 科研运行（ITER）；ITER 2039 D-T（ITER）；塔姆 萨哈罗夫 托卡马克（Tokamak）；T-1 1958（Tokamak）；T-3 1968（Tokamak）；EAST 1066 秒（Experimental Advanced Superconducting Tokamak）；WEST 1337 秒（WEST (formerly Tore Supra)）；阿普尔顿 1882 水电（Vulcan Street Plant）；三峡 2250 万千瓦（Three Gorges Dam）；布莱斯 1887 风力发电（James Blyth (engineer)）；布拉什 1888 风力发电机（Charles F. Brush）；拉库尔 丹麦（Poul la Cour）；温讷比 1991 11 台 450 千瓦（Vindeby Offshore Wind Farm）；贝克勒尔 1839 光生伏特（Photovoltaic effect）；1954 贝尔实验室 硅电池 6%（Solar cell）；先锋 1 号 1958（Vanguard 1）；宫坂力 2009 3.8%（Perovskite solar cell）；拉德瑞罗 1904（Larderello）；拉德瑞罗 1913 商业地热（Geothermal power）；朗斯潮汐 1966 240 MW（Rance Tidal Power Station）；巴西 1975 酒精计划（Ethanol fuel in Brazil）；尼科尔森 卡莱尔 1800 电解水（Electrolysis of water）；格罗夫 1839 燃料电池（William Robert Grove）；Mirai 2014（Toyota Mirai）；伽伐尼 1780 年代（Luigi Galvani）；伏打 1800 电堆（Voltaic pile）；普朗特 1859 铅酸（Lead–acid battery）；福尔 1881 涂膏极板（Lead–acid battery）；惠廷厄姆 1970 年代（M. Stanley Whittingham）；古迪纳夫 1980 钴酸锂（John B. Goodenough）；吉野彰 1985（Akira Yoshino）；索尼 1991 商用锂离子（Lithium-ion battery）；2019 诺贝尔化学奖（Akira Yoshino）；1997 磷酸铁锂 古迪纳夫（Lithium iron phosphate）；宁德时代 2021 钠离子（Sodium-ion battery）；斯凯拉斯-卡扎科斯 全钒液流（Vanadium redox battery）；特斯拉 南澳 2017 100 MW（Hornsdale Power Reserve）；贝克尔 1957 双电层电容专利（Supercapacitor）；NEC 超级电容器（Supercapacitor）；默多克 1792 煤气照明（William Murdoch）；1812 煤气公司（Gas Light and Coke Company）；斯旺 1878–1879 碳丝灯（Joseph Swan）；爱迪生 1879 10 月 碳丝（Incandescent light bulb）；格默 1926 荧光灯专利（Fluorescent lamp）；GE 1938 荧光灯（Fluorescent lamp）；弗朗西斯 1848–1849 水轮机（James B. Francis）；石岛湾 高温气冷堆 2023 商运（HTR-PM）；1807 蓓尔美尔街 煤气路灯（Pall Mall, London）；格罗夫 1839 气体电池（Fuel cell）。

## 三、收词范围的对照来源

- 维基百科"重要条目"（Vital Articles）第 4、5 级"技术"与"物理科学"下的相关子页面，逐条与本篇词条清单比对。
- 维基百科"历史发明年表"（Timeline of historic inventions）1700 年以后的相关条目。
- 国际能源署《World Energy Outlook》与《Energy Technology Perspectives》中的技术清单，用于补齐储能、电网和氢能类词条。

## 四、延伸阅读（未作为核对依据）

- 瓦茨拉夫·斯米尔，《能量与文明》——从人力、畜力到化石燃料和电力的能量史。
- 戴维·麦凯，《可持续能源：事实与真相》（Sustainable Energy — Without the Hot Air）——用简单算术比较各种能源，可在线免费阅读。
- 丹尼尔·耶金，《奖赏》与《能源重塑世界》——石油与能源地缘政治。
- 理查德·罗兹，《原子弹秘史》——核裂变的发现与第一座反应堆。
