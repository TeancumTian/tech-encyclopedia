#!/usr/bin/env python3
"""Generate all diagrams for 第 5 篇「人工智能」 -> assets/figs/ai/*.svg"""
from __future__ import annotations
import math, random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from svgkit import Fig, C, INK, MUTED, tw

OUT = Path(__file__).resolve().parents[1] / "assets" / "figs" / "ai"
FIGS = {}

def fig(fn):
    FIGS[fn.__name__.lstrip("_").replace("_", "-")] = fn
    return fn

def chips(f, x, y, w, items, col, fs=11, rowh=24):
    dark, _ = C[col]
    cx, cy = x, y
    for it in items:
        cw = tw(it, fs) + 12
        if cx + cw > x + w:
            cx, cy = x, cy + rowh
        f.rect(cx, cy, cw, 19, fill="#fff", stroke=dark, sw=0.8, rx=9)
        f.text(cx + cw / 2, cy + 13.5, it, fs=fs)
        cx += cw + 6
    return cy + rowh

# ------------------------------------------------------------------ concept map
@fig
def concept_map():
    f = Fig(680, 940, "人工智能 知识地图")
    f.text(340, 30, "人工智能 · 知识地图", fs=21, weight=700)
    f.text(340, 52, "中间自下而上：从“写规则”到“学规律”，再到大模型和它的应用与治理。左边是历史，右边是根原理。", fs=11.5, fill=MUTED)
    X, W = 168, 344
    layers = [  # bottom -> top
        ("思想源头", "slate", ["图灵测试", "符号主义", "专家系统", "搜索与规划", "AI 寒冬", "聊天机器人"]),
        ("机器学习", "green", ["监督 · 无监督 · 自监督", "强化学习", "回归与分类", "决策树 · SVM · 贝叶斯", "过拟合", "损失函数 · 梯度下降"]),
        ("神经网络与深度学习", "blue", ["感知机", "反向传播", "CNN", "RNN · LSTM", "ResNet", "ImageNet", "词向量", "注意力", "Transformer", "GAN · 扩散模型"]),
        ("算力与数据", "teal", ["GPU · TPU · AI 芯片", "数据标注", "评测基准", "联邦学习"]),
        ("大模型时代", "purple", ["GPT · ChatGPT", "缩放定律", "预训练与微调", "Token · 上下文", "RLHF", "推理模型", "RAG", "智能体", "多模态 · MoE", "开放权重", "幻觉"]),
        ("感知与语言", "amber", ["计算机视觉", "人脸识别", "OCR", "自然语言处理", "机器翻译", "语音识别 · 合成", "推荐系统", "知识图谱"]),
        ("里程碑与应用", "pink", ["深蓝", "AlphaGo", "AI for Science", "AI 编程", "具身智能", "医疗 AI", "深度伪造"]),
        ("安全与治理", "red", ["对齐", "偏见与公平", "可解释性", "隐私", "AI 监管", "AGI 之争"]),
    ]
    top, bottom = 76, 812
    def nrows(items, w=W - 22, fs=10.5):
        cx, r = 0, 1
        for it in items:
            cw = tw(it, fs) + 12
            if cx + cw > w: cx, r = 0, r + 1
            cx += cw + 6
        return r
    need = [42 + 23 * nrows(it) for _, _, it in layers]
    extra = (bottom - top - sum(need)) / len(layers)
    y = bottom
    for i, (name, col, items) in enumerate(layers):
        lh = need[i] + extra; y -= lh
        dark, light = C[col]
        f.rect(X, y + 5, W, lh - 10, fill=light, stroke=dark, sw=1.4, rx=8)
        f.text(X + 12, y + 24, name, fs=14, fill=dark, weight=700, anchor="start")
        chips(f, X + 12, y + 32 + (extra - 0) / 2 * 0, W - 22, items, col, fs=10.5, rowh=23)
        if i < len(layers) - 1:
            f.arrow(X + W / 2, y + 7, X + W / 2, y - 3, color=dark, sw=2.2, size=9)
    f.text(X + W / 2, bottom + 20, "↑ 方法越来越通用，规模越来越大，影响越来越广", fs=11.5, fill=C["blue"][0], weight=700)
    # left: history
    LX = 8
    f.text(LX + 72, 90, "七十年起落", fs=14, weight=700, fill=C["slate"][0])
    hist = [("1950", "图灵测试"), ("1956", "达特茅斯会议"), ("1958", "感知机"), ("1966", "ELIZA"), ("1974", "第一次寒冬"),
            ("1980s", "专家系统热"), ("1986", "反向传播"), ("1997", "深蓝胜卡斯帕罗夫"), ("2012", "AlexNet"),
            ("2016", "AlphaGo"), ("2017", "Transformer"), ("2020", "GPT-3"), ("2022", "ChatGPT"),
            ("2024", "推理模型 · 诺奖"), ("2025", "智能体 · 开放权重"), ("2026", "GPT-6 等新一代")]
    y0, step = 112, (bottom - 120) / (len(hist) - 1)
    f.line(LX + 16, y0 - 6, LX + 16, y0 + step * (len(hist) - 1) + 6, stroke=C["slate"][0], sw=2)
    for k, (yr, nm) in enumerate(hist):
        y = y0 + k * step
        winter = "寒冬" in nm
        f.circle(LX + 16, y, 4.5, fill=C["red"][0] if winter else C["slate"][0], stroke="#fff", sw=1)
        f.text(LX + 25, y + 4, yr, fs=10, fill=MUTED, anchor="start", weight=700)
        f.text(LX + 62, y + 4, nm, fs=10.5, anchor="start", fill=C["red"][0] if winter else INK)
    # right: principles
    RX = 522
    def side(y, title, col, items):
        dark, light = C[col]
        h = 32 + 21 * len(items)
        f.rect(RX, y, 150, h, fill=light, stroke=dark, sw=1.2, rx=8)
        f.text(RX + 75, y + 21, title, fs=13, fill=dark, weight=700)
        for k, it in enumerate(items):
            f.text(RX + 10, y + 42 + 21 * k, "· " + it, fs=11, anchor="start")
        return y + h
    y = side(84, "怎么学（根原理）", "green", ["优化：梯度下降", "概率与统计推断", "信息：压缩即理解"])
    y = side(y + 14, "为什么变强", "purple", ["规模效应", "指数增长的算力", "缩放定律"])
    y = side(y + 14, "为什么要管", "red", ["激励与博弈", "反馈与控制", "冗余与安全"])
    y = side(y + 14, "四个核心问题", "slate", ["数据从哪来？", "目标怎么定？", "会不会出错？", "谁来负责？"])
    f.rect(10, 862, 660, 66, fill="#f9fafb", stroke="#d1d5db", rx=8)
    f.text(340, 884, "和其他篇的接口", fs=12.5, weight=700)
    f.text(340, 905, "GPU 与数据中心 → 第 3 篇「计算与软件」　芯片制造 → 第 2 篇「电与电子」　搜索与推荐平台 → 第 4 篇", fs=11, fill=MUTED)
    f.text(340, 922, "机器人本体与工厂自动化 → 第 7 篇「制造与自动化」　AI 制药 → 医学篇", fs=11, fill=MUTED)
    return f

