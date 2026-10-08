# 本篇资料来源与核实记录

**一句话：本篇所有年份、人物和关键数字都至少对照过一个公开来源；AI 变化极快，2025–2026 年的模型、用户数和法规状态直接引用发布方或官方公报，均截至 2026 年 10 月。**

## 一、按原始来源核对的最新数据

| 正文中的说法 | 来源（访问于 2026 年 10 月） |
|---|---|
| GPT-6 Astra 于 2026 年 9 月 3 日发布；GPT-6 Sol、Luna 于 9 月 22 日发布 | OpenAI：openai.com/index/gpt-6-astra/ ；openai.com/index/introducing-gpt-6-sol-and-luna/ |
| ChatGPT 每周用户超过 12 亿（2026 年 9 月底） | OpenAI DevDay 2026（9 月 29 日）报道：theverge.com/ai-artificial-intelligence/1002265/chatgpt-now-has-1-2-billion-weekly-users-openai-says |
| Claude Opus 5.5（2026 年 9 月 22 日） | Anthropic：anthropic.com/claude-opus-5-5 |
| Gemini 4 Argon 9 月底起先向经审核的网络安全防御者开放 | Google：blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/ ；deepmind.google/models/gemini/cyber/ |
| SpaceXAI（原 xAI）Grok 4.7（2026 年 9 月） | x.ai/news/grok-4-7 |
| DeepSeek V4 预览版 2026 年 4 月 24 日发布，MIT 许可证；V4-Pro 总参数约 1.6 万亿、每 token 激活约 490 亿、上下文 100 万 token | api-docs.deepseek.com/news/news260424 ；huggingface.co/deepseek-ai/DeepSeek-V4-Pro |
| 英伟达 Vera Rubin（配 HBM4）2026 年量产出货 | blogs.nvidia.com/blog/vera-rubin/ |
| 欧盟《人工智能法》：2024 年 8 月 1 日生效；2026 年 7 月的修正案（Regulation (EU) 2026/1744，“AI 数字综合法案”）把独立高风险系统义务推迟到 2027 年 12 月 2 日、嵌入产品的推迟到 2028 年 8 月 2 日；透明度义务 2026 年 8 月 2 日起适用 | eur-lex.europa.eu/eli/reg/2026/1744/oj ；ai-act-service-desk.ec.europa.eu/en/ai-act/timeline/timeline-implementation-eu-ai-act |
| XCON 据估计每年为 DEC 节省约 2500 万美元 | en.wikipedia.org/wiki/Xcon ；Stanford 档案“Digital Corp. Saves Millions” |
| 2024 年诺贝尔物理学奖（霍普菲尔德、辛顿）与化学奖（贝克；哈萨比斯、江珀） | nobelprize.org/prizes/physics/2024/ ；nobelprize.org/prizes/chemistry/2024/ |

## 二、批量核对（年份与人物）

方法：用脚本 `tools/factcheck.py` 读取英文维基百科对应条目的全文，检查正文中的年份或关键词是否出现在相应上下文中；未通过的逐条人工复核并修改正文。共核对 155 项（其中一部分是对首轮未通过项换用其他条目的复核），通过 132 项；仍未通过的均已人工处理，见下。原始结果保存在 `research/factcheck/ai.result.tsv、ai2.result.tsv`。

**未通过项的处理：**

- DENDRAL 1965：维基百科称项目始于 1964 年，各来源不一 → 正文改为“1960 年代中期”
- XCON 节省 2500 万美元/年：维基百科正文未直接写出数字；经网络检索（维基百科 Xcon 条目摘要与 DEC 当年报道）确认“约 2500 万美元/年”的估计，保留
- 随机森林 2001、XGBoost 2014：换用 Leo Breiman、XGBoost（Tianqi Chen）条目核对通过；XGBoost 首次发布于 2014 年（GitHub，2016 年 KDD 论文）
- 辛顿 2006 深度信念网络：维基百科正文未直接写出年份；Hinton、Osindero、Teh 2006 年发表于《神经计算》的论文为公认出处，保留
- 2018 年图灵奖：改用 Geoffrey Hinton 条目核对通过
- Bahdanau 2014 注意力：改用 Seq2seq 条目核对通过（论文 arXiv:1409.0473，2014 年 9 月）
- Gemini 1.5 百万 token：调整匹配词（one-million）后通过
- InstructGPT 13 亿参数胜过 1750 亿：改用 GPT-3 条目确认 InstructGPT；数字出自 Ouyang 等 2022 年论文《Training language models to follow instructions with human feedback》摘要，保留
- 混合专家 1991：维基百科未写明；出处为 Jacobs、Jordan、Nowlan、Hinton 1991 年《Adaptive Mixtures of Local Experts》（Neural Computation），保留
- DeepSeek-V3 6710 亿/370 亿：出自 DeepSeek-V3 技术报告（arXiv:2412.19437，2024 年 12 月），保留；V4 数据见上表
- Tapestry 1992：出处为 Goldberg 等 1992 年《ACM 通讯》论文《Using collaborative filtering to weave an information tapestry》，保留
- AlphaGo 4:1：维基百科写作“AlphaGo won all but the fourth game”，复核通过
- GraphCast 2023：出处为 Lam 等 2023 年 11 月《科学》论文，保留
- IDx-DR 2018 年 4 月：FDA 于 2018 年 4 月 11 日批准（FDA 新闻稿），保留
- 部分“通过”项只匹配到数字本身（如 Mark I 的 400 个光电管），已人工阅读上下文确认

