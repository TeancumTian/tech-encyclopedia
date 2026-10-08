#!/usr/bin/env python3
"""Generate all diagrams for 第 1 篇「能源与动力」 -> assets/figs/energy/*.svg

Also provides `concept_map_layout()`, the shared full-page map layout reused by
figs_electronics.py and figs_internet.py.
"""
from __future__ import annotations
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from svgkit import Fig, C, INK, MUTED, tw

OUT = Path(__file__).resolve().parents[1] / "assets" / "figs" / "energy"
FIGS = {}

def fig(fn):
    FIGS[fn.__name__.replace("_", "-")] = fn
    return fn


# ------------------------------------------------------------------ shared map layout
def concept_map_layout(title, subtitle, layers, hist, sides, footer, flow_note, upward=False,
                       hist_title="关键年份", top=78, bottom=808):
    """layers: list of (name, color, [chips]) in reading order (top->bottom unless upward)."""
    f = Fig(680, 940, title)
    f.text(340, 30, title, fs=21, weight=700)
    f.text(340, 52, subtitle, fs=11.5, fill=MUTED)
    X, W = 168, 344
    # measure rows per layer
    def rows_for(items):
        n, cx = 1, X + 12
        for it in items:
            w = tw(it, 11) + 12
            if cx + w > X + W - 10:
                n, cx = n + 1, X + 12
            cx += w + 6
        return n
    need = [40 + 24 * rows_for(it) for _, _, it in layers]
    gap = 14
    avail = bottom - top - gap * (len(layers) - 1)
    scale = avail / sum(need)
    hs = [n * scale for n in need]
    order = list(range(len(layers)))
    ys, y = [], top
    seq = list(reversed(order)) if upward else order
    pos = {}
    for i in seq:
        pos[i] = y
        y += hs[i] + gap
    for i, (name, col, items) in enumerate(layers):
        y, h = pos[i], hs[i]
        dark, light = C[col]
        f.rect(X, y, W, h, fill=light, stroke=dark, sw=1.4, rx=8)
        f.text(X + 12, y + 21, name, fs=14, fill=dark, weight=700, anchor="start")
        cx, cy = X + 12, y + 31 + (h - need[i]) / 2
        for it in items:
            w = tw(it, 11) + 12
            if cx + w > X + W - 10:
                cx, cy = X + 12, cy + 24
            star = it.endswith("★")
            f.rect(cx, cy, w, 19, fill=dark if star else "#fff", stroke=dark, sw=0.8, rx=9)
            f.text(cx + w / 2, cy + 13.5, it, fs=11, fill="#fff" if star else INK, weight=700 if star else 400)
            cx += w + 6
    # arrows between consecutive layers in reading order
    for a, b in zip(order, order[1:]):
        ya_bot = pos[a] + hs[a]; yb_top = pos[b]
        dark = C[layers[a][1]][0]
        if not upward:
            f.arrow(X + W / 2, ya_bot + 1, X + W / 2, yb_top - 1, color=dark, sw=2.2, size=9)
        else:
            f.arrow(X + W / 2, ya_bot + gap if False else pos[a] - 1, X + W / 2, pos[b] + hs[b] + 1, color=dark, sw=2.2, size=9)
    f.text(X + W / 2, bottom + 22, flow_note, fs=11.5, fill=C["blue"][0], weight=700)
    # left timeline
    LX = 10
    f.text(LX + 70, top + 12, hist_title, fs=14, weight=700, fill=C["slate"][0])
    y0 = top + 36
    step = (bottom - 14 - y0) / (len(hist) - 1)
    f.line(LX + 18, y0 - 6, LX + 18, y0 + step * (len(hist) - 1) + 6, stroke=C["slate"][0], sw=2)
    for k, (yr, nm) in enumerate(hist):
        yy = y0 + k * step
        f.circle(LX + 18, yy, 4.5, fill=C["slate"][0], stroke="#fff", sw=1)
        f.text(LX + 28, yy + 4, yr, fs=10.5, fill=MUTED, anchor="start", weight=700)
        f.text(LX + 60, yy + 4, nm, fs=11.5, anchor="start")
    # right side boxes
    RX, y = 524, top + 4
    for t, col, items in sides:
        dark, light = C[col]
        h = 34 + 21 * len(items)
        f.rect(RX, y, 148, h, fill=light, stroke=dark, sw=1.2, rx=8)
        f.text(RX + 74, y + 22, t, fs=13, fill=dark, weight=700)
        for k, it in enumerate(items):
            f.text(RX + 10, y + 43 + 21 * k, "· " + it, fs=11, anchor="start")
        y += h + 14
    # footer
    f.rect(10, 860, 660, 66, fill="#f9fafb", stroke="#d1d5db", rx=8)
    f.text(340, 882, "和其他篇的接口", fs=12.5, weight=700)
    for k, line in enumerate(footer):
        f.text(340, 904 + 17 * k, line, fs=11, fill=MUTED)
    return f


