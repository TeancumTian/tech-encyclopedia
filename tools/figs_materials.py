#!/usr/bin/env python3
"""Generate all diagrams for 第 6 篇「材料与化工」 -> assets/figs/materials/*.svg"""
from __future__ import annotations
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from svgkit import Fig, C, INK, MUTED, tw

OUT = Path(__file__).resolve().parents[1] / "assets" / "figs" / "materials"
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

def nrows(items, w, fs):
    cx, r = 0, 1
    for it in items:
        cw = tw(it, fs) + 12
        if cx + cw > w: cx, r = 0, r + 1
        cx += cw + 6
    return r

def layered_map(f, layers, top, bottom, X=168, W=344, fs=11, footer=""):
    need = [44 + 24 * nrows(it, W - 22, fs) for _, _, _, it in layers]
    extra = (bottom - top - sum(need)) / len(layers)
    y = bottom
    for i, (name, sub, col, items) in enumerate(layers):
        lh = need[i] + extra; y -= lh
        dark, light = C[col]
        f.rect(X, y + 5, W, lh - 10, fill=light, stroke=dark, sw=1.4, rx=8)
        f.text(X + 12, y + 25, name, fs=14, fill=dark, weight=700, anchor="start")
        if sub: f.text(X + 18 + tw(name, 14), y + 25, sub, fs=10.5, fill=MUTED, anchor="start")
        chips(f, X + 12, y + 34 + extra / 2 - 4, W - 22, items, col, fs=fs)
        if i < len(layers) - 1:
            f.arrow(X + W / 2, y + 7, X + W / 2, y - 3, color=dark, sw=2.2, size=9)
    if footer: f.text(X + W / 2, bottom + 20, footer, fs=11.5, fill=C["blue"][0], weight=700)

def timeline(f, title, hist, top, bottom, LX=8, hl=()):
    f.text(LX + 72, top - 2, title, fs=14, weight=700, fill=C["slate"][0])
    y0, step = top + 22, (bottom - top - 30) / (len(hist) - 1)
    f.line(LX + 16, y0 - 6, LX + 16, y0 + step * (len(hist) - 1) + 6, stroke=C["slate"][0], sw=2)
    for k, (yr, nm) in enumerate(hist):
        y = y0 + k * step
        f.circle(LX + 16, y, 4.5, fill=C["slate"][0], stroke="#fff", sw=1)
        f.text(LX + 25, y + 4, yr, fs=10, fill=MUTED, anchor="start", weight=700)
        f.text(LX + 58, y + 4, nm, fs=10.5, anchor="start")

def side(f, y, title, col, items, RX=522, w=150):
    dark, light = C[col]
    h = 32 + 21 * len(items)
    f.rect(RX, y, w, h, fill=light, stroke=dark, sw=1.2, rx=8)
    f.text(RX + w / 2, y + 21, title, fs=13, fill=dark, weight=700)
    for k, it in enumerate(items):
        f.text(RX + 10, y + 42 + 21 * k, "· " + it, fs=11, anchor="start")
    return y + h