# ------------------------------------------------------------------ A figures
@fig
def artificial_intelligence():
    f = Fig(680, 300, "AI 的三条路线")
    x0, x1, ya = 50, 650, 230
    def X(yr): return x0 + (yr - 1950) / (2026 - 1950) * (x1 - x0)
    f.line(x0, ya, x1, ya, sw=1.4)
    for yr in range(1950, 2030, 10):
        f.line(X(yr), ya, X(yr), ya + 5)
        f.text(X(yr), ya + 18, str(yr), fs=10.5, fill=MUTED)
    f.text(X(2026), ya + 18, "2026", fs=10.5, fill=MUTED)
    bands = [(1956, 1992, "符号主义：人写规则", "amber", 150), (1985, 2015, "机器学习：从数据中学", "green", 175), (2010, 2026, "深度学习与大模型", "blue", 200)]
    for a, b, lab, col, y in bands:
        dark, light = C[col]
        f.rect(X(a), y, X(b) - X(a), 20, fill=light, stroke=dark, rx=10)
        f.text((X(a) + X(b)) / 2, y + 14.5, lab, fs=11.5, weight=700, fill=dark)
    # hype curve
    pts = [(1950, 40), (1956, 70), (1965, 95), (1973, 82), (1976, 45), (1980, 52), (1985, 98), (1988, 92), (1991, 50), (1996, 58),
           (2000, 62), (2006, 70), (2012, 95), (2016, 110), (2020, 118), (2023, 132), (2026, 135)]
    def Y(v): return 140 - v * 0.85
    d = "M" + " L".join(f"{X(a):.1f},{Y(v):.1f}" for a, v in pts)
    f.path(d, stroke=C["purple"][0], sw=2.2)
    f.text(X(1950), 18, "紫线：热度与投入（示意）", fs=11, fill=C["purple"][0], anchor="start", weight=700)
    for a, b in [(1974, 1980), (1987, 1993)]:
        f.rect(X(a), 20, X(b) - X(a), 122, fill=C["gray"][1], stroke="none", rx=0, opacity=0.9)
        f.text((X(a) + X(b)) / 2, 34, "寒冬", fs=11, fill=C["red"][0], weight=700)
    f.path(d, stroke=C["purple"][0], sw=2.2)
    for yr, lab, dy in [(1956, "达特茅斯", -10), (1997, "深蓝", -10), (2012, "AlexNet", -10), (2016, "AlphaGo", -12), (2022, "ChatGPT", -10)]:
        i = max(k for k, (aa, _) in enumerate(pts) if aa <= yr)
        (a0, v0), (a1, v1) = pts[i], pts[min(i + 1, len(pts) - 1)]
        yy = Y(v0 if a1 == a0 else v0 + (v1 - v0) * (yr - a0) / (a1 - a0))
        f.circle(X(yr), yy, 3.5, fill=C["purple"][0], stroke="#fff")
        f.text(X(yr), yy + dy, lab, fs=10.5, weight=700)
    f.text(340, 286, "三条路线前后接力、互有重叠；今天的“AI”多指第三条", fs=11, fill=MUTED)
    return f

