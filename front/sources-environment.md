# 本篇资料来源与核实记录

**一句话：本篇的年份、人物和关键数字都至少对照过一个公开来源；气候数据只引用 IPCC、IEA 等机构的原始报告，且标明年份，读者应以最新报告为准。**

## 一、按原始来源核对的最新数据

| 正文中的说法 | 来源（访问于 2026 年 10 月） |
|---|---|
| IPCC 第六次评估报告（2021–2023）：人类活动使气候变暖"毋庸置疑"；全球长期升温约 1.3–1.4 °C，2024 年单年首次超过 1.5 °C | ipcc.ch/report/ar6/syr/ ；WMO《2024 年全球气候状况》（2024 年 1.55 ± 0.13 °C）与《2025 年全球气候状况》（2025 年 1.43 ± 0.13 °C） |
| 大气 CO₂ 浓度已超过 420 ppm | NOAA 莫纳罗亚观测站：gml.noaa.gov/ccgg/trends/ |
| 2025 年全球电动汽车销量超过 2000 万辆、约占新车四分之一；中国新车中近 55% 是电动车 | IEA《Global EV Outlook 2026》执行摘要：iea.org/reports/global-ev-outlook-2026/executive-summary （终校时核对；初稿引用的是 2025 版的 2024 年数据“约 1700 万辆”，为与第 8 篇统一改用最新版） |
| 欧盟要求 2025 年起航油掺混可持续航空燃料（2%）并逐年提高 | 欧盟 ReFuelEU Aviation 条例（EU）2023/2405 |
| 2023 年起谷歌（GraphCast）、华为（盘古气象）等 AI 天气模型在部分指标上追上传统数值模式 | 《科学》2023 年 GraphCast 论文；《自然》2023 年 Pangu-Weather 论文 |

## 二、批量核对（年份与人物）

方法：用脚本 `tools/factcheck.py` 读取英文维基百科对应条目的全文，检查正文中的年份或关键词是否出现在相应上下文中；未通过的换用其他条目复核，或查找机构官网、原始论文和权威媒体，逐条人工处理。本篇共核对 79 项（含复核项），脚本通过 71 项；其余均已人工处理，见下。原始结果保存在 `research/factcheck/` 下的 `environment.result.tsv` 及共享复核文件中。

**未通过项的处理：**

- 太平洋海啸预警中心：维基百科写 1948 年开始运作，NOAA 写 1949 年建立 → 正文改为"20 世纪 40 年代末美国在夏威夷建立海啸预警系统"（Tsunami warning system 条目复核通过）
- 卫生填埋：最早实践的年份说法不一 → 正文写"20 世纪 30–40 年代"，Sanitary landfill 条目核对弗雷斯诺 1937 年通过
- 《基加利修正案》2016：Kigali Amendment 条目匹配失败 → 改用 Montreal Protocol 条目核对通过
- HYBRIT 2021 首批无化石钢、中国 2018 年禁止进口洋垃圾：无单独英文条目 → 分别用 SSAB、China's waste import ban 条目核对通过
- 埃克森·瓦尔迪兹号漏油后的生物修复（施肥促进细菌降解）：维基百科相关条目未写出 → 美国 EPA 与《自然》1994 年报道确认，保留
- 可口可乐 1969 年委托的包装生命周期评估：维基百科 Life-cycle assessment 条目未写出 → 为 LCA 史文献中的公认首例（Midwest Research Institute 研究），保留

**已核对通过的说法（括号内为维基百科条目名）：**