**已核对通过的说法（括号内为维基百科条目名）：**

达特茅斯会议 1956（Dartmouth workshop）；图灵 1950 Mind 论文（Computing Machinery and Intelligence）；塞尔 中文屋 1980（Chinese room）；GPT-4.5 图灵测试 73%（Turing test）；逻辑理论家 1956（Logic Theorist）；纽厄尔 西蒙 1975 图灵奖（Herbert A. Simon）；A* 1968 哈特 尼尔森 拉斐尔（A* search algorithm）；STRIPS 1971（Stanford Research Institute Problem Solver）；莱特希尔报告 1973（Lighthill report）；《感知机》1969（Perceptrons (book)）；ELIZA 1966（ELIZA）；小冰 2014（Xiaoice）；塞缪尔 1959 机器学习（Arthur Samuel (computer scientist)）；勒让德 1805 最小二乘（Least squares）；皮尔逊 1901 PCA（Principal component analysis）；劳埃德 k-means 1957（K-means clustering）；BERT 2018（BERT (language model)）；萨顿 巴托 2024 图灵奖（Richard S. Sutton）；DQN 2013 Atari（Deep reinforcement learning）；CART 1984（Decision tree learning）；SVM 1992 核技巧（Support vector machine）；贝叶斯 1763（Bayes' theorem）；双下降 2019（Double descent）；柯西 1847 梯度下降（Gradient descent）；罗宾斯—门罗 1951（Stochastic gradient descent）；Adam 2014（Stochastic gradient descent）；罗森布拉特 1958 感知机（Perceptron）；Mark I 400 光电管（Perceptron）；麦卡洛克—皮茨 1943（Artificial neuron）；霍普菲尔德 1982（Hopfield network）；万能近似 Cybenko 1989（Universal approximation theorem）；林纳因马 1970 反向模式自动微分（Backpropagation）；韦伯斯 1974（Paul Werbos）；鲁梅尔哈特 辛顿 威廉姆斯 1986（Backpropagation）；AlexNet 2012 错误率 15.3%（AlexNet）；福岛邦彦 新认知机 1980（Neocognitron）；杨立昆 1989 卷积网络（Convolutional neural network）；LSTM 1997（Long short-term memory）；谷歌翻译 2016 神经机器翻译（Google Neural Machine Translation）；ResNet 2015 152 层（Residual neural network）；ImageNet 2009 1400 万张（ImageNet）；ILSVRC 2010–2017（ImageNet）；word2vec 2013（Word2vec）；弗斯 1957 词由其伴随者定义（Distributional semantics）；Transformer 2017 八位作者（Attention Is All You Need）；GAN 2014 古德费洛（Generative adversarial network）；StyleGAN 2018（StyleGAN）；扩散模型 2015 索尔—迪克斯坦（Diffusion model）；DDPM 2020（Diffusion model）；GPT-1 1.17 亿参数 2018（GPT-1）；GPT-2 15 亿参数 2019（GPT-2）；GPT-3 1750 亿参数 2020（GPT-3）；GPT-4 2023 年 3 月（GPT-4）；o1 2024 年 9 月（OpenAI o1）；GPT-5 2025 年 8 月（GPT-5）；ChatGPT 2022-11-30（ChatGPT）；ChatGPT 5 天 100 万用户（ChatGPT）；卡普兰 2020 缩放定律（Neural scaling law）；Chinchilla 2022 约 20 token/参数（Chinchilla (language model)）；LoRA 2021（Fine-tuning (deep learning)）；BPE 1994 盖奇（Byte-pair encoding）；RLHF 克里斯蒂安诺 2017（Reinforcement learning from human feedback）；思维链 2022（Prompt engineering）；DeepSeek-R1 2025 年 1 月（DeepSeek）；RAG 刘易斯 2020（Retrieval-augmented generation）；MCP 2024 年 11 月（Model Context Protocol）；CLIP 4 亿图文对 2021（Contrastive Language-Image Pre-training）；GPT-4o 2024（GPT-4o）；LLaMA 2023 年 2 月（Llama (language model)）；Llama 2 2023 年 7 月（Llama (language model)）；知识蒸馏 2015 辛顿（Knowledge distillation）；Mata v. Avianca 2023 虚假判例（Hallucination (artificial intelligence)）；Sora 2024 年 2 月（Sora (text-to-video model)）；世界模型 Ha & Schmidhuber 2018（World model (artificial intelligence)）；TPU 2016（Tensor Processing Unit）；V100 2017 张量核心（Volta (microarchitecture)）；美国 2022 芯片出口管制（United States New Export Controls on Advanced Computing and Semiconductors to China）；亚马逊 MTurk 2005（Amazon Mechanical Turk）；Scale AI 2016（Scale AI）；MMLU 2020（MMLU）；SWE-bench 2023（SWE-bench）；人类最后的考试 2025（Humanity's Last Exam）；联邦学习 2016 麦克马汉（Federated learning）；YOLO 2015（You Only Look Once）；SAM 2023（Segment Anything）；DeepFace 2014（DeepFace）；Face ID 2017（Face ID）；库兹韦尔 1974 OCR 公司（Ray Kurzweil）；乔治城—IBM 1954（Georgetown–IBM experiment）；ALPAC 1966（ALPAC）；Audrey 1952（Speech recognition）；Whisper 68 万小时 2022（Whisper (speech recognition system)）；WaveNet 2016（WaveNet）；Voder 1939（Voder）；Netflix 大奖 2006/2009（Netflix Prize）；谷歌知识图谱 2012（Google Knowledge Graph）；Siri 2011（Siri）；Alexa 2014（Amazon Alexa）；深蓝 1997 3.5—2.5（Deep Blue versus Garry Kasparov）；深蓝 每秒 2 亿局面（Deep Blue (chess computer)）；AlphaGo 樊麾 5:0 2015 年 10 月（AlphaGo）；AlphaGo 柯洁 3:0 2017（AlphaGo versus Ke Jie）；AlphaGo Zero 2017（AlphaGo Zero）；AlphaFold2 CASP14 2020（AlphaFold）；AlphaFold 约 2 亿结构（AlphaFold）；2024 诺贝尔化学奖 哈萨比斯 江珀（Demis Hassabis）；2024 诺贝尔物理学奖 霍普菲尔德 辛顿（John Hopfield）；Copilot 2021（GitHub Copilot）；vibe coding 柯林斯年度词 2025（Vibe coding）；RT-2 2023（Vision-language-action model）；深度伪造 2017（Deepfake）；香港 2 亿港元深伪诈骗 2024（Deepfake）；维纳 1960 机器自动化的后果（Norbert Wiener）；博斯特罗姆《超级智能》2014（Superintelligence: Paths, Dangers, Strategies）；英国 AI 安全峰会 2023（AI Safety Summit）；ProPublica COMPAS 2016（COMPAS (software)）；Gender Shades 2018（Joy Buolamwini）；GDPR 2018（General Data Protection Regulation）；意大利 2023 暂禁 ChatGPT（ChatGPT）；欧盟 AI 法 2024 生效（Artificial Intelligence Act）；中国 生成式 AI 暂行办法 2023（Interim Measures for the Management of Generative Artificial Intelligence Services）；AGI 一词 Goertzel/Legg（Artificial general intelligence）；DeepMind 2010 创立（Google DeepMind）；OpenAI 2015 创立（OpenAI）；随机森林 2001 布雷曼（Leo Breiman）；2018 图灵奖 辛顿（Geoffrey Hinton）；注意力 Bahdanau 2014（Seq2seq）；Gemini 1.5 百万 token（Gemini (language model)）；InstructGPT（GPT-3）；AlphaGo 4:1 李世石（AlphaGo versus Lee Sedol）；XGBoost 陈天奇（XGBoost）；DENDRAL 1960 年代（Dendral）。

## 三、收词范围的对照来源

- 维基百科“重要条目”（Vital Articles）第 4、5 级“技术”与“计算”相关子页面中的人工智能条目，逐条与本篇词条比对。
- 维基百科“人工智能年表”（Timeline of artificial intelligence）与“机器学习年表”（Timeline of machine learning）。
- 斯坦福大学《AI 指数报告》（AI Index）各年版本的章节目录，用于检查大模型时代的必要关键词。

## 四、延伸阅读（未作为核对依据）

- Stuart Russell、Peter Norvig，《人工智能：现代方法》——AI 的标准教材。
- Ian Goodfellow、Yoshua Bengio、Aaron Courville，《深度学习》（“花书”）。
- 周志华，《机器学习》（“西瓜书”）——中文入门教材。
- Melanie Mitchell，《AI 3.0》——给普通读者的 AI 能力与局限。
- Stuart Russell，《AI 新生：破解人机共存密码》——对齐与安全问题。
- Cade Metz，《深度学习革命》——深度学习人物史。