# ------------------------------------------------------------------ concept map
@fig
def concept_map():
    f = Fig(680, 940, "材料与化工 知识地图")
    f.text(340, 30, "材料与化工 · 知识地图", fs=21, weight=700)
    f.text(340, 52, "中间自下而上：从矿石、空气和石油出发，经冶金与化工，变成金属、化学品、高分子和先进材料。", fs=11.5, fill=MUTED)
    layers = [
        ("采矿与资源", "原料从哪来", "slate", ["现代采矿", "泡沫浮选", "锂资源提取", "关键矿产", "稀土"]),
        ("金属与冶金", "把氧拿走", "blue", ["高炉炼铁", "贝塞麦转炉", "平炉", "氧气顶吹转炉", "电弧炉", "钢", "不锈钢", "电解铝", "钛", "合金", "高温合金", "形状记忆合金", "镀锌", "钕铁硼磁体"]),
        ("基础化工", "拆开再拼", "amber", ["合成氨", "硫酸", "氯碱", "制碱法", "合成染料", "空气分离", "工业催化", "催化裂化", "石油化工", "化学工程", "洗涤剂"]),
        ("高分子", "排成长链", "green", ["高分子学说", "橡胶硫化", "赛璐珞", "电木", "塑料", "聚乙烯", "齐格勒—纳塔", "尼龙", "合成纤维", "聚四氟乙烯", "合成橡胶", "芳纶", "生物塑料"]),
        ("无机与先进材料", "设计结构", "purple", ["浮法玻璃", "玻璃纤维", "先进陶瓷", "碳纤维", "复合材料", "纳米技术", "富勒烯", "碳纳米管", "石墨烯", "气凝胶", "超材料", "计算材料学"]),
    ]
    layered_map(f, layers, 76, 812, footer="↑ 从“找到什么用什么”到“需要什么造什么”")
    timeline(f, "三百年里程碑", [("1709", "焦炭炼铁"), ("1839", "橡胶硫化"), ("1856", "转炉 · 苯胺紫"), ("1861", "索尔维制碱"),
             ("1886", "电解铝"), ("1907", "电木"), ("1913", "合成氨投产"), ("1913", "不锈钢"), ("1920", "大分子学说"),
             ("1935", "尼龙"), ("1942", "流化催化裂化"), ("1952", "氧气转炉"), ("1953", "齐格勒催化剂"), ("1959", "浮法玻璃"),
             ("1965", "芳纶"), ("1984", "钕铁硼"), ("1985", "富勒烯"), ("2004", "石墨烯"), ("2023", "AI 预测新晶体")], 90, 812)
    y = side(f, 84, "根原理", "green", ["氧化还原：冶金", "化学键与催化：化工", "聚合：高分子", "结构决定性质"])
    y = side(f, y + 14, "四大支柱（斯米尔）", "blue", ["钢", "水泥（第 12 篇）", "塑料", "氨"])
    y = side(f, y + 14, "代价与挑战", "red", ["碳排放：钢、氨、水泥", "塑料污染", "资源集中与断供", "永久化学品 PFAS"])
    y = side(f, y + 14, "读一个材料时问", "slate", ["原子怎么排列？", "从什么原料来？", "能耗与排放多少？", "用完去哪里？"])
    f.rect(10, 862, 660, 66, fill="#f9fafb", stroke="#d1d5db", rx=8)
    f.text(340, 884, "和其他篇的接口", fs=12.5, weight=700)
    f.text(340, 905, "半导体硅 → 第 2 篇「电与电子」　电池材料 → 第 1 篇「能源与动力」　化肥与农业 → 农业篇", fs=11, fill=MUTED)
    f.text(340, 922, "水泥与混凝土 → 第 12 篇「建筑与城市」　塑料回收 → 第 15 篇「环境与可持续」", fs=11, fill=MUTED)
    return f

