# 本篇资料来源与核实记录

**一句话：本篇所有年份、人物和关键数字都至少对照过一个公开来源；2023–2026 年的最新进展直接引用监管机构、学术期刊或原始报道。本篇只介绍技术原理和历史，不构成医疗建议。**

## 一、按原始来源核对的最新数据

| 正文中的说法 | 来源（访问于 2026 年 10 月） |
|---|---|
| 过去 50 年全球免疫规划至少挽救了 1.54 亿人的生命 | 世界卫生组织 2024 年 4 月新闻稿；Shattock et al., *The Lancet* 2024；en.wikipedia.org/wiki/Vaccination |
| 野生脊灰病毒仅在巴基斯坦和阿富汗传播 | WHO 东地中海区域《EMR Polio Bulletin》第 1461 期（截至 2026 年 10 月 4 日：阿富汗 35 例、巴基斯坦 5 例）；脊灰《国际卫生条例》突发事件委员会第 45 次会议声明（2026-08-25） |
| 2019 年全球约 127 万人直接死于细菌耐药 | GRAM 研究，*The Lancet* 2022；en.wikipedia.org/wiki/Antimicrobial_resistance |
| 2025 年美国批准每年只需注射两次的 HIV 暴露前预防药 | 美国 FDA 2025 年 6 月 18 日批准来那卡帕韦（Yeztugo）：accessdata.fda.gov 批准函 NDA 220020；吉利德新闻稿；路透社 2025-06-18 |
| 2025 年为单个患儿定制的碱基编辑疗法 | Musunuru et al., “Patient-Specific In Vivo Gene Editing to Treat a Rare Genetic Disease”, *NEJM* 2025（CPS1 缺乏症患儿 KJ）；宾夕法尼亚大学医学院新闻稿 |
| 2023 年英美批准首个 CRISPR 疗法（Casgevy） | 英国 MHRA 2023-11-16、美国 FDA 2023-12-08；en.wikipedia.org/wiki/Exagamglogene_autotemcel |
| 人类基因组最后约 8% 的空缺在 2022 年补齐 | Nurk et al., *Science* 2022（T2T 联盟） |
| 测一个人类基因组：2001 年约 1 亿美元 → 2022 年约 500 美元（图中曲线） | 美国国家人类基因组研究所（NHGRI）“DNA Sequencing Costs: Data”数据表（genome.gov，2022 年 5 月版：2001 年 9 月 9,526 万美元，2022 年 5 月 525 美元） |
| 2024 年起 Neuralink 等公司开展脑机接口人体试验 | Neuralink 2024 年 1 月首例植入的公开报道；en.wikipedia.org/wiki/Neuralink |
| AlphaFold 2020 年达到接近实验的精度，2024 年诺贝尔化学奖 | CASP14 结果；nobelprize.org 2024 年化学奖公告 |
| 全球已植入超过一百万个人工耳蜗 | 美国国家耳聋与其他交流障碍研究所（NIDCD）“Quick Statistics About Hearing”（引 Zeng 2022：截至 2022 年 7 月全球超过 100 万个） |
| 全球约 1200 万人经辅助生殖技术出生（正文写“超过一千万”） | en.wikipedia.org/wiki/In_vitro_fertilisation（引 2023 年估计：约 1200 万） |

## 二、批量核对（年份与人物）

方法：用脚本 `tools/factcheck.py` 读取英文维基百科对应条目的全文，检查正文中的年份或关键词是否出现在相应上下文中；未通过的逐条人工复核。三轮共核对 230 项，批量通过 206 项；未通过项均已人工处理，见下。原始结果保存在 `research/factcheck/biomed*.result.tsv`。

**未通过项的处理：**