@fig
def concept_map():
    layers = [
        ("① 能量从哪来", "amber", ["煤 · 石油 · 天然气", "石油钻探", "水力压裂", "LNG", "核裂变★", "核聚变★",
                                  "水力", "风力★", "海上风电", "光伏★", "钙钛矿", "光热", "地热", "潮汐", "生物燃料", "氢能"]),
        ("② 把热和流动变成功", "red", ["蒸汽机★", "汽轮机", "内燃机★", "柴油机", "燃气轮机", "斯特林",
                                     "水轮机", "联合循环", "热电联产", "热泵", "制冷★", "空调"]),
        ("③ 发电与输电", "blue", ["电网★", "交直流之争", "高压直流", "特高压", "智能电网", "微电网",
                                 "调峰", "需求响应", "虚拟电厂", "电力市场"]),
        ("④ 把能量存起来", "green", ["电池★", "铅酸", "锂离子★", "磷酸铁锂", "钠离子", "固态电池",
                                    "液流电池", "电网级储能", "抽水蓄能", "超级电容", "电解水制氢", "燃料电池"]),
        ("⑤ 用起来：光与热", "purple", ["煤气灯", "白炽灯", "荧光灯", "LED（见第 2 篇）", "冰箱 · 空调"]),
        ("怎样比较不同能源", "slate", ["度电成本 LCOE", "容量因子", "能源投资回报率", "核安全与核事故", "乏燃料"]),
    ]
    hist = [("1712", "纽科门蒸汽机"), ("1769", "瓦特冷凝器"), ("1800", "伏打电堆"), ("1859", "石油钻井"),
            ("1876", "四冲程内燃机"), ("1882", "第一座电站"), ("1884", "汽轮机"), ("1888", "交直流之争"),
            ("1942", "第一座反应堆"), ("1954", "硅太阳能电池"), ("1957", "压水堆核电"), ("1991", "锂离子电池"),
            ("2009", "特高压"), ("2022", "聚变点火"), ("2025", "光伏累计近 3 TW")]
    sides = [
        ("第一性原理", "red", ["能量守恒", "熵增：热不能全变功", "卡诺效率 ∝ 温差", "能量密度", "电磁感应", "质能等价 E=mc²"]),
        ("能量密度对比", "amber", ["汽油 ≈ 46 MJ/kg", "煤 ≈ 24 MJ/kg", "锂电池 ≈ 0.9 MJ/kg", "铀-235 ≈ 8×10⁷ MJ/kg"]),
        ("2025 年发电结构", "teal", ["煤电 ≈ 33%", "可再生 ≈ 34%", "其中风 · 光 ≈ 17%", "核电 ≈ 9%", "（Ember 2026 数据）"]),
    ]
    footer = ["发电机 · 电动机 · 变压器 → 第 2 篇「电与电子」　汽车 · 船舶 → 第 8 篇　飞机 · 火箭发动机 → 第 9 篇",
              "碳排放与碳捕集 → 第 15 篇「环境与气候技术」　核武器 → 第 13 篇「安全与国防」"]
    return concept_map_layout("能源与动力 · 知识地图",
                              "从上往下读：能量从自然界来，经热机或发电机转换，通过电网送达，存进电池，最后变成光、热和动力。",
                              layers, hist, sides, footer, "↓ 每一步转换都有损失：能量守恒，但能用的能量越来越少（熵增）")


# ------------------------------------------------------------------ 热机
@fig
def steam_engine():
    f = Fig(680, 320, "瓦特蒸汽机")
    # boiler
    f.rect(30, 150, 150, 110, fill=C["slate"][1], stroke=C["slate"][0], sw=1.6, rx=14)
    f.text(105, 176, "锅炉", fs=14, weight=700, fill=C["slate"][0])
    for k in range(4):
        x = 52 + k * 30
        f.path(f"M{x},250 q8,-14 0,-26 q-8,-12 0,-24", stroke=C["red"][0], sw=2)
    f.text(105, 290, "烧煤加热", fs=11.5, fill=C["red"][0], weight=700)
    # steam pipe
    f.path("M120,150 L120,90 L250,90", stroke=C["amber"][0], sw=6)
    f.text(185, 82, "蒸汽", fs=11.5, fill=C["amber"][0], weight=700)
    # cylinder
    f.rect(250, 60, 120, 170, fill="#fff7ed", stroke=INK, sw=2, rx=4)
    f.rect(258, 120, 104, 22, fill=C["slate"][0], stroke=INK, rx=2)
    f.text(310, 135, "活塞", fs=11, fill="#fff", weight=700)
    f.rect(304, 20, 12, 100, fill=C["slate"][1], stroke=INK, rx=2)
    f.text(310, 54, "", fs=10)
    f.text(310, 252, "气缸始终保持高温", fs=11.5, fill=C["red"][0], weight=700)
    f.arrow(310, 150, 310, 210, color=C["amber"][0], sw=2, label="", size=9)
    f.text(325, 190, "蒸汽推动", fs=10.5, fill=C["amber"][0], anchor="start")
    # beam
    f.line(310, 20, 560, 20, stroke=C["slate"][0], sw=6)
    f.circle(435, 20, 7, fill="#fff", stroke=INK, sw=2)
    f.text(435, 44, "横梁 / 曲柄 → 旋转", fs=11, fill=MUTED)
    # condenser
    f.path("M370,215 L470,215 L470,240", stroke=C["amber"][0], sw=5)
    f.rect(430, 240, 120, 60, fill=C["blue"][1], stroke=C["blue"][0], sw=1.8, rx=8)
    f.text(490, 264, "分离冷凝器", fs=13, weight=700, fill=C["blue"][0])
    f.text(490, 283, "泡在冷水里", fs=10.5, fill=C["blue"][0])
    f.arrow(430, 290, 190, 240, color=C["blue"][0], sw=1.6, dash="5 4")
    f.text(300, 280, "冷凝水送回锅炉", fs=10.5, fill=C["blue"][0])
    # flywheel
    f.circle(600, 130, 55, fill="none", stroke=C["slate"][0], sw=5)
    f.circle(600, 130, 6, fill=C["slate"][0], stroke="none")
    f.line(560, 20, 600, 130, stroke=C["slate"][0], sw=3)
    f.text(600, 210, "飞轮：输出转动", fs=11.5, weight=700, fill=C["slate"][0])
    f.rect(560, 240, 110, 60, fill="#fff", stroke=C["red"][0], rx=8)
    f.lines(615, 262, ["纽科门机：冷水浇气缸", "瓦特：在别处冷凝", "→ 省煤约 3/4"], fs=10, fill=INK)
    return f


