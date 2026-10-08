# 本篇资料来源与核实记录

**一句话：本篇的年份、人物和关键数字都至少对照过一个公开来源；"有声电影""视觉暂留"等常见误传在正文的"注意"里专门纠正。**

## 一、按原始来源核对的最新数据

| 正文中的说法 | 来源（访问于 2026 年 10 月） |
|---|---|
| CCD 1969 年由贝尔实验室博伊尔和史密斯发明，2009 年获诺贝尔物理学奖 | nobelprize.org/prizes/physics/2009/summary/ |
| 柯达在 2012 年申请破产保护 | en.wikipedia.org/wiki/Kodak |

## 二、批量核对（年份与人物）

方法：用脚本 `tools/factcheck.py` 读取英文维基百科对应条目的全文，检查正文中的年份或关键词是否出现在相应上下文中；未通过的换用其他条目复核，或查找机构官网、原始论文和权威媒体，逐条人工处理。本篇共核对 125 项（含复核项），脚本通过 119 项；其余均已人工处理，见下。原始结果保存在 `research/factcheck/` 下的 `media.result.tsv`、`media2.result.tsv` 及共享复核文件中。

**未通过项的处理：**

- 柯达口号"你按快门，其余交给我们"：Kodak 条目未匹配 → 改用 George Eastman 条目核对通过
- 王永民 1983 年五笔字型、基尔霍夫与本生 1859 年光谱分析、惠普 ThinkJet 1984 年：首轮匹配失败 → 分别用 Wubi method、Gustav Kirchhoff、HP ThinkJet 条目复核通过
- 王选汉字激光照排：英文维基百科条目简略 → 以北京大学、新华社等中文公开资料为准；正文不写具体年份，只写"让中文印刷告别了铅与火"
- 有声电影：正文注明《爵士歌手》（1927）用的是唱片同步（Vitaphone），不是光学录音
- 电影：正文"注意"说明"视觉暂留"并非连续运动感的真正原因（实际是似动现象和大脑的运动知觉）

**已核对通过的说法（括号内为维基百科条目名）：**

