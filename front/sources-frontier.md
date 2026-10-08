# 本篇资料来源与核实记录

**一句话：本篇的年份、人物和关键数字都至少对照过一个公开来源；量子计算等领域的纪录变化很快，正文的"最新"数字截至 2026 年 10 月，读者应以官方最新发布为准。**

## 一、按原始来源核对的最新数据

| 正文中的说法 | 来源（访问于 2026 年 10 月） |
|---|---|
| 2024 年 12 月谷歌 Willow 芯片首次演示"低于阈值"的量子纠错 | blog.google 2024 年 12 月 9 日；《自然》2024 年论文；en.wikipedia.org/wiki/Willow_processor |
| 2024 年 8 月 NIST 发布首批三项后量子密码标准（ML-KEM、ML-DSA、SLH-DSA） | nist.gov 新闻稿 2024 年 8 月 13 日（FIPS 203/204/205） |
| 2025 年诺贝尔物理学奖授予克拉克、德沃雷、马蒂尼斯，表彰电路中的宏观量子隧穿和能量量子化 | nobelprize.org/prizes/physics/2025/summary/ |
| 2025 年诺贝尔化学奖授予北川进、罗布森、亚吉，表彰金属有机框架 | nobelprize.org/prizes/chemistry/2025/summary/ |
| 2025 年 2 月 19 日微软发布 Majorana 1（称片上 8 个拓扑量子比特）；《自然》同期论文的审稿材料中编辑部写明结果“不构成马约拉纳零能模存在的证据”，学界仍有争议 | 微软 Azure Quantum 博客 2025-02-19；Nature 638, 651 (2025) 及同刊审稿记录；APS Physics 2025 年报道 physics.aps.org/articles/v18/57 （终校时核对） |
| 2023 年阿秒光脉冲获诺贝尔物理学奖；2023 年量子点获诺贝尔化学奖 | nobelprize.org/prizes/physics/2023/ ；/chemistry/2023/ |

## 二、批量核对（年份与人物）

方法：用脚本 `tools/factcheck.py` 读取英文维基百科对应条目的全文，检查正文中的年份或关键词是否出现在相应上下文中；未通过的换用其他条目复核，或查找机构官网、原始论文和权威媒体，逐条人工处理。本篇共核对 94 项（含复核项），脚本通过 77 项；其余均已人工处理，见下。原始结果保存在 `research/factcheck/` 下的 `frontier.result.tsv`、`frontier2.result.tsv` 及共享复核文件中。

**未通过项的处理：**

- 费曼 1981 年提出量子模拟：Quantum computing 条目匹配失败 → 改用 Richard Feynman 条目核对通过（1981 年演讲，1982 年发表）
- 格赖纳 2002 年光晶格超流–莫特绝缘体相变：维基百科未在同一句写出 → 以 2002 年《自然》论文（Greiner 等）为准，保留
- 机器人科学家 Adam 2009：维基百科条目未匹配 → 阿伯里斯特威斯大学 2009 年 4 月新闻稿与《科学》2009 年论文确认
- 利物浦大学移动机器人化学家 8 天 688 次实验：无英文条目 → 《自然》2020 年论文（Burger 等）与利物浦大学新闻稿确认
- 斯托达特 1991 年轮烷、费林加 1999 年分子马达：Molecular machine 条目核对 1991 年通过；费林加 1999 年以《自然》论文为准；2016 年诺贝尔化学奖由 nobelprize.org 确认
- MOF-5 1999、本多–藤岛 1972、拓扑相 2016 年诺贝尔奖：分别改用 Metal–organic framework、Photocatalysis、David J. Thouless 条目复核通过
- 阿秒脉冲 2001 年、2025 年诺贝尔物理学奖：首轮未通过 → 改用 Attosecond、John M. Martinis 条目核对通过

**已核对通过的说法（括号内为维基百科条目名）：**

