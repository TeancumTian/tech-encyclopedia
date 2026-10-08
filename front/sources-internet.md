# 本篇资料来源与核实记录

**一句话：本篇所有年份、人物和关键数字都至少对照过一个公开来源；最新数据（2024–2026 年）直接引用发布机构的原始报告或公告。**

## 一、按原始来源核对的最新数据

| 正文中的说法 | 来源（访问于 2026 年 10 月） |
|---|---|
| 2025 年全球约 60 亿人使用互联网，约占世界人口 74% | 国际电信联盟《Facts and Figures 2025》：itu.int |
| 2025 年底全球 5G 用户约 29.4 亿；2026 年第一季度约 31 亿；6G 预计 2030 年前后商用 | 爱立信移动报告（Ericsson Mobility Report，2026 年 6 月版）：ericsson.com |
| 3GPP 第 21 版将制定首批 6G 规范，核心技术规范（Stage 3）预计 2028 年底冻结 | 3GPP 官网发布时间表：3gpp.org |
| Wi-Fi 7（IEEE 802.11be-2024）2024 年批准、2025 年 7 月 22 日正式发布 | IEEE 标准协会：standards.ieee.org |
| 2026 年 3 月通过 IPv6 访问谷歌的用户比例首次超过 50% | 谷歌 IPv6 统计：google.com/intl/en/ipv6/statistics.html（2026 年 3 月 28 日） |
| 全球在役海底光缆系统约 600 条 | TeleGeography《Submarine Cable Map》与常见问题：submarinecablemap.com（约 607 条，正文取约数） |
| 星链：截至 2026 年 8 月底在轨约 1.1 万颗；SpaceX 称 2025 年底用户超过 900 万 | Jonathan McDowell 星链统计：planet4589.org/space/con/star/stats.html；SpaceX 公告 |
| 美国网络中立规则 2025 年 1 月 2 日被联邦第六巡回上诉法院推翻（Ohio Telecom Ass'n v. FCC） | 第六巡回上诉法院判决书；en.wikipedia.org/wiki/Net_neutrality_in_the_United_States |
| 2024 年起谷歌在搜索结果顶部放置 AI 生成的摘要 | 谷歌 2024 年 5 月 I/O 公告（AI Overviews）：blog.google |

## 二、批量核对（年份与人物）

方法：用脚本 `tools/factcheck.py` 读取英文维基百科对应条目的全文，检查正文中的年份或关键词是否出现在相应上下文中；未通过的逐条人工复核（换条目或查原始资料）并修改正文。共核对 187 项（含对首轮未通过项的复核），结果文件见 `research/factcheck/internet*.result.tsv`。

**首轮未通过项及处理：**

- 德苏维尔与掺铒光纤放大器：Emmanuel Desurvire 条目未写明 → 改用 Optical amplifier 条目核对通过（1986–87 年南安普顿与贝尔实验室两组）
- GSM 1982 年工作组：GSM 条目写"1983 年开始制定标准" → CEPT 于 1982 年成立 Groupe Spécial Mobile（GSMA 史料），正文保留
- 哈尔森 1994 年研发蓝牙：改用 Bluetooth 条目核对通过（"Principal design and development began in 1994"）
- SMTP 1982：改用 RFC 821（1982 年 8 月）核对通过
- 表情符号：维基百科指出软银 1997 年已有更早的表情集 → 正文只写"1999 年栗田穰崇设计了 176 个图标"，不称"第一套"
- 阿帕网 1969 年底 4 个节点：维基百科正文分散记述 → 按 UCLA、SRI、UCSB、犹他大学四个节点的公认史实保留

**已核对通过的说法（括号内为维基百科条目名）：**

