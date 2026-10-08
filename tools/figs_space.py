#!/usr/bin/env python3
"""Generate all diagrams for 第 9 篇「航天与空间」 -> assets/figs/space/*.svg"""
from __future__ import annotations
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from svgkit import Fig, C, INK, MUTED, tw

OUT = Path(__file__).resolve().parents[1] / "assets" / "figs" / "space"
FIGS = {}

def fig(fn):
    FIGS[fn.__name__.replace("_", "-")] = fn
    return fn

def chips(f, x, y, w, items, color, fs=10.5, gap=5, solid=()):
    cx, cy = x, y
    for it in items:
        cw = tw(it, fs) + 12
        if cx + cw > x + w:
            cx, cy = x, cy + fs * 1.6 + 5
        dark, light = C[color]
        s = it in solid
        f.rect(cx, cy, cw, fs * 1.6, fill=dark if s else "#fff", stroke=dark, sw=0.9, rx=fs * 0.8)
        f.text(cx + cw / 2, cy + fs * 1.13, it, fs=fs, fill="#fff" if s else INK, weight=700 if s else 400)
        cx += cw + gap
    return cy + fs * 1.6

def ellipse(f, cx, cy, rx, ry, stroke=INK, sw=1.4, fill="none", dash=None):
    d = f"M{cx-rx},{cy} A{rx},{ry} 0 1,0 {cx+rx},{cy} A{rx},{ry} 0 1,0 {cx-rx},{cy} Z"
    f.path(d, stroke=stroke, sw=sw, fill=fill, dash=dash)

def sat(f, x, y, col="blue", s=1.0):
    dark, light = C[col]
    f.rect(x - 6 * s, y - 5 * s, 12 * s, 10 * s, fill=dark, stroke=dark, rx=1.5)
    f.rect(x - 20 * s, y - 3 * s, 12 * s, 6 * s, fill=light, stroke=dark, sw=0.8, rx=0.5)
    f.rect(x + 8 * s, y - 3 * s, 12 * s, 6 * s, fill=light, stroke=dark, sw=0.8, rx=0.5)

CORE = {"火箭", "火箭方程", "可回收火箭", "轨道与宇宙速度", "卫星导航", "阿波罗登月"}