@fig
def internal_combustion_engine():
    f = Fig(680, 330, "四冲程内燃机")
    steps = [("① 进气", "活塞下行\n吸入油气", "blue", 0.85, "in"), ("② 压缩", "活塞上行\n压到约 1/10", "purple", 0.2, None),
             ("③ 做功", "点火爆燃\n推活塞下行", "red", 0.85, "fire"), ("④ 排气", "活塞上行\n推出废气", "slate", 0.2, "out")]
    for k, (t, d, col, p, mode) in enumerate(steps):
        x = 20 + k * 165
        dark, light = C[col]
        f.text(x + 72, 28, t, fs=15, weight=700, fill=dark)
        # cylinder walls
        f.path(f"M{x+30},50 L{x+30},200 M{x+114},50 L{x+114},200", stroke=INK, sw=3)
        f.line(x + 30, 50, x + 114, 50, stroke=INK, sw=3)
        # valves
        lv = mode == "in"; rv = mode == "out"
        f.line(x + 48, 50 + (10 if lv else 0), x + 48, 30 + (10 if lv else 0), stroke=C["blue"][0], sw=3)
        f.line(x + 96, 50 + (10 if rv else 0), x + 96, 30 + (10 if rv else 0), stroke=C["slate"][0], sw=3)
        f.circle(x + 72, 46, 4, fill=C["amber"][0], stroke="none")
        py = 60 + p * 110
        fill = {"in": C["blue"][1], "fire": C["red"][1], "out": "#e5e7eb", None: C["purple"][1]}[mode]
        f.rect(x + 32, 52, 80, py - 52, fill=fill, stroke="none", rx=0)
        if mode == "fire":
            f.poly([(x + 72, 56), (x + 62, 76), (x + 72, 72), (x + 66, 94), (x + 84, 68), (x + 74, 70), (x + 80, 56)], fill=C["amber"][0], stroke=C["red"][0], sw=1, closed=True)
        f.rect(x + 32, py, 80, 26, fill=C["slate"][0], stroke=INK, rx=2)
        # rod to crank
        f.circle(x + 72, 250, 26, fill="none", stroke=MUTED, sw=1.2, dash="3 3")
        ang = {0.85: math.pi / 2, 0.2: -math.pi / 2}[p]
        cxp, cyp = x + 72 + 26 * math.cos(ang + 0.6), 250 + 26 * math.sin(ang + 0.6) * (1 if p > 0.5 else 1)
        f.line(x + 72, py + 13, cxp, cyp, stroke=INK, sw=3)
        f.circle(x + 72, 250, 4, fill=INK, stroke="none")
        dy = 1 if p > 0.5 else -1
        f.arrow(x + 136, 120, x + 136, 120 + 40 * dy if mode != "fire" else 165, color=dark, sw=2)
        f.lines(x + 72, 298, [d.replace("\n", " ")], fs=10.5, fill=dark, weight=700)
    f.text(340, 322, "曲轴转两圈完成一个循环；只有第 ③ 步对外做功", fs=11.5, fill=MUTED)
    return f


@fig
def heat_pump():
    f = Fig(520, 250, "热泵")
    f.rect(10, 40, 160, 170, fill=C["blue"][1], stroke=C["blue"][0], rx=10)
    f.text(90, 64, "室外（冷）0°C", fs=13, weight=700, fill=C["blue"][0])
    f.rect(350, 40, 160, 170, fill=C["red"][1], stroke=C["red"][0], rx=10)
    f.text(430, 64, "室内（暖）22°C", fs=13, weight=700, fill=C["red"][0])
    f.box(195, 100, 130, 60, "热泵", "slate", fs=15, sub="压缩机 + 制冷剂循环", solid=True)
    f.arrow(60, 130, 192, 130, color=C["blue"][0], sw=6, size=14)
    f.text(110, 116, "空气中的热 2 份", fs=11.5, fill=C["blue"][0], weight=700)
    f.arrow(260, 30, 260, 96, color=C["amber"][0], sw=4, size=12)
    f.text(260, 24, "电 1 份", fs=12, fill=C["amber"][0], weight=700)
    f.arrow(328, 130, 470, 130, color=C["red"][0], sw=10, size=18)
    f.text(410, 112, "送出热 3 份", fs=12, fill=C["red"][0], weight=700)
    f.text(260, 236, "能效比 COP ≈ 3：不是\u201c产生\u201d热，而是把热从冷处\u201c搬\u201d到暖处", fs=11.5, fill=INK)
    return f