# ------------------------------------------------------------------ A figures
@fig
def steel():
    f = Fig(680, 360, "钢：碳含量与炼钢路线")
    x0, x1, y = 60, 640, 70
    def X(c): return x0 + c / 4.5 * (x1 - x0)
    zones = [(0, 0.02, "纯铁", "slate"), (0.02, 2.1, "钢", "blue"), (2.1, 4.5, "铸铁 / 生铁", "amber")]
    f.text(340, 24, "同样是铁，碳含量差一点，“性格”完全不同", fs=13.5, weight=700)
    for a, b, lab, col in zones:
        dark, light = C[col]
        f.rect(X(a), y, max(X(b) - X(a), 8), 34, fill=light, stroke=dark, rx=0)
        if b - a > 0.5: f.text((X(a) + X(b)) / 2, y + 22, lab, fs=13, weight=700, fill=dark)
    for c in [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5]:
        f.line(X(c), y + 34, X(c), y + 39); f.text(X(c), y + 52, f"{c:g}%", fs=10, fill=MUTED)
    f.text(340, y + 70, "含碳量（质量百分比）", fs=11, fill=MUTED)
    f.text(x0, y + 70, "← 最左一窄条：纯铁（<0.02%）", fs=10, fill=C["slate"][0], anchor="start")
    notes = [(x0 + 2, "start", "低碳钢：软、韧、好焊", "钢筋 · 车身 · 钢板"), (X(1.35), "middle", "高碳钢：硬", "刀具 · 弹簧 · 钢轨"),
             (X(3.3), "middle", "铸铁：硬而脆", "井盖 · 机床床身")]
    for xx, anc, t, sub in notes:
        f.text(xx, y - 24, t, fs=11, weight=700, anchor=anc)
        f.text(xx, y - 9, sub, fs=10, fill=MUTED, anchor=anc)
    # routes
    yy = 180
    f.text(20, yy, "两条主要炼钢路线（2025 年全球产量占比）", fs=13.5, weight=700, anchor="start", fill=C["blue"][0])
    f.box(20, yy + 16, 110, 44, "铁矿石 + 焦炭", "slate", fs=12, weight=400)
    f.arrow(132, yy + 38, 160, yy + 38)
    f.box(162, yy + 16, 90, 44, "高炉", "red", fs=13.5, sub="还原出铁水")
    f.arrow(254, yy + 38, 282, yy + 38)
    f.box(284, yy + 16, 110, 44, "转炉吹氧", "amber", fs=13.5, sub="烧掉多余的碳")
    f.text(339, yy + 76, "约 69%", fs=12, weight=700, fill=C["amber"][0])
    f.box(20, yy + 96, 110, 44, "废钢", "slate", fs=12, weight=400)
    f.arrow(132, yy + 118, 282, yy + 118)
    f.box(284, yy + 96, 110, 44, "电弧炉", "green", fs=13.5, sub="用电熔化")
    f.text(339, yy + 156, "约 30%", fs=12, weight=700, fill=C["green"][0])
    f.arrow(396, yy + 38, 440, yy + 70); f.arrow(396, yy + 118, 440, yy + 88)
    f.box(442, yy + 56, 90, 46, "钢水", "blue", fs=13.5, solid=True, sub="调成分")
    f.arrow(534, yy + 79, 556, yy + 79)
    f.box(558, yy + 50, 104, 58, "连铸 · 轧制", "blue", fs=12.5, sub="钢板 · 钢筋\n型钢 · 钢管")
    return f

@fig
def haber_bosch():
    f = Fig(680, 330, "哈伯—博施合成氨回路")
    f.text(340, 28, "N₂ + 3H₂ ⇌ 2NH₃（放热、体积缩小）", fs=15, weight=700)
    f.box(20, 70, 120, 48, "氮气 N₂", "blue", fs=14, sub="来自空气")
    f.box(20, 150, 120, 48, "氢气 H₂", "green", fs=14, sub="天然气 · 煤 · 电解水")
    f.arrow(142, 94, 182, 126); f.arrow(142, 174, 182, 142)
    f.box(184, 108, 110, 52, "压缩机", "slate", fs=14, sub="150—300 个大气压")
    f.arrow(296, 134, 330, 134, sw=2)
    f.rect(332, 66, 120, 136, fill=C["amber"][1], stroke=C["amber"][0], sw=1.8, rx=10)
    f.text(392, 92, "反应塔", fs=14.5, weight=700, fill=C["amber"][0])
    for i in range(4):
        for j in range(5):
            f.circle(352 + j * 20, 112 + i * 18, 5, fill="#9ca3af", stroke="#4b5563", sw=0.8)
    f.text(392, 192, "铁催化剂 · 400—500°C", fs=10.5, fill=C["amber"][0], weight=700)
    f.arrow(454, 134, 490, 134, sw=2)
    f.box(492, 104, 110, 60, "冷凝器", "teal", fs=14, sub="氨先变成液体\n被分离出来")
    f.arrow(547, 166, 547, 214, color=C["teal"][0], sw=2)
    f.box(492, 216, 110, 40, "液氨 NH₃", "teal", fs=14, solid=True)
    f.text(620, 240, "→ 化肥", fs=12, weight=700, anchor="start", fill=C["teal"][0])
    f.path("M602,120 C660,120 660,40 560,40 L300,40 C250,40 240,70 240,106", stroke=C["red"][0], sw=2, dash="6 4")
    f.head(240, 106, math.pi / 2, C["red"][0])
    f.text(450, 56, "未反应的 N₂、H₂ 循环回去再用", fs=12, weight=700, fill=C["red"][0])
    f.lines(240, 286, ["高压：推动平衡向生成氨的一边", "高温 + 催化剂：让反应足够快"], fs=11.5, fill=INK)
    f.text(240, 318, "每次通过只转化一小部分，靠循环把原料几乎用尽", fs=11, fill=MUTED)
    return f

