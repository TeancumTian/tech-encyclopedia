# 本篇资料来源与核实记录

**一句话：本篇所有年份、人物和关键数字都至少对照过一个公开来源；最新数据（2024–2026 年）直接引用发布机构的原始页面。**

## 一、按原始来源核对的最新数据

| 正文中的说法 | 来源（访问于 2026 年 10 月） |
|---|---|
| 2026 年 6 月 TOP500 榜首为 LineShine，约 2.2 EFLOPS，纯 CPU 架构；Frontier 于 2022 年成为首台百亿亿次（E 级）超算 | TOP500 官网新闻与 2026 年 6 月榜单：top500.org/news/lineshine-debuts-no-1-top500-enters-new-global-exascale-era/ ；top500.org/lists/top500/2026/06/ |
| Unicode 18.0（2026 年 9 月）共 172,808 个字符 | Unicode 联盟：unicode.org/versions/latest/ （发布说明：“adds 13,007 characters, for a total of 172,808”） |
| 2024 年数据中心用电约 415 太瓦时、占全球 1.5%；2025 年增长约 17%；2030 年约 950 太瓦时、接近 3% | 国际能源署：iea.org/reports/energy-and-ai/executive-summary ；iea.org/reports/key-questions-on-energy-and-ai/executive-summary |
| Apple II 1977 年上市，起价 1298 美元 | en.wikipedia.org/wiki/Apple_II_(1977_computer) |
| Intel 4004：1971 年，约 2300 个晶体管，740 kHz，为 Busicom 计算器设计 | en.wikipedia.org/wiki/Intel_4004 |

## 二、批量核对（年份与人物）

方法：用脚本 `tools/factcheck.py` 读取英文维基百科对应条目的全文，检查正文中的年份或关键词是否出现在相应上下文中；未通过的逐条人工复核并修改正文。共核对 185 项（其中 15 项是对首轮未通过项换用其他条目的复核），通过 172 项；仍未通过的均已人工处理，见下。原始结果保存在 `research/factcheck/*.result.tsv`。

**首轮未通过项的处理：**

- Hennessy Patterson 2017 图灵奖：改用 David Patterson 条目核对通过
- Wilkes 1965 slave memory：维基百科正文未直接写出年份；1965 年论文《Slave Memories and Dynamic Storage Allocation》为公认出处，保留
- JavaScript 1995 Eich 10 天：改用 Brendan Eich 条目核对通过
- SEQUEL 1974：SQL 条目确认 SEQUEL 名称；1974 年见 Chamberlin 与 Boyce 的论文
- 开源 1998：改用 Open-source software / Open Source Initiative 条目核对通过
- 微服务 2011/2012：未找到可靠年份 → 正文改为“2010 年代前期开始被广泛使用”
- Lamport 1978 逻辑时钟：见上
- Doom 1993 引擎：改用 Doom (1993 video game) 与 Doom engine 条目核对通过
- McCarthy 1961 公用计算：改用 John McCarthy 条目核对通过
- Wilkes 1965 slave memory：维基百科正文未直接写出年份；1965 年论文《Slave Memories and Dynamic Storage Allocation》为公认出处，保留
- 微服务 2011/2012：未找到可靠年份 → 正文改为“2010 年代前期开始被广泛使用”
- Lamport 1978 paper：论文《Time, Clocks, and the Ordering of Events in a Distributed System》发表于 1978 年《ACM 通讯》，已在 Lamport timestamp 条目中核对到论文
- Unicode 17 字符数：维基百科已更新为 18.0 → 以 unicode.org 官方页面为准，正文改为 Unicode 18.0 的 172,808 个字符

**已核对通过的说法（括号内为维基百科条目名）：**