Fourier 1824 greenhouse（Joseph Fourier）；Foote 1856（Eunice Newton Foote）；Tyndall 1859 infrared（John Tyndall）；Arrhenius 1896（Svante Arrhenius）；Earth without greenhouse -18（Greenhouse effect）；Keeling 1958 Mauna Loa（Keeling Curve）；Keeling 315 ppm（Keeling Curve）；Manabe Wetherald 1967（Syukuro Manabe）；Manabe Nobel 2021（Syukuro Manabe）；ISO 14040（Life-cycle assessment）；Richardson 1922（Lewis Fry Richardson）；ENIAC forecast 1950（Numerical weather prediction）；Dansgaard ice core（Willi Dansgaard）；EPICA 800000 years（European Project for Ice Coring in Antarctica）；Argo 2000（Argo (oceanography)）；Argo 3000 floats 2007（Argo (oceanography)）；Argo 2000 m depth（Argo (oceanography)）；GOSAT 2009（Greenhouse Gases Observing Satellite）；OCO-2 2014（Orbiting Carbon Observatory 2）；TROPOMI 2017（Sentinel-5 Precursor）；IPCC 1988（Intergovernmental Panel on Climate Change）；IPCC Nobel 2007（Intergovernmental Panel on Climate Change）；AR6 unequivocal（IPCC Sixth Assessment Report）；Indian Ocean tsunami 2004 deaths（2004 Indian Ocean earthquake and tsunami）；Indian Ocean warning 2006（Indian Ocean Tsunami Warning System）；Bhola cyclone 1970（1970 Bhola cyclone）；Paris Agreement 2015（Paris Agreement）；China 2060 neutrality（Carbon neutrality）；Finland carbon tax 1990（Carbon tax）；EU ETS 2005（European Union Emissions Trading System）；China national ETS 2021（Chinese national carbon trading scheme）；Acid Rain Program SO2 trading（Emissions trading）；Sleipner 1996（Sleipner gas field）；Val Verde 1972 EOR（Carbon capture and storage）；Orca 2021 4000 t（Climeworks）；Virgin Atlantic biofuel 2008（Aviation biofuel）；SAF blend 50%（Sustainable aviation fuel）；Cottrell 1907（Frederick Gardner Cottrell）；Battersea FGD（Flue-gas desulfurization）；Catalytic converter 1975（Catalytic converter）；Houdry catalytic converter（Eugene Houdry）；Midgley tetraethyllead 1921（Thomas Midgley Jr.）；Patterson lead（Clair Cameron Patterson）；Leaded gasoline ended 2021 Algeria（Tetraethyllead）；Molina Rowland 1974（Mario J. Molina）；Ozone hole 1985 Farman（Ozone depletion）；Montreal Protocol 1987（Montreal Protocol）；Montreal universal ratification（Montreal Protocol）；Activated sludge 1914 Ardern Lockett（Activated sludge）；Loeb Sourirajan reverse osmosis（Sidney Loeb）；Lake Erie phosphorus（Lake Erie）；Taihu algae 2007（Lake Tai）；HEPA Manhattan Project（HEPA）；HEPA 99.97% 0.3 µm（HEPA）；SCR Japan 1970s（Selective catalytic reduction）；Volkswagen emissions 2015（Volkswagen emissions scandal）；US embassy Beijing air（Air pollution in China）；Aluminium recycling 5%（Aluminium recycling）；9% plastic recycled（Plastic recycling）；Thompson microplastics 2004（Microplastics）；Nottingham destructor 1874（Incineration）；Pinatubo 0.5 °C（Mount Pinatubo）；Crutzen 2006 geoengineering（Paul J. Crutzen）；Kigali 2016（Montreal Protocol）；HYBRIT 2021（SSAB）；China waste ban 2018（China's waste import ban）；PTWC 1949（Tsunami warning system）；Fresno sanitary landfill 1937（Sanitary landfill）。

## 三、收词范围的对照来源

- 维基百科"重要条目"（Vital Articles）第 4 级"技术"与第 5 级"技术"下各子页面（共 3306 个条目名），逐条与本书词条清单比对，补入 10 个遗漏词条：冰芯与古气候、Argo 浮标与海洋观测、温室气体与甲烷监测、IPCC 气候评估、灾害预警系统、碳移除、烟气脱硝、空气质量监测、环境修复与生物修复、卫生填埋；"温室效应"升为 A 级并配全页图。
- 维基百科"历史发明年表"（Timeline of historic inventions）1700 年以后的条目。
- IPCC 第六次评估报告第三工作组（减缓）的技术分类。

## 四、延伸阅读（未作为核对依据）

- 蕾切尔·卡森，《寂静的春天》。
- 比尔·盖茨，《气候经济与人类未来》——按排放部门梳理减排技术。
- 戴维·麦凯，《可持续能源：事实与真相》（作者公开免费提供）。
- IPCC 第六次评估报告《决策者摘要》（官网有中文版）。