@fig
def polymer():
    f = Fig(680, 330, "高分子：从单体到长链")
    f.text(20, 28, "① 聚合：小分子（单体）首尾相连", fs=13.5, weight=700, anchor="start", fill=C["green"][0])
    for k in range(5):
        f.circle(40 + k * 34, 64, 11, fill=C["green"][1], stroke=C["green"][0], sw=1.4)
    f.text(108, 96, "单体（如乙烯）", fs=11, fill=MUTED)
    f.arrow(210, 64, 260, 64, color=C["green"][0], sw=2, label="聚合", loff=(0, -8))
    xs = [280 + k * 26 for k in range(15)]
    for a, b in zip(xs, xs[1:]):
        f.line(a, 64, b, 64, stroke=C["green"][0], sw=2.4)
    for x in xs:
        f.circle(x, 64, 8, fill=C["green"][1], stroke=C["green"][0], sw=1.2)
    f.text(468, 96, "长链：一条链常有几千到几十万个单体", fs=11, fill=MUTED)
    f.line(20, 116, 660, 116, stroke="#e5e7eb")
    f.text(20, 140, "② 链怎么排，决定材料的“性格”", fs=13.5, weight=700, anchor="start", fill=C["blue"][0])
    def chain(pts, col):
        f.poly(pts, stroke=C[col][0], sw=2.2)
    panels = [(20, "直链、排列规整", "硬、结晶度高：高密度聚乙烯、纤维", "blue"),
              (240, "带支链、排不整齐", "软、透明：低密度聚乙烯薄膜", "amber"),
              (460, "链与链之间交联成网", "热固性塑料 · 硫化橡胶", "red")]
    for x, t, s, col in panels:
        f.rect(x, 152, 200, 124, fill="#fff", stroke=C[col][0], rx=8)
        f.text(x + 100, 296, t, fs=12.5, weight=700, fill=C[col][0])
        f.text(x + 100, 314, s, fs=10.5, fill=MUTED)
    for k in range(5):
        y = 170 + k * 22
        chain([(36 + i * 21, y + (4 if i % 2 else -4)) for i in range(9)], "blue")
    import random
    random.seed(4)
    for k in range(4):
        y = 176 + k * 26
        pts = [(256 + i * 20, y + (5 if i % 2 else -5)) for i in range(9)]
        chain(pts, "amber")
        for i in (2, 5):
            bx, by = pts[i]
            f.line(bx, by, bx + 8, by + (14 if k % 2 else -14), stroke=C["amber"][0], sw=2)
    for k in range(4):
        y = 176 + k * 26
        chain([(476 + i * 20, y + (5 if i % 2 else -5)) for i in range(9)], "red")
    for k in range(3):
        for i in (1, 4, 7):
            x = 476 + i * 20 + (k % 2) * 20
            f.line(x, 176 + k * 26 + 5, x, 176 + (k + 1) * 26 - 5, stroke=INK, sw=1.6, dash="3 2")
    f.text(560, 270, "虚线 = 交联化学键", fs=10, fill=MUTED)
    return f

@fig
def plastics():
    f = Fig(680, 360, "常见塑料与塑料垃圾的去向")
    codes = [("1", "PET", "饮料瓶 · 涤纶"), ("2", "HDPE", "奶瓶 · 管道"), ("3", "PVC", "水管 · 地板"), ("4", "LDPE", "薄膜 · 塑料袋"),
             ("5", "PP", "餐盒 · 保险杠"), ("6", "PS", "泡沫 · 一次性杯"), ("7", "其他", "PC · 尼龙 · 混合")]
    f.text(340, 24, "塑料标识码：说明“是什么塑料”，不代表一定能回收", fs=13.5, weight=700)
    w = 92
    for k, (n, ab, use) in enumerate(codes):
        x = 18 + k * w
        cx = x + w / 2 - 4
        f.poly([(cx, 44), (cx - 22, 82), (cx + 22, 82)], stroke=C["teal"][0], sw=2, closed=True, fill=C["teal"][1])
        f.text(cx, 76, n, fs=15, weight=700, fill=C["teal"][0])
        f.text(cx, 102, ab, fs=12.5, weight=700)
        f.text(cx, 120, use, fs=10, fill=MUTED)
    f.line(20, 146, 660, 146, stroke="#e5e7eb")
    f.text(340, 176, "全球塑料垃圾最终去了哪里（2019 年，经合组织估算）", fs=13.5, weight=700)
    parts = [("回收", 9, "green"), ("焚烧", 19, "amber"), ("卫生填埋", 50, "slate"), ("管理不当 / 泄漏到环境", 22, "red")]
    x, y, W = 30, 196, 620
    for lab, pct, col in parts:
        ww = W * pct / 100
        f.rect(x, y, ww, 44, fill=C[col][1], stroke=C[col][0], rx=0)
        f.text(x + ww / 2, y + 27, f"{pct}%", fs=14, weight=700, fill=C[col][0])
        f.text(x + ww / 2, y + 62, lab, fs=11.5, weight=700, fill=C[col][0])
        x += ww
    f.lines(340, 290, ["“管理不当”指露天堆放、露天焚烧或流入河流海洋。", "回收的塑料还有相当一部分因杂质多而被降级使用或再次丢弃。"], fs=11, fill=MUTED)
    f.text(340, 340, "2024 年全球塑料产量约 4.3 亿吨（欧洲塑料协会）", fs=11.5, weight=700, fill=INK)
    return f

