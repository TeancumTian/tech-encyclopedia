# 本篇资料来源与核实记录

**一句话：本篇所有年份、人物和关键数字都至少对照过一个公开来源；2025–2026 年的最新数据直接引用发布机构或原始报道页面。**

## 一、按原始来源核对的最新数据

| 正文中的说法 | 来源（访问于 2026 年 10 月） |
|---|---|
| 到 2025 年中国高铁运营里程超过 5 万公里（2025 年 12 月 26 日西延高铁开通时突破，年底约 5.04 万公里） | 国家铁路局：source.nra.gov.cn/xwzx/xwxx/xwlb/202512/t20251226_350314.shtml ；新华社英文稿 english.news.cn/20251226/82fd20d06c6b4dddb8c40f77e27188f0/c.html ；《2025 年交通运输行业发展统计公报》gov.cn/lianbo/202606/content_7072829.htm |
| 2025 年全球电动汽车（纯电加插混）销量超过 2000 万辆（比 2024 年增长 20%），约占新车销量的四分之一 | 国际能源署《Global EV Outlook 2026》：iea.org/reports/global-ev-outlook-2026/trends-in-electric-cars ；IEA Global EV Data Explorer |
| 到 2026 年 9 月 Waymo 在美国约 15 个城市运营付费无人驾驶出租车，每周约 50 万单 | TechCrunch，2026-09-24：techcrunch.com/2026/09/24/waymo-is-scaling-fast-heres-what-the-fleet-data-shows/ |
| 全球每年约 119 万人死于道路交通事故（2021 年数据） | 世界卫生组织《Global status report on road safety 2023》：who.int/publications/i/item/9789240086517 |
| 汽油车只有约 12–30% 的燃料能量到达车轮；电动车电网到车轮在 77% 以上 | 美国能源部：fueleconomy.gov/feg/atv.shtml ；fueleconomy.gov/feg/evtech.shtml |
| 1879 年泰德沃特管道长约 175 公里（109 英里），是第一条长距离输油管道 | 宾夕法尼亚州历史标志 hmdb.org/m.asp?m=59155 ；en.wikipedia.org/wiki/Tidewater_Oil_Company |
| T 型车基本款售价 1909 年 825 美元，1925 年降到 260 美元 | en.wikipedia.org/wiki/Ford_Model_T |
| C919 于 2023 年 5 月投入商业运营；亿航 EH216-S 于 2023 年 10 月获型号合格证 | en.wikipedia.org/wiki/Comac_C919 ；en.wikipedia.org/wiki/EHang |

## 二、批量核对（年份与人物）

方法：用脚本 `tools/factcheck.py` 读取英文维基百科对应条目的全文，检查正文中的年份或关键词是否出现在相应上下文中；未通过的逐条人工复核并修改正文。共核对 109 项（其中十余项是对首轮未通过项换用其他条目的复核），通过 101 项；仍未通过的均已人工处理，见下。原始结果保存在 `research/factcheck/transport*.result.tsv`。

**首轮未通过项的处理：**

- 西门子 1879 电力铁路：Siemens 公司条目未写年份 → 改用 Werner von Siemens 与 Electric locomotive 条目核对通过
- F-8 数字电传 1972：无独立条目 → 改用 Fly-by-wire 与 Vought F-8 条目核对通过
- 泰德沃特管道 1879：维基百科无独立条目 → 以宾夕法尼亚州历史标志与 Tidewater Oil Company 条目为准（1879 年，109 英里 ≈ 175 公里），保留
- 胡利 1902 柏油碎石路：Tarmac 条目未写年份 → 改用 Edgar Purnell Hooley 条目核对通过
- WHO 每年 119 万道路死亡：维基百科数字版本不一 → 以 WHO《2023 年全球道路安全状况报告》原文为准（见上表）
- T 型车售价：初稿写“850 美元降到 300 美元以下”，核对后改为基本款 1909 年 825 美元、1925 年 260 美元（正文与词条数据同步修改）
- 集装箱化前后每吨装卸成本（5.86 美元 → 0.16 美元）：未找到可靠一手出处 → 正文不使用该数字
- 兴登堡号遇难人数：按维基百科改为共 36 人（艇上 35 人、地面 1 人）
- 电动车 2025 年销量份额：初稿“超过四分之一” → 按 IEA 原文改为“约占四分之一”

**已核对通过的说法（括号内为维基百科条目名）：**

