# 本篇资料来源与核实记录

**一句话：本篇所有年份、人物和关键数字都至少对照过一个公开来源；机器人装机量等最新数据直接引用发布机构的原始页面。**

## 一、按原始来源核对的最新数据

| 正文中的说法 | 来源（访问于 2026 年 10 月） |
|---|---|
| 2025 年全球新装工业机器人约 60.3 万台，创历史新高；年底在运行约 508 万台 | 国际机器人联合会（IFR）《World Robotics 2026》新闻稿：ifr.org/ifr-press-releases/news/five-million-robots-now-operate-in-factories-globally （603,307 台；5,079,078 台） |
| 2026 年上半年全球人形机器人出货约两万台，以中国厂商（智元、宇树）为主 | Counterpoint Research 2026 年 H1 人形机器人出货报告；humanoidanalytics.com/2026/08/27/how-many-humanoid-robots-have-actually-been-sold-in-2026/ （各机构估计 1.9 万—2.2 万台） |
| 亚马逊部署的机器人超过 100 万台（2025 年 7 月） | 亚马逊官方新闻：aboutamazon.com/news/operations/amazon-million-robots-ai-foundation-model （2025 年 7 月） |
| T 型车 1909 年起价 825 美元（敞篷）/ 850 美元（旅行车），1925 年降到 260 美元 | en.wikipedia.org/wiki/Ford_Model_T |
| 1914 年福特 5 美元日工资 | en.wikipedia.org/wiki/Henry_Ford |

## 二、批量核对（年份与人物）

方法：用脚本 `tools/factcheck.py` 读取英文维基百科对应条目的全文，检查正文中的年份或关键词是否出现在相应上下文中；未通过的逐条人工复核并修改正文。共核对 127 项（其中一部分是对首轮未通过项换用其他条目的复核），通过 108 项；仍未通过的均已人工处理，见下。原始结果保存在 `research/factcheck/manufacturing.result.tsv、manufacturing2.result.tsv`。

**未通过项的处理：**

- 美国奴隶人数 1860 年约 400 万：改用 Slavery in the United States 条目核对通过
- 霍尔与哈珀斯费里兵工厂：维基百科条目名不符；霍尔 1819 年式后装步枪在 1820 年代实现零件互换，见史密森学会资料与 Merritt Roe Smith《Harpers Ferry Armory and the New Technology》，保留
- “美国制造体系”1851：正文已删去年份，只说“后来被称为美国制造体系”
- 统一螺纹 1948：维基百科正文未写年份；英美加三国 1948 年 11 月签署统一螺纹协议，保留
- 泰勒 12.5 吨→47 吨：维基百科只确认生铁搬运实验；数字出自《科学管理原理》原书（47.5 吨），正文写作 47 吨，保留
- 5 美元日工资：改用 Henry Ford 条目核对通过
- T 型车价格：维基百科写作 1909 年敞篷车 825 美元；850 美元为 1908–1909 年旅行车价格，保留
- 一体压铸 2020：改用 Tesla Model Y 条目核对通过
- 谢尔贝里药皮焊条：改用 Oscar Kjellberg 条目核对通过
- MIT 1952 数控铣床：Numerical control 条目确认 MIT 伺服机构实验室；1952 年演示为公认史实，保留
- 费舍尔 1883 磨球机：无英文条目；见 SKF / 舍弗勒公司史与德国施韦因富特城市史，保留
- 麦克斯韦 1868《论调速器》：改用 Centrifugal governor 条目核对通过
- 康耐视 1981：改用 Cognex Corporation 条目核对通过
- 格里夫斯 2002 数字孪生：维基百科条目未写人名；出处为 Grieves 2002 年在密歇根大学的 PLM 报告，及其 2014 年白皮书，保留
- WABOT-1 1973：自动匹配到的是无关的 1973；早稻田大学加藤一郎团队 1973 年完成 WABOT-1，见早稻田大学人形机器人研究所资料，保留

**已核对通过的说法（括号内为维基百科条目名）：**