巴贝奇 1822 提出差分机（Difference engine）；1991 年科学博物馆建成差分机 2 号（Difference engine）；洛夫莱斯 1843 注释（Ada Lovelace）；霍勒瑞斯 1890 人口普查（Herman Hollerith）；雅卡尔 1804 织机（Jacquard machine）；图灵 1936 论文（Turing machine）；ENIAC 1945 完成/1946 公开（ENIAC）；巨人计算机 1943/44（Colossus computer）；冯·诺依曼 1945 EDVAC 报告（First Draft of a Report on the EDVAC）；S/360 1964 年 4 月发布（IBM System/360）；PDP-8 1965 售价约 1.8 万美元（PDP-8）；Altair 8800 1975（Altair 8800）；IBM PC 1981（IBM Personal Computer）；香农 1937 硕士论文布尔代数（A Symbolic Analysis of Relay and Switching Circuits）；Eccles–Jordan 触发器 1918（Flip-flop (electronics)）；4004 1971（Intel 4004）；8086 1978（Intel 8086）；IBM 801 Cocke（IBM 801）；ARM1 1985（ARM architecture family）；RISC-V 基金会 2015（RISC-V）；POWER4 2001 首款多核（POWER4）；GeForce 256 1999（GeForce 256）；CUDA 2007（CUDA）；Dennard 1966/1967 DRAM（Robert H. Dennard）；Intel 1103 1970（Intel 1103）；HBM JEDEC 2013（High Bandwidth Memory）；舛冈富士雄 闪存 1984 / NAND 1987（Flash memory）；IBM 350 RAMAC 1956（IBM 350）；软盘 1971 8 英寸（Floppy disk）；CD 1982（Compact disc）；蓝光 2006（Blu-ray）；USB 1996 Bhatt（USB）；Osborne 1 1981（Osborne 1）；GRiD Compass 1982（GRiD Compass）；Apollo 导航计算机（Apollo Guidance Computer）；CDC 6600 1964（CDC 6600）；Cray-1 1976 160 MFLOPS（Cray-1）；Frontier 2022 exascale（Frontier (supercomputer)）；欧几里得算法（Euclidean algorithm）；al-Khwarizmi 词源（Algorithm）；TAOCP 1968（The Art of Computer Programming）；Quicksort 霍尔 1959/1961（Quicksort）；归并排序 冯·诺依曼 1945（Merge sort）；Dijkstra 1956 构思 1959 发表 20 分钟（Dijkstra's algorithm）；贝尔曼 1950s 动态规划（Dynamic programming）；克莱尼 1951 正则（Regular expression）；Booth 1947 汇编（Assembly language）；霍珀 A-0 1952（A-0 System）；FORTRAN 1957（Fortran）；巴克斯 1977 图灵奖（John Backus）；Lisp 1958（Lisp (programming language)）；COBOL 1959（COBOL）；BASIC 1964 Kemeny Kurtz（BASIC）；Altair BASIC 1975（Altair BASIC）；C 语言 1972（C (programming language)）；K&R 1978（The C Programming Language）；Böhm–Jacopini 1966（Structured program theorem）；Goto 有害 1968（Considered harmful）；Simula 67（Simula）；Wirth 1976 Algorithms + Data Structures = Programs（Algorithms + Data Structures = Programs）；GC 1959 McCarthy（Garbage collection (computer science)）；Python 1991（Python (programming language)）；Java 1995 Gosling（Java (programming language)）；Oracle 收购 Sun 2010（Sun Microsystems）；Node.js 2009（Node.js）；IEEE 754 1985（IEEE 754）；Kahan 1989 图灵奖（William Kahan）；CTSS 1961（Compatible Time-Sharing System）；Corbató 1990 图灵奖（Fernando J. Corbató）；Unix 1969 / C 重写 1973（Unix）；Thompson Ritchie 1983 图灵奖（Ken Thompson）；Atlas 虚拟内存 1962（Atlas (computer)）；Dijkstra 信号量 1962/65（Semaphore (programming)）；哲学家就餐 1965（Dining philosophers problem）；BIOS 一词 Kildall 1975（BIOS）；Windows 1.0 1985（Windows 1.0）；Windows 95（Windows 95）；Linux 1991 Torvalds（Linux）；Git 2005（Git）；GitHub 2008（GitHub）；Mac OS X 2001（Mac OS X 10.0）；安卓 2003 创立 2005 收购 2008 HTC Dream（Android (operating system)）；HTC Dream 2008（HTC Dream）；VM/370 1972（VM (operating system)）；VMware 1999（VMware Workstation）；Docker 2013（Docker (software)）；Kubernetes 2014 Borg（Kubernetes）；IMS 阿波罗（IBM Information Management System）；Codd 1970（Relational model）；Codd 1981 图灵奖（Edgar F. Codd）；Oracle 1979（Oracle Database）；Jim Gray 1998 图灵奖（Jim Gray (computer scientist)）；Bigtable 2006（Bigtable）；Dynamo 2007（Dynamo (storage system)）；NoSQL 2009（NoSQL）；MapReduce 2004（MapReduce）；Hadoop 2006（Apache Hadoop）；数据仓库 1980 年代末 IBM（Data warehouse）；Huffman 1952（Huffman coding）；LZ77 1977（LZ77 and LZ78）；Luhn 1953 哈希（Hash table）；Unicode 1.0 1991（Unicode）；UTF-8 1992 Thompson Pike（UTF-8）；汉明码 1950（Hamming code）；RAID 1988（RAID）；5G LDPC/Polar（Polar code (coding theory)）；1968 NATO 软件工程会议（Software engineering）；Brooks 1975 人月神话（The Mythical Man-Month）；Mark II 飞蛾 1947（Software bug）；SCCS 1972（Source Code Control System）；GNU 1983（GNU Project）；FSF 1985（Free Software Foundation）；敏捷宣言 2001 Snowbird（Agile software development）；Log4Shell 2021（Log4Shell）；xz 后门 2024（XZ Utils backdoor）；DevOps 2009（DevOps）；REST 2000（REST）；Lamport 2013 图灵奖（Leslie Lamport）；CAP 2000 / 2002（CAP theorem）；Paxos 1989/1998（Paxos (computer science)）；Raft 2014（Raft (algorithm)）；Bourne shell 1979（Bourne shell）；Bash 1989（Bash (Unix shell)）；Alto 1973（Xerox Alto）；演示之母 1968（The Mother of All Demos）；Lisa 1983（Apple Lisa）；鼠标 1964 English（Computer mouse）；VisiCalc 1979（VisiCalc）；Lotus 1-2-3 1983（Lotus 1-2-3）；Excel 1985（Microsoft Excel）；Bravo 1974（Bravo (editor)）；Electric Pencil 1976（Electric Pencil）；WordStar 1978（WordStar）；Sketchpad 1963（Sketchpad）；Sutherland 1988 图灵奖（Ivan Sutherland）；Whitted 光线追踪 1980（Ray tracing (graphics)）；玩具总动员 1995 首部全 CG（Toy Story）；Tennis for Two 1958（Tennis for Two）；Spacewar! 1962（Spacewar!）；Pong 1972（Pong）；Magnavox Odyssey 1972（Magnavox Odyssey）；Unreal Engine 1998（Unreal Engine）；Unity 2005（Unity (game engine)）；App Store 2008 年 7 月（App Store (Apple)）；Y2K 成本（Year 2000 problem）；2038 问题（Year 2038 problem）；Salesforce 1999（Salesforce）；AWS Lambda 2014（AWS Lambda）；S3 2006（Amazon S3）；EC2 2006（Amazon Elastic Compute Cloud）；Azure 2010（Microsoft Azure）；阿里云 2009（Alibaba Cloud）；Monte Carlo Ulam 1946（Monte Carlo method）；ENIAC 1950 天气预报（Numerical weather prediction）；Cook 1971 NP 完全（Cook–Levin theorem）；Karp 21 问题 1972（Karp's 21 NP-complete problems）；千禧年大奖难题 2000（Millennium Prize Problems）；I. J. Good 1965 智能爆炸（Technological singularity）；Vinge 1993（Technological singularity）；Kurzweil 2005 / 2045（Technological singularity）；AKS 素数检验在 P 中（AKS primality test）；Hennessy Patterson 2017 图灵奖（David Patterson (computer scientist)）；JavaScript 10 天（Brendan Eich）；SEQUEL 1974（SQL）；开源 1998（Open-source software）；开源 1998 OSI（Open Source Initiative）；Lamport 1978（Lamport timestamp）；Doom 1993（Doom (1993 video game)）；Doom engine licensed（Doom engine）；McCarthy 1961 utility（John McCarthy (computer scientist)）；ARM 出货（Arm Holdings）；Mother of all demos 鼠标 窗口（The Mother of All Demos）。

## 三、收词范围的对照来源

- 维基百科"重要条目"（Vital Articles）第 4 级"技术"全部条目，以及第 5 级"技术"下各子页面（共 3306 个条目名），逐条与本书词条清单比对，补入了 94 个遗漏词条。
- 维基百科"历史发明年表"（Timeline of historic inventions）1700 年以后的全部条目。

## 四、延伸阅读（未作为核对依据）

- Charles Petzold，《编码：隐匿在计算机软硬件背后的语言》（Code）——从电报和继电器讲到 CPU，最适合入门。
- David Patterson、John Hennessy，《计算机组成与设计》——硬件部分的标准教材。
- Andrew Tanenbaum，《现代操作系统》。
- Thomas Cormen 等，《算法导论》。
- Martin Kleppmann，《数据密集型应用系统设计》——数据库、分布式系统部分的最佳读物。
- Walter Isaacson，《创新者》——计算机与互联网的人物史。