@fig
def machine_learning():
    f = Fig(680, 250, "机器学习与传统编程")
    def row(y, title, col, a, b, mid, out, note):
        dark, light = C[col]
        f.text(30, y + 32, title, fs=14, weight=700, fill=dark, anchor="start")
        f.box(150, y, 110, 26, a, "slate", fs=12, weight=400)
        f.box(150, y + 36, 110, 26, b, "slate", fs=12, weight=400)
        f.arrow(262, y + 13, 318, y + 28, color=dark); f.arrow(262, y + 49, 318, y + 34, color=dark)
        f.box(320, y + 10, 130, 42, mid, col, fs=13, solid=True)
        f.arrow(452, y + 31, 500, y + 31, color=dark)
        f.box(502, y + 12, 140, 38, out, col, fs=13)
        f.text(396, y + 76, note, fs=11, fill=MUTED)
    row(18, "传统编程", "amber", "规则（人写）", "数据", "程序", "答案", "人必须先想清楚每一条规则")
    row(122, "机器学习", "green", "数据", "答案（标注）", "学习算法", "规则（模型）", "规则由算法从例子里“总结”出来，再用来预测新数据")
    return f

@fig
def neural_network():
    f = Fig(680, 320, "神经元与神经网络")
    f.text(160, 26, "一个人工神经元", fs=14, weight=700, fill=C["blue"][0])
    xs = [("x₁", 80), ("x₂", 150), ("x₃", 220)]
    cx, cy = 200, 150
    for (lab, y), w in zip(xs, ["w₁", "w₂", "w₃"]):
        f.circle(40, y, 15, fill=C["slate"][1], stroke=C["slate"][0]); f.text(40, y + 5, lab, fs=13)
        f.arrow(56, y, cx - 34, cy + (y - 150) * 0.25, color=C["blue"][0])
        f.text(100, (y + cy) / 2 - 4 + (y - 150) * 0.15, w, fs=12, fill=C["amber"][0], weight=700)
    f.circle(cx, cy, 32, fill=C["blue"][1], stroke=C["blue"][0], sw=1.8)
    f.text(cx, cy - 2, "Σ + b", fs=14, weight=700)
    f.text(cx, cy + 15, "加权求和", fs=9.5, fill=MUTED)
    f.arrow(cx + 33, cy, 268, cy, color=C["blue"][0])
    f.rect(270, cy - 20, 40, 40, fill="#fff", stroke=C["purple"][0], rx=4)
    f.path(f"M274,{cy+12} L290,{cy+12} L306,{cy-14}", stroke=C["purple"][0], sw=2)
    f.text(290, cy + 36, "激活函数", fs=10.5, fill=C["purple"][0])
    f.arrow(312, cy, 335, cy, color=C["blue"][0]); f.text(345, cy + 5, "y", fs=14, weight=700)
    f.lines(170, 262, ["输出 = 激活( w₁x₁ + w₂x₂ + w₃x₃ + b )", "“学习”= 调整权重 w 和偏置 b"], fs=11.5, fill=INK)
    # network
    f.line(370, 30, 370, 300, stroke="#e5e7eb", sw=1)
    f.text(525, 26, "很多神经元分层连接", fs=14, weight=700, fill=C["blue"][0])
    layers = [3, 4, 4, 2]; lx = [400, 480, 560, 640]
    pos = []
    for n, x in zip(layers, lx):
        ys = [160 + (k - (n - 1) / 2) * 52 for k in range(n)]
        pos.append([(x, y) for y in ys])
    for a, b in zip(pos, pos[1:]):
        for (x1, y1) in a:
            for (x2, y2) in b:
                f.line(x1, y1, x2, y2, stroke="#93c5fd", sw=0.9)
    cols = ["slate", "blue", "blue", "green"]
    for p, col in zip(pos, cols):
        for (x, y) in p:
            f.circle(x, y, 12, fill=C[col][1], stroke=C[col][0], sw=1.4)
    for x, lab in zip([400, 520, 640], ["输入层", "隐藏层", "输出层"]):
        f.text(x, 282, lab, fs=12, weight=700)
    f.text(520, 302, "层数多 = “深”度学习", fs=10.5, fill=MUTED)
    return f