@fig
def refrigeration():
    f = Fig(680, 320, "蒸气压缩制冷循环")
    # loop boxes
    f.box(250, 30, 180, 56, "冷凝器（放热）", "red", fs=13.5, sub="高压气体 → 液体，热散到室外")
    f.box(250, 234, 180, 56, "蒸发器（吸热）", "blue", fs=13.5, sub="低压液体 → 气体，从冰箱内吸热")
    f.box(520, 132, 130, 56, "压缩机", "slate", fs=14, sub="耗电做功", solid=True)
    f.box(30, 132, 130, 56, "膨胀阀", "purple", fs=14, sub="降压降温")
    f.arrow(585, 130, 432, 60, color=C["red"][0], sw=2.4, label="高温高压气", loff=(36, -6), lcolor=C["red"][0])
    f.arrow(248, 60, 96, 130, color=C["red"][0], sw=2.4, label="高压液", loff=(-30, -6), lcolor=C["red"][0])
    f.arrow(96, 190, 248, 262, color=C["blue"][0], sw=2.4, label="低温低压液", loff=(-40, 10), lcolor=C["blue"][0])
    f.arrow(432, 262, 585, 190, color=C["blue"][0], sw=2.4, label="低压气", loff=(30, 10), lcolor=C["blue"][0])
    for k in range(3):
        f.arrow(300 + k * 40, 26, 300 + k * 40, 6, color=C["red"][0], sw=1.4, size=6)
        f.arrow(300 + k * 40, 314, 300 + k * 40, 294, color=C["blue"][0], sw=1.4, size=6)
    f.text(340, 160, "制冷剂在管路里循环", fs=13, weight=700, fill=INK)
    f.text(340, 180, "液体蒸发吸热、气体凝结放热（相变）", fs=11.5, fill=MUTED)
    return f


@fig
def combined_cycle():
    f = Fig(520, 260, "联合循环电厂")
    f.box(20, 40, 150, 70, "燃气轮机", "red", fs=14, sub="燃烧 1400°C 以上")
    f.box(20, 160, 150, 60, "天然气 + 空气", "amber", fs=12.5)
    f.arrow(95, 158, 95, 112, color=C["amber"][0], sw=2)
    f.box(350, 40, 150, 70, "发电机 1", "blue", fs=14, sub="约 2/3 电力")
    f.arrow(172, 75, 348, 75, color=C["slate"][0], sw=2.4, label="转轴", loff=(0, -6))
    f.box(200, 150, 130, 70, "余热锅炉", "slate", fs=13.5, sub="约 600°C 排气\n把水烧成蒸汽")
    f.arrow(140, 112, 220, 148, color=C["red"][0], sw=2, label="高温排气", loff=(-6, -10))
    f.box(350, 150, 150, 70, "汽轮机 + 发电机 2", "blue", fs=12.5, sub="约 1/3 电力")
    f.arrow(332, 185, 348, 185, color=C["amber"][0], sw=2)
    f.text(260, 248, "单独燃气轮机效率约 40%，加上余热再利用 → 60% 以上", fs=11.5, weight=700, fill=C["green"][0])
    return f


# ------------------------------------------------------------------ 电力系统
@fig
def power_grid():
    f = Fig(680, 300, "电网")
    xs = [20, 175, 330, 485]
    f.box(xs[0], 90, 130, 70, "发电厂", "amber", fs=14, sub="约 20 千伏")
    f.box(xs[1], 90, 120, 70, "升压变电站", "red", fs=13, sub="升到 220–1000 千伏")
    f.box(xs[3], 90, 120, 70, "降压变电站", "green", fs=13, sub="降到 10 千伏")
    # transmission towers
    for k in range(3):
        tx = 330 + k * 55
        f.poly([(tx, 160), (tx + 14, 80), (tx + 28, 160)], stroke=C["slate"][0], sw=1.6)
        f.line(tx + 4, 100, tx + 24, 100, stroke=C["slate"][0], sw=1.4)
    f.path("M318,100 Q360,118 389,100 Q417,118 444,100 Q470,118 482,104", stroke=C["red"][0], sw=2)
    f.text(400, 72, "高压输电线（远距离）", fs=12, weight=700, fill=C["red"][0])
    f.arrow(152, 125, 173, 125, color=INK, sw=2)
    f.arrow(297, 125, 318, 125, color=INK, sw=2)
    f.arrow(605, 125, 625, 125, color=INK, sw=2)
    f.lines(650, 110, ["工厂", "家庭", "220 伏"], fs=11.5, weight=700, fill=C["green"][0])
    # formula
    f.rect(40, 200, 600, 82, fill="#fff", stroke=C["blue"][0], rx=10)
    f.text(340, 224, "为什么要升高电压？功率 P = 电压 U × 电流 I，线路损耗 = I² × R", fs=13, weight=700, fill=C["blue"][0])
    f.text(340, 248, "电压提高 10 倍 → 同样功率下电流降到 1/10 → 损耗降到 1/100", fs=12, fill=INK)
    f.text(340, 270, "电网每一秒都必须让发电 = 用电，否则频率偏离 50 赫兹", fs=11.5, fill=MUTED)
    return f