# ------------------------------------------------------------------ small figures
@fig
def blast_furnace():
    f = Fig(520, 320, "高炉：逆流反应器")
    pts = [(200, 30), (320, 30), (350, 150), (340, 250), (180, 250), (170, 150)]
    f.poly(pts, stroke=C["slate"][0], sw=3, fill="#fff7ed", closed=True)
    for k in range(7):
        y = 50 + k * 26
        col = ["#9ca3af", "#1f2937"][k % 2]
        f.rect(205 - (k * 3 if k < 4 else 9), y, 110 + (k * 6 if k < 4 else 18), 12, fill=col, stroke="none", rx=2, opacity=0.55)
    f.rect(185, 222, 150, 12, fill="#fde68a", stroke="none", rx=0)
    f.rect(182, 234, 156, 14, fill="#f97316", stroke="none", rx=0)
    f.text(260, 232, "炉渣", fs=10, weight=700)
    f.text(260, 246, "铁水（约 1500°C）", fs=10, weight=700, fill="#fff")
    f.text(260, 20, "炉顶分层装入：铁矿石 · 焦炭 · 石灰石", fs=11.5, weight=700)
    f.arrow(110, 70, 110, 200, color=C["slate"][0], sw=2.4)
    f.text(98, 136, "炉料下沉", fs=12, weight=700, fill=C["slate"][0], anchor="end")
    f.arrow(410, 200, 410, 70, color=C["red"][0], sw=2.4)
    f.text(422, 130, "热气 + CO 上升", fs=12, weight=700, fill=C["red"][0], anchor="start")
    f.text(422, 148, "把氧“抢”走", fs=11, fill=C["red"][0], anchor="start")
    for y in (200, 215):
        f.arrow(130, y, 172, y, color=C["amber"][0], sw=1.8)
    f.text(120, 222, "热风", fs=11, weight=700, fill=C["amber"][0], anchor="end")
    f.arrow(338, 241, 380, 262, color="#f97316", sw=2)
    f.text(386, 272, "出铁口", fs=11, fill="#c2410c", anchor="start", weight=700)
    f.text(260, 300, "Fe₂O₃ + 3CO → 2Fe + 3CO₂", fs=13, weight=700)
    return f