# ------------------------------------------------------------------ concept map
@fig
def concept_map():
    f = Fig(680, 940, "航天与空间 知识地图")
    f.text(340, 30, "航天与空间 · 知识地图", fs=21, weight=700)
    f.text(340, 52, "左边按“离地球多远”排列，右边是四条主线。实心为核心词条。", fs=11, fill=MUTED)
    rows = [
        ("星际空间", "> 180 亿公里", ["旅行者 1 号（空间探测器）"], "slate"),
        ("行星际", "上亿公里", ["空间探测器", "火星车", "引力弹弓", "核电池", "行星防御"], "purple"),
        ("日地 L2 点", "约 150 万公里", ["太空望远镜（韦布）"], "purple"),
        ("月球", "约 38 万公里", ["阿波罗登月", "重返月球"], "amber"),
        ("静止轨道", "35786 公里", ["地球静止轨道", "通信卫星", "气象卫星"], "teal"),
        ("中轨道", "约 2 万公里", ["卫星导航"], "teal"),
        ("近地轨道", "200–2000 公里", ["空间站", "遥感", "侦察卫星", "立方星", "太空垃圾", "卫星互联网"], "blue"),
        ("亚轨道", "约 100 公里", ["V-2 火箭", "太空旅游"], "blue"),
        ("地面", "发射与回收", ["火箭", "可回收火箭", "星舰"], "red"),
    ]
    Y0, RH, X0, W = 72, 66, 10, 322
    for i, (name, dist, items, col) in enumerate(rows):
        y = Y0 + i * RH
        dark, light = C[col]
        f.rect(X0, y, W, RH - 6, fill=light, stroke=dark, sw=0.8, rx=6)
        f.text(X0 + 10, y + 22, name, fs=12.5, weight=700, anchor="start", fill=dark)
        f.text(X0 + 10, y + 40, dist, fs=10, anchor="start", fill=MUTED)
        chips(f, X0 + 100, y + 8, W - 108, items, col, fs=10.5, solid=CORE)
    # earth arc
    f.path(f"M{X0},{Y0 + 9 * RH + 22} Q{X0 + W/2},{Y0 + 9 * RH - 8} {X0 + W},{Y0 + 9 * RH + 22}", stroke=C["blue"][0], sw=2, fill=C["blue"][1])
    f.text(X0 + W / 2, Y0 + 9 * RH + 14, "地 球", fs=12, weight=700, fill=C["blue"][0])
    f.arrow(X0 + W + 6, Y0 + 9 * RH - 10, X0 + W + 6, Y0 + 6, color=MUTED, sw=1.2, size=7)
    # right: four lines
    RX, RW = 350, 320
    lines = [
        ("① 速度预算", "动量守恒 · 能量密度 · 指数增长", "blue", ["火箭方程", "火箭", "多级火箭", "液体火箭发动机", "固体火箭", "电推进", "可回收火箭", "星舰"]),
        ("② 轨道力学", "万有引力与轨道 · 相对论效应", "purple", ["轨道与宇宙速度", "人造卫星", "地球静止轨道", "引力弹弓", "卫星导航", "太空垃圾"]),
        ("③ 在极端环境里活下来", "稳态与负反馈 · 传热 · 冗余", "green", ["载人航天", "生命保障系统", "再入与防热", "航天服", "空间站", "联盟号", "航天飞机"]),
        ("④ 谁在推动", "激励与博弈 · 规模效应", "amber", ["太空竞赛", "斯普特尼克 1 号", "首次载人航天", "中国航天", "商业航天", "太空旅游"]),
    ]
    y = 72
    for title, roots, col, items in lines:
        dark, light = C[col]
        h = 142
        f.rect(RX, y, RW, h, fill="#fff", stroke=dark, sw=1.4, rx=8)
        f.rect(RX, y, RW, 28, fill=dark, stroke=dark, rx=8)
        f.rect(RX, y + 18, RW, 10, fill=dark, stroke=dark, rx=0)
        f.text(RX + 12, y + 19, title, fs=13, weight=700, fill="#fff", anchor="start")
        f.text(RX + 12, y + 46, "根原理：" + roots, fs=10.5, fill=dark, anchor="start", weight=700)
        chips(f, RX + 12, y + 56, RW - 22, items, col, fs=10.5, solid=CORE)
        y += h + 8
    # timeline
    ty = 726
    f.text(340, ty, "时间线", fs=13, weight=700)
    ev = [(1903, "火箭方程"), (1926, "液体火箭"), (1942, "V-2"), (1957, "第一颗卫星"), (1961, "加加林"), (1969, "登月"),
          (1981, "航天飞机"), (1998, "国际空间站"), (2003, "神舟五号"), (2015, "火箭回收"), (2019, "月背着陆"), (2026, "重返绕月")]
    x0, x1 = 30, 650
    f.line(x0, ty + 40, x1, ty + 40, stroke=INK, sw=1.6)
    for k, (yr, lab) in enumerate(ev):
        x = x0 + k * (x1 - x0) / (len(ev) - 1)
        f.circle(x, ty + 40, 4, fill=C["red"][0], stroke=C["red"][0])
        up = k % 2 == 0
        f.text(x, ty + (26 if up else 60), str(yr), fs=10.5, weight=700)
        f.text(x, ty + (14 if up else 74), lab, fs=10, fill=MUTED)
    # interfaces
    y = 822
    f.rect(8, y, 664, 70, fill="#f9fafb", stroke="#d1d5db", rx=8)
    f.text(340, y + 22, "和其他篇的接口", fs=12, weight=700)
    f.text(340, y + 42, "通信卫星、卫星互联网 → 第 4 篇　洲际导弹 → 第 13 篇　原子钟、射电望远镜 → 第 16 篇", fs=10.8, fill=MUTED)
    f.text(340, y + 59, "隔热陶瓷、液氧 → 第 6 篇　气候模型、数值天气预报 → 第 15 篇　网约车、数字地图靠卫星导航", fs=10.8, fill=MUTED)
    f.text(340, 918, "一句话：上太空难在“快”而不在“高”——100 公里只需几分钟，难的是每秒近 8 公里的水平速度。", fs=11.5, weight=700, fill=INK)
    return f

