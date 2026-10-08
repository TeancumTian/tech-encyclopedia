# 本篇资料来源与核实记录

**一句话：本篇所有年份、人物和关键数字都至少对照过一个公开来源；最新数据（2024–2026 年）直接引用发布机构的原始报告或公告。**

## 一、按原始来源核对的最新数据

| 正文中的说法 | 来源（访问于 2026 年 10 月） |
|---|---|
| 台积电 2 纳米（N2）2025 年第四季度量产，采用 GAA 结构；3 纳米 2022 年底量产 | 台积电财报与新闻稿：pr.tsmc.com |
| 英特尔 18A 于 2025 年开始量产 | 英特尔公告与 2025 年财报：intel.com |
| 2026 年第二季度台积电占全球前十大晶圆代工营收的 72.5% | TrendForce 晶圆代工季度排名（2026 年 9 月发布）：trendforce.com |
| 英伟达 Blackwell GPU 约 2080 亿个晶体管 | 英伟达 GTC 2024 发布资料：nvidia.com |
| 苹果 A17 Pro 约 190 亿个晶体管 | 苹果 2023 年发布会资料；en.wikipedia.org/wiki/Apple_A17 |
| 2023 年全球约 6.7 亿人没有用上电 | 国际能源署、IRENA、联合国统计司、世界银行、世卫组织《Tracking SDG 7: The Energy Progress Report 2025》：trackingsdg7.esmap.org |

## 二、批量核对（年份与人物）

方法：用脚本 `tools/factcheck.py` 读取英文维基百科对应条目的全文，检查正文中的年份或关键词是否出现在相应上下文中；未通过的逐条人工复核（换条目或查原始资料）并修改正文。共核对 143 项（含对首轮未通过项的复核），结果文件见 `research/factcheck/electronics*.result.tsv`。

**首轮未通过项及处理：**

- 劳芬—法兰克福 1891 年三相输电：维基百科无独立英文条目 → 改用 Mikhail Dolivo-Dobrovolsky 条目核对通过（1891 年 8 月投运、175 公里）
- 布莱克负反馈专利 1937 年获批：改用 Negative-feedback amplifier 条目核对通过（US 2,102,671）
- 奥尔 1940 年发现 PN 结：维基百科 P–n junction 条目写作 1939 年 → 查计算机历史博物馆与 PBS 资料，确认 1940 年 2 月 23 日的硅棒实验，正文保留"1940 年 2 月"
- 拉斯罗普、纳尔 1957 年光刻：维基百科写明 1957 年发明、1958 年在 IRE 会议上公开、选用"photolithography"一词 → 正文改为"1957 年首次用光刻法制作晶体管，1958 年公开发表时采用了'光刻'这个名字"
- 三星 2022 年 3 纳米 GAA：改用 3 nm process 条目核对通过
- AMD 2019 年小芯片：改用 Epyc 条目核对通过（第二代"Rome"）
- ANITA 1961：改用 Sumlock ANITA calculator 条目核对通过
- 精工 Astron 1969：改用 Quartz clock 条目核对通过
- 阿德勒 1956 年超声波遥控：改用 Remote control 条目核对通过（Space Command）
- 费舍尔 1908 年 Thor 洗衣机：维基百科记载费舍尔专利 1910 年获批，Thor 品牌 1908 年由赫尔利机器公司推出（以公司史料为准），正文保留"1908 年推出"
- 原晶体管条目中"每年生产的晶体管数超过地球上沙粒总数"一说未找到可靠出处 → 删除

**已核对通过的说法（括号内为维基百科条目名）：**