- 劳特布尔 1973 年 MRI、爱因托芬 1903 年心电图、遗传密码 1966 年破译完成、肯德鲁 1958 年肌红蛋白、T2T 2022、曹培生驻极体滤材：首轮匹配窗口或条目名不对，第二轮改用正确条目后通过
- 宫颈涂片：早期草稿写 1943 年 → 帕帕尼古拉乌与特劳特 1941 年发表论文、1943 年出版专著，正文和收词表改为 1941 年
- 骨髓移植：早期草稿写 1957 年 → 托马斯最早的尝试在 1950 年代末，收词表年份改为 1958 年，正文写“20 世纪 50 年代末”
- PET 1975 年、氮芥化疗 1946 年：维基百科正文没有对应的完整句子，人工按 Ter-Pogossian、Phelps 等 1975 年论文和 Goodman、Gilman 1946 年发表的结果确认
- 第一款晶体管助听器 1952 年：人工核对 Sonotone 1010（1952 年 12 月 29 日上市，电子管与晶体管混合），保留
- 潘特里奇：早期草稿写 1966 年 → 维基百科写 1965 年在贝尔法斯特救护车上装上首台便携除颤器，正文改为 1965 年
- 人工耳蜗：早期草稿写“约一百万人植入” → 统计口径是植入装置数（有人双耳植入），改为“全球已植入超过一百万个人工耳蜗”
- 胸片剂量：早期草稿写“约 0.1 毫希沃特” → 维基百科写正位约 0.02、侧位约 0.08 毫希沃特，正文与图改为“约 0.02–0.1 毫希沃特，不超过自然环境中十来天的本底辐射”
- 伍德与普拉瓦兹 1853 年注射器、范恩（John Vane）1971 年阿司匹林机理、科克伦 1972 年著作、伯格 1972 年重组 DNA、Taq 聚合酶 1988 年、脑类器官 2013 年、英克西兰每年两针：维基百科正文未写出对应年份或剂量，人工按原始论文或说明书确认，保留
- ECMO、BiVACOR 全人工心脏：表述无法在来源中精确对应，正文删去具体细节，只保留“心肺机的原理发展出 ECMO”

**已核对通过的说法（括号内为维基百科条目名）：**