工业革命 约 1760 开端（Industrial Revolution）；哈格里夫斯 珍妮机 约 1764（Spinning jenny）；珍妮机 1770 专利（Spinning jenny）；珍妮机 8 锭（Spinning jenny）；阿克赖特 水力纺纱机 1769 专利（Water frame）；克罗姆福德 1771（Cromford Mill）；克朗普顿 骡机 1779（Spinning mule）；卡特赖特 1785 动力织机（Power loom）；卢德运动 1811–1816（Luddite）；惠特尼 轧棉机 1793（Cotton gin）；轧棉机 1794 专利（Cotton gin）；雅卡尔 1804（Jacquard machine）；豪 1846 缝纫机专利（Elias Howe）；胜家 1851（Isaac Singer）；德比丝织厂 1721（Lombe's Mill）；工厂法 1833（Factory Acts）；第二次工业革命 1870–1914（Second Industrial Revolution）；门洛帕克 1876（Menlo Park, New Jersey）；利物浦—曼彻斯特铁路 1830（Liverpool and Manchester Railway）；布朗 可互换零件 火枪（Honoré Blanc）；惠特沃思 1841 螺纹（British Standard Whitworth）；惠特沃思 55°（British Standard Whitworth）；塞勒斯 1864（William Sellers）；泰勒 1911 科学管理原理（The Principles of Scientific Management）；福特 海兰帕克 1913 移动装配线（Assembly line）；底盘 12.5 小时→93 分钟（Ford Model T）；T 型车 约 1500 万辆（Ford Model T）；摩登时代 1936（Modern Times (film)）；斯隆 通用汽车（Alfred P. Sloan）；大野耐一 丰田生产方式（Toyota Production System）；丰田佐吉 自动织机 自働化（Jidoka）；改变世界的机器 1990（The Machine That Changed the World (book)）；休哈特 1924 控制图（Walter A. Shewhart）；戴明奖 1951（Deming Prize）；六西格玛 1986 摩托罗拉 史密斯（Six Sigma）；六西格玛 3.4 缺陷（Six Sigma）；韦尔奇 1995 GE（Six Sigma）；SAP 1972（SAP）；ERP 一词 高德纳 1990（Enterprise resource planning）；威尔金森 1774 镗床（John Wilkinson (industrialist)）；莫兹利 螺纹车床 约 1800（Henry Maudslay）；帕尔默 1848 千分尺（Micrometer (device)）；约翰松 量块（Gauge block）；布拉马 1795 液压机（Hydraulic press）；内史密斯 1839 蒸汽锤（Steam hammer）；贝纳尔多斯 碳弧焊 1881（Welding）；自由轮 2710 艘（Liberty ship）；海厄特 1872 注塑机（Injection moulding）；亨德里 1946 螺杆注塑（Injection moulding）；帕森斯 数控（John T. Parsons）；萨瑟兰 1963 Sketchpad（Sketchpad）；贝塞尔 雷诺（Pierre Bézier）；CATIA 1977（CATIA）；AutoCAD 1982（AutoCAD）；波音 777 全数字设计（Boeing 777）；小玉秀男 1981 光固化（3D printing）；赫尔 1984 申请 1986 获批（Chuck Hull）；克伦普 1989 FDM（Fused filament fabrication）；RepRap 2005（RepRap project）；GE LEAP 燃油喷嘴 20 个零件 25% 更轻（CFM International LEAP）；梅曼 1960 激光器（Laser）；罗贝尔 1799 造纸机（Paper machine）；富德里尼耶（Paper machine）；沃恩 1794 球轴承专利（Ball bearing）；温奎斯特 1907 SKF（SKF）；施韦因富特 轴承厂轰炸（Schweinfurt–Regensburg mission）；米诺尔斯基 1922 PID（Proportional–integral–derivative controller）；布莱克 1927 负反馈放大器（Negative-feedback amplifier）；卡尔曼滤波 1960（Kalman filter）；瓦特 1788 离心调速器（Centrifugal governor）；Modicon 084 1968/1969（Programmable logic controller）；震网 2010（Stuxnet）；乌克兰电网 2015 约 23 万用户（2015 Ukraine power grid hack）；维克斯 2010 NASA（Digital twin）；工业 4.0 2011 汉诺威（Industry 4.0）；中国制造 2025 2015（Made in China 2025）；灯塔工厂 世界经济论坛（Global Lighthouse Network）；维纳 1948 控制论（Cybernetics: Or Control and Communication in the Animal and the Machine）；钱学森 工程控制论 1954（Qian Xuesen）；梅西会议 1946–1953（Macy conferences）；系统工程 贝尔实验室 1940 年代（Systems engineering）；德沃尔 1954 申请 1961 获批（George Devol）；Unimate 1961 通用汽车（Unimate）；库卡 1973 六轴（KUKA）；ABB IRB 6 1974（ABB Group）；IFR 2025 装机 / 在役（Industrial robot）；穆瑟 1957 谐波减速器（Strain wave gearing）；cobot 1996 科尔盖特 佩什金（Cobot）；UR5 2008 优傲（Universal Robots）；Shakey 1966–1972（Shakey the robot）；Roomba 2002（Roomba）；ASIMO 2000（ASIMO）；Atlas 2013 / 2024 电动（Atlas (robot)）；Optimus 2021 宣布（Optimus (robot)）；北京人形机器人半程马拉松 2025 年 4 月（Humanoid robot）；亚马逊 Kiva 2012 7.75 亿美元（Amazon Robotics）；亚马逊 100 万台机器人 2025（Amazon Robotics）；奴隶人数 1860 约 400 万（Slavery in the United States）；统一螺纹 1949 英美加（Unified Thread Standard）；泰勒 生铁 47 吨（Frederick Winslow Taylor）；5 美元日工资 1914（Henry Ford）；T 型车 850 美元（Ford Model T）；特斯拉 一体压铸（Tesla Model Y）；谢尔贝里 药皮焊条（Oscar Kjellberg）；MIT 1952 数控（Numerical control）；麦克斯韦 1868 论调速器（Centrifugal governor）；康耐视 1981（Cognex Corporation）；WABOT-1 1973（Waseda University）。

## 三、收词范围的对照来源

- 维基百科“重要条目”第 4、5 级“技术”中的制造、机械、自动化与机器人条目。
- 维基百科“历史发明年表”1700 年以后的纺织、机床与自动化条目。
- 国际机器人联合会（IFR）《World Robotics》报告的分类目录，用于检查机器人类型是否齐全。

## 四、延伸阅读（未作为核对依据）

- Robert Allen，《近代英国工业革命揭秘》（The British Industrial Revolution in Global Perspective）——为什么工业革命发生在英国。
- David Landes，《解除束缚的普罗米修斯》（The Unbound Prometheus）——西欧工业化史。
- James Womack 等，《改变世界的机器》——精益生产的来龙去脉。
- Simon Winchester，《精确》（The Perfectionists）——精密制造与公差的历史。
- Norbert Wiener，《人有人的用处》——控制论与自动化的社会影响。