@fig
def capacity_factor():
    f = Fig(520, 250, "容量因子")
    data = [("核电", 0.90, "red"), ("燃煤", 0.55, "slate"), ("水电", 0.40, "blue"), ("海上风电", 0.40, "teal"),
            ("陆上风电", 0.30, "green"), ("光伏", 0.17, "amber")]
    x0, y0, bw = 110, 30, 250
    for k, (n, v, col) in enumerate(data):
        y = y0 + k * 30
        f.text(x0 - 10, y + 16, n, fs=12, anchor="end", weight=700)
        f.rect(x0, y + 2, bw, 20, fill="#f3f4f6", stroke="#e5e7eb", rx=3)
        f.rect(x0, y + 2, bw * v, 20, fill=C[col][0], stroke="none", rx=3)
        f.text(x0 + bw * v + 6, y + 17, f"约 {int(v*100)}% → {v*8.76:.1f} 太瓦时/年", fs=10.5, anchor="start", fill=INK)
    f.text(260, 236, "同为 1 吉瓦装机，全年满发可发 8.76 太瓦时；数值为典型值，因地而异", fs=10.5, fill=MUTED)
    return f


# ------------------------------------------------------------------ 核能
@fig
def nuclear_fission_reactor():
    f = Fig(680, 330, "核裂变链式反应与反应堆")
    # chain reaction left
    f.text(150, 24, "链式反应", fs=14, weight=700, fill=C["red"][0])
    def nuc(x, y, r=13, col="amber"):
        f.circle(x, y, r, fill=C[col][1], stroke=C[col][0], sw=1.6)
    def neu(x, y):
        f.circle(x, y, 4, fill=C["blue"][0], stroke="none")
    neu(20, 160); f.arrow(26, 160, 52, 160, color=C["blue"][0], sw=1.4, size=6)
    nuc(66, 160, 15); f.text(66, 192, "U-235", fs=10, fill=MUTED)
    gen = [(66, 160)]
    pts1 = [(140, 90), (140, 160), (140, 230)]
    for (x, y) in pts1:
        f.arrow(84, 160, x - 18, y, color=C["blue"][0], sw=1.2, size=6)
        nuc(x, y)
    for (x, y) in pts1:
        for dy in (-22, 0, 22):
            f.arrow(x + 16, y, 212, y + dy, color=C["blue"][0], sw=1, size=5)
            nuc(221, y + dy, 8)
    f.text(150, 290, "每次裂变放出 2–3 个中子", fs=11, fill=INK)
    f.text(150, 308, "若都引发新裂变 → 指数增长", fs=11, fill=C["red"][0], weight=700)
    # reactor right
    RX = 300
    f.text(RX + 120, 24, "反应堆：把增长控制在\u201c恰好 1\u201d", fs=14, weight=700, fill=C["blue"][0])
    f.rect(RX + 20, 40, 200, 240, fill=C["blue"][1], stroke=C["blue"][0], sw=2, rx=20)
    f.text(RX + 120, 296, "压力容器（水既是慢化剂也是冷却剂）", fs=10.5, fill=C["blue"][0])
    for k in range(4):
        x = RX + 50 + k * 45
        f.rect(x, 110, 14, 140, fill=C["amber"][0], stroke="none", rx=3)
    f.text(RX + 120, 268, "燃料棒", fs=10.5, fill=C["amber"][0], weight=700)
    for k in range(3):
        x = RX + 72 + k * 45
        f.rect(x, 30, 10, 150, fill=INK, stroke="none", rx=2)
    f.text(RX + 120, 100, "", fs=10)
    f.arrow(RX + 240, 140, RX + 240, 70, color=INK, sw=1.6)
    f.text(RX + 248, 104, "控制棒：", fs=11, anchor="start", weight=700)
    f.text(RX + 248, 120, "插入吸中子 → 减速", fs=10.5, anchor="start")
    f.text(RX + 248, 136, "抽出 → 加速", fs=10.5, anchor="start")
    f.arrow(RX + 222, 230, RX + 300, 230, color=C["red"][0], sw=2.4)
    f.text(RX + 262, 220, "热水", fs=11, fill=C["red"][0], weight=700)
    f.box(RX + 302, 200, 70, 60, "蒸汽\n发电机", "slate", fs=11.5)
    f.text(RX + 340, 176, "", fs=10)
    return f