# ------------------------------------------------------------------ rocket
@fig
def rocket():
    f = Fig(680, 320, "火箭")
    cx = 110
    # fairing
    f.path(f"M{cx-22},90 C{cx-22},50 {cx},28 {cx},28 C{cx},28 {cx+22},50 {cx+22},90 Z", stroke=C["slate"][0], fill="#fff", sw=1.4)
    f.rect(cx - 22, 90, 44, 40, fill=C["purple"][1], stroke=C["purple"][0], rx=1)
    f.rect(cx - 22, 130, 44, 70, fill=C["blue"][1], stroke=C["blue"][0], rx=1)
    f.rect(cx - 22, 200, 44, 18, fill="#e5e7eb", stroke=C["slate"][0], rx=1)
    f.rect(cx - 22, 218, 44, 36, fill=C["amber"][1], stroke=C["amber"][0], rx=1)
    f.path(f"M{cx-14},254 L{cx+14},254 L{cx+20},280 L{cx-20},280 Z", stroke=C["slate"][0], fill="#9ca3af", sw=1.2)
    f.path(f"M{cx-12},282 C{cx-18},300 {cx-6},312 {cx},318 C{cx+6},312 {cx+18},300 {cx+12},282 Z", stroke=C["red"][0], fill=C["amber"][1], sw=1.2)
    def lab(y, t, col):
        f.line(cx + 26, y, cx + 60, y, stroke=C[col][0], sw=1, dash="3 2")
        f.text(cx + 64, y + 4, t, fs=11.5, anchor="start", fill=C[col][0], weight=700)
    lab(60, "整流罩 + 载荷", "slate"); lab(110, "第二级", "purple"); lab(165, "燃料贮箱", "blue")
    lab(236, "氧化剂贮箱", "amber"); lab(268, "发动机", "slate"); lab(304, "燃气向后喷出", "red")
    f.arrow(40, 220, 40, 120, color=C["green"][0], sw=2.6, size=10)
    f.text(40, 108, "推力", fs=12, weight=700, fill=C["green"][0])
    # mass bar
    bx, by, bw = 300, 50, 360
    f.text(bx + bw / 2, 30, "典型运载火箭的起飞质量构成", fs=13, weight=700)
    segs = [(88, "blue", "推进剂 约 85–90%"), (9, "slate", "结构"), (3, "green", "载荷")]
    x = bx
    for w, col, t in segs:
        ww = bw * w / 100
        f.rect(x, by, ww, 34, fill=C[col][0] if col != "slate" else C[col][1], stroke=C[col][0], rx=2)
        f.text(x + ww / 2, by + 22, t if w > 20 else "", fs=12, fill="#fff", weight=700)
        x += ww
    f.text(bx + bw * 0.925, by + 52, "结构", fs=10.5, fill=C["slate"][0], weight=700)
    f.text(bx + bw * 0.985, by + 68, "载荷 2–4%", fs=10.5, fill=C["green"][0], weight=700, anchor="end")
    # nozzle
    ny = 200
    f.text(bx + bw / 2, 128, "拉瓦尔喷管：先收缩、再扩张", fs=13, weight=700)
    f.path(f"M{bx},{ny-50} L{bx+90},{ny-50} L{bx+150},{ny-14} L{bx+330},{ny-56} L{bx+330},{ny+56} L{bx+150},{ny+14} L{bx+90},{ny+50} L{bx},{ny+50} Z", stroke=C["slate"][0], fill="#f8fafc", sw=1.6)
    f.rect(bx + 4, ny - 44, 82, 88, fill=C["red"][1], stroke=C["red"][0], rx=6)
    f.text(bx + 45, ny - 4, "燃烧室", fs=11.5, weight=700, fill=C["red"][0])
    f.text(bx + 45, ny + 14, "高温高压", fs=10, fill=MUTED)
    for k, (x1, x2, col, w) in enumerate([(bx + 100, bx + 140, "amber", 1.6), (bx + 170, bx + 230, "red", 2.2), (bx + 250, bx + 320, "red", 2.8)]):
        f.arrow(x1, ny, x2, ny, color=C[col][0], sw=w, size=8)
    f.text(bx + 150, ny + 40, "喉部：音速", fs=10.5, fill=INK)
    f.text(bx + 270, ny - 22, "超音速", fs=10.5, fill=C["red"][0], weight=700)
    f.text(bx + 270, ny + 34, "2.5–4.5 km/s", fs=11, fill=C["red"][0], weight=700)
    f.text(bx + bw / 2, 290, "推力 = 每秒喷出的质量 × 喷气速度", fs=12, weight=700)
    f.text(bx + bw / 2, 308, "自带氧化剂，真空中照样工作", fs=10.5, fill=MUTED)
    return f

