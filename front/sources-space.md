# 本篇资料来源与核实记录

**一句话：本篇所有年份、人物和关键数字都至少对照过一个公开来源；2025–2026 年的最新进展直接引用发布机构或原始报道页面。**

## 一、按原始来源核对的最新数据

| 正文中的说法 | 来源（访问于 2026 年 10 月） |
|---|---|
| 2026 年 4 月阿尔忒弥斯 2 号载 4 人绕月飞行（4 月 1 日发射、4 月 10 日溅落），为 1972 年以来首次飞离近地轨道 | NASA：nasa.gov/news-release/nasa-welcomes-record-setting-artemis-ii-moonfarers-back-to-earth/ |
| 2026 年 7 月 10 日长征十号乙首飞，第一级由海上平台“拦阻网”捕获，中国首次成功回收入轨火箭 | 新华社：english.news.cn/20260710/3ad9cf3d515642f0ba3922040b9a28c6/c.html |
| 到 2026 年 8 月，猎鹰 9 号助推器 B1067 已飞行 37 次 | Space.com：space.com/space-exploration/launches-spacecraft/spacex-starship-record-37th-booster-flight-100-falcon-9-launches |
| 2025 年猎鹰 9 号发射约 165 次 | Space.com：space.com/space-exploration/private-spaceflight/spacex-shatters-its-rocket-launch-record-yet-again-167-orbital-flights-in-2025 ；SpaceNews 2025 年度发射统计 |
| 2026 年 9 月星舰第 14 次试飞首次进入轨道并释放星链卫星 | en.wikipedia.org/wiki/Starship_flight_14 ；Ars Technica 2026-09 报道 |
| 2026 年 9 月在轨工作的卫星约 1.7 万颗，其中约三分之二是星链 | Jonathan McDowell, Jonathan's Space Report：planet4589.org/space/stats/active.html （9 月底 16,914 颗，其中星链 11,143 颗） |
| 旅行者 1 号到 2026 年距地球超过 250 亿公里，信号单程近一天（NASA 页面：2026 年 11 月 18 日将达约 259 亿公里、一光日） | NASA “Where are Voyager 1 and 2 now”：science.nasa.gov/mission/voyager/where-are-voyager-1-and-voyager-2-now/ |
| Landsat 数据 2008 年起免费开放 | 美国地质调查局：usgs.gov/landsat-missions/april-21-2008-imagery-everyone |
| GPS 星上时钟每天快约 38 微秒（狭义相对论慢约 7 微秒、广义相对论快约 45 微秒） | en.wikipedia.org/wiki/Error_analysis_for_the_Global_Positioning_System |
| DART 撞击使迪莫弗斯的公转周期缩短约 32 分钟 | en.wikipedia.org/wiki/Double_Asteroid_Redirection_Test ；NASA 2022-10-11 新闻稿 |

## 二、批量核对（年份与人物）

方法：用脚本 `tools/factcheck.py` 读取英文维基百科对应条目的全文，检查正文中的年份或关键词是否出现在相应上下文中；未通过的逐条人工复核。共核对 102 项，通过 97 项；未通过项均已人工处理，见下。原始结果保存在 `research/factcheck/space*.result.tsv`。

**首轮未通过项的处理：**

- 阿波罗 11 号 1969 年 7 月 20 日：脚本的匹配窗口没有覆盖日期，人工查看 Apollo 11 条目确认（7 月 20 日登月）
- 猎鹰 9 号单枚助推器复用次数：维基百科无 B1058 独立条目 → 改用 Space.com 报道，正文写成 B1067 在 2026 年 8 月第 37 次飞行
- 戈达德 1926 年液体火箭飞行 2.5 秒、高约 12 米：维基百科引用的戈达德日记原文为“rose 41 feet & went 184 feet, in 2.5 secs.”，保留
- 阿波罗月球样品约 382 千克：维基百科 Moon rock 条目写 381 千克，NASA 官方资料常写 382 千克（842 磅），两者一致到四舍五入，保留“约 382 千克”
- Landsat 2008 年免费：维基百科正文未写出 → 以 USGS 公告为准（见上表）
- 早期草稿“在轨卫星超过 1 万颗”：按 McDowell 2026 年 9 月统计更新为约 1.7 万颗
- 早期草稿“星舰成败参半”：与实际试飞记录不符 → 改为“2026 年 9 月第 14 次试飞首次进入轨道”

**已核对通过的说法（括号内为维基百科条目名）：**