@fig
def backpropagation():
    f = Fig(680, 290, "前向传播与反向传播")
    names = [("输入", "slate"), ("第 1 层", "blue"), ("第 2 层", "blue"), ("输出\n预测值", "green"), ("损失\n和正确答案差多少", "red")]
    xs = [20, 150, 280, 410, 540]; w, y, h = 110, 110, 64
    for (lab, col), x in zip(names, xs):
        rows = lab.split("\n")
        f.box(x, y, w if x < 540 else 125, h, rows[0], col, fs=13.5, sub=rows[1] if len(rows) > 1 else None, sub_fs=10)
    for a, b in zip(xs, xs[1:]):
        f.arrow(a + w + 2, y + 18, b - 2, y + 18, color=C["blue"][0], sw=2)
    f.text(330, 62, "① 前向：数据一层层算过去，得到预测", fs=13, weight=700, fill=C["blue"][0])
    f.arrow(60, 76, 600, 76, color=C["blue"][0], sw=2.2)
    for a, b in zip(xs, xs[1:]):
        f.arrow(b - 2, y + 48, a + w + 2, y + 48, color=C["red"][0], sw=2, dash="5 3")
    f.arrow(600, 200, 60, 200, color=C["red"][0], sw=2.2)
    f.text(330, 222, "② 反向：误差从后往前传，用链式法则算出每个权重“该往哪调、调多少”", fs=13, weight=700, fill=C["red"][0])
    f.box(150, 238, 380, 38, "③ 更新：w ← w − 学习率 × 梯度", "amber", fs=13.5)
    f.text(600, 262, "重复上亿次", fs=11, fill=MUTED)
    return f