@fig
def fusion_power():
    f = Fig(680, 300, "核聚变")
    f.text(170, 26, "氘—氚聚变", fs=14, weight=700, fill=C["red"][0])
    def nucleus(x, y, p, n):
        k = 0
        for i in range(p + n):
            a = i * 2 * math.pi / max(1, p + n)
            col = C["red"][0] if i < p else C["slate"][0]
            f.circle(x + 8 * math.cos(a) * (1 if p + n > 1 else 0), y + 8 * math.sin(a) * (1 if p + n > 1 else 0), 7, fill=col, stroke="#fff", sw=1)
    nucleus(50, 90, 1, 1); f.text(50, 124, "氘 D", fs=11)
    nucleus(50, 190, 1, 2); f.text(50, 226, "氚 T", fs=11)
    f.arrow(72, 100, 140, 135, color=INK); f.arrow(72, 180, 140, 150, color=INK)
    f.circle(160, 142, 22, fill=C["amber"][1], stroke=C["amber"][0], sw=2)
    f.text(160, 147, "1 亿°C", fs=10, weight=700)
    f.arrow(184, 130, 250, 90, color=INK); f.arrow(184, 154, 250, 200, color=INK)
    nucleus(270, 80, 2, 2); f.text(270, 115, "氦-4（3.5 MeV）", fs=11)
    f.circle(270, 205, 7, fill=C["slate"][0], stroke="#fff"); f.text(270, 232, "中子（14.1 MeV）", fs=11)
    f.text(170, 270, "质量亏损约 0.4% → E = mc² 释放能量", fs=11.5, weight=700, fill=C["red"][0])
    # right: two routes
    f.rect(360, 40, 300, 110, fill=C["blue"][1], stroke=C["blue"][0], rx=10)
    f.text(510, 62, "磁约束（托卡马克）", fs=13, weight=700, fill=C["blue"][0])
    f.path("M400,105 C400,75 480,75 480,105 C480,135 400,135 400,105 Z", stroke=C["blue"][0], sw=6)
    f.path("M415,105 C415,90 465,90 465,105 C465,120 415,120 415,105 Z", stroke=C["pink"][0], sw=2.5)
    f.lines(570, 92, ["强磁场把等离子体", "关在环形\u201c磁笼\u201d里", "ITER · EAST · WEST"], fs=10.5)
    f.rect(360, 165, 300, 110, fill=C["purple"][1], stroke=C["purple"][0], rx=10)
    f.text(510, 187, "惯性约束（激光）", fs=13, weight=700, fill=C["purple"][0])
    f.circle(440, 230, 8, fill=C["amber"][0], stroke="none")
    for a in range(0, 360, 45):
        r = math.radians(a)
        f.arrow(440 + 34 * math.cos(r), 230 + 34 * math.sin(r), 440 + 12 * math.cos(r), 230 + 12 * math.sin(r), color=C["purple"][0], sw=1.2, size=5)
    f.lines(570, 218, ["激光瞬间压缩燃料丸", "NIF 2022 年首次", "实现能量增益"], fs=10.5)
    return f


# ------------------------------------------------------------------ 可再生
@fig
def pumped_storage():
    f = Fig(520, 250, "抽水蓄能")
    f.path("M10,70 L120,70 L170,220 L510,220", stroke=C["slate"][0], sw=2, fill="none")
    f.rect(15, 50, 100, 22, fill=C["blue"][1], stroke=C["blue"][0], rx=2)
    f.text(65, 42, "上水库", fs=12.5, weight=700, fill=C["blue"][0])
    f.rect(330, 196, 170, 24, fill=C["blue"][1], stroke=C["blue"][0], rx=2)
    f.text(415, 188, "下水库", fs=12.5, weight=700, fill=C["blue"][0])
    f.path("M110,72 L300,200", stroke=C["blue"][0], sw=6)
    f.box(270, 150, 90, 40, "水泵水轮机", "slate", fs=11.5, solid=True)
    f.arrow(230, 110, 175, 76, color=C["amber"][0], sw=2.4)
    f.lines(250, 100, ["电多（白天光伏）", "→ 抽水上山"], fs=11, fill=C["amber"][0], weight=700, anchor="start")
    f.arrow(200, 130, 255, 165, color=C["blue"][0], sw=2.4)
    f.lines(130, 160, ["电少（晚高峰）", "→ 放水发电"], fs=11, fill=C["blue"][0], weight=700)
    f.text(260, 244, "往返效率约 70–80%；全球装机约 2 亿千瓦，是最大的储能方式", fs=11, fill=MUTED)
    return f