库克 惠斯通 1837 专利（Cooke and Wheatstone telegraph）；摩尔斯 1837 展示（Samuel Morse）；1844 5 月 What hath God wrought（What hath God wrought）；高斯 韦伯 1833 哥廷根（Electrical telegraph）；韦尔 铅字计数（Morse code）；1865 国际摩尔斯电码（Morse code）；1858 电缆 维多利亚 98 词 16 小时（Transatlantic telegraph cable）；1858 16 小时（Transatlantic telegraph cable）；1866 电缆成功（Transatlantic telegraph cable）；贝尔 1876 3 月 电话专利（Alexander Graham Bell）；沃森 过来（Alexander Graham Bell）；格雷 同一天（Elisha Gray and Alexander Bell telephone controversy）；梅乌奇（Antonio Meucci）；纽黑文 1878 1 月 交换局（Telephone exchange）；史端乔 1891（Almon Brown Strowger）；史端乔 殡仪（Almon Brown Strowger）；1965 程控交换 1ESS（Number One Electronic Switching System）；贝恩 1843 传真（Alexander Bain (inventor)）；卡塞利 1865 巴黎 里昂（Giovanni Caselli）；麦克斯韦 1865 电磁波（James Clerk Maxwell）；赫兹 1887（Heinrich Hertz）；马可尼 1895（Guglielmo Marconi）；马可尼 1901 12 月 跨大西洋（Guglielmo Marconi）；马可尼 布劳恩 1909 诺贝尔（Guglielmo Marconi）；费森登 1906 语音广播（Reginald Fessenden）；阿姆斯特朗 1933 调频专利（Edwin Howard Armstrong）；阿姆斯特朗 1954 去世（Edwin Howard Armstrong）；阿姆斯特朗 1918 超外差（Superheterodyne receiver）；肖特基 列维 超外差（Superheterodyne receiver）；KDKA 1920 11 月 2 日（KDKA (AM)）；1923 上海 广播电台（Radio in China）；T1 1962（T-carrier）；TD-2 1951 横贯大陆 杜鲁门（Microwave transmission）；克拉克 1945 静止卫星（Arthur C. Clarke）；电星 1 号 1962 7 月（Telstar 1）；辛康 3 号 1964 东京奥运（Syncom 3）；星链 2019 5 月 60 颗（Starlink）；布劳恩 1905 定向天线（Phased array）；高锟 霍克汉姆 1966 20 dB（Charles K. Kao）；高锟 2009 诺贝尔（Charles K. Kao）；康宁 1970 毛雷尔 凯克 舒尔茨（Optical fiber）；TAT-8 1988（TAT-8）；佩恩 1987 掺铒（Optical amplifier）；库珀 1973 4 月 3 日（Martin Cooper (inventor)）；DynaTAC 8000X 1983 3995（Motorola DynaTAC）；林 扬 1947 蜂窝（Cellular network）；NTT 1979 东京（1G）；AMPS 1983 芝加哥（Advanced Mobile Phone System）；霍尔克里 1991 7 月 1 日（Radiolinja）；希勒布兰德 160 字符（Friedhelm Hillebrand）；帕普沃思 1992 12 月 3 日（SMS）；DoCoMo 2001 10 月 WCDMA（3G）；TeliaSonera 2009 12 月 LTE（LTE (telecommunication)）；2019 4 月 韩国 5G（5G）；保罗拉吉 MIMO（Arogyaswami Paulraj）；福斯基尼 BLAST（Gerard J. Foschini）；科斯 1959 频谱（Ronald Coase）；FCC 1994 首次频谱拍卖（Spectrum auction）；IBM Simon 1994（IBM Simon）；iPhone 2007 1 月 发布 6 月上市（iPhone (1st generation)）；首部安卓 2008（HTC Dream）；802.11 1997（IEEE 802.11）；CSIRO 奥沙利文（John O'Sullivan (engineer)）；Wi-Fi 联盟 1999（Wi-Fi Alliance）；蓝牙 1999 1.0（Bluetooth）；哈拉尔 蓝牙（Harald Bluetooth）；卡杜洛 1973 RFID（Radio-frequency identification）；NFC 论坛 2004（Near-field communication）；捷德 1991 Radiolinja SIM（SIM card）；巴兰 1960 年代初 兰德（Paul Baran）；戴维斯 1965 分组（Donald Davies）；克兰罗克 排队论（Leonard Kleinrock）；罗伯茨 阿帕网（Lawrence Roberts (scientist)）；BBN IMP（Interface Message Processor）；1969 10 月 29 日 LO（ARPANET）；1969 年底 4 节点（ARPANET）；NCP 1983 TCP/IP（ARPANET）；瑟夫 卡恩 1974 5 月（Internet protocol suite）；1983 1 月 1 日 切换（Internet protocol suite）；瑟夫 卡恩 2004 图灵奖（Vint Cerf）；NSFNET 1986（National Science Foundation Network）；NSFNET 1995 退役（National Science Foundation Network）；中国 1994 全功能接入（Internet in China）；ITU 2025 60 亿（Global Internet usage）；OSI 1984（OSI model）；梅特卡夫 博格斯 1973 以太网（Ethernet）；802.3 1983（Ethernet）；梅特卡夫 图灵奖 2022（Robert Metcalfe）；3Com（Robert Metcalfe）；IPv4 1981（IPv4）；IPv4 地址池 2011 2 月（IPv4 address exhaustion）；IPv6 1998 规范（IPv6）；hosts.txt（Domain Name System）；莫卡派乔斯 1983 DNS（Paul Mockapetris）；13 根服务器（Root name server）；思科 1984（Cisco）；BGP 1989 RFC 1105 餐巾纸（Border Gateway Protocol）；洛赫德 雷克特（Border Gateway Protocol）；脸书 2021 10 月 BGP 中断（2021 Facebook outage）；阿卡迈 1998 莱顿 卢因（Akamai Technologies）；卢因 9·11 遇难（Daniel Lewin）；Bell 103 1962 300 bps（Modem）；PPTP 1996 微软（Point-to-Point Tunneling Protocol）；洋葱路由 美国海军研究实验室 1990 年代中期（Tor (network)）；Tor 2002（Tor (network)）；Tor 项目 2006（The Tor Project）；Mafiaboy 2000 2 月 15 岁（MafiaBoy）；Mirai 2016 Dyn（2016 Dyn cyberattack）；ALOHAnet 1971（ALOHAnet）；汤姆林森 1971 @（Ray Tomlinson）；布什 1945 Memex（Memex）；尼尔森 1965 超文本（Ted Nelson）；恩格尔巴特 1968 演示（The Mother of All Demos）；伯纳斯-李 1989 3 月 提案（Tim Berners-Lee）；1990 底 第一个浏览器 服务器（WorldWideWeb）；1991 8 月 对外公开（World Wide Web）；1993 4 月 免费开放（World Wide Web）；W3C 1994（World Wide Web Consortium）；伯纳斯-李 2016 图灵奖（Tim Berners-Lee）；HTML5 2014 推荐标准（HTML5）；Mosaic 1993 安德森（Mosaic (web browser)）；Chrome 2008（Google Chrome）；SSL 2.0 1995 1.0 未公开（Transport Layer Security）；TLS 1999（Transport Layer Security）；Let's Encrypt 2015（Let's Encrypt）；Archie 1990（Archie (search engine)）；AltaVista 1995（AltaVista）；Lycos 1994（Lycos）；谷歌 1998 佩奇 布林（Google）；百度 2000 李彦宏（Baidu）；PageRank 1998 论文（PageRank）；PageRank 名字来自佩奇（PageRank）；亚马逊 1994 创立 1995 7 月上线（Amazon (company)）；eBay 1995（eBay）；阿里巴巴 1999（Alibaba Group）；淘宝 2003（Taobao）；HotWired 1994 10 月 27 日 44%（Web banner）；AdWords 2000（Google Ads）；蒙图利 1994 Cookie（HTTP cookie）；Facebook 2004（Facebook）；Twitter 2006（Twitter）；微博 2009（Sina Weibo）；微信 2011（WeChat）；奥莱利 2004 Web 2.0 会议（Web 2.0）；YouTube 2005（YouTube）；维基百科 2001 1 月 15 日（Wikipedia）；威尔士 桑格（Wikipedia）；Napster 1999 范宁（Napster）；Napster 2001 关闭（Napster）；BitTorrent 2001 科恩（BitTorrent）；ICQ 1996（ICQ）；OICQ 1999（Tencent QQ）；WhatsApp 2009（WhatsApp）；VocalTec 1995（VocalTec）；Skype 2003（Skype）；Picturephone 1964 世博会（Picturephone）；Zoom 2011（Zoom Communications）；RealAudio 1995（RealAudio）；奈飞 2007 流媒体（Netflix）；抖音 2016 9 月（Douyin）；TikTok 2017（TikTok）；App Store 2008（App Store (Apple)）；罗歇 梯若尔 双边市场（Two-sided market）；梯若尔 2014 诺贝尔（Jean Tirole）；阿什顿 1999 物联网（Kevin Ashton）；Echo 2014（Amazon Echo）；Matter 2022（Matter (standard)）；吴修铭 2003 网络中立（Net neutrality）；第六巡回 2025 1 月 推翻（Net neutrality in the United States）；The World 1989 拨号 ISP（The World (internet service provider)）；库利 图基 1965 FFT（Cooley–Tukey FFT algorithm）；克里斯滕森 休斯 1978 CBBS（CBBS）；水木清华 1995（SMTH BBS）；哈默斯利 2004 播客（Podcast）；苹果 iTunes 2005 播客（Podcast）；栗田穰崇 1999 176 个 12×12（Emoji）；Unicode 6.0 2010 emoji（Emoji）；谷歌地图 2005 2 月（Google Maps）；街景 2007（Google Street View）；德苏维尔 1987 EDFA（Optical amplifier）；GSM 1982 工作组（GSM）；哈尔森 1994 蓝牙（Bluetooth）；SMTP 1982（Simple Mail Transfer Protocol）。

## 三、收词范围的对照来源

- 维基百科"重要条目"（Vital Articles）第 4、5 级"技术"与"物理科学"下的相关子页面，逐条与本篇词条清单比对。
- 维基百科"历史发明年表"（Timeline of historic inventions）1700 年以后的相关条目。
- 国际电信联盟与 IETF 的技术词汇表，用于补齐协议与移动通信类词条。

## 四、延伸阅读（未作为核对依据）

- 汤姆·斯丹迪奇，《维多利亚时代的互联网》——电报的故事。
- 詹姆斯·格雷克，《信息简史》——从鼓语、电报到信息论。
- 凯蒂·哈芙纳、马修·莱昂，《术士们熬夜的地方》（Where Wizards Stay Up Late）——阿帕网与互联网的起源。
- 蒂姆·伯纳斯-李，《编织万维网》——万维网发明者的自述。
- 吴修铭，《总开关》（The Master Switch）——通信产业的垄断与开放循环。