# ------------------------------------------------------------------ rocket equation
@fig
def rocket_equation():
    f = Fig(680, 300, "火箭方程")
    X0, Y0, W, H = 70, 30, 380, 220
    f.line(X0, Y0 + H, X0 + W, Y0 + H, stroke=INK, sw=1.2); f.line(X0, Y0, X0, Y0 + H, stroke=INK, sw=1.2)
    vmax = 14
    for v in range(0, 15, 2):
        x = X0 + v / vmax * W
        f.line(x, Y0 + H, x, Y0 + H + 4, stroke=INK); f.text(x, Y0 + H + 18, str(v), fs=11)
    f.text(X0 + W / 2, Y0 + H + 36, "需要的速度增量（公里/秒）", fs=11.5, fill=MUTED)
    for p in (0, 25, 50, 75, 100):
        y = Y0 + H - p / 100 * H
        f.line(X0 - 4, y, X0, y, stroke=INK); f.text(X0 - 8, y + 4, f"{p}%", fs=10.5, anchor="end")
        if p: f.line(X0, y, X0 + W, y, stroke="#e5e7eb", sw=0.8)
    f.text(X0 - 8, Y0 - 12, "推进剂占起飞质量", fs=10.5, fill=MUTED, anchor="start")
    def curve(ve, col, lab):
        pts = [(X0 + v / 10 / vmax * W, Y0 + H - (1 - math.exp(-(v / 10) / ve)) * H) for v in range(0, 141)]
        f.poly(pts, stroke=C[col][0], sw=2.4)
        return pts
    curve(4.4, "blue", "")
    curve(3.0, "amber", "")
    xl = X0 + 9.4 / vmax * W
    f.line(xl, Y0, xl, Y0 + H, stroke=C["red"][0], sw=1.2, dash="5 3")
    f.text(xl - 4, Y0 + H - 12, "进入近地轨道 ≈ 9.4", fs=10.5, fill=C["red"][0], anchor="end", weight=700)
    for ve, col in ((4.4, "blue"), (3.0, "amber")):
        fr = 1 - math.exp(-9.4 / ve)
        y = Y0 + H - fr * H
        f.circle(xl, y, 4, fill=C[col][0], stroke=C[col][0])
        f.text(xl + 8, y + (14 if col == "blue" else -6), f"{fr*100:.0f}%", fs=11, fill=C[col][0], weight=700, anchor="start")
    f.text(X0 + 0.55 * W, Y0 + H - 0.55 * H, "液氢液氧（喷气 4.4 km/s）", fs=11, fill=C["blue"][0], weight=700, anchor="start")
    f.text(X0 + 0.10 * W, Y0 + H - 0.80 * H + 8, "煤油液氧（约 3.0 km/s）", fs=11, fill=C["amber"][0], weight=700, anchor="start")
    # formula box
    f.rect(480, 40, 190, 120, fill=C["purple"][1], stroke=C["purple"][0], rx=8)
    f.text(575, 66, "齐奥尔科夫斯基方程", fs=12.5, weight=700, fill=C["purple"][0])
    f.text(575, 98, "Δv = vₑ · ln(m₀ / m₁)", fs=15, weight=700, mono=True)
    f.text(575, 124, "vₑ 喷气速度", fs=10.5, fill=MUTED)
    f.text(575, 140, "m₀ 起飞质量　m₁ 烧完后质量", fs=10.5, fill=MUTED)
    f.lines(575, 190, ["速度增量线性增加，", "质量比却指数增加：", "剩给箱体和载荷的份额", "很快逼近于零"], fs=11.5, lh=1.4)
    return f