@fig
def aluminum_smelting():
    f = Fig(520, 270, "电解铝的电解槽")
    f.rect(70, 70, 380, 150, fill="#fff", stroke=C["slate"][0], sw=3, rx=4)
    f.rect(73, 100, 374, 92, fill=C["amber"][1], stroke="none", rx=0)
    f.text(260, 182, "熔融冰晶石 + 溶解的 Al₂O₃（约 960°C）", fs=11.5, weight=700, fill=C["amber"][0])
    f.rect(73, 192, 374, 25, fill="#cbd5e1", stroke="none", rx=0)
    f.text(260, 209, "液态铝（沉在槽底）", fs=11.5, weight=700, fill="#334155")
    f.rect(70, 217, 380, 12, fill="#1f2937", stroke="none", rx=0)
    f.text(460, 228, "阴极（−）", fs=11, anchor="start", weight=700)
    for x in (130, 230, 330):
        f.rect(x, 50, 60, 90, fill="#374151", stroke="#111827", rx=2)
        f.line(x + 30, 30, x + 30, 50, stroke="#111827", sw=3)
        for d in (-12, 12):
            f.circle(x + 30 + d, 150, 4, fill="#fff", stroke=C["slate"][0], sw=0.8)
    f.text(260, 22, "碳阳极（+）：氧在这里与碳结合成 CO₂ 逸出", fs=11.5, weight=700)
    f.text(260, 256, "总反应：2Al₂O₃ + 3C → 4Al + 3CO₂　（每吨铝耗电约 1.3 万—1.5 万度）", fs=11, fill=MUTED)
    f.arrow(40, 60, 40, 220, color=C["red"][0], sw=2.2)
    f.text(34, 140, "电流", fs=11, weight=700, fill=C["red"][0], anchor="end")
    return f

@fig
def carbon_fiber():
    f = Fig(520, 250, "比强度对比")
    items = [("高强度钢", 190, "slate"), ("铝合金", 200, "slate"), ("钛合金", 215, "slate"), ("碳纤维复合材料", 1100, "blue"), ("碳纤维（单丝）", 2700, "blue")]
    f.text(260, 22, "比强度 = 强度 ÷ 密度（越长越“轻而强”，数量级示意）", fs=12, weight=700)
    x0, y0, W = 130, 44, 320
    for k, (lab, v, col) in enumerate(items):
        y = y0 + k * 36
        f.text(x0 - 8, y + 17, lab, fs=11.5, anchor="end", weight=700 if col == "blue" else 400)
        ww = W * v / 2700
        f.rect(x0, y + 4, ww, 20, fill=C[col][1], stroke=C[col][0], rx=3)
        f.text(x0 + ww + 6, y + 18, f"≈{v}", fs=10.5, fill=MUTED, anchor="start")
    f.text(260, 236, "单位：kN·m/kg。复合材料只在纤维方向上最强", fs=10.5, fill=MUTED)
    return f

@fig
def graphene():
    f = Fig(520, 260, "石墨烯的蜂窝晶格")
    a = 18
    pts = set()
    for i in range(-1, 9):
        for j in range(-1, 7):
            cx = 30 + i * a * math.sqrt(3) + (j % 2) * a * math.sqrt(3) / 2
            cy = 30 + j * a * 1.5
            hexp = [(cx + a * math.cos(math.radians(60 * k + 30)), cy + a * math.sin(math.radians(60 * k + 30))) for k in range(6)]
            if all(14 < x < 300 and 14 < y < 230 for x, y in hexp):
                f.poly(hexp, stroke=C["slate"][0], sw=1.4, closed=True)
                for p in hexp: pts.add((round(p[0], 1), round(p[1], 1)))
    for x, y in pts:
        f.circle(x, y, 3.2, fill=INK, stroke="#fff", sw=0.5)
    f.text(160, 250, "每个碳原子连着 3 个邻居，厚度只有一个原子", fs=11, fill=MUTED)
    # nanotube
    f.text(410, 30, "卷起来 → 碳纳米管", fs=12, weight=700, fill=C["blue"][0])
    f.rect(340, 44, 140, 50, fill=C["blue"][1], stroke=C["blue"][0], rx=25)
    for k in range(6):
        f.path(f"M{360+k*20},46 Q{352+k*20},69 {360+k*20},92", stroke=C["blue"][0], sw=0.9)
    f.text(410, 132, "叠起来 → 石墨", fs=12, weight=700, fill=C["amber"][0])
    for k in range(4):
        f.poly([(345, 150 + k * 18), (470, 150 + k * 18), (490, 140 + k * 18), (365, 140 + k * 18)], stroke=C["amber"][0], fill=C["amber"][1], sw=1, closed=True)
    f.text(410, 228, "层间结合很弱，用胶带就能撕下一层", fs=10.5, fill=MUTED)
    return f

def main():
    only = set(sys.argv[1:])
    for name, fn in FIGS.items():
        if only and name not in only: continue
        fn().save(OUT / f"{name}.svg")
    print("wrote", len(FIGS) if not only else len(only), "figures to", OUT)

if __name__ == "__main__":
    main()