詹纳 1796 牛痘（Edward Jenner）；天花 1980 宣布根除（Smallpox）；天花 1977 最后自然病例 索马里（Smallpox）；斯诺 1854 宽街水泵（1854 Broad Street cholera outbreak）；巴斯德 1864 巴氏消毒（Pasteurization）；科赫 1882 结核杆菌（Robert Koch）；科赫法则（Koch's postulates）；泽西城 1908 氯化（Water chlorination）；口服补液 1968 达卡（Oral rehydration therapy）；尚贝兰 高压灭菌器 1879（Autoclave）；N95 1995（N95 respirator）；沙利度胺 1962 修正案（Kefauver Harris Amendment）；莫顿 1846 乙醚（William T. G. Morton）；李斯特 1867 石炭酸（Joseph Lister）；塞麦尔维斯 洗手 1847（Ignaz Semmelweis）；兰德施泰纳 1901 血型（Karl Landsteiner）；1930 诺贝尔 兰德施泰纳（Karl Landsteiner）；吉本 1953 心肺机（John Heysham Gibbon）；科尔夫 1943 透析（Willem Johan Kolff）；1958 植入起搏器 瑞典（Artificial cardiac pacemaker）；默里 1954 双胞胎肾移植（Joseph Murray）；环孢素 1983 批准（Ciclosporin）；查恩利 1962 髋关节（John Charnley）；腹腔镜胆囊切除 1985 1987（Laparoscopy）；达芬奇 2000 FDA（Da Vinci Surgical System）；克拉克 1978 多通道耳蜗（Graeme Clark (doctor)）；BrainGate 2004（BrainGate）；德林克 1928 铁肺（Iron lung）；格吕恩齐格 1977 球囊（Andreas Gruentzig）；雷奈克 1816（René Laennec）；伦琴 1895（Wilhelm Röntgen）；伦琴 1901 首届诺贝尔物理学奖（Wilhelm Röntgen）；豪恩斯菲尔德 1971 CT（Godfrey Hounsfield）；CT 1979 诺贝尔 科马克（Allan MacLeod Cormack）；2003 诺贝尔 MRI 曼斯菲尔德（Peter Mansfield）；唐纳德 1956 产科超声（Ian Donald）；爱因托芬 1924 诺贝尔（Willem Einthoven）；伯格 1924 脑电（Hans Berger）；赫希奥维茨 光纤胃镜 1957（Basil Hirschowitz）；青柳卓雄 1972 血氧（Takuo Aoyagi）；侧流层析 验孕 1988（Lateral flow test）；CGM 1999 FDA（Continuous glucose monitor）；杰弗里斯 1984 DNA 指纹（Alec Jeffreys）；霍夫曼 1897 阿司匹林（Aspirin）；弗莱明 1928 青霉素（Alexander Fleming）；1945 诺贝尔 青霉素（Penicillin）；多马克 百浪多息 1935（Prontosil）；班廷 贝斯特 1922（Insulin (medication)）；1923 诺贝尔 胰岛素（Frederick Banting）；MRC 链霉素试验 1948（Randomized controlled trial）；避孕药 1960 FDA（Combined oral contraceptive pill）；放疗 1896（Radiation therapy）；洛伐他汀 1987（Lovastatin）；远藤章 他汀（Akira Endo (biochemist)）；HAART 1996（Management of HIV/AIDS）；何大一 鸡尾酒（David Ho）；克勒 米尔斯坦 1975 单抗（Monoclonal antibody）；1984 诺贝尔 单抗（César Milstein）；格列卫 2001（Imatinib）；伊匹木单抗 2011（Ipilimumab）；2018 诺贝尔 本庶佑 艾利森（Tasuku Honjo）；Kymriah 2017（Tisagenlecleucel）；卡里科 韦斯曼 2023 诺贝尔（Katalin Karikó）；BNT162b2 2020 12 月 英国（Pfizer–BioNTech COVID-19 vaccine）；艾塞那肽 2005（Exenatide）；司美格鲁肽 2017（Semaglutide）；屠呦呦 1972 2015（Tu Youyou）；DNA 1953 沃森 克里克（Nucleic acid double helix）；照片 51（Photo 51）；尼伦伯格 1961（Marshall Warren Nirenberg）；史密斯 1970 限制酶（Hamilton O. Smith）；科恩 博耶 1973（Recombinant DNA）；基因泰克 1976（Genentech）；重组胰岛素 1982 Humulin（Insulin (medication)）；穆利斯 1983 PCR（Kary Mullis）；1993 诺贝尔 PCR（Kary Mullis）；桑格 1977（Sanger sequencing）；人类基因组 2003（Human Genome Project）；454 2005（454 Life Sciences）；人类基因组测序成本（Whole genome sequencing）；杜德纳 卡彭蒂耶 2012（CRISPR gene editing）；2020 诺贝尔 CRISPR（Jennifer Doudna）；碱基编辑 2016 刘如谦（David R. Liu）；Casgevy 2023（Exagamglogene autotemcel）；基因治疗 1990 阿珊蒂（Gene therapy）；多莉 1996（Dolly (sheep)）；山中伸弥 2006（Shinya Yamanaka）；2012 诺贝尔 山中（Shinya Yamanaka）；类器官 2009 克莱弗斯（Organoid）；路易丝·布朗 1978（Louise Brown）；爱德华兹 2010 诺贝尔（Robert G. Edwards）；合成生物学 2000 拨动开关（Synthetic biology）；AlphaFold 2020 CASP14（AlphaFold）；2024 诺贝尔化学 哈萨比斯（Demis Hassabis）；冷冻电镜 2017 诺贝尔（Cryogenic electron microscopy）；人类微生物组计划 2007（Human Microbiome Project）；光遗传学 2005（Optogenetics）；索尔克 1955（Polio vaccine）；萨宾 口服 1961（Albert Sabin）；野生脊灰 巴基斯坦 阿富汗（Poliomyelitis eradication）；芬克 1912 维生素（Casimir Funk）；加碘盐 1924 美国（Iodised salt）；考温霍文 1960 胸外按压（Cardiopulmonary resuscitation）；1990 诺贝尔 托马斯（E. Donnall Thomas）；利奥塔 1969 人工心脏（Artificial heart）；贾维克-7 1982（Jarvik-7）；埃弗勒斯特 詹宁斯 1933（Wheelchair）；里德利 1949 人工晶体（Harold Ridley (ophthalmologist)）；LASIK 1990s（LASIK）；布伦马克 骨整合（Per-Ingvar Brånemark）；大急流城 1945 氟化（Water fluoridation）；库尔特 1953（Coulter counter）；里瓦-罗奇 1896（Scipione Riva-Rocci）；科罗特科夫 1905（Korotkov sounds）；奥尔巴特 1867 体温计（Thomas Clifford Allbutt）；盖亚特 1991 循证（Evidence-based medicine）；科克伦 1993（Cochrane (organisation)）；泽尔蒂纳 吗啡 1804（Morphine）；氯丙嗪 1952（Chlorpromazine）；氟西汀 1987（Fluoxetine）；HeLa 1951（HeLa）；法尔 梅洛 1998（RNA interference）；帕替司兰 2018（Patisiran）；阿诺德 1993 定向进化（Frances Arnold）；2018 诺贝尔 阿诺德（Frances Arnold）；劳特布尔 1973 MRI（Magnetic resonance imaging）；爱因托芬 1903 心电（Electrocardiography）；遗传密码 1966 完成（Har Gobind Khorana）；肯德鲁 1958 肌红蛋白（Myoglobin）；T2T 2022 完整（Human genome）；托马斯 骨髓移植（Hematopoietic stem cell transplantation）；青柳 1972 血氧（Pulse oximetry）；曹培生 驻极体（Peter Tsai）；伊莉莎白 Dr. 卡雷尔 培养（Cell culture）；WHO 疫苗 50 年 1.54 亿（Vaccination）；天花 20 世纪 3 亿人（Smallpox）；多尔 希尔 1950 吸烟（Richard Doll）；口服补液 1971 难民营（Oral rehydration therapy）；脊灰 1988 35 万例（Global Polio Eradication Initiative）；美国 911 1968（9-1-1）；凯尔西 沙利度胺（Frances Oldham Kelsey）；WHO 手术安全核查表 2008（WHO Surgical Safety Checklist）；Rh 血型 1940（Rh blood group system）；芝加哥 1937 血库（Blood bank）；科尔夫 1945 首位存活（Willem Johan Kolff）；斯克里布纳 1960 分流管（Belding Hibbard Scribner）；起搏器 拉松 活到 2001（Arne Larsson）；ICD 1980（Implantable cardioverter-defibrillator）；巴纳德 1967 心脏移植（Christiaan Barnard）；穆雷 1987 腹腔镜胆囊（Laparoscopy）；林德伯格手术 2001（Lindbergh operation）；易卜生 1952 哥本哈根（Bjørn Aage Ibsen）；兰格 瓦坎蒂 1993 组织工程（Tissue engineering）；阿塔拉 2006 膀胱（Anthony Atala）；库利 1969 全人工心脏（Denton Cooley）；贾维克-7 112 天（Jarvik-7）；胸片 0.1 mSv（Chest radiograph）；达马迪安 1977 全身 MRI（Raymond Damadian）；蒂塞利乌斯 1948 诺贝尔（Arne Tiselius）；链霉素 1943（Streptomycin）；磺胺酏剂 1937（Elixir sulfanilamide）；MRSA 1961（Methicillin-resistant Staphylococcus aureus）；耐药 2019 127 万（Antimicrobial resistance）；桑格 1955 胰岛素序列（Frederick Sanger）；林德 1747 坏血病（James Lind）；法伯 1948 叶酸拮抗剂（Sidney Farber）；齐多夫定 1987（Zidovudine）；来那卡帕韦 2025（Lenacapavir）；首个治疗性单抗 1986 OKT3（Muromonab-CD3）；曲妥珠单抗 1998（Trastuzumab）；帕替司兰 脂质纳米颗粒（Patisiran）；司美格鲁肽 2021 减重（Semaglutide）；523 项目 1967（Project 523）；阿西洛马 1975（Asilomar Conference on Recombinant DNA）；查克拉巴蒂 1980（Diamond v. Chakrabarty）；马克萨姆 吉尔伯特 1977（Maxam–Gilbert sequencing）；桑格 1980 第二次诺贝尔（Frederick Sanger）；人类基因组 1990 启动（Human Genome Project）；人类基因组 27 亿美元（Human Genome Project）；人类基因组 约 2 万个基因（Human genome）；人类基因组 中国 1%（Human Genome Project）；Solexa 2006（Illumina dye sequencing）；2013 迈利亚德 基因专利（Association for Molecular Pathology v. Myriad Genetics）；戴霍夫 图集 1965（Margaret Oakley Dayhoff）；GenBank 1982（GenBank）；BLAST 1990（BLAST (biotechnology)）；张锋 2013 人类细胞（Feng Zhang）；贺建奎 判刑 3 年（He Jiankui）；先导编辑 2019（Prime editing）；盖尔辛格 1999（Jesse Gelsinger）；Luxturna 2017（Voretigene neparvovec）；Zolgensma 2019（Onasemnogene abeparvovec）；格登 1962 蛙（John Gurdon）；多莉 277 次（Dolly (sheep)）；中中 华华 2018（Zhong Zhong and Hua Hua）；汤姆森 1998 人胚胎干细胞（James Thomson (cell biologist)）；ICSI 1992（Intracytoplasmic sperm injection）；辅助生殖 超过千万（In vitro fertilisation）；文特尔 2010 合成基因组（Mycoplasma laboratorium）；青霉素 深罐发酵 1943 辉瑞（Penicillin）；肯德鲁 佩鲁茨 1962（Max Perutz）；粪菌移植 Rebyota 2022（Fecal microbiota transplant）；光遗传 2021 盲人（Optogenetics）；HeLa 脊灰疫苗（HeLa）；法尔 梅洛 2006 诺贝尔（Andrew Fire）；阿诺德 有机溶剂 DMF（Frances Arnold）。