戈达德 1926 液体火箭（Robert H. Goddard）；齐奥尔科夫斯基 1903 火箭方程（Tsiolkovsky rocket equation）；V-2 1942 首次成功（V-2 rocket）；V-2 1944 进入太空（V-2 rocket）；冯·布劳恩 回形针行动（Wernher von Braun）；土星五号 三级（Saturn V）；猎鹰 9 2015 12 月 着陆（Falcon 9）；星舰 2023 首次综合飞行（SpaceX Starship）；星舰 2024 筷子回收（SpaceX Starship flight test 5）；SERT-1 1964 离子推进（SERT-1）；深空一号 离子推进（Deep Space 1）；斯普特尼克 1957 10 月 4 日（Sputnik 1）；斯普特尼克 83.6 kg（Sputnik 1）；NASA 1958 成立（NASA）；加加林 1961 4 月 12 日 108 分钟（Vostok 1）；Syncom 3 1964 静止（Syncom）；克拉克 1945 静止通信卫星（Geostationary orbit）；立方星 1999 CalPoly Stanford（CubeSat）；GPS 1978 首颗（Global Positioning System）；GPS 1995 完全运行（Global Positioning System）；GPS 相对论 38 微秒（Error analysis for the Global Positioning System）；北斗 2020 全球（BeiDou）；伽利略 Galileo（Galileo (satellite navigation)）；Landsat 1972（Landsat program）；TIROS-1 1960（TIROS-1）；Corona 1960（Corona (satellite)）；凯斯勒综合征 1978（Kessler syndrome）；12 人登月（Apollo program）；阿波罗 17 1972（Apollo 17）；航天飞机 135 次（Space Shuttle）；挑战者号 1986（Space Shuttle Challenger disaster）；哥伦比亚号 2003（Space Shuttle Columbia disaster）；礼炮 1 号 1971（Salyut 1）；国际空间站 1998 首个舱段（International Space Station）；ISS 2000 起长期有人（International Space Station）；天宫 2022 建成（Tiangong space station）；东方红一号 1970（Dong Fang Hong I）；杨利伟 神舟五号 2003（Shenzhou 5）；嫦娥四号 2019 月背（Chang'e 4）；嫦娥五号 2020 采样（Chang'e 5）；嫦娥六号 2024 月背采样（Chang'e 6）；天问一号 祝融 2021（Zhurong (rover)）；列昂诺夫 1965 出舱（Alexei Leonov）；联盟号 1967 首飞（Soyuz (spacecraft)）；蒂托 2001 太空游客（Dennis Tito）；旅行者 1 号 1977（Voyager 1）；旅行者 1 号 2012 星际空间（Voyager 1）；引力弹弓 水手 10 号（Gravity assist）；Transit 4A RTG 1961（Radioisotope thermoelectric generator）；钚-238 半衰期 87.7（Plutonium-238）；索杰纳 1997（Sojourner (rover)）；毅力号 2021（Perseverance (rover)）；哈勃 1990（Hubble Space Telescope）；韦布 2021 发射（James Webb Space Telescope）；韦布 6.5 米（James Webb Space Telescope）；阿尔忒弥斯 1 2022（Artemis I）；阿尔忒弥斯 2 2026（Artemis II）；DART 2022 32 分钟（Double Asteroid Redirection Test）；猎鹰 1 2008 入轨（Falcon 1）；龙飞船 2020 载人（Crew Dragon Demo-2）；商业轨道运输 COTS（Commercial Orbital Transportation Services）；V-2 生产死亡多于袭击死亡（V-2 rocket）；V-2 射程约 320 km（V-2 rocket）；土星五号 110 米（Saturn V）；F-1 最大单燃烧室（Rocketdyne F-1）；阿波罗导航计算机 2048 字 RAM（Apollo Guidance Computer）；斯普特尼克 58 cm 96 分钟（Sputnik 1）；阿波罗 1 号 1967 火灾（Apollo 1）；阿波罗 13 号 1970（Apollo 13）；Syncom 3 东京奥运（Syncom）；KAL007 GPS 民用（Global Positioning System）；KH-11 1976（KH-11 KENNEN）；铱星 2009 碰撞（2009 satellite collision）；2007 反卫星试验（2007 Chinese anti-satellite missile test）；风云一号 1988（Fengyun）；科马罗夫 1967（Vladimir Komarov）；联盟 11 号 1971（Soyuz 11）；捷列什科娃 1963（Valentina Tereshkova）；艾伦 钝头体（H. Julian Allen）；翟志刚 2008 出舱（Zhai Zhigang）；灵感 4 号 2021（Inspiration4）；维珍银河 2021 载客（Virgin Galactic Unity 22）；机遇号 90 天（Opportunity (rover)）；机智号 2021 首飞（Ingenuity (helicopter)）；哈勃 1993 维修（STS-61）；韦布 18 块镜片（James Webb Space Telescope）；新视野号 2015 冥王星（New Horizons）；朱雀二号 2023 甲烷入轨（Zhuque-2）；猎鹰 9 2017 首次复用（Falcon 9）；国际空间站 98% 水回收（ISS ECLSS）；和平号 1986（Mir）；旅行者 2 号 天王星 海王星（Voyager 2）；加加林 弹射 7 km（Vostok 1）；钱学森 中国航天（Qian Xuesen）；猎户座 SLS 阿尔忒弥斯（Artemis program）；水手 10 号 1974 金星（Mariner 10）；深空网（NASA Deep Space Network）。

## 三、收词范围的对照来源

- 维基百科“重要条目”（Vital Articles）第 4 级“技术”中的 Space 一节（Spaceflight、Launch vehicle、Rocket engine、Satellite、Space station、Astronaut、Apollo 11、ISS、Mir、Saturn V、Soyuz、Vostok 1、Hubble、Voyager 等）逐条比对：单个任务和机构（NASA、ESA、Roscosmos、和平号、土星五号等）不单独立条，并入[太空竞赛]、[空间站]、[阿波罗登月]、[太空望远镜]、[空间探测器]等词条讲述。
- 维基百科“历史发明年表”与“航天大事年表”（Timeline of spaceflight）中 1900 年以后的里程碑。

## 四、延伸阅读（未作为核对依据）

- Don Pettit，《The Tyranny of the Rocket Equation》（NASA 航天员的短文）——把火箭方程讲得最透的一篇。
- Andrew Chaikin，《登月》（A Man on the Moon）——阿波罗计划最好的叙事史。
- Robert Zubrin，《赶往火星》（The Case for Mars）——就地取材思路的代表作。
- Eric Berger，《Liftoff》《Reentry》——SpaceX 从猎鹰 1 号到可回收火箭的内部历史。
- 《中国航天》杂志与中国载人航天工程官网——中国航天的一手资料。