@fig
def deep_learning():
    f = Fig(680, 330, "深度学习：逐层抽象的特征")
    f.text(340, 24, "每一层在前一层的基础上，学到更抽象的特征", fs=13.5, weight=700, fill=C["blue"][0])
    xs = [70, 200, 330, 460, 590]
    labs = ["像素", "边缘", "纹理与角", "部件", "物体"]
    for x, lab in zip(xs, labs):
        f.rect(x - 48, 40, 96, 96, fill="#fff", stroke=C["blue"][0], rx=6)
        f.text(x, 156, lab, fs=12.5, weight=700)
    random.seed(3)
    for i in range(8):
        for j in range(8):
            g = random.randint(150, 240)
            f.rect(xs[0] - 44 + i * 11, 44 + j * 11, 11, 11, fill=f"rgb({g},{g},{g})", stroke="none", rx=0)
    for k, ang in enumerate([0, 45, 90, 135]):
        cx, cy = xs[1] - 22 + (k % 2) * 44, 66 + (k // 2) * 44
        a = math.radians(ang)
        f.line(cx - 14 * math.cos(a), cy - 14 * math.sin(a), cx + 14 * math.cos(a), cy + 14 * math.sin(a), stroke=INK, sw=3)
    x = xs[2]
    f.path(f"M{x-34},{60} L{x-14},{60} L{x-14},{80}", sw=2.5)
    f.path(f"M{x+6},{60} Q{x+26},{56} {x+34},{78}", sw=2.5)
    for k in range(4):
        f.path(f"M{x-34},{100+k*7} Q{x-24},{94+k*7} {x-14},{100+k*7}", sw=1.6)
    f.circle(x + 20, 110, 12, fill="none")
    x = xs[3]
    f.path(f"M{x-34},{75} Q{x-22},{58} {x-10},{75} Q{x-22},{88} {x-34},{75} Z", sw=2, fill=C["green"][1]); f.circle(x - 22, 75, 4, fill=INK)
    f.poly([(x + 8, 92), (x + 20, 60), (x + 32, 92)], sw=2, fill=C["amber"][1], closed=True)
    f.path(f"M{x-30},{112} Q{x},{124} {x+30},{112}", sw=2)
    x = xs[4]
    f.circle(x, 92, 30, fill=C["amber"][1], stroke=C["amber"][0], sw=2)
    f.poly([(x - 28, 76), (x - 22, 46), (x - 8, 66)], fill=C["amber"][1], stroke=C["amber"][0], sw=2, closed=True)
    f.poly([(x + 28, 76), (x + 22, 46), (x + 8, 66)], fill=C["amber"][1], stroke=C["amber"][0], sw=2, closed=True)
    f.circle(x - 11, 88, 3.5, fill=INK); f.circle(x + 11, 88, 3.5, fill=INK)
    f.text(x, 108, "猫", fs=13, weight=700)
    for a, b in zip(xs, xs[1:]):
        f.arrow(a + 50, 88, b - 50, 88, color=C["blue"][0])
    # three pillars
    f.rect(60, 270, 560, 20, fill=C["slate"][1], stroke=C["slate"][0], rx=3)
    f.box(150, 186, 380, 36, "2012 年后的深度学习突破", "blue", fs=14, solid=True)
    for x, lab, sub, col in [(90, "数据", "ImageNet 等\n千万级标注", "green"), (275, "算力", "GPU 并行\n计算", "amber"), (460, "算法", "ReLU · Dropout\n残差连接", "purple")]:
        f.box(x, 226, 130, 44, lab, col, fs=13, sub=sub.replace("\n", " "), sub_fs=10)
    f.text(340, 308, "三根柱子缺一不可：方法早就有了，缺的是数据和算力", fs=11, fill=MUTED)
    return f

@fig
def transformer_model():
    f = Fig(680, 380, "Transformer 的结构")
    toks = ["小猫", "没有", "过", "马路"]
    xs = [120, 210, 300, 390]
    for t, x in zip(toks, xs):
        f.box(x - 38, 330, 76, 30, t, "slate", fs=13, weight=400)
        f.arrow(x, 328, x, 300, color=C["slate"][0])
    f.box(70, 266, 370, 32, "词嵌入 + 位置编码（每个词变成一串数字）", "teal", fs=12, weight=400)
    f.rect(60, 70, 390, 186, fill="#fff", stroke=C["blue"][0], sw=1.6, rx=10, dash="6 4")
    f.text(470, 168, "× N 层", fs=16, weight=700, fill=C["blue"][0], anchor="start")
    f.text(470, 188, "（几十到上百层）", fs=10.5, fill=MUTED, anchor="start")
    f.box(80, 186, 350, 56, "自注意力", "amber", fs=14, sub="每个词“看”所有其他词，决定从谁那里取信息")
    f.box(80, 104, 350, 56, "前馈网络", "blue", fs=14, sub="每个词各自再加工一遍")
    f.arrow(255, 186, 255, 162, color=C["blue"][0], sw=2)
    f.text(70, 92, "（每个子层都有“残差连接 + 归一化”，便于堆深）", fs=10, fill=MUTED, anchor="start")
    f.arrow(255, 104, 255, 64, color=C["green"][0], sw=2)
    f.box(150, 22, 210, 40, "输出：下一个词的概率", "green", fs=13)
    f.lines(540, 250, ["要点：", "所有词并行处理，", "不像 RNN 逐个读，", "因此能用 GPU", "高效训练超大模型"], fs=11.5, fill=INK, anchor="start")
    return f

@fig
def llm():
    f = Fig(680, 360, "大语言模型：训练与生成")
    f.text(20, 26, "训练：两大阶段", fs=14, weight=700, fill=C["purple"][0], anchor="start")
    f.box(20, 40, 150, 60, "海量文本", "slate", fs=13.5, sub="网页 · 书籍 · 代码\n数万亿 token")
    f.arrow(172, 70, 212, 70, color=C["purple"][0])
    f.box(214, 40, 150, 60, "预训练", "purple", fs=14, solid=True, sub="反复练习\n预测下一个词")
    f.arrow(366, 70, 396, 70, color=C["purple"][0])
    f.box(398, 40, 110, 60, "基础模型", "purple", fs=13, sub="会续写\n不太听话")
    f.arrow(510, 70, 530, 70, color=C["purple"][0])
    f.box(532, 40, 140, 60, "对齐与后训练", "green", fs=13, sub="指令微调 · RLHF\n强化学习练推理")
    f.text(602, 118, "→ 聊天助手", fs=12, weight=700, fill=C["green"][0])
    f.line(20, 136, 660, 136, stroke="#e5e7eb")
    f.text(20, 160, "生成：一次只吐一个 token，再把它接回输入", fs=14, weight=700, fill=C["blue"][0], anchor="start")
    f.box(20, 200, 150, 44, "今天 天气", "slate", fs=14, weight=400)
    f.arrow(172, 222, 212, 222, color=C["blue"][0])
    f.box(214, 194, 110, 56, "模型", "blue", fs=15, solid=True, sub="Transformer")
    f.arrow(326, 222, 356, 222, color=C["blue"][0])
    probs = [("很", .42), ("不错", .21), ("晴朗", .15), ("怎么", .08), ("…", .14)]
    for k, (t, p) in enumerate(probs):
        y = 180 + k * 19
        f.text(392, y + 12, t, fs=11.5, anchor="end")
        f.rect(398, y + 2, p * 300, 13, fill=C["amber"][1] if k else C["amber"][0], stroke=C["amber"][0], rx=2)
        f.text(404 + p * 300, y + 13, f"{p:.2f}", fs=10, fill=MUTED, anchor="start")
    f.text(470, 290, "按概率挑出“很”", fs=11.5, weight=700, fill=C["amber"][0])
    f.curve(470, 300, 250, 350, 95, 248, color=C["blue"][0], sw=1.6)
    f.text(280, 342, "“今天天气很” → 再预测下一个……直到结束", fs=11.5, fill=C["blue"][0], weight=700)
    return f

# ------------------------------------------------------------------ small figures
@fig
def reinforcement_learning():
    f = Fig(520, 220, "强化学习的循环")
    f.box(40, 80, 150, 60, "智能体", "blue", fs=16, solid=True, sub="策略：此刻做什么")
    f.box(330, 80, 150, 60, "环境", "green", fs=16, solid=True, sub="棋盘 · 游戏 · 真实世界")
    f.curve(190, 90, 260, 20, 330, 90, color=C["blue"][0], sw=2)
    f.text(260, 40, "动作", fs=13, weight=700, fill=C["blue"][0])
    f.curve(330, 132, 260, 205, 190, 132, color=C["green"][0], sw=2)
    f.text(260, 186, "新状态 + 奖励（得分）", fs=13, weight=700, fill=C["green"][0])
    f.text(260, 214, "目标：让长期累计奖励最大", fs=11, fill=MUTED)
    return f

@fig
def overfitting():
    f = Fig(520, 210, "欠拟合、恰好与过拟合")
    random.seed(7)
    xsamp = [0.05 + i * 0.09 for i in range(11)]
    ys = [math.sin(x * 5) * 0.35 + 0.5 + random.uniform(-0.1, 0.1) for x in xsamp]
    titles = [("欠拟合：太简单", "amber"), ("恰好：抓住规律", "green"), ("过拟合：死记噪声", "red")]
    for k, (t, col) in enumerate(titles):
        ox, oy, w, h = 15 + k * 170, 30, 150, 140
        f.rect(ox, oy, w, h, fill="#fff", stroke="#d1d5db", rx=4)
        f.text(ox + w / 2, oy - 8, t, fs=12, weight=700, fill=C[col][0])
        P = lambda x, y: (ox + 8 + x * (w - 16), oy + h - 8 - y * (h - 16))
        for x, y in zip(xsamp, ys):
            px, py = P(x, y); f.circle(px, py, 3.2, fill=C["slate"][0], stroke="#fff", sw=0.6)
        if k == 0:
            a, b = P(0, 0.62), P(1, 0.38); f.line(*a, *b, stroke=C[col][0], sw=2)
        elif k == 1:
            pts = [P(x / 50, math.sin(x / 50 * 5) * 0.35 + 0.5) for x in range(51)]
            f.poly(pts, stroke=C[col][0], sw=2)
        else:
            pts = []
            for i in range(len(xsamp) - 1):
                x1, x2, y1, y2 = xsamp[i], xsamp[i + 1], ys[i], ys[i + 1]
                for s in range(10):
                    t = s / 10; x = x1 + (x2 - x1) * t
                    y = y1 + (y2 - y1) * t + math.sin(t * math.pi) * (0.12 if i % 2 else -0.12)
                    pts.append(P(x, y))
            pts.append(P(xsamp[-1], ys[-1]))
            f.poly(pts, stroke=C[col][0], sw=2)
    f.text(260, 198, "同样的数据点：模型太简单抓不住规律，太复杂会把噪声也背下来", fs=11, fill=MUTED)
    return f

@fig
def gradient_descent():
    f = Fig(520, 250, "梯度下降")
    cx, cy = 300, 125
    for k, r in enumerate([20, 45, 72, 100, 128]):
        f.path(f"M{cx-r*1.6},{cy} A{r*1.6},{r*0.8} 0 1,0 {cx+r*1.6},{cy} A{r*1.6},{r*0.8} 0 1,0 {cx-r*1.6},{cy}", stroke=C["blue"][0], sw=1, fill=C["blue"][1] if k == 0 else "none", opacity=0.9)
    f.circle(cx, cy, 4, fill=C["green"][0], stroke="#fff")
    f.text(cx + 8, cy + 18, "最低点（损失最小）", fs=11, fill=C["green"][0], weight=700, anchor="start")
    pts = [(108, 60), (150, 168), (205, 92), (240, 148), (268, 112), (286, 132), (296, 124)]
    for a, b in zip(pts, pts[1:]):
        f.arrow(*a, *b, color=C["red"][0], sw=1.8, size=7)
    f.circle(*pts[0], 4.5, fill=C["red"][0], stroke="#fff")
    f.text(100, 48, "起点（随机初始化）", fs=11, fill=C["red"][0], weight=700)
    f.text(260, 240, "等高线 = 损失相同的参数组合；每步沿当前最陡的下坡方向走一小步（步长 = 学习率）", fs=10.5, fill=MUTED)
    return f

@fig
def cnn():
    f = Fig(520, 230, "卷积：小窗口滑过图像")
    n, s, ox, oy = 6, 24, 30, 40
    vals = [[0,0,1,1,0,0],[0,1,1,1,1,0],[1,1,0,0,1,1],[1,1,0,0,1,1],[0,1,1,1,1,0],[0,0,1,1,0,0]]
    for i in range(n):
        for j in range(n):
            f.rect(ox + j * s, oy + i * s, s, s, fill="#dbeafe" if vals[i][j] else "#fff", stroke="#9ca3af", sw=0.6, rx=0)
            f.text(ox + j * s + s / 2, oy + i * s + 16, str(vals[i][j]), fs=10, fill=MUTED)
    f.rect(ox + s, oy + s, 3 * s, 3 * s, fill="none", stroke=C["amber"][0], sw=2.6, rx=0)
    f.text(ox + 3 * s, oy - 10, "输入图像（像素）", fs=12, weight=700)
    kx, ky = 230, 70
    k = [[1, 0, -1], [1, 0, -1], [1, 0, -1]]
    for i in range(3):
        for j in range(3):
            f.rect(kx + j * s, ky + i * s, s, s, fill=C["amber"][1], stroke=C["amber"][0], sw=0.8, rx=0)
            f.text(kx + j * s + s / 2, ky + i * s + 16, str(k[i][j]), fs=11, weight=700)
    f.text(kx + 36, ky - 10, "卷积核 3×3", fs=12, weight=700, fill=C["amber"][0])
    f.text(kx + 36, ky + 92, "（找竖直边缘）", fs=10.5, fill=MUTED)
    f.curve(ox + 4 * s + 4, oy + s + 10, 190, 40, kx - 4, ky + 20, color=C["amber"][0], sw=1.4)
    fx, fy = 380, 58
    for i in range(4):
        for j in range(4):
            hl = i == 1 and j == 1
            f.rect(fx + j * s, fy + i * s, s, s, fill=C["green"][1] if not hl else C["green"][0], stroke=C["green"][0], sw=0.8, rx=0)
    f.text(fx + 2 * s, fy - 10, "特征图 4×4", fs=12, weight=700, fill=C["green"][0])
    f.arrow(kx + 3 * s + 6, ky + 36, fx - 6, fy + 12, color=C["green"][0])
    f.text(fx + 2 * s, fy + 4 * s + 18, "对应位置相乘再求和", fs=10.5, fill=MUTED)
    f.text(260, 214, "同一个卷积核滑遍整张图：参数少，且无论边缘在哪里都能被找到", fs=11, fill=MUTED)
    return f

@fig
def attention_mechanism():
    f = Fig(520, 210, "注意力：“它”指的是谁")
    toks = ["小猫", "没有", "过", "马路", "，", "因为", "它", "太", "累", "了"]
    wts = [0.9, 0.05, 0.02, 0.25, 0.0, 0.05, 0.0, 0.08, 0.35, 0.03]
    x0, step, yb = 30, 48, 150
    xs = [x0 + i * step + 18 for i in range(len(toks))]
    it = toks.index("它")
    for i, (t, x) in enumerate(zip(toks, xs)):
        col = "red" if i == it else ("amber" if i == 0 else "slate")
        f.box(x - 20, yb, 40, 28, t, col, fs=12.5, weight=700 if i in (0, it) else 400, solid=i == it)
    for i, (x, w) in enumerate(zip(xs, wts)):
        if i == it or w <= 0: continue
        h = 30 + abs(it - i) * 9
        f.path(f"M{xs[it]},{yb-2} Q{(xs[it]+x)/2},{yb-2-h} {x},{yb-2}", stroke=C["amber"][0], sw=0.6 + w * 7, opacity=0.35 + w * 0.65)
    f.text((xs[0] + xs[it]) / 2, 92, "权重最大（约 0.9）", fs=11, weight=700, fill=C["amber"][0])
    f.text(260, 200, "线越粗 = 注意力权重越大。模型在算“它”时，主要从“小猫”那里取信息", fs=11, fill=MUTED)
    return f

@fig
def diffusion_model():
    f = Fig(520, 212, "扩散模型：从噪声中还原图像")
    random.seed(11)
    xs = [20, 120, 220, 320, 420]; y, s = 50, 80
    levels = [1.0, 0.75, 0.5, 0.25, 0.0]
    for x, lv in zip(xs, levels):
        f.rect(x, y, s, s, fill="#fff", stroke=INK, rx=3)
        if lv < 1:
            op = 1 - lv
            f.rect(x + 1, y + 1, s - 2, s - 2, fill="#dbeafe", stroke="none", rx=2, opacity=op)
            f.circle(x + 58, y + 22, 9, fill="#fbbf24", stroke="none")
            f.poly([(x + 2, y + 78), (x + 28, y + 40), (x + 48, y + 62), (x + 60, y + 50), (x + 78, y + 78)], fill="#86efac", stroke="#059669", sw=1, closed=True, opacity=op)
        for _ in range(int(220 * lv)):
            px, py = x + random.uniform(2, s - 4), y + random.uniform(2, s - 4)
            g = random.randint(60, 200)
            f.rect(px, py, 3, 3, fill=f"rgb({g},{g},{g})", stroke="none", rx=0)
    for a, b in zip(xs, xs[1:]):
        f.arrow(a + s + 3, y + 30, b - 3, y + 30, color=C["blue"][0], sw=1.8)
        f.arrow(b - 3, y + 54, a + s + 3, y + 54, color=C["red"][0], sw=1.2, dash="4 3")
    f.text(260, 30, "生成：一步步去噪（模型学会预测“该去掉哪些噪声”）→", fs=12, weight=700, fill=C["blue"][0])
    f.text(260, 172, "← 训练时：给真实图片一步步加噪，让模型学习如何反过来", fs=12, weight=700, fill=C["red"][0])
    f.text(60, 147, "纯噪声", fs=11, fill=MUTED); f.text(460, 147, "清晰图像", fs=11, fill=MUTED)
    f.text(260, 200, "文字提示（如“山与太阳”）在每一步引导去噪的方向", fs=10.5, fill=MUTED)
    return f

@fig
def scaling_laws():
    f = Fig(520, 250, "缩放定律")
    ox, oy, w, h = 70, 30, 400, 170
    f.line(ox, oy + h, ox + w, oy + h); f.line(ox, oy, ox, oy + h)
    for k in range(6):
        x = ox + k * w / 5
        f.line(x, oy + h, x, oy + h + 4)
        f.text(x, oy + h + 17, "10" + str(18 + k * 2).translate(str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")), fs=10.5, fill=MUTED)
    f.text(ox + w / 2, oy + h + 36, "训练算力（浮点运算次数，对数刻度）", fs=11.5, weight=700)
    f.text(30, oy + h / 2, "损失", fs=11.5, weight=700)
    f.text(30, oy + h / 2 + 15, "(对数)", fs=10, fill=MUTED)
    f.line(ox + 10, oy + 20, ox + w - 10, oy + h - 20, stroke=C["blue"][0], sw=2.2, dash="6 4")
    random.seed(5)
    for k in range(9):
        t = (k + 0.5) / 9
        x = ox + 10 + t * (w - 20); y = oy + 20 + t * (h - 40) + random.uniform(-6, 6)
        f.circle(x, y, 5, fill=C["purple"][1], stroke=C["purple"][0], sw=1.4)
    f.text(ox + w - 120, oy + 30, "一条直线：", fs=12, weight=700, fill=C["blue"][0], anchor="start")
    f.text(ox + w - 120, oy + 48, "算力每涨 10 倍，", fs=11, anchor="start")
    f.text(ox + w - 120, oy + 64, "损失按固定比例下降", fs=11, anchor="start")
    f.text(ox + 30, oy + h - 10, "每个点 = 一个不同规模的模型（示意）", fs=10.5, fill=MUTED, anchor="start")
    return f

def main():
    only = set(sys.argv[1:])
    for name, fn in FIGS.items():
        if only and name not in only: continue
        fn().save(OUT / f"{name}.svg")
    print("wrote", len(FIGS) if not only else len(only), "figures to", OUT)

if __name__ == "__main__":
    main()
