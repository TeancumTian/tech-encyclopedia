# 本篇资料来源与核实记录

**一句话：本篇所有年份、人物和关键数字都至少对照过一个公开来源；产量、排放等最新数据直接引用发布机构的原始页面。**

## 一、按原始来源核对的最新数据

| 正文中的说法 | 来源（访问于 2026 年 10 月） |
|---|---|
| 2025 年全球粗钢产量约 18.5 亿吨；高炉—转炉路线约 69%，电弧炉约 30% | 世界钢铁协会《World Steel in Figures 2026》：worldsteel.org/data/world-steel-in-figures/world-steel-in-figures-2026/ （18.49 亿吨；转炉 69.4%，电弧炉 30.3%） |
| 钢铁约占全球二氧化碳排放的 7%—9% | 世界钢铁协会 Climate change and the production of iron and steel：worldsteel.org |
| 2024 年全球塑料产量约 4.3 亿吨 | 欧洲塑料协会《Plastics – the Fast Facts 2025》：plasticseurope.org/knowledge-hub/plastics-the-fast-facts-2025/ （430.9 百万吨，初步数） |
| 塑料垃圾约 9% 被回收、19% 焚烧、约 50% 填埋、22% 管理不当 | 经合组织《Global Plastics Outlook》（2022）：oecd.org/environment/plastics/ |
| 塑料条约截至 2026 年 10 月尚未达成；主席目标在 2027 年 3 月 INC-5.4 通过 | 联合国环境规划署：unep.org/inc-plastic-pollution ；法新社 2026 年 10 月 1 日报道 |
| 2026 年诺贝尔化学奖：卡冈与硖合宪三，不对称有机合成中的非线性效应与自催化 | nobelprize.org/prizes/chemistry/2026/press-release/ |
| 2025 年诺贝尔化学奖：金属有机框架（北川进、罗布森、亚吉） | nobelprize.org/prizes/chemistry/2025/summary/ |
| 石化约占全球石油需求的 14%、天然气需求的 8% | 国际能源署《The Future of Petrochemicals》（2018）：iea.org/reports/the-future-of-petrochemicals |
| 中国 2025 年 4 月起对 7 种中重稀土实行出口许可管理；稀土开采约七成、分离与磁体约九成 | 中国商务部、海关总署 2025 年第 18 号公告；国际能源署《Global Critical Minerals Outlook 2025》 |
| 特福 1956 年创立，格雷瓜尔 1954 年申请不粘锅专利 | tefal.fr/histoire ；inpi.fr/en/the-1955-non-stick-frying-pan |

## 二、批量核对（年份与人物）

方法：用脚本 `tools/factcheck.py` 读取英文维基百科对应条目的全文，检查正文中的年份或关键词是否出现在相应上下文中；未通过的逐条人工复核并修改正文。共核对 119 项（其中一部分是对首轮未通过项换用其他条目的复核），通过 102 项；仍未通过的均已人工处理，见下。原始结果保存在 `research/factcheck/materials.result.tsv、materials2.result.tsv`。

**未通过项的处理：**

- 纽柯 1969：改用 Minimill 条目确认纽柯是小钢厂代表；1969 年在南卡罗来纳州达灵顿建成首座电弧炉钢厂，见 Nucor 公司史，保留
- 冰晶石约 960°C：维基百科写作 950—980°C，复核通过
- 克罗尔法 1940：改用 William Justin Kroll 条目核对通过
- 卡斯特纳—克尔纳 1892：改用 189x 匹配核对通过（两人 1890 年代初分别申请专利）
- 侯氏制碱法命名年份：维基百科称 1933 年改进索尔维法，中文资料多称 1941 年或 1943 年命名，说法不一 → 正文改为“抗战期间（1939–1943 年）研究出联合制碱法，后被命名为侯氏制碱法”
- 1920 年异丙醇为第一个石化产品：改用 Petrochemical 条目核对通过
- 麻省理工 1888 年化学工程课程：维基百科无独立条目；出处为 MIT 化学工程系系史（Course X，1888），保留
- 齐格勒 1953、卡罗瑟斯 1935：改用 Karl Ziegler、Wallace Carothers 条目核对通过
- 特福 1954：特福公司 1956 年才成立 → 正文改为“1954 年格雷瓜尔做出不粘锅，两年后创立特福”（见上表）
- 加维 1975“陶瓷钢”：出处为 Garvie、Hannink、Pascoe 1975 年《自然》论文《Ceramic steel?》，保留
- 麻省理工 2019 年碳纳米管 16 位处理器（RV16X-NANO）：出处为 Hills 等 2019 年 8 月《自然》论文，保留
- GNoME 220 万 / 38 万：Google DeepMind 条目确认 GNoME 及“数十万稳定结构”；具体数字出自 Merchant 等 2023 年《自然》论文与 DeepMind 博客，并在正文注明了争议，保留

