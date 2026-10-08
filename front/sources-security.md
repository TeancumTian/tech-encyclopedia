# 本篇资料来源与核实记录

**一句话：本篇的年份、人物和关键数字都至少对照过一个公开来源；武器类词条只写公开的原理、历史和影响，不涉及任何设计或操作细节。**

## 一、按原始来源核对的最新数据

| 正文中的说法 | 来源（访问于 2026 年 10 月） |
|---|---|
| 2024 年 7 月 19 日 CrowdStrike Falcon 的错误内容更新导致约 850 万台 Windows 设备蓝屏（微软估计，不到全部 Windows 设备的 1%；终校时核对） | 微软官方博客 2024 年 7 月 20 日；en.wikipedia.org/wiki/2024_CrowdStrike-related_IT_outages |
| 美国 NIST 2024 年 8 月发布首批后量子密码标准（见 17 篇） | nist.gov 新闻稿 2024 年 8 月 13 日 |

## 二、批量核对（年份与人物）

方法：用脚本 `tools/factcheck.py` 读取英文维基百科对应条目的全文，检查正文中的年份或关键词是否出现在相应上下文中；未通过的换用其他条目复核，或查找机构官网、原始论文和权威媒体，逐条人工处理。本篇共核对 104 项（含复核项），脚本通过 102 项；其余均已人工处理，见下。原始结果保存在 `research/factcheck/` 下的 `security.result.tsv` 及共享复核文件中。

**未通过项的处理：**

- 索布雷罗合成硝化甘油：维基百科写 1846 年 → 正文由 1847 年改为 1846 年
- 防火墙 DEC 1988：维基百科写 DEC 工程师 1987 年开发包过滤系统，其他来源多写 1988 年 → 正文改为"20 世纪 80 年代末"

**已核对通过的说法（括号内为维基百科条目名）：**