特里维西克 1804 蒸汽机车（Richard Trevithick）；火箭号 1829 雨山竞赛（Stephenson's Rocket）；斯托克顿—达灵顿铁路 1825（Stockton and Darlington Railway）；利物浦—曼彻斯特铁路 1830（Liverpool and Manchester Railway）；标准轨距 1435 mm（Standard-gauge railway）；英国 1846 轨距法（Rail gauge）；铁路时间 1847 英国（Railway time）；美加铁路标准时间 1883（Railway time）；伦敦大都会铁路 1863（Metropolitan Railway）；里希特费尔德有轨电车 1881（Gross-Lichterfelde Tramway）；新干线 1964 东海道（Tokaido Shinkansen）；中国高铁里程（High-speed rail in China）；上海磁浮 2004 商业运营（Shanghai maglev train）；上海磁浮 431 km/h（Shanghai maglev train）；安全自行车 Rover 1885 Starley（Safety bicycle）；本茨 1886 专利（Benz Patent-Motorwagen）；邓禄普 1888 充气轮胎（John Boyd Dunlop）；戴姆勒 1885 摩托车（Daimler Reitwagen）；T 型车 1908（Ford Model T）；T 型车 1500 万辆（Ford Model T）；沃尔沃 三点式安全带 1959 Bohlin（Nils Bohlin）；科隆—波恩高速 1932（Autobahn）；麦克亚当 碎石路（John Loudon McAdam）；克利夫兰 1914 电动红绿灯（Traffic light）；伦敦 1868 煤气信号灯（Traffic light）；普锐斯 1997（Toyota Prius）；特斯拉 Roadster 2008（Tesla Roadster (first generation)）；DARPA 大挑战 2004（DARPA Grand Challenge）；DARPA 2005 斯坦福 Stanley（DARPA Grand Challenge (2005)）；Waymo 无人驾驶商业服务 2018（Waymo）；优步 2009 成立（Uber）；库里蒂巴 BRT 1974（Rede Integrada de Transporte）；超级高铁 马斯克 2013 白皮书（Hyperloop）；Hyperloop One 2023 倒闭（Hyperloop One）；克莱蒙特号 1807 富尔顿（North River Steamboat）；螺旋桨 1836 史密斯 埃里克森（Propeller）；苏伊士运河 1869（Suez Canal）；巴拿马运河 1914（Panama Canal）；麦克莱恩 理想 X 1956（Ideal X）；ISO 集装箱标准 1968（Containerization）；的里雅斯特号 1960（Trieste (bathyscaphe)）；奋斗者号 2020（Fendouzhe）；哈里森 H4 1761（John Harrison）；蒙戈尔菲耶 1783（Montgolfier brothers）；齐柏林 LZ 1 1900（Zeppelin LZ 1）；兴登堡号 1937（Hindenburg disaster）；莱特兄弟 1903 12 月 17 日（Wright brothers）；莱特飞行 12 秒 37 米（Wright Flyer）；西科斯基 VS-300 1939（Vought-Sikorsky VS-300）；He 178 1939（Heinkel He 178）；惠特尔 1930 专利（Frank Whittle）；彗星客机 1952（De Havilland Comet）；波音 707 1958（Boeing 707）；波音 747 1970 投入运营（Boeing 747）；协和 1969 首飞 2003 退役（Concorde）；斯佩里 自动驾驶仪 1912（Autopilot）；空客 A320 电传（Airbus A320 family）；克罗伊登 1920 空管（Air traffic control）；安许茨 陀螺罗经 1908（Gyrocompass）；叉车 托盘（Pallet）；西门子 1879 柏林博览会电力机车（Werner von Siemens）；西门子 1879 电力铁路（Electric locomotive）；F-8 数字电传 1972（Vought F-8 Crusader）；F-8 数字电传 1972（Fly-by-wire）；中国高铁 5 万公里 时间（High-speed rail in China）；蒸汽船 菲奇 1787（Steamboat）；欧洲之星 TGV 1981（TGV）；集装箱 TEU 全球海运（Container ship）；锂电池 价格 下降（Electric car）；电动车 2025 销量份额（Electric car）；美国第一条横贯大陆铁路 1869（First transcontinental railroad）；伦敦城南铁路 1890 电力地铁（City and South London Railway）；纽约地铁 1904（New York City Subway）；北京地铁 1969（Beijing Subway）；京津城际 2008（Beijing–Tianjin intercity railway）；1956 州际公路法（Interstate Highway System）；沪嘉高速 1988（Shanghai–Jiading Expressway）；屈尼奥 1769 蒸汽车（Nicolas-Joseph Cugnot）；博世 ABS 1978（Anti-lock braking system）；滴滴 2012（DiDi）；ofo 2014/2015（Ofo (company)）；Bird 2017（Bird Global）；库里蒂巴 勒纳（Jaime Lerner）；波哥大 TransMilenio 2000（TransMilenio）；广州 BRT 2010（Guangzhou Bus Rapid Transit）；深圳 2017 全电动公交（Shenzhen Bus Group）；大西方号 1838（SS Great Western）；大不列颠号 1843（SS Great Britain）；韦纳姆 1871 风洞（Wind tunnel）；普朗特 1904 边界层（Boundary layer）；JT9D 747（Pratt & Whitney JT9D）；C919 2023 首次商业航班（Comac C919）；图-144 1968 首飞（Tupolev Tu-144）；斯佩里 1914 巴黎演示（Autopilot）；A320 1987 首飞（Airbus A320 family）；大峡谷空中相撞 1956（1956 Grand Canyon mid-air collision）；FAA 1958（Federal Aviation Administration）；亿航 EH216 2023 型号合格证（EHang）；大疆 2006（DJI）；戴姆勒 1896 卡车（Truck）；胡利 柏油碎石 1902（Edgar Purnell Hooley）。

## 三、收词范围的对照来源

- 维基百科“重要条目”（Vital Articles）第 4 级“技术”中的 Transportation、Transport infrastructure、Navigation 各节逐条比对：出租车并入[网约车]、船闸并入[现代运河]、轮胎并入[充气轮胎]、滑翔机与机翼并入[飞机]和[空气动力学]、卫星导航放在第 9 篇；畜力运输、帆船、马车等前工业时代条目不在本书“近现代”范围内；桥梁、隧道归第 12 篇。
- 维基百科“历史发明年表”（Timeline of historic inventions）1760 年以后与交通相关的全部条目。

## 四、延伸阅读（未作为核对依据）

- Marc Levinson，《集装箱改变世界》（The Box）——集装箱如何重塑全球贸易，本篇“标准胜过机器”一线的最佳读物。
- Christian Wolmar，《铁路改变世界》（Blood, Iron and Gold）——全球铁路史。
- John D. Anderson，《飞行导论》（Introduction to Flight）——空气动力学与飞机设计的入门教材。
- David McCullough，《莱特兄弟》（The Wright Brothers）。
- Vaclav Smil，《Prime Movers of Globalization》——柴油机与燃气轮机如何支撑全球化。