## 三、收词范围的对照来源

- 维基百科“重要条目”（Vital Articles）第 4 级“生物与健康科学”（Biology and health sciences）中的医学与生物技术部分，以及第 5 级的 Health、Biology 两节逐条比对。据此新增 18 条：脊髓灰质炎疫苗、维生素与食品强化、急救医疗体系、心肺复苏与 AED、造血干细胞移植、人工心脏与心室辅助装置、现代轮椅、人工晶体与激光矫视、现代牙科、血液检验与检验自动化、血压计与体温计、癌症筛查、循证医学、吗啡与阿片类药物、精神类药物、细胞培养与 HeLa 细胞、RNA 干扰与核酸药物、定向进化与蛋白质工程。
- 不单独立条的：具体疾病（癌症、糖尿病、艾滋病等，并入相应疗法词条）、解剖与生理学概念（属于基础科学而非技术）、单个药品品牌和医疗机构。
- 与其他篇的分工：转基因作物、精准发酵放在第 11 篇；AI 预测蛋白质结构放在第 5 篇；激光、电子显微镜、X 射线晶体学放在第 16 篇。

## 四、延伸阅读（未作为核对依据）

- 悉达多·穆克吉，《基因传》《众病之王：癌症传》——基因和癌症治疗史最好读的两本书。
- 罗伊·波特，《剑桥插图医学史》——从古代到现代医学的通史。
- 丽贝卡·斯克鲁特，《永生的海拉》——HeLa 细胞和知情同意的故事。
- 沃尔特·艾萨克森，《破解生命密码》——CRISPR 的发现和杜德纳的故事。
- 本·戈尔达克，《小心坏科学》——讲清随机对照试验和循证医学的入门书。