# ------------------------------------------------------------------ reusable rocket
@fig
def reusable_rocket():
    f = Fig(680, 320, "可回收火箭")
    sea = 270
    f.rect(0, sea, 680, 50, fill="#e0f2fe", stroke="#e0f2fe", rx=0)
    f.rect(0, sea - 4, 150, 54, fill="#f3f4f6", stroke="#d1d5db", rx=0)
    # pad
    f.rect(40, sea - 14, 30, 10, fill=C["slate"][0], stroke=C["slate"][0], rx=1)
    # ascent
    f.path(f"M55,{sea-16} C70,170 120,90 230,60", stroke=C["blue"][0], sw=2.4)
    f.path("M230,60 C330,30 470,24 650,30", stroke=C["purple"][0], sw=2, dash="6 4")
    f.text(640, 20, "第二级继续入轨", fs=11, fill=C["purple"][0], weight=700, anchor="end")
    # booster return
    f.path("M230,60 C280,40 330,60 360,100 C390,140 430,190 520,250", stroke=C["red"][0], sw=2.2)
    # ship
    f.rect(495, sea - 10, 60, 10, fill=C["slate"][0], stroke=C["slate"][0], rx=2)
    f.text(525, sea + 22, "海上无人船", fs=11, weight=700)
    f.text(75, sea + 22, "发射场", fs=11, weight=700)
    steps = [(55, sea - 30, "① 起飞"), (230, 60, "② 一二级分离"), (300, 52, "③ 调头"), (365, 108, "④ 再入点火"), (430, 175, "⑤ 栅格舵控向"), (515, 238, "⑥ 着陆点火"), (530, sea - 14, "⑦ 着陆")]
    for k, (x, y, t) in enumerate(steps):
        f.circle(x, y, 5, fill=C["red"][0] if k >= 2 else C["blue"][0], stroke="#fff", sw=1.4)
    labs = [(65, sea - 40, "① 起飞", "start"), (220, 84, "② 一二级分离（约 2.5 分钟）", "end"), (300, 38, "③ 调头", "middle"),
            (378, 106, "④ 再入点火：减速、降温", "start"), (442, 172, "⑤ 栅格舵控制方向", "start"), (560, 232, "⑥ 着陆点火", "start"), (566, sea - 12, "⑦ 张开着陆腿落下", "start")]
    for x, y, t, a in labs:
        f.text(x, y, t, fs=11, anchor=a, weight=700, fill=INK)
    f.box(170, 140, 190, 56, "代价：留出返回燃料", "amber", fs=11.5, sub="运力比一次性使用少约三成", sub_fs=10.5)
    f.box(170, 204, 190, 56, "收益：最贵的一级反复用", "green", fs=11.5, sub="推进剂常不到成本的 1%", sub_fs=10.5)
    return f

# ------------------------------------------------------------------ orbit
@fig
def orbit():
    f = Fig(680, 380, "牛顿的山顶大炮")
    cx, cy, R = 220, 200, 100
    f.circle(cx, cy, R, fill=C["blue"][1], stroke=C["blue"][0], sw=2)
    f.text(cx, cy + 6, "地球", fs=16, weight=700, fill=C["blue"][0])
    top = cy - R
    f.path(f"M{cx-16},{top+4} L{cx},{top-16} L{cx+16},{top+4} Z", stroke=C["slate"][0], fill=C["slate"][1])
    my = top - 16
    rp, ra = R + 16, 150
    a = (rp + ra) / 2; b = math.sqrt(rp * ra)
    ellipse(f, cx, cy + (a - rp), b, a, stroke=C["purple"][0], sw=1.8, dash="6 4")
    f.circle(cx, cy, rp, fill="none", stroke=C["green"][0], sw=2.2)
    def traj(ang_deg, col):
        ang = math.radians(ang_deg)
        ex, ey = cx + R * math.sin(ang), cy - R * math.cos(ang)
        c1x = cx + (ex - cx) * 0.6 + 10
        f.path(f"M{cx},{my} Q{c1x:.1f},{my - 4} {ex:.1f},{ey:.1f}", stroke=C[col][0], sw=1.8)
    traj(25, "amber"); traj(60, "amber")
    f.text(cx + 40, my - 14, "慢：很快落地", fs=10.5, fill=C["amber"][0], anchor="start", weight=700)
    f.text(cx + 124, top + 58, "更快：落得更远", fs=10.5, fill=C["amber"][0], anchor="start", weight=700)
    f.lines(cx - rp - 8, cy - 30, ["7.9 km/s：", "一直绕着“落”", "＝圆轨道"], fs=11.5, lh=1.35, fill=C["green"][0], anchor="end", weight=700)
    f.text(cx + 70, cy + 168, "再快一些：椭圆轨道", fs=11, fill=C["purple"][0], weight=700, anchor="start")
    f.path(f"M{cx},{my} C{cx+140},{my-8} {cx+260},{my+20} {cx+400},{my+86}", stroke=C["red"][0], sw=2)
    f.arrow(cx + 392, my + 82, cx + 412, my + 92, color=C["red"][0], sw=2)
    f.text(cx + 300, my + 38, "11.2 km/s：摆脱地球", fs=11.5, fill=C["red"][0], weight=700, anchor="start")
    f.box(470, 170, 200, 48, "第一宇宙速度 7.9 km/s", "green", fs=12, sub="环绕地球", sub_fs=10.5)
    f.box(470, 226, 200, 48, "第二宇宙速度 11.2 km/s", "red", fs=12, sub="飞离地球", sub_fs=10.5)
    f.box(470, 282, 200, 48, "第三宇宙速度 16.7 km/s", "slate", fs=12, sub="飞出太阳系", sub_fs=10.5)
    f.text(570, 352, "（地球表面附近、不计空气阻力）", fs=10, fill=MUTED)
    return f