Minié ball 1849（Minié ball）；Dreyse needle gun 1841（Dreyse needle gun）；StG 44 1944（StG 44）；AK-47 1947（AK-47）；Gatling 1861（Gatling gun）；Maxim gun 1884（Maxim gun）；Nobel dynamite 1867（Dynamite）；TNT 1863（TNT）；Vieille Poudre B 1884（Poudre B）；Ypres chlorine 1915（Second Battle of Ypres）；Geneva Protocol 1925（Geneva Protocol）；CWC 1993 1997（Chemical Weapons Convention）；OPCW Nobel 2013（Organisation for the Prohibition of Chemical Weapons）；Tank Mark I 1916（Mark I tank）；HMS Argus 1918（HMS Argus (I49)）；Midway 1942（Battle of Midway）；USS Enterprise CVN-65 1961（USS Enterprise (CVN-65)）；USS Holland 1900（USS Holland (SS-1)）；USS Nautilus 1954（USS Nautilus (SSN-571)）；Langevin sonar（Sonar）；Hülsmeyer 1904（Christian Hülsmeyer）；Daventry experiment 1935（Daventry Experiment）；Cavity magnetron 1940 Randall Boot（Cavity magnetron）；Whitehead torpedo 1866（Whitehead torpedo）；Gloire 1859（French ironclad Gloire）；HMS Dreadnought 1906（HMS Dreadnought (1906)）；Fokker interrupter 1915（Synchronization gear）；Me 262 1944（Messerschmitt Me 262）；F-22 2005（Lockheed Martin F-22 Raptor）；E-3 Sentry 1977（Boeing E-3 Sentry）；BWC 1972 1975（Biological Weapons Convention）；Sverdlovsk anthrax 1979（Sverdlovsk anthrax leak）；IAEA 1957（International Atomic Energy Agency）；NPT 1968（Treaty on the Non-Proliferation of Nuclear Weapons）；NPT 1970 force（Treaty on the Non-Proliferation of Nuclear Weapons）；NPT extended 1995（Treaty on the Non-Proliferation of Nuclear Weapons）；North Korea withdrew 2003（Treaty on the Non-Proliferation of Nuclear Weapons）；Hahn fission 1938（Nuclear fission）；Trinity July 1945（Trinity (nuclear test)）；Ivy Mike 1952（Ivy Mike）；RDS-37 1955（RDS-37）；Tsar Bomba 1961 50 Mt（Tsar Bomba）；China H-bomb 1967（Test No. 6）；PTBT 1963（Partial Nuclear Test Ban Treaty）；R-7 1957（R-7 Semyorka）；Atlas ICBM 1959（SM-65 Atlas）；V-1 1944（V-1 flying bomb）；Thanh Hoa Bridge 1972（Thanh Hóa Bridge）；ABM Treaty 1972（Anti-Ballistic Missile Treaty）；US withdrew ABM 2002（Anti-Ballistic Missile Treaty）；Iron Dome 2011（Iron Dome）；Ufimtsev stealth（Pyotr Ufimtsev）；F-117 1983（Lockheed F-117 Nighthawk）；F-117 first flight 1981（Lockheed F-117 Nighthawk）；Window chaff Hamburg 1943（Chaff (countermeasure)）；Predator 1995（General Atomics MQ-1 Predator）；LaWS 2014 USS Ponce（AN/SEQ-3 Laser Weapon System）；Kwolek Kevlar 1965（Kevlar）；Rejewski 1932（Marian Rejewski）；Polish 1939 July sharing（Marian Rejewski）；Kerckhoffs 1883（Kerckhoffs's principle）；Shannon 1949 secrecy（Communication Theory of Secrecy Systems）；DES 1977（Data Encryption Standard）；DES broken 1998（Data Encryption Standard）；AES 2001 Rijmen（Advanced Encryption Standard）；Diffie-Hellman 1976（Diffie–Hellman key exchange）；RSA 1977（RSA cryptosystem）；GCHQ Ellis Cocks（Clifford Cocks）；Diffie Hellman Turing 2015（Whitfield Diffie）；RSA Turing 2002（Ron Rivest）；X.509 1988（X.509）；Let's Encrypt 2015（Let's Encrypt）；CTSS passwords（Password）；Passkeys 2022（WebAuthn）；Galton fingerprints 1892（Fingerprint）；Scotland Yard 1901（Fingerprint）；Touch ID 2013（Touch ID）；Face ID 2017（Face ID）；Elk Cloner 1982（Elk Cloner）；Brain virus 1986（Brain (computer virus)）；Morris worm 1988（Morris worm）；ILOVEYOU 2000（ILOVEYOU）；AIDS trojan 1989（AIDS (Trojan horse)）；CryptoLocker 2013（CryptoLocker）；WannaCry 2017（WannaCry ransomware attack）；CVE 1999（Common Vulnerabilities and Exposures）；Heartbleed 2014（Heartbleed）；Zero trust Kindervag 2010（Zero trust architecture）；BeyondCorp 2014（BeyondCorp）；NIST 800-207 2020（Zero trust architecture）；Stuxnet 2010（Stuxnet）；CCTV Siemens 1942（Closed-circuit television）；RSA-250 2020（RSA numbers）；CrowdStrike 2024 8.5 million（2024 CrowdStrike-related IT outages）；SolarWinds 2020（2020 United States federal government data breach）；PGP 1991（Pretty Good Privacy）；Signal Protocol 2013（Signal Protocol）；WhatsApp E2EE 2016（WhatsApp）；Phishing AOL 1995（Phishing）；phishing term 1995/1996（Phishing）。

## 三、收词范围的对照来源

- 维基百科"重要条目"（Vital Articles）第 4 级"技术"与第 5 级"技术"下各子页面（共 3306 个条目名），逐条与本书词条清单比对，补入 2 个遗漏词条：端到端加密、网络钓鱼与社会工程。
- 维基百科"历史发明年表"（Timeline of historic inventions）1700 年以后的条目。
- 各词条以公开百科和历史文献为准；核武器、导弹等只写物理原理的通俗说明和历史影响。

## 四、延伸阅读（未作为核对依据）

- 西蒙·辛格，《密码故事》——从古典密码到公钥密码。
- 理查德·罗兹，《原子弹出世记》——核武器的科学史。
- Ross Anderson，《安全工程》（Security Engineering）——信息安全的标准参考书，作者公开免费提供。
- 布鲁斯·施奈尔，《秘密与谎言》。