Niépce 1826/1827 earliest photo（Nicéphore Niépce）；Daguerre 1839（Daguerreotype）；Talbot calotype（Henry Fox Talbot）；Eastman Kodak 1888（George Eastman）；Brownie 1900 one dollar（Brownie (camera)）；Maxwell 1861 color（Color photography）；Autochrome 1907（Autochrome Lumière）；Kodachrome 1935（Kodachrome）；CCD 1969 Boyle Smith（Charge-coupled device）；CCD Nobel 2009（Willard Boyle）；Sasson 1975 digital camera（Steven Sasson）；Kodak bankruptcy 2012（Kodak）；Sharp J-SH04 2000（Camera phone）；Herschel infrared 1800（Infrared）；Kirsch first digital image 1957（Russell A. Kirsch）；Kirsch 176（Russell A. Kirsch）；Scott phonautograph 1857（Phonautograph）；Edison phonograph 1877（Phonograph）；Berliner gramophone 1887（Emile Berliner）；LP 1948（LP record）；Rice Kellogg loudspeaker 1925（Loudspeaker）；Poulsen 1898（Valdemar Poulsen）；AEG Magnetophon（Magnetophon）；Ampex 1948（Ampex）；Walkman 1979（Walkman）；iPod 2001（IPod）；CD 1982（Compact disc）；CD 74 minutes（Compact disc）；MPEG-1 Layer III 1993（MP3）；Brandenburg MP3（Karlheinz Brandenburg）；Napster 1999（Napster）；Muybridge 1878（Eadweard Muybridge）；Lumière 28 December 1895（Auguste and Louis Lumière）；Kinetoscope Dickson（Kinetoscope）；De Forest Phonofilm 1923（Phonofilm）；Jazz Singer 1927 Vitaphone（The Jazz Singer）；Nipkow 1884（Paul Gottlieb Nipkow）；Baird January 1926（John Logie Baird）；Farnsworth 1927（Philo Farnsworth）；BBC television 1936（BBC Television）；Apollo 11 600 million（Apollo 11）；NTSC color 1953（NTSC）；PAL 1967（PAL）；Ampex VRX-1000 1956（Ampex）；Betamax 1975（Betamax）；VHS 1976（VHS）；H.264 2003（Advanced Video Coding）；HEVC 2013（High Efficiency Video Coding）；AV1 2018（AV1）；DCT 1974 Ahmed（Discrete cosine transform）；JPEG 1992（JPEG）；Sutherland HMD 1968（The Sword of Damocles (virtual reality)）；Oculus Kickstarter 2012（Oculus Rift）；Facebook acquired Oculus 2014（Oculus Rift）；Pokémon Go 2016（Pokémon Go）；US digital transition 2009（Digital television transition in the United States）；DTMB 2006（DTMB）；Snow Crash metaverse 1992（Metaverse）；Facebook renamed Meta 2021（Meta Platforms）；Koenig Times 1814（Friedrich Koenig）；Hoe rotary 1843（Rotary printing press）；Sholes typewriter 1868（Typewriter）；Remington 1873/1874（Sholes and Glidden typewriter）；Carlson xerography 1938（Chester Carlson）；Xerox 914 1959（Xerox 914）；Starkweather laser printer 1971（Laser printing）；HP LaserJet 1984（LaserJet）；Canon bubble jet 1977（Inkjet printing）；Project Gutenberg 1971（Project Gutenberg）；Kindle 2007（Amazon Kindle）；E Ink MIT（E Ink）；TeX 1978（TeX）；Desktop publishing 1985（Desktop publishing）；Einstein stimulated emission 1917（Stimulated emission）；Townes maser 1954（Maser）；Schawlow Townes 1958（Laser）；Maiman 1960 ruby（Theodore Maiman）；Laser Nobel 1964（Charles H. Townes）；Gabor holography 1947（Dennis Gabor）；Gabor Nobel 1971（Dennis Gabor）；Fraunhofer lines 1814（Fraunhofer lines）；Cesium discovered 1860（Caesium）；Laue 1912（Max von Laue）；Photo 51 1952（Photo 51）；Ruska 1931（Ernst Ruska）；Ruska Nobel 1986（Ernst Ruska）；Cryo-EM Nobel 2017（Cryogenic electron microscopy）；STM 1981 Binnig Rohrer（Scanning tunneling microscope）；IBM xenon atoms 1989（IBM (atoms)）；Jansky 1932（Karl Guthe Jansky）；FAST 2016（Five-hundred-meter Aperture Spherical Telescope）；EHT black hole 2019（Event Horizon Telescope）；Babcock 1953 adaptive optics（Adaptive optics）；Essen caesium clock 1955（Louis Essen）；Second defined 1967（Second）；9192631770（Caesium standard）；Metre Convention 1875（Metre Convention）；SI named 1960（International System of Units）；SI redefinition 20 May 2019（2019 revision of the SI）；Libby radiocarbon 1949（Radiocarbon dating）；Libby Nobel 1960（Willard Libby）；Abbe 1873（Diffraction-limited system）；Zernike Nobel 1953（Frits Zernike）；Super-resolution Nobel 2014（Super-resolution microscopy）；Keck 1993（W. M. Keck Observatory）；Keck 36 segments（W. M. Keck Observatory）；ELT 39 m（Extremely Large Telescope）；Geiger 1908（Geiger counter）；Geiger-Müller 1928（Geiger counter）；Zhang Heng 132 seismoscope（Zhang Heng）；Milne seismograph 1880（John Milne）；GB railway time 1847（Railway time）；North America standard time 1883（Standard time）；Meridian Conference 1884（International Meridian Conference）；Leap second abolished 2035（Leap second）；Wubi 1983（Wubi method）；Kirchhoff Bunsen 1859（Gustav Kirchhoff）；ThinkJet 1984（HP ThinkJet）；Kodak slogan（George Eastman）。

## 三、收词范围的对照来源

- 维基百科"重要条目"（Vital Articles）第 4 级"技术"与第 5 级"技术"下各子页面（共 3306 个条目名），逐条与本书词条清单比对，本篇首轮对照未发现遗漏的必要词条。
- 维基百科"历史发明年表"（Timeline of historic inventions）1700 年以后的条目。

## 四、延伸阅读（未作为核对依据）

- 尤金·赫克特，《光学》——光学部分的标准教材。
- 马歇尔·麦克卢汉，《理解媒介》。
- 吴军，《浪潮之巅》中关于柯达、施乐的章节。
- 史蒂芬·约翰逊，《我们如何走到今天：重塑世界的 6 项创新》——玻璃、声音、光等章节。