# ------------------------------------------------------------------ gnss
@fig
def gnss():
    f = Fig(680, 320, "卫星导航")
    cx, cy, R = 250, 560, 330
    f.circle(cx, cy, R, fill=C["blue"][1], stroke=C["blue"][0], sw=2)
    rx, ry = 250, cy - R
    f.rect(rx - 7, ry - 14, 14, 22, fill=INK, stroke=INK, rx=3)
    f.text(rx, ry + 26, "接收机（手机）", fs=11, weight=700)
    sats = [(70, 70, "①"), (190, 36, "②"), (330, 44, "③"), (440, 90, "④")]
    for x, y, n in sats:
        sat(f, x, y, "teal", 1.0)
        f.line(x, y + 6, rx, ry - 14, stroke=C["teal"][0], sw=1.2, dash="5 3")
        f.text(x, y - 12, n, fs=12, weight=700, fill=C["teal"][0])
    f.text(110, 150, "距离 = 光速 × 信号传播时间", fs=11.5, fill=INK, weight=700, anchor="middle")
    f.text(400, 170, "4 颗卫星 → 4 个方程", fs=11.5, fill=INK, weight=700)
    f.text(400, 188, "解出 x、y、z 和时钟误差 t", fs=11, fill=MUTED)
    # right box relativity
    bx = 500
    f.rect(bx, 30, 170, 270, fill="#fff", stroke=C["purple"][0], sw=1.4, rx=8)
    f.text(bx + 85, 54, "星上原子钟每天", fs=12.5, weight=700, fill=C["purple"][0])
    f.text(bx + 85, 84, "速度快 → 慢 7 μs", fs=11.5, fill=INK)
    f.text(bx + 85, 102, "（狭义相对论）", fs=10, fill=MUTED)
    f.text(bx + 85, 130, "引力弱 → 快 45 μs", fs=11.5, fill=INK)
    f.text(bx + 85, 148, "（广义相对论）", fs=10, fill=MUTED)
    f.line(bx + 20, 160, bx + 150, 160, stroke=C["purple"][0], sw=1)
    f.text(bx + 85, 184, "合计快约 38 μs", fs=13, weight=700, fill=C["purple"][0])
    f.text(bx + 85, 214, "不修正，定位误差", fs=11.5, fill=INK)
    f.text(bx + 85, 232, "每天累积约 10 公里", fs=11.5, fill=C["red"][0], weight=700)
    f.text(bx + 85, 266, "1 微秒 ≈ 300 米", fs=11, fill=MUTED)
    return f