@fig
def wind_turbine():
    f = Fig(680, 320, "风力发电机")
    # turbine
    cx, cy = 140, 110
    f.poly([(cx - 6, cy), (cx - 12, 300), (cx + 12, 300), (cx + 6, cy)], fill="#e5e7eb", stroke=C["slate"][0], closed=True)
    for a in (-90, 30, 150):
        r = math.radians(a)
        ex, ey = cx + 95 * math.cos(r), cy + 95 * math.sin(r)
        nx, ny = -math.sin(r) * 9, math.cos(r) * 9
        f.poly([(cx, cy), (cx + nx, cy + ny), (ex, ey)], fill="#f9fafb", stroke=C["slate"][0], closed=True, sw=1.4)
    f.rect(cx - 4, cy - 12, 50, 24, fill=C["slate"][0], stroke="none", rx=6)
    f.circle(cx, cy, 8, fill="#fff", stroke=C["slate"][0], sw=2)
    f.text(cx + 34, cy - 18, "机舱：齿轮箱 + 发电机", fs=10, anchor="start", fill=MUTED)
    for k in range(3):
        f.arrow(10, 70 + k * 40, 40, 70 + k * 40, color=C["teal"][0], sw=1.6)
    f.text(25, 56, "风", fs=11, weight=700, fill=C["teal"][0])
    # blade cross-section lift
    f.text(360, 30, "叶片剖面：像机翼一样产生升力", fs=12.5, weight=700, fill=C["blue"][0])
    f.path("M305,80 C330,57 400,60 445,78 C400,86 330,92 305,80 Z", fill=C["blue"][1], stroke=C["blue"][0], sw=1.6)
    f.arrow(262, 82, 300, 80, color=C["teal"][0], sw=1.6)
    f.arrow(375, 74, 375, 42, color=C["red"][0], sw=2.2)
    f.text(382, 50, "升力 → 带动转子", fs=10.5, anchor="start", fill=C["red"][0])
    # power curve
    gx, gy, gw, gh = 470, 50, 190, 170
    f.line(gx, gy + gh, gx + gw, gy + gh, stroke=INK); f.line(gx, gy, gx, gy + gh, stroke=INK)
    pts = []
    for i in range(0, 101):
        v = i / 100 * 25
        p = 0 if v < 3 else (min(1, ((v - 3) / 9) ** 3) if v < 12 else 1)
        if v > 24: p = 0
        pts.append((gx + v / 25 * gw, gy + gh - p * (gh - 20)))
    f.poly(pts, stroke=C["green"][0], sw=2.2)
    f.text(gx + gw / 2, gy + gh + 18, "风速（米/秒）", fs=10.5, fill=MUTED)
    f.text(gx + 6, gy - 6, "功率", fs=10.5, fill=MUTED, anchor="start")
    f.text(gx + 60, gy + 70, "∝ 风速³", fs=12, weight=700, fill=C["green"][0])
    f.text(gx + 150, gy + 12, "额定", fs=10, fill=MUTED)
    f.text(gx + 12, gy + gh - 6, "切入", fs=10, fill=MUTED, anchor="start")
    # formula band
    f.rect(240, 130, 210, 150, fill="#fff", stroke=C["teal"][0], rx=10)
    f.lines(345, 156, ["风的功率 P = ½ ρ A v³", "", "风速翻倍 → 功率 8 倍", "叶片加长一倍 → 扫风面积 4 倍", "", "贝茨极限：最多取走 59%"], fs=11.5, fill=INK)
    f.text(345, 300, "", fs=10)
    f.text(560, 300, "风速过大时顺桨停机保护", fs=10.5, fill=MUTED)
    return f


@fig
def solar_pv():
    f = Fig(680, 320, "光伏电池")
    X, W = 160, 300
    f.rect(X, 60, W, 18, fill=C["slate"][0], stroke="none", rx=2)
    for k in range(6):
        f.rect(X + 20 + k * 48, 52, 8, 26, fill="#9ca3af", stroke="none")
    f.text(X + W + 10, 72, "正面电极（栅线）", fs=11, anchor="start", fill=MUTED)
    f.rect(X, 78, W, 70, fill=C["blue"][1], stroke=C["blue"][0], rx=0)
    f.text(X + W + 10, 118, "N 型硅（富电子）", fs=11.5, anchor="start", weight=700, fill=C["blue"][0])
    f.rect(X, 148, W, 22, fill="#fff", stroke=C["purple"][0], rx=0, dash="4 3")
    f.text(X + W + 10, 164, "PN 结：内建电场", fs=11.5, anchor="start", weight=700, fill=C["purple"][0])
    f.rect(X, 170, W, 90, fill=C["red"][1], stroke=C["red"][0], rx=0)
    f.text(X + W + 10, 220, "P 型硅（富空穴）", fs=11.5, anchor="start", weight=700, fill=C["red"][0])
    f.rect(X, 260, W, 16, fill=C["slate"][0], stroke="none", rx=2)
    f.text(X + W + 10, 274, "背面电极", fs=11, anchor="start", fill=MUTED)
    # photons
    for k in range(3):
        x = X + 70 + k * 80
        f.path(f"M{x-40},10 l8,8 l-6,4 l10,10 l-6,4 l14,14", stroke=C["amber"][0], sw=2)
        f.arrow(x - 20, 50, x - 6, 150, color=C["amber"][0], sw=1.4, size=7)
    f.text(70, 24, "阳光（光子）", fs=12, weight=700, fill=C["amber"][0])
    # electron hole pair
    f.circle(X + 150, 158, 6, fill=C["blue"][0], stroke="none")
    f.text(X + 150, 162, "−", fs=10, fill="#fff", weight=700)
    f.circle(X + 175, 162, 6, fill="#fff", stroke=C["red"][0], sw=2)
    f.text(X + 175, 166, "+", fs=10, fill=C["red"][0], weight=700)
    f.arrow(X + 150, 150, X + 150, 92, color=C["blue"][0], sw=1.8)
    f.arrow(X + 175, 172, X + 175, 240, color=C["red"][0], sw=1.8)
    f.text(X + 115, 120, "电子↑", fs=10.5, fill=C["blue"][0], weight=700)
    f.text(X + 210, 215, "空穴↓", fs=10.5, fill=C["red"][0], weight=700)
    # external circuit
    f.path(f"M{X},69 L60,69 L60,268 L{X},268", stroke=INK, sw=2)
    f.circle(60, 168, 20, fill=C["amber"][1], stroke=C["amber"][0], sw=2)
    f.text(60, 173, "负载", fs=11, weight=700)
    f.arrow(60, 100, 60, 140, color=C["blue"][0], sw=1.6)
    f.text(30, 300, "外电路中电子从 N 侧流回 P 侧，点亮负载", fs=11, fill=MUTED, anchor="start")
    f.text(470, 300, "晶硅电池效率约 22–25%", fs=11, fill=MUTED, anchor="start")
    return f


