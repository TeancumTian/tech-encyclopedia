# 本篇资料来源与核实记录

**一句话：本篇的年份、人物和关键数字都至少对照过一个公开来源；加密货币部分不写价格，只写原理和公开的监管事件。**

## 一、按原始来源核对的最新数据

| 正文中的说法 | 来源（访问于 2026 年 10 月） |
|---|---|
| 2016 年印度推出 UPI，2020 年巴西央行推出 Pix，美国 2023 年上线 FedNow | NPCI、巴西央行、美联储官网；en.wikipedia.org/wiki/Unified_Payments_Interface ；/Pix_(payment_system) ；/FedNow |
| 2024 年美国批准比特币现货 ETF | 美国 SEC 2024 年 1 月 10 日声明 |
| 2025 年 7 月 18 日美国签署《GENIUS 法案》（S.1582，公法 119-27），为支付型稳定币设立储备与披露要求 | congress.gov/bill/119th-congress/senate-bill/1582 ；白宫 2025 年 7 月公告（终校时核对） |

## 二、批量核对（年份与人物）

方法：用脚本 `tools/factcheck.py` 读取英文维基百科对应条目的全文，检查正文中的年份或关键词是否出现在相应上下文中；未通过的换用其他条目复核，或查找机构官网、原始论文和权威媒体，逐条人工处理。本篇共核对 83 项（含复核项），脚本通过 77 项；其余均已人工处理，见下。原始结果保存在 `research/factcheck/` 下的 `fintech.result.tsv` 及共享复核文件中。

**未通过项的处理：**

- EMV 1994：维基百科写首版标准 1995 年；EMVCo 资料显示三家 1994 年开始联合发布 1.0 版各部分，1996 年发布 EMV '96 → 正文改为"1994 年……开始联合发布 EMV 标准"
- 斯坦福联邦信用合作社 1994 年首家网上银行：维基百科 Online banking 条目未写 → 换用 Stanford Federal Credit Union 条目核对通过
- 微信支付 2013：维基百科 WeChat Pay / WeChat 条目未在同一句写出 → 腾讯公开资料确认 2013 年 8 月上线，保留
- Szabo 1994 智能合约：维基百科 Smart contract 条目引用 Szabo 1990 年代的文章；1994 年为 Szabo 本人网站所载首篇文章年份，保留
- 智能投顾：正文由早先的说法改为以 2010 年 Betterment 公开上线为起点（Robo-advisor 条目核对通过）

**已核对通过的说法（括号内为维基百科条目名）：**

Ritty cash register 1879（Cash register）；NCR Patterson 1884（NCR Corporation）；Calahan stock ticker 1867（Ticker tape）；Woodland Silver 1949（Barcode）；UPC Laurer 1973（Universal Product Code）；First UPC scan 1974（Universal Product Code）；QR code 1994 Denso（QR code）；Hara QR（QR code）；Everitt postcard vending 1883（Vending machine）；Hero of Alexandria vending（Vending machine）；EDI Berlin airlift（Electronic data interchange）；Amazon Go 2018（Amazon Go）；Australia polymer banknote 1988（Polymer banknote）；Diners Club 1950（Diners Club International）；BankAmericard 1958（Visa Inc.）；Visa 1976（Visa Inc.）；Mastercard 1966 Interbank（Mastercard）；UnionPay 2002（UnionPay）；ATM 1967 Barclays Enfield（Automated teller machine）；Shepherd-Barron（John Shepherd-Barron）；SWIFT founded 1973（SWIFT）；SWIFT live 1977（SWIFT）；PayPal 1998（PayPal）；eBay acquired PayPal 2002（PayPal）；Alipay 2004（Alipay）；Apple Pay 2014（Apple Pay）；M-Pesa 2007（M-Pesa）；M-Pesa poverty 2 percent（M-Pesa）；UPI 2016（Unified Payments Interface）；Pix 2020（Pix (payment system)）；FedNow 2023（FedNow）；Faster Payments 2008（Faster Payments）；FICO 1989（Credit score in the United States）；Fair Isaac 1956（FICO）；PSD2 2018（Payment Services Directive）；ERMA 1959（Electronic Recording Machine, Accounting）；MICR（Magnetic ink character recognition）；Herstatt 1974（Settlement risk）；Nasdaq 1971（Nasdaq）；Big Bang 1986（Big Bang (financial markets)）；Decimalization 2001（Decimalisation）；Black-Scholes 1973（Black–Scholes model）；Nobel 1997 Scholes Merton（Black–Scholes model）；Bachelier 1900（Louis Bachelier）；LTCM 1998（Long-Term Capital Management）；Flash crash 2010（2010 flash crash）；Betterment 2010（Betterment (company)）；Kiva 2005（Kiva (organization)）；Zopa 2005（Zopa）；Kickstarter 2009（Kickstarter）；Bitcoin whitepaper 2008（Bitcoin）；Genesis block 3 January 2009（Bitcoin）；Pizza 10000 BTC 2010（Bitcoin）；21 million cap（Bitcoin）；Bitcoin spot ETF 2024（Bitcoin）；Haber Stornetta 1991（Blockchain）；Ethereum Merge 2022（Ethereum）；Ethereum 2015 launch（Ethereum）；The DAO 2016（The DAO）；Tether 2014（Tether (cryptocurrency)）；Terra collapse 2022（Terra (blockchain)）；GENIUS Act 2025（GENIUS Act）；MakerDAO DAI 2017（Dai (cryptocurrency)）；Uniswap 2018（Uniswap）；CryptoKitties 2017（CryptoKitties）；Beeple 69 million（Everydays: the First 5000 Days）；Sand Dollar 2020（Central bank digital currency）；e-CNY pilot 2020（Digital renminbi）；Stanford FCU 1994 internet banking（Stanford Federal Credit Union）；EDI 1960s/1970s（Electronic data interchange）；vending machine 1883 Everitt（Vending machine）；ERMA 1959 MICR（Electronic Recording Machine, Accounting）；polymer banknote Australia 1988（Polymer banknote）；Betterment 2008 robo（Robo-advisor）；Zopa 2005 P2P（Peer-to-peer lending）。

## 三、收词范围的对照来源

- 维基百科"重要条目"（Vital Articles）第 4 级"技术"与第 5 级"技术"下各子页面（共 3306 个条目名），逐条与本书词条清单比对，补入 9 个遗漏词条：自动售货机、刷卡终端 POS、电子数据交换、自助收银与无人商店、钞票防伪技术、银行电子化与磁墨水字符、清算与结算系统、智能投顾、众筹与网络借贷。
- 维基百科"历史发明年表"（Timeline of historic inventions）1700 年以后的条目。
- 国际清算银行（BIS）支付与市场基础设施委员会的术语表。

## 四、延伸阅读（未作为核对依据）

- 尼尔·弗格森，《货币崛起》。
- 大卫·格雷伯，《债：第一个 5000 年》。
- 阿尔文德·纳拉亚南等，《比特币与加密货币技术》（普林斯顿公开课教材）。
- 马克·莱文森，《集装箱改变世界》——条形码与现代物流的背景。