# ------------------------------------------------------------------ apollo
@fig
def apollo():
    f = Fig(680, 330, "阿波罗月球轨道交会")
    ex, ey, er = 110, 175, 60
    mx, my, mr = 490, 175, 34
    f.circle(ex, ey, er, fill=C["blue"][1], stroke=C["blue"][0], sw=2); f.text(ex, ey + 5, "地球", fs=14, weight=700, fill=C["blue"][0])
    f.circle(mx, my, mr, fill="#e5e7eb", stroke="#6b7280", sw=2); f.text(mx, my + 5, "月球", fs=13, weight=700, fill="#374151")
    # parking orbit
    f.circle(ex, ey, er + 14, fill="none", stroke=C["slate"][0], sw=1, dash="3 3")
    # lunar orbit
    f.circle(mx, my, mr + 22, fill="none", stroke=C["purple"][0], sw=1.6, dash="5 3")
    # outbound
    f.path(f"M{ex+50},{ey-52} C230,40 380,50 {mx-40},{my-46}", stroke=C["blue"][0], sw=2)
    f.arrow(mx - 60, my - 52, mx - 44, my - 47, color=C["blue"][0], sw=2)
    # return
    f.path(f"M{mx-40},{my+46} C380,300 230,300 {ex+52},{ey+48}", stroke=C["green"][0], sw=2)
    f.arrow(ex + 70, ey + 64, ex + 54, ey + 50, color=C["green"][0], sw=2)
    # LM descent/ascent
    f.arrow(mx + 30, my - 50, mx + 16, my - 30, color=C["red"][0], sw=2, size=7)
    f.arrow(mx + 30, my + 30, mx + 44, my + 50, color=C["amber"][0], sw=2, size=7)
    lab = [
        (ex, ey - er - 24, "① 土星五号发射，进入停泊轨道", "middle"),
        (300, 50, "② 飞往月球（约 3 天）", "middle"),
        (mx + 30, my - 76, "③ 进入月球轨道", "start"),
        (mx + 40, my - 26, "④ 登月舱下降", "start"),
        (mx + 52, my + 60, "⑤ 上升级起飞、对接", "start"),
        (300, 296, "⑥ 只有指令舱返回地球", "middle"),
    ]
    for x, y, t, a in lab:
        f.text(x, y, t, fs=11.5, weight=700, anchor=a)
    f.text(mx, my + mr + 46, "指令舱留在轨道等待", fs=10.5, fill=C["purple"][0], anchor="middle")
    f.box(220, 130, 160, 74, "关键：月球轨道交会", "purple", fs=12, sub="只让轻巧的登月舱\n下到月面再上来\n→ 一枚土星五号就够", sub_fs=10.2)
    f.text(ex, 318, "共约 8 天", fs=10.5, fill=MUTED)
    return f

# ------------------------------------------------------------------ multistage (small)
@fig
def multistage_rocket():
    f = Fig(520, 250, "多级火箭")
    def stack(x, n, lab, sub):
        y = 200
        cols = ["amber", "blue", "purple"]
        hs = [70, 44, 28]
        for k in range(3):
            if k < 3 - n: continue
        top = y
        for k in range(3 - n, 3):
            pass
        yb = 200
        for k in range(3):
            if k < 3 - n:
                continue
            h = hs[k]
            f.rect(x - 16 + k * 2, yb - h, 32 - k * 4, h, fill=C[cols[k]][1], stroke=C[cols[k]][0], rx=2)
            yb -= h
        f.path(f"M{x-10},{yb} L{x},{yb-18} L{x+10},{yb} Z", stroke=C["green"][0], fill=C["green"][1])
        f.text(x, 222, lab, fs=11.5, weight=700)
        f.text(x, 238, sub, fs=10, fill=MUTED)
    stack(70, 3, "起飞", "推动全部质量")
    stack(200, 2, "扔掉第一级", "剩下的轻多了")
    stack(330, 1, "扔掉第二级", "只剩最后一级")
    f.path("M460,190 L470,172 L480,190 Z", stroke=C["green"][0], fill=C["green"][1]); f.text(470, 222, "载荷入轨", fs=11.5, weight=700)
    for x in (110, 240, 370):
        f.arrow(x, 120, x + 50, 120, color=INK, sw=1.6)
    f.text(260, 26, "每一级都只推动“更轻的剩余部分”，各级速度增量相加", fs=12, weight=700)
    # falling stages
    f.rect(150, 160, 14, 30, fill=C["amber"][1], stroke=C["amber"][0], rx=2, dash="3 2")
    f.text(157, 152, "↓", fs=12, fill=C["amber"][0])
    f.rect(280, 175, 12, 20, fill=C["blue"][1], stroke=C["blue"][0], rx=2, dash="3 2")
    f.text(286, 168, "↓", fs=12, fill=C["blue"][0])
    return f