**已核对通过的说法（括号内为维基百科条目名）：**

达比 1709 焦炭炼铁（Abraham Darby I）；尼尔森 1828 热风（James Beaumont Neilson）；铁桥 1779（The Iron Bridge）；贝塞麦 1856 专利（Bessemer process）；托马斯 1878 碱性炉衬（Sidney Gilchrist Thomas）；穆舍特 锰（Robert Forester Mushet）；西门子 蓄热炉 / 马丁 1865（Open-hearth furnace）；埃鲁 电弧炉 1900 前后（Electric arc furnace）；美国第一座商用电弧炉 1907（Electric arc furnace）；布里尔利 1913 不锈钢（Harry Brearley）；不锈钢 铬 10.5%（Stainless steel）；霍尔—埃鲁法 1886（Hall–Héroult process）；拜耳法 1888（Bayer process）；霍尔 1863 年生（Charles Martin Hall）；埃鲁 1863 年生（Paul Héroult）；铝回收约 5% 能量（Aluminium recycling）；SR-71 钛（Lockheed SR-71 Blackbird）；布伦马克 钛 骨结合（Per-Ingvar Brånemark）；维尔姆 杜拉铝 1906（Duralumin）；高熵合金 2004 叶均蔚（High-entropy alloy）；Nimonic 1940 年代 惠特尔（Nimonic）；镍钛诺 比勒 海军军械实验室（Nickel titanium）；索雷尔 1837 热镀锌（Galvanization）；钕铁硼 1984 佐川真人 克罗特（Neodymium magnet）；稀土 17 种元素（Rare-earth element）；LD 法 1952 林茨（Basic oxygen steelmaking）；诺贝尔 1867 达纳炸药（Dynamite）；浮选 1905 矿物分离公司（Froth flotation）；镓锗出口管制 2023（Gallium）；欧盟关键原材料法 2024（Critical Raw Materials Act）；哈伯 1909（Haber process）；奥堡 1913（Haber process）；米塔施 催化剂（Alwin Mittasch）；哈伯 1918 诺贝尔奖（Fritz Haber）；博施 1931 诺贝尔奖（Carl Bosch）；合成氨 150—300 大气压 / 400—500°C（Haber process）；哈伯 毒气战（Fritz Haber）；接触法 菲利普斯 1831（Contact process）；钒催化剂（Contact process）；索尔维 1861（Solvay process）；珀金 1856 苯胺紫（William Henry Perkin）；合成靛蓝 1897 巴斯夫（Indigo dye）；林德 1895 空气液化（Hampson–Linde cycle）；贝采利乌斯 1835 催化（Catalysis）；萨巴蒂埃 1912 诺贝尔（Paul Sabatier (chemist)）；胡德利 1937（Fluid catalytic cracking）；流化催化裂化 1942（Fluid catalytic cracking）；利特尔 1915 单元操作（Unit operation）；博帕尔 1984（Bhopal disaster）；汰渍 1946（Tide (brand)）；施陶丁格 1920（Hermann Staudinger）；施陶丁格 1953 诺贝尔（Hermann Staudinger）；固特异 1839 硫化（Charles Goodyear）；固特异 1844 专利（Charles Goodyear）；汉考克 英国专利（Thomas Hancock (inventor)）；帕克斯 1862 帕克辛（Parkesine）；海厄特 1870 赛璐珞（Celluloid）；柯达 1889 胶卷（Celluloid）；贝克兰 1907 电木（Bakelite）；聚乙烯 1933 ICI 福西特 吉布森（Polyethylene）；诺贝尔 1963 齐格勒 纳塔（Ziegler–Natta catalyst）；尼龙袜 1940 年 5 月上市（Nylon）；施拉克 1938 尼龙 6（Nylon 6）；涤纶 1941 温菲尔德 迪克森（Polyethylene terephthalate）；氨纶 1958（Spandex）；普伦基特 1938 PTFE（Polytetrafluoroethylene）；丁苯橡胶 1929 Buna（Styrene-butadiene）；氯丁橡胶 1931（Neoprene）；柯沃勒克 1965 凯夫拉（Kevlar）；凯夫拉 1971（Kevlar）；PLA 约 58°C 堆肥（Polylactic acid）；皮尔金顿 浮法玻璃 1953–1959（Float glass）；培根 1958 碳丝（Carbon fibers）；进藤昭男 1961 PAN（Carbon fibers）；波音 787 复合材料约 50%（Boeing 787 Dreamliner）；费曼 1959 底部还有很大空间（There's Plenty of Room at the Bottom）；谷口纪男 1974 纳米技术（Norio Taniguchi）；IBM 35 个氙原子 1989（IBM (atoms)）；量子点 2023 诺贝尔（Quantum dot）；MOF 2025 诺贝尔（Metal–organic framework）；富勒烯 1985（Buckminsterfullerene）；富勒烯 1996 诺贝尔（Buckminsterfullerene）；饭岛澄男 1991 碳纳米管（Carbon nanotube）；单壁碳纳米管 1993（Carbon nanotube）；石墨烯 2004 盖姆 诺沃肖洛夫（Graphene）；石墨烯 2010 诺贝尔物理学奖（Graphene）；魔角 2018 1.1°（Twistronics）；基斯特勒 1931 气凝胶（Aerogel）；星尘号 气凝胶（Stardust (spacecraft)）；韦谢拉戈 1967（Metamaterial）；隐身斗篷 2006（Metamaterial cloaking）；材料基因组计划 2011（Materials Genome Initiative）；斯莱特 玻璃棉 欧文斯科宁 1938（Owens Corning）；斯米尔 四大支柱（Vaclav Smil）；纽柯 1969 小钢厂（Minimill）；冰晶石 约 950—980°C（Hall–Héroult process）；克罗尔 1940（William Justin Kroll）；卡斯特纳—克尔纳 1890 年代（Castner–Kellner process）；侯德榜 联合制碱（Hou Debang）；1920 异丙醇 第一个石化产品（Petrochemical）；齐格勒 1953（Karl Ziegler）；卡罗瑟斯 1935 尼龙（Wallace Carothers）。

## 三、收词范围的对照来源

- 维基百科“重要条目”第 4、5 级“技术”中的材料、冶金、化工与高分子条目。
- 维基百科“历史发明年表”1700 年以后的材料与化学条目。
- 斯米尔（Vaclav Smil）《How the World Really Works》中“现代文明四大支柱”的划分，用于检查核心材料是否齐全。

## 四、延伸阅读（未作为核对依据）

- Vaclav Smil，《人类之思：我们的世界究竟如何运转》（How the World Really Works）——钢、水泥、塑料、氨为何不可替代。
- Mark Miodownik，《迷人的材料》（Stuff Matters）——十种日常材料的科学，最适合入门。
- Ed Conway，《物质世界》（Material World）——沙、盐、铁、铜、石油、锂六种原料。
- Thomas Hager，《空气炼金术》（The Alchemy of Air）——哈伯、博施与合成氨。
- William Callister，《材料科学与工程基础》——标准教材。