富兰克林 1752 风筝实验（Kite experiment）；富兰克林 1750 避雷针设想（Lightning rod）；汤姆孙 1897 电子（J. J. Thomson）；汤姆孙 1906 诺贝尔（J. J. Thomson）；奥斯特 1820（Hans Christian Ørsted）；斯特金 1824 电磁铁（William Sturgeon）；亨利 强力电磁铁（Joseph Henry）；亨利 1835 继电器（Relay）；法拉第 1831 电磁感应（Michael Faraday）；法拉第 圆盘发电机（Homopolar generator）；西门子 1866 自励发电机（Werner von Siemens）；法拉第 1821 电磁旋转（Electric motor）；雅可比 1834 柯尼斯堡（Moritz von Jacobi）；达文波特 1837 专利（Thomas Davenport (inventor)）；费拉里斯 1885 感应电机（Galileo Ferraris）；特斯拉 1887–1888 感应电机（Induction motor）；ZBD 1885 变压器（ZBD transformer）；斯坦利 1886 交流系统（William Stanley Jr.）；多利沃-多布罗沃尔斯基 三相（Mikhail Dolivo-Dobrovolsky）；达尔泽尔 1961 漏电保护（Residual-current device）；列宁 1920 电气化（GOELRO plan）；1936 农村电气化法（Rural Electrification Act）；贝尔实验室 1956 晶闸管 通用电气（Thyristor）；巴利加 IGBT（B. Jayant Baliga）；IGBT 1982（Insulated-gate bipolar transistor）；特斯拉 Model 3 碳化硅（Silicon carbide）；霍尔特 Apple II 开关电源（Rod Holt）；弗莱明 1904 真空二极管（John Ambrose Fleming）；德福雷斯特 1906 Audion（Audion）；1915 横跨大陆长途电话（First transcontinental telephone call）；莱顿瓶 1745（Leyden jar）；欧姆 1827（Ohm's law）；布莱克 1927 8 月 渡轮（Harold Stephen Black）；拉加齐尼 1947 运算放大器（Operational amplifier）；μA741 1968（Operational amplifier）；卡迪 1921 石英振荡器（Crystal oscillator）；马里森 1927 石英钟（Warren Marrison）；艾斯勒 1936 PCB（Paul Eisler）；近炸引信 PCB（Printed circuit board）；布劳恩 1874 整流（Karl Ferdinand Braun）；巴丁 布拉顿 1947 12 月 点接触（History of the transistor）；肖克利 1948 结型（History of the transistor）；1956 诺贝尔 晶体管（John Bardeen）；八叛徒 仙童（Traitorous eight）；阿塔拉 姜大元 1959 MOSFET（MOSFET）；MOSFET 1960 发表（Mohamed M. Atalla）；万拉斯 萨支唐 1963 CMOS（CMOS）；基尔比 1958 9 月 集成电路（Jack Kilby）；诺伊斯 1959 单片集成（Robert Noyce）；基尔比 2000 诺贝尔（Jack Kilby）；诺伊斯 1990 去世（Robert Noyce）；赫尔尼 1959 平面工艺（Jean Hoerni）；摩尔 1965 电子学杂志（Moore's law）；摩尔 1975 修正 两年（Moore's law）；米德 推广 摩尔定律 名字（Moore's law）；登纳德 1974（Dennard scaling）；登纳德 DRAM（Robert H. Dennard）；登纳德缩放 约 2005 失效（Dennard scaling）；A17 Pro 190 亿（Apple A17）；丘克拉斯基 1916（Jan Czochralski）；EUV 2019 量产（Extreme ultraviolet lithography）；惠特菲尔德 层流洁净室（Willis Whitfield）；松托拉 1974 ALD（Tuomo Suntola）；胡正明 1999 FinFET（Fin field-effect transistor）；英特尔 2011 22 纳米 三栅（Fin field-effect transistor）；张忠谋 1987 台积电（TSMC）；SPICE 1973（SPICE）；米德 康威 1979（Mead–Conway VLSI chip design revolution）；UCIe 2022（UCIe）；芯片与科学法案 2022 8 月（CHIPS and Science Act）；2022 10 月 出口管制（United States New Export Controls on Advanced Computing and Semiconductors to China）；奈奎斯特 1928（Nyquist–Shannon sampling theorem）；香农 1949 采样（Nyquist–Shannon sampling theorem）；里夫斯 1937 PCM（Alec Reeves）；赛灵思 1985 XC2064（Xilinx）；弗里曼 FPGA（Ross Freeman）；AMD 2022 收购赛灵思（Xilinx）；谷歌 2016 TPU（Tensor Processing Unit）；比特币 ASIC 2013（Bitcoin network）；布劳恩 1897 阴极射线管（Cathode-ray tube）；泰克 511 1947（Tektronix）；海尔迈耶 1968 LCD（George H. Heilmeier）；夏普 1973 液晶计算器（Liquid-crystal display）；何伦亚克 1962 LED（Nick Holonyak）；赤崎勇 天野浩 中村修二 2014（Shuji Nakamura）；邓青云 范斯莱克 1987 OLED（Ching W. Tang）；江红星 2000 MicroLED（MicroLED）；约翰逊 1965 电容触摸屏（Touchscreen）；雅各布森 1997 E Ink（E Ink）；Kindle 2007（Amazon Kindle）；博伊尔 史密斯 1969 CCD（Charge-coupled device）；CCD 2009 诺贝尔（Willard Boyle）；福萨姆 CMOS 传感器（Eric Fossum）；亚德诺 1991 加速度计（Analog Devices）；霍尔 1879（Hall effect）；居里兄弟 1880（Piezoelectricity）；朗之万 声呐（Paul Langevin）；塞贝克 1821（Thomas Johann Seebeck）；帕尔帖 1834（Jean Charles Athanase Peltier）；斯潘塞 1945 微波炉（Percy Spencer）；1947 首台商用微波炉 1.8 米（Microwave oven）；兰德尔 布特 1940 2 月 磁控管（Cavity magnetron）；Regency TR-1 1954 10 月（Regency TR-1）；TR-55 1955 索尼 1958（Sony）；Cal Tech 1967（Calculator）；Busicom 1969 4004（Intel 4004）；Fitbit 2009（Fitbit）；Apple Watch 2015（Apple Watch）；Arduino 2005 伊夫雷亚 班齐（Arduino）；树莓派 2012 35 美元（Raspberry Pi）；WPC 2008 Qi 2010（Qi (standard)）；Qi2 2023（Qi (standard)）；真力时 1950 有线遥控（Remote control）；波利 1955 Flash-Matic（Eugene Polley）；GE Monitor-Top 1927（Refrigerator）；布斯 1901 吸尘器（Hubert Cecil Booth）；斯潘格勒 1907 胡佛（James Murray Spangler）；西屋 1971 电磁炉（Induction cooking）；东芝 1955 电饭锅（Rice cooker）；约翰逊 1883 恒温器（Warren S. Johnson）；布茨 1885（Albert Butz）；Nest 2011（Google Nest）；布莱克 专利 1937（Negative-feedback amplifier）；奥尔 1940 PN 结（P–n junction）；奥尔 1940 太阳能电池（Solar cell）；拉斯罗普 纳尔 1957 光刻（Photolithography）；三星 2022 3 纳米 GAA（3 nm process）；AMD 2019 霄龙 小芯片（Epyc）；ANITA 1961（Sumlock ANITA calculator）；精工 Astron 1969 12 月（Quartz clock）；阿德勒 1956 超声波遥控（Remote control）。

## 三、收词范围的对照来源

- 维基百科"重要条目"（Vital Articles）第 4、5 级"技术"与"物理科学"下的相关子页面，逐条与本篇词条清单比对。
- 维基百科"历史发明年表"（Timeline of historic inventions）1700 年以后的相关条目。
- IEEE 电子与电气工程里程碑（IEEE Milestones）清单，用于补齐电力与电子元件类词条。

## 四、延伸阅读（未作为核对依据）

- 查尔斯·佩措尔德，《编码》——从电报、继电器讲到逻辑门和 CPU。
- 保罗·霍洛维茨、温菲尔德·希尔，《电子学的艺术》（The Art of Electronics）——实用电子电路的经典。
- 克里斯·米勒，《芯片战争》——半导体产业与地缘政治。
- 迈克尔·里奥丹、莉莲·霍德森，《晶体之火》（Crystal Fire）——晶体管的发明史。