Deutsch 1985（David Deutsch）；Shor 1994（Shor's algorithm）；IBM factored 15 2001（Shor's algorithm）；Google Sycamore 2019 53 qubits（Sycamore processor）；Sycamore 200 seconds 10000 years（Quantum supremacy）；Jiuzhang 2020（Jiuzhang (quantum computer)）；Willow December 2024（Willow processor）；Nobel 2025 physics Clarke Devoret Martinis（John M. Martinis）；Schumacher qubit term（Qubit）；Shor 1995 error correction（Quantum error correction）；Kitaev 1997 surface code（Toric code）；Microsoft Majorana 2025（Majorana 1）；BB84 1984（BB84）；Micius 2016（Micius (satellite)）；Micius QKD 2017（Micius (satellite)）；Beijing Shanghai QKD 2017（Quantum key distribution）；NIST PQC 2016（Post-quantum cryptography）；NIST FIPS 203 August 2024（Post-quantum cryptography）；Feynman 1982 Simulating Physics（Quantum simulator）；Onnes 1911（Heike Kamerlingh Onnes）；Meissner 1933（Meissner effect）；BCS 1957（BCS theory）；BCS Nobel 1972（BCS theory）；Lawrence cyclotron 1931（Cyclotron）；Cockcroft Walton 1932（Cockcroft–Walton generator）；Higgs 2012（Higgs boson）；LHC 27 km（Large Hadron Collider）；Synchrotron light 1947 GE（Synchrotron radiation）；SSRF 2009（Shanghai Synchrotron Radiation Facility）；GW150914 14 September 2015（First observation of gravitational waves）；LIGO Nobel 2017（LIGO）；LIGO 4 km（LIGO）；Bednorz Müller 1986（High-temperature superconductivity）；YBCO 1987 93 K（Yttrium barium copper oxide）；Laser cooling Nobel 1997（Laser cooling）；BEC 1995（Bose–Einstein condensate）；BEC Nobel 2001（Bose–Einstein condensate）；CPA 1985 Mourou Strickland（Chirped pulse amplification）；CPA Nobel 2018（Chirped pulse amplification）；Attosecond Nobel 2023（Anne L'Huillier）；Carver Mead neuromorphic（Neuromorphic computing）；TrueNorth 2014（TrueNorth）；Loihi 2017（Cognitive computer）；GMR 1988（Giant magnetoresistance）；GMR Nobel 2007（Giant magnetoresistance）；IBM GMR head 1997（Giant magnetoresistance）；Freescale MRAM 2006（Magnetoresistive RAM）；Ekimov 1981 quantum dots（Alexey Ekimov）；Quantum dot Nobel 2023（Quantum dot）；Bawendi 1993（Moungi Bawendi）；Church DNA storage 2012（DNA digital data storage）；215 petabytes per gram（DNA digital data storage）；Frontier exascale 2022（Frontier (supercomputer)）；Sauvage catenane 1983（Jean-Pierre Sauvage）；Molecular machines Nobel 2016（Molecular machine）；Chua memristor 1971（Memristor）；HP memristor 2008（Memristor）；MOF Nobel 2025（Omar M. Yaghi）；QAHE 2013 Xue（Quantum anomalous Hall effect）；Domen 100 m2 2021（Photocatalytic water splitting）；Feynman 1981（Richard Feynman）；Stoddart 1991（Molecular machine）；MOF-5 1999（Metal–organic framework）；Honda-Fujishima 1972（Photocatalysis）；Thouless 2016（David J. Thouless）；High-Tc 1986 Bednorz Muller（High-temperature superconductivity）；BEC 1995 Cornell Wieman（Bose–Einstein condensate）；CPA 1985 Strickland Mourou（Chirped pulse amplification）；Chua 1971 memristor（Memristor）；MOF Nobel 2025（Metal–organic framework）；MOF-5 1999 Yaghi（Metal–organic framework）；Feynman 1982 quantum simulation（Quantum simulator）；attosecond 2001 pulse（Attosecond）；attosecond Nobel 2023（Pierre Agostini）；Martinis Nobel 2025（John M. Martinis）；Google Willow 2024（Willow processor）。

## 三、收词范围的对照来源

- 维基百科"重要条目"（Vital Articles）第 4 级"技术"与第 5 级"技术"下各子页面（共 3306 个条目名），逐条与本书词条清单比对，补入 8 个遗漏词条：量子模拟、高温超导、激光冷却与冷原子、超快激光与阿秒脉冲、忆阻器与存内计算、金属有机框架、拓扑材料、人工光合作用。
- 2016–2025 年诺贝尔物理学奖、化学奖获奖主题，逐年检查是否已有对应词条。

## 四、延伸阅读（未作为核对依据）

- 迈克尔·尼尔森、艾萨克·庄，《量子计算与量子信息》——标准教材，前两章适合入门。
- 斯科特·阿伦森，《德谟克利特以来的量子计算》。
- 曹天元，《上帝掷骰子吗？》——量子力学通俗史。
- 国家标准与技术研究院（NIST）后量子密码项目主页。