# ------------------------------------------------------------------ 储能
@fig
def battery():
    f = Fig(680, 300, "电池的基本结构")
    f.rect(140, 70, 400, 170, fill="#f9fafb", stroke=INK, sw=1.6, rx=8)
    f.rect(160, 85, 90, 140, fill=C["slate"][1], stroke=C["slate"][0], sw=1.6, rx=4)
    f.text(205, 150, "负极", fs=14, weight=700, fill=C["slate"][0])
    f.text(205, 170, "易失电子", fs=10.5, fill=MUTED)
    f.text(205, 186, "（氧化）", fs=10.5, fill=MUTED)
    f.rect(430, 85, 90, 140, fill=C["red"][1], stroke=C["red"][0], sw=1.6, rx=4)
    f.text(475, 150, "正极", fs=14, weight=700, fill=C["red"][0])
    f.text(475, 170, "得电子", fs=10.5, fill=MUTED)
    f.text(475, 186, "（还原）", fs=10.5, fill=MUTED)
    f.rect(250, 85, 180, 140, fill=C["blue"][1], stroke="none", rx=0)
    f.line(340, 85, 340, 225, stroke=MUTED, sw=1.2, dash="4 3")
    f.text(340, 104, "电解质 + 隔膜", fs=11.5, weight=700, fill=C["blue"][0])
    for k in range(3):
        y = 135 + k * 28
        f.arrow(270, y, 410, y, color=C["teal"][0], sw=1.6)
        f.circle(300 + k * 30, y, 7, fill=C["teal"][1], stroke=C["teal"][0])
        f.text(300 + k * 30, y + 4, "+", fs=10, weight=700, fill=C["teal"][0])
    f.text(340, 214, "离子在内部穿过", fs=10.5, fill=C["teal"][0], weight=700)
    # external circuit
    f.path("M205,85 L205,40 L475,40 L475,85", stroke=INK, sw=2)
    f.circle(340, 40, 16, fill=C["amber"][1], stroke=C["amber"][0], sw=2)
    f.text(340, 45, "灯", fs=11, weight=700)
    f.arrow(240, 40, 310, 40, color=C["blue"][0], sw=2)
    f.arrow(372, 40, 440, 40, color=C["blue"][0], sw=2)
    f.text(270, 30, "电子 e⁻", fs=11, fill=C["blue"][0], weight=700)
    f.text(340, 268, "电压由两极材料\u201c抢电子\u201d能力之差决定；容量由能参与反应的材料多少决定", fs=11.5, fill=INK)
    f.text(340, 288, "充电电池：外加电压把电子和离子推回去，反应逆转", fs=11, fill=MUTED)
    return f


@fig
def lithium_ion():
    f = Fig(680, 300, "锂离子电池")
    # graphite anode layers
    f.text(160, 30, "负极：石墨（层状）", fs=13, weight=700, fill=C["slate"][0])
    for k in range(6):
        y = 60 + k * 30
        f.line(60, y, 260, y, stroke=C["slate"][0], sw=3)
    f.text(510, 30, "正极：金属氧化物（如磷酸铁锂）", fs=13, weight=700, fill=C["red"][0])
    for r in range(6):
        for c in range(6):
            f.rect(420 + c * 30, 52 + r * 30, 18, 18, fill=C["red"][1], stroke=C["red"][0], sw=1, rx=2)
    # separator
    f.line(340, 50, 340, 230, stroke=MUTED, sw=1.6, dash="5 4")
    f.text(340, 246, "隔膜（只让锂离子通过）", fs=10.5, fill=MUTED)
    # ions
    for k, (x, y) in enumerate([(100, 75), (180, 105), (130, 165), (220, 195)]):
        f.circle(x, y, 7, fill=C["amber"][0], stroke="#fff", sw=1)
    for (x, y) in [(445, 120), (505, 180)]:
        f.circle(x, y, 7, fill=C["amber"][0], stroke="#fff", sw=1)
    f.arrow(270, 110, 410, 110, color=C["green"][0], sw=2.4, label="放电：Li⁺ → 正极", loff=(0, -8), lcolor=C["green"][0])
    f.arrow(410, 160, 270, 160, color=C["purple"][0], sw=2.4, label="充电：Li⁺ → 负极", loff=(0, 20), lcolor=C["purple"][0])
    f.circle(560, 270, 7, fill=C["amber"][0], stroke="#fff"); f.text(572, 274, "锂离子 Li⁺", fs=10.5, anchor="start")
    f.text(240, 278, "锂离子像坐摇椅一样在两极之间来回\u201c摇\u201d，电子则走外电路", fs=11.5, fill=INK)
    return f


def main():
    only = set(sys.argv[1:])
    for name, fn in FIGS.items():
        if only and name not in only: continue
        fn().save(OUT / f"{name}.svg")
    print("wrote", len(FIGS) if not only else len(only), "figures to", OUT)

if __name__ == "__main__":
    main()