# ------------------------------------------------------------------ GEO (small)
@fig
def geostationary_orbit():
    f = Fig(520, 280, "地球静止轨道")
    cx, cy, R, ro = 190, 145, 42, 112
    for k in range(3):
        a = math.radians(90 + k * 120)
        sx, sy = cx + ro * math.cos(a), cy - ro * math.sin(a)
        # coverage tangent lines
        th = math.acos(R / ro)
        for s in (-1, 1):
            b = a + s * th
            tx, ty = cx + R * math.cos(b), cy - R * math.sin(b)
            f.line(sx, sy, tx, ty, stroke=C["teal"][0], sw=0.9, dash="3 3")
        sat(f, sx, sy, "teal", 0.9)
    f.circle(cx, cy, ro, fill="none", stroke=C["purple"][0], sw=1.4, dash="6 4")
    f.circle(cx, cy, R, fill=C["blue"][1], stroke=C["blue"][0], sw=2)
    f.text(cx, cy + 5, "地球", fs=12, weight=700, fill=C["blue"][0])
    f.text(cx, cy - R - 6, "↺", fs=13, fill=C["blue"][0])
    f.lines(400, 70, ["赤道上空", "35786 公里"], fs=13, lh=1.35, weight=700, fill=C["purple"][0])
    f.lines(400, 130, ["绕一圈 ≈ 一天", "与地球同步转动", "从地面看“静止”"], fs=11.5, lh=1.45)
    f.lines(400, 210, ["三颗卫星覆盖", "两极以外的大部分地区"], fs=11.5, lh=1.45, fill=C["teal"][0], weight=700)
    f.text(cx, 272, "（示意，比例未按实际）", fs=10, fill=MUTED)
    return f

# ------------------------------------------------------------------ gravity assist (small)
@fig
def gravity_assist():
    f = Fig(520, 260, "引力弹弓")
    px, py = 200, 140
    f.circle(px, py, 30, fill=C["amber"][1], stroke=C["amber"][0], sw=2)
    f.text(px, py + 5, "行星", fs=12, weight=700, fill=C["amber"][0])
    f.arrow(px - 20, py + 48, px + 50, py + 48, color=C["amber"][0], sw=2.4)
    f.text(px + 56, py + 52, "行星绕日运动", fs=10.5, fill=C["amber"][0], anchor="start", weight=700)
    f.path(f"M140,226 C150,180 130,120 {px-30},{py-48} C{px+10},{py-78} 300,40 380,20", stroke=C["blue"][0], sw=2.2)
    f.arrow(360, 26, 384, 18, color=C["blue"][0], sw=2.2)
    f.text(132, 224, "飞入", fs=11, fill=C["blue"][0], weight=700, anchor="end")
    f.text(330, 46, "飞出", fs=11, fill=C["blue"][0], weight=700, anchor="end")
    # vector inset
    ox, oy = 400, 170
    f.text(455, 112, "相对太阳的速度", fs=11, weight=700)
    f.arrow(ox, oy, ox + 50, oy - 30, color=C["blue"][0], sw=1.8, size=7)
    f.text(ox + 20, oy - 28, "v相对", fs=9.5, fill=C["blue"][0])
    f.arrow(ox + 50, oy - 30, ox + 100, oy - 30, color=C["amber"][0], sw=1.8, size=7)
    f.text(ox + 78, oy - 36, "v行星", fs=9.5, fill=C["amber"][0])
    f.arrow(ox, oy, ox + 100, oy - 30, color=C["red"][0], sw=2.2, size=8)
    f.text(ox + 50, oy + 4, "合成后更快", fs=10.5, fill=C["red"][0], weight=700)
    f.text(260, 252, "相对行星：飞进多快，飞出也多快；相对太阳：被行星“带”了一程", fs=10.5, fill=MUTED)
    return f

def main():
    only = set(sys.argv[1:])
    for name, fn in FIGS.items():
        if only and name not in only: continue
        fn().save(OUT / f"{name}.svg")
    print("wrote", len(only) if only else len(FIGS), "figures to", OUT)

if __name__ == "__main__":
    main()
