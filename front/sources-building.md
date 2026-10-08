# 本篇资料来源与核实记录

**一句话：本篇的年份、人物和关键数字都至少对照过一个公开来源；"谁最先发明"有争议的地方（喷淋头、自动扶梯）按维基百科和专利记录写成"早期实用的"。**

## 一、按原始来源核对的最新数据

| 正文中的说法 | 来源（访问于 2026 年 10 月） |
|---|---|
| 2022 年土耳其恰纳卡莱 1915 大桥建成，主跨 2023 米，为世界最大跨度悬索桥 | en.wikipedia.org/wiki/1915_Çanakkale_Bridge |
| 有限元：1956 年特纳等人论文，1960 年克劳夫提出 "finite element" 一词 | en.wikipedia.org/wiki/Ray_W._Clough ；en.wikipedia.org/wiki/Finite_element_method |

## 二、批量核对（年份与人物）

方法：用脚本 `tools/factcheck.py` 读取英文维基百科对应条目的全文，检查正文中的年份或关键词是否出现在相应上下文中；未通过的换用其他条目复核，或查找机构官网、原始论文和权威媒体，逐条人工处理。本篇共核对 63 项（含复核项），脚本通过 60 项；其余均已人工处理，见下。原始结果保存在 `research/factcheck/` 下的 `building.result.tsv` 及共享复核文件中。

**未通过项的处理：**

- Parmelee 1874 喷淋头：Fire sprinkler system 条目称其为"第二种"自动喷淋头 → 改用 Henry S. Parmelee 条目核对 1874 年通过；正文改为"发明了早期实用的自动喷水灭火喷头，用来保护他的钢琴厂"
- 有限元 Turner/Clough 1956：Finite element method 条目未写人名 → 改用 Ray W. Clough 条目核对 1956 年与 1960 年通过
- 自动扶梯：雷诺 1896 年在科尼岛、奥的斯 1900 年在巴黎世博会，均核对通过；正文据此修正了早先的年份
- 地理信息系统：CGIS "1963" 未在维基百科正文找到 → 正文改为"1960 年代"，并用 Roger Tomlinson 条目核对通过

**已核对通过的说法（括号内为维基百科条目名）：**

Aspdin Portland cement 1824（Portland cement）；Monier reinforced concrete 1867（Joseph Monier）；Hennebique 1892（François Hennebique）；Freyssinet prestressed 1928（Eugène Freyssinet）；Home Insurance Building 1885 Jenney（Home Insurance Building）；Empire State Building 1931（Empire State Building）；Burj Khalifa 828 m（Burj Khalifa）；Burj Khalifa 2010（Burj Khalifa）；Taipei 101 damper 660 tonnes（Taipei 101）；Otis safety elevator 1854（Elisha Otis）；Otis first passenger elevator 1857（Elisha Otis）；Siemens electric elevator 1880（Elevator）；Lever House 1952（Lever House）；Seagram Building 1958（Seagram Building）；Crystal Palace 1851（The Crystal Palace）；Brooklyn Bridge 1883（Brooklyn Bridge）；Tacoma Narrows 1940（Tacoma Narrows Bridge (1940)）；1915 Çanakkale Bridge 2023 m（1915 Çanakkale Bridge）；Brunel shield 1818（Tunnelling shield）；Thames Tunnel 1843（Thames Tunnel）；Gotthard Base Tunnel 2016 57 km（Gotthard Base Tunnel）；Hoover Dam 1936（Hoover Dam）；Three Gorges 22,500 MW（Three Gorges Dam）；Delta Works 1953 flood（Delta Works）；Maeslantkering 1997（Maeslantkering）；Thames Barrier 1982（Thames Barrier）；Channel Tunnel 1994（Channel Tunnel）；Øresund Bridge 2000（Øresund Bridge）；HZMB 2018（Hong Kong–Zhuhai–Macau Bridge）；Afsluitdijk 1932（Afsluitdijk）；Kansai airport 1994（Kansai International Airport）；Snow cholera 1854（John Snow）；Great Stink 1858（Great Stink）；Bazalgette sewers（Joseph Bazalgette）；Cumming S-trap 1775（Alexander Cumming）；Bramah 1778（Joseph Bramah）；Grinnell 1881（Fire sprinkler system）；Passivhaus 1990/1991 Darmstadt（Passive house）；LEED 1998（Leadership in Energy and Environmental Design）；Haussmann renovation 1853（Haussmann's renovation of Paris）；Jacobs 1961 Death and Life（The Death and Life of Great American Cities）；Sponge city 2015（Sponge city）；Smoke detector 1965 Pearsall（Smoke detector）；Esri 1969（Esri）；Clough coined FEM 1960（Finite element method）；Liebherr tower crane 1949（Liebherr Group）；William Otis steam shovel 1839（William Otis）；Iron Bridge 1779（The Iron Bridge）；Escalator Reno 1896（Escalator）；Lockport water filtration（Water purification）；Parmelee 1874（Henry S. Parmelee）；Turner Clough 1956（Ray W. Clough）；Clough coined finite element 1960（Ray W. Clough）；Reno escalator 1896 Coney Island（Escalator）；Otis escalator 1900 Paris（Escalator）；smoke detector 1965 Pearsall（Smoke detector）；GIS Tomlinson 1963（Geographic information system）；FEM Turner 1956 Clough 1960（Finite element method）；CGIS Tomlinson 1960s（Roger Tomlinson）。

## 三、收词范围的对照来源

- 维基百科"重要条目"（Vital Articles）第 4 级"技术"与第 5 级"技术"下各子页面（共 3306 个条目名），逐条与本书词条清单比对，补入 9 个遗漏词条：有限元分析、地基与深基础、大跨度空间结构、自动扶梯、铸铁桥与桁架桥、填海造地与疏浚、雨洪管理与海绵城市、烟雾报警器、地理信息系统。
- 维基百科"历史发明年表"（Timeline of historic inventions）1700 年以后的条目。

## 四、延伸阅读（未作为核对依据）

- J. E. 戈登，《结构是什么》（Structures: Or Why Things Don't Fall Down）——最好懂的结构力学入门。
- 马里奥·萨尔瓦多里，《建筑为什么站得住》。
- 简·雅各布斯，《美国大城市的死与生》。
- 爱德华·格莱泽，《城市的胜利》。
