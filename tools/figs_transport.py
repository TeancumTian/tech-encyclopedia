#!/usr/bin/env python3
"""Generate all diagrams for 第 8 篇「交通运输」 -> assets/figs/transport/*.svg"""
from __future__ import annotations
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from svgkit import Fig, C, INK, MUTED, tw

OUT = Path(__file__).resolve().parents[1] / "assets" / "figs" / "transport"
FIGS = {}

def fig(fn):
    FIGS[fn.__name__.replace("_", "-")] = fn
    return fn

def chips(f, x, y, w, items, color, fs=10.5, gap=5, solid=()):
    """flow chips inside width w starting at (x,y); returns bottom y"""
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

# ------------------------------------------------------------------ concept map
@fig
def concept_map():
    f = Fig(680, 940, "交通运输 知识地图")
    f.text(340, 30, "交通运输 · 知识地图", fs=21, weight=700)
    f.text(340, 52, "横向是四种运输方式，纵向是四个时代：每一次动力换代，都让“移动一吨一公里”更便宜。实心为核心词条。", fs=11, fill=MUTED)
    cols = [("铁路与城市轨道", "blue"), ("道路与汽车", "amber"), ("水运与管道", "teal"), ("航空", "purple")]
    eras = [("蒸汽时代", "约 1760–1880", "煤 + 蒸汽机"),
            ("内燃与电气", "约 1880–1945", "石油 + 内燃机 + 电动机"),
            ("喷气与高速", "约 1945–2000", "喷气发动机 + 标准化"),
            ("电动与智能", "约 2000–2026", "电池 + 传感器 + AI")]
    cells = [
        [["蒸汽机车", "铁路", "标准轨距", "地铁", "电气化铁路"], ["现代路面"], ["航海天文钟", "蒸汽船", "螺旋桨", "现代运河", "管道运输"], ["热气球"]],
        [["有轨电车"], ["汽车", "自行车", "摩托车", "充气轮胎", "卡车", "T 型车", "红绿灯", "高速公路"], ["陀螺罗经", "托盘与叉车"], ["飞艇", "飞机", "自动驾驶仪", "空管", "直升机", "喷气发动机", "空气动力学"]],
        [["高速铁路"], ["汽车安全", "快速公交", "混合动力"], ["集装箱运输", "载人深潜器"], ["喷气客机", "涡扇", "超音速客机", "电传飞控"]],
        [["磁悬浮", "超级高铁"], ["电动汽车", "充电网络", "自动驾驶", "驾驶辅助", "激光雷达", "网约车", "共享单车"], [], ["无人机", "eVTOL"]],
    ]
    core = {"铁路", "高速铁路", "汽车", "电动汽车", "自动驾驶", "集装箱运输", "飞机", "喷气发动机"}
    X0, CW, Y0, RH = 112, 139, 84, 148
    for j, (name, col) in enumerate(cols):
        dark, light = C[col]
        f.rect(X0 + j * CW + 2, Y0, CW - 4, 26, fill=dark, stroke=dark, rx=6)
        f.text(X0 + j * CW + CW / 2, Y0 + 18, name, fs=12.5, fill="#fff", weight=700)
    for i, (era, yrs, power) in enumerate(eras):
        y = Y0 + 32 + i * RH
        f.rect(8, y, 100, RH - 6, fill=C["slate"][1], stroke=C["slate"][0], rx=8, sw=1)
        f.text(58, y + 40, era, fs=13.5, weight=700, fill=C["slate"][0])
        f.text(58, y + 60, yrs, fs=10.5, fill=MUTED)
        rows = power.split(" + ")
        for k, r in enumerate(rows):
            f.text(58, y + 86 + k * 16, r, fs=10.5, fill=INK)
        for j, (_, col) in enumerate(cols):
            dark, light = C[col]
            f.rect(X0 + j * CW + 2, y, CW - 4, RH - 6, fill=light, stroke=dark, sw=0.8, rx=6, opacity=0.9)
            items = cells[i][j]
            if items:
                chips(f, X0 + j * CW + 8, y + 8, CW - 14, items, col, solid=core)
            else:
                f.text(X0 + j * CW + CW / 2, y + RH / 2, "远洋船舶仍以柴油机为主", fs=10, fill=MUTED)
        if i < 3:
            f.arrow(58, y + RH - 4, 58, y + RH + 4, color=C["slate"][0], sw=1.6, size=7)
    # systems & standards
    y = Y0 + 32 + 4 * RH + 6
    f.rect(8, y, 664, 74, fill="#fff", stroke=C["green"][0], sw=1.4, rx=8)
    f.text(20, y + 22, "贯穿各时代：系统与标准往往比单台机器更重要", fs=13, weight=700, fill=C["green"][0], anchor="start")
    chips(f, 20, y + 34, 640, ["标准轨距（1435 mm）", "铁路时间 → 时区", "集装箱（TEU）", "托盘尺寸", "交通信号", "空中交通管制", "SAE 自动驾驶分级", "充电接口标准"], "green", fs=11)
    # principles strip
    y += 84
    f.text(340, y + 14, "反复出现的根原理", fs=12.5, weight=700)
    xs = 22
    for p, col in [("能量守恒", "amber"), ("牛顿定律", "blue"), ("动量守恒", "blue"), ("流体与升力", "teal"), ("能量密度", "amber"), ("标准化", "green"), ("规模效应", "green"), ("反馈与控制", "purple")]:
        xs += f.pill(xs, y + 24, p, col, fs=11) + 8
    # interfaces
    y += 60
    f.rect(8, y, 664, 50, fill="#f9fafb", stroke="#d1d5db", rx=8)
    f.text(340, y + 20, "和其他篇的接口", fs=12, weight=700)
    f.text(340, y + 39, "发动机与电池 → 第 1 篇　卫星导航 → 第 9 篇　雷达、军用无人机 → 第 13 篇　桥梁与隧道 → 第 12 篇", fs=10.8, fill=MUTED)
    return f

# ------------------------------------------------------------------ railway
@fig
def railway():
    f = Fig(680, 300, "铁路")
    f.text(170, 26, "拉动 1 吨重物所需的滚动阻力（典型量级）", fs=13, weight=700)
    bars = [("钢轮—钢轨", 15, "blue", "约 10–20 牛"), ("汽车轮胎—沥青路", 100, "amber", "约 100 牛"), ("轮胎—松软土路", 300, "red", "数百牛")]
    for k, (lab, v, col, txt) in enumerate(bars):
        y = 50 + k * 58
        f.text(20, y + 14, lab, fs=12, anchor="start", weight=700)
        w = v * 0.95
        f.rect(20, y + 22, max(w, 6), 20, fill=C[col][0], stroke=C[col][0], rx=3)
        f.text(28 + max(w, 6), y + 37, txt, fs=11.5, anchor="start", fill=C[col][0], weight=700)
    f.text(170, 236, "同样的牵引力，在铁轨上能拉动重得多的货物", fs=11.5, fill=INK)
    f.text(170, 254, "（阻力系数：钢轨约 0.001–0.002，公路轮胎约 0.01）", fs=10.5, fill=MUTED)
    # wheelset
    ox = 360
    f.text(ox + 155, 26, "锥形踏面：列车自己“找正”", fs=13, weight=700)
    for rx in (ox + 50, ox + 250):
        f.rect(rx - 10, 188, 20, 14, fill=C["slate"][0], stroke=C["slate"][0], rx=2)
    f.line(ox + 20, 202, ox + 300, 202, stroke=C["slate"][0], sw=1)
    # axle
    f.rect(ox + 40, 128, 240, 8, fill="#9ca3af", stroke="#6b7280", rx=3)
    # wheels as trapezoids (cone: larger radius toward flange inside)
    def wheel(cx, flip):
        s = -1 if flip else 1          # s=+1: inner side is to the right
        o, i = cx - 22 * s, cx + 22 * s  # outer / inner face x
        pts = [(o, 132 - 52), (i, 132 - 60), (i, 132 + 60), (o, 132 + 52)]
        f.poly(pts, stroke=C["blue"][0], fill=C["blue"][1], sw=1.6, closed=True)
        fl = i if not flip else i - 6
        f.rect(fl, 132 - 68, 6, 136, fill=C["blue"][0], stroke=C["blue"][0], rx=2)
    wheel(ox + 50, False); wheel(ox + 250, True)
    f.text(ox + 80, 60, "轮缘", fs=10.5, fill=C["blue"][0], weight=700)
    f.text(ox + 220, 60, "轮缘", fs=10.5, fill=C["blue"][0], weight=700)
    f.box(ox + 8, 218, 300, 52, "过弯时离心作用把轮对推向外轨", "amber", fs=11.5, sub="外侧车轮滚在“大直径”处、内侧在“小直径”处\n两轮一快一慢，自动转向弯道", sub_fs=10.5, weight=700)
    f.text(ox + 150, 118, "车轴（两轮刚性相连）", fs=10.5, fill=MUTED)
    return f

# ------------------------------------------------------------------ HSR
@fig
def high_speed_rail():
    f = Fig(680, 300, "高速铁路的空气阻力")
    X0, Y0, W, H = 70, 40, 360, 210
    f.line(X0, Y0 + H, X0 + W, Y0 + H, stroke=INK, sw=1.2); f.line(X0, Y0, X0, Y0 + H, stroke=INK, sw=1.2)
    vmax, ymax = 400, 64
    for v in range(0, 401, 100):
        x = X0 + v / vmax * W
        f.line(x, Y0 + H, x, Y0 + H + 4, stroke=INK, sw=1)
        f.text(x, Y0 + H + 18, str(v), fs=11)
    f.text(X0 + W / 2, Y0 + H + 36, "速度（公里/小时）", fs=11.5, fill=MUTED)
    for yv in (1, 8, 16, 27, 64):
        y = Y0 + H - yv / ymax * H
        f.line(X0 - 4, y, X0, y, stroke=INK, sw=1); f.text(X0 - 8, y + 4, f"×{yv}", fs=10.5, anchor="end")
    f.text(X0 - 8, Y0 - 12, "相对 100 km/h 时", fs=10.5, fill=MUTED, anchor="start")
    def curve(pw, col):
        pts = []
        for v in range(0, 401, 10):
            r = (v / 100) ** pw
            if r > ymax: break
            pts.append((X0 + v / vmax * W, Y0 + H - r / ymax * H))
        f.poly(pts, stroke=C[col][0], sw=2.4)
        return pts[-1]
    a = curve(2, "blue"); b = curve(3, "red")
    f.text(X0 + W - 6, Y0 + H - 16 / ymax * H - 8, "空气阻力 ∝ v²", fs=12, fill=C["blue"][0], weight=700, anchor="end")
    f.text(b[0] - 14, b[1] + 4, "所需功率 ∝ v³", fs=12, fill=C["red"][0], weight=700, anchor="end")
    for v, col in ((200, "slate"), (300, "slate")):
        x = X0 + v / vmax * W
        f.line(x, Y0, x, Y0 + H, stroke=C[col][0], sw=0.8, dash="4 3")
    # right notes
    f.box(460, 50, 205, 64, "100 → 200 km/h", "blue", fs=12.5, sub="阻力 ×4　功率 ×8", sub_fs=12)
    f.box(460, 126, 205, 64, "100 → 300 km/h", "red", fs=12.5, sub="阻力 ×9　功率 ×27", sub_fs=12)
    f.lines(562, 216, ["所以高铁必须：", "流线型长车头 · 平滑车身", "专用线路 · 大功率电力牵引"], fs=11.5, fill=INK)
    f.text(562, 284, "（只计空气阻力部分，示意）", fs=10, fill=MUTED)
    return f

# ------------------------------------------------------------------ automobile
@fig
def automobile():
    f = Fig(680, 340, "汽车的五大系统")
    # car silhouette
    body = "M60,170 L110,170 L150,118 L300,108 L380,140 L470,150 L500,175 L500,200 L60,200 Z"
    f.path(body, stroke=C["slate"][0], sw=2, fill=C["slate"][1])
    f.path("M160,122 L290,114 L340,140 L150,146 Z", stroke=C["slate"][0], sw=1.2, fill="#fff")
    for cx in (130, 420):
        f.circle(cx, 205, 26, fill="#374151", stroke="#111827", sw=2); f.circle(cx, 205, 10, fill="#9ca3af", stroke="#6b7280")
    def tag(x, y, tx, ty, title, sub, col):
        f.line(x, y, tx, ty, stroke=C[col][0], sw=1.2, dash="3 2"); f.circle(x, y, 4, fill=C[col][0], stroke=C[col][0])
        f.box(tx - 70, ty - 20, 140, 40, title, col, fs=12, sub=sub, sub_fs=9.8)
    tag(450, 170, 590, 120, "① 动力", "发动机 / 电机+电池", "red")
    tag(330, 190, 400, 268, "② 传动", "离合器·变速箱·差速器", "amber")
    tag(130, 205, 90, 268, "③ 底盘", "悬架·转向·制动·轮胎", "blue")
    tag(230, 112, 230, 50, "④ 车身", "乘员舱·吸能结构", "slate")
    tag(380, 142, 520, 50, "⑤ 电子电气", "几十到上百个控制单元", "purple")
    f.text(340, 312, "燃油车 → 电动车：①② 变化最大（电池+电机，通常只需单级减速器）", fs=11.5, fill=INK)
    f.text(340, 330, "③④ 大体不变；⑤ 越来越像一台装在轮子上的电脑", fs=11.5, fill=INK)
    return f

# ------------------------------------------------------------------ EV
@fig
def electric_vehicle():
    f = Fig(680, 250, "能量到达车轮的比例")
    f.text(340, 24, "同样 100 份能量，有多少真正推动了车轮？", fs=13.5, weight=700)
    X0, W = 120, 520
    def bar(y, label, segs):
        f.text(X0 - 10, y + 26, label, fs=13, weight=700, anchor="end")
        x = X0
        for w, col, txt, sub in segs:
            ww = W * w / 100
            dark, light = C[col]
            f.rect(x, y, ww, 42, fill=light if col != "green" else dark, stroke=dark, rx=3, sw=1)
            tc = "#fff" if col == "green" else INK
            f.text(x + ww / 2, y + 19, txt, fs=12, fill=tc, weight=700)
            if sub: f.text(x + ww / 2, y + 34, sub, fs=10, fill=tc if col == "green" else MUTED)
            x += ww
    bar(46, "汽油车", [(21, "green", "到达车轮", "约 12–30%"), (79, "red", "发动机废热、排气、怠速和传动损失", "约 70–88%")])
    bar(116, "电动车", [(80, "green", "到达车轮（含刹车回收）", "77% 以上"), (20, "amber", "充电、电控", "和电机损失")])
    f.text(340, 192, "差距来自热机的卡诺极限：燃油车的能量大部分以热的形式散掉；电动机没有这个限制。", fs=11.5)
    f.text(340, 212, "电动车的总排放还取决于发电方式——煤电多的地方优势变小，清洁电多的地方优势变大。", fs=11, fill=MUTED)
    f.text(340, 236, "数据：美国能源部 fueleconomy.gov（电动车按电网到车轮计）", fs=10, fill=MUTED)
    return f

# ------------------------------------------------------------------ autonomous vehicle
@fig
def autonomous_vehicle():
    f = Fig(680, 330, "自动驾驶")
    nodes = [("感知", "摄像头 · 雷达 · 激光雷达\n定位与地图", "blue", 40, 40),
             ("预测", "其他车辆和行人\n几秒后会在哪里", "purple", 260, 40),
             ("规划", "选一条安全、舒适\n合乎规则的轨迹", "amber", 480, 40),
             ("控制", "转向 · 油门 · 制动", "green", 480, 150)]
    for name, sub, col, x, y in nodes:
        f.box(x, y, 160, 74, name, col, fs=14, sub=sub, sub_fs=10.5)
    f.arrow(202, 77, 258, 77, color=INK, sw=1.6); f.arrow(422, 77, 478, 77, color=INK, sw=1.6)
    f.arrow(560, 116, 560, 148, color=INK, sw=1.6)
    f.box(260, 150, 160, 74, "车辆与环境", "slate", fs=14, sub="车动了，世界也在变", sub_fs=10.5)
    f.arrow(478, 187, 422, 187, color=INK, sw=1.6)
    f.curve(258, 187, 120, 190, 120, 116, color=C["blue"][0], sw=1.6)
    f.text(130, 200, "再次测量（每秒数十次）", fs=10.5, fill=C["blue"][0], anchor="end")
    # SAE levels
    y = 248
    f.text(20, y - 6, "SAE 分级", fs=12, weight=700, anchor="start")
    levels = [("L0", "无自动化"), ("L1", "单项辅助"), ("L2", "组合辅助"), ("L3", "有条件自动"), ("L4", "限定区域无人"), ("L5", "任何条件无人")]
    w = 106
    for k, (l, d) in enumerate(levels):
        col = "amber" if k <= 2 else "green"
        f.box(20 + k * w + 2, y, w - 4, 44, l, col, fs=13, sub=d, sub_fs=10)
    f.line(20 + 3 * w, y - 8, 20 + 3 * w, y + 52, stroke=C["red"][0], sw=2, dash="5 3")
    f.text(20 + 3 * w - 8, y + 70, "← 人必须全程监督", fs=11, fill=C["amber"][0], weight=700, anchor="end")
    f.text(20 + 3 * w + 8, y + 70, "系统负责驾驶 →", fs=11, fill=C["green"][0], weight=700, anchor="start")
    return f

# ------------------------------------------------------------------ container
@fig
def container_shipping():
    f = Fig(680, 330, "集装箱运输")
    # left: before
    f.rect(10, 10, 300, 200, fill="#fff7ed", stroke=C["amber"][0], rx=8)
    f.text(160, 32, "之前：件杂货", fs=14, weight=700, fill=C["amber"][0])
    import random
    rnd = random.Random(3)
    for k in range(26):
        x = 30 + rnd.random() * 250; y = 50 + rnd.random() * 100
        if k % 3 == 0: f.circle(x, y + 8, 9, fill="#fde68a", stroke="#b45309")
        elif k % 3 == 1: f.rect(x, y, 22, 16, fill="#fed7aa", stroke="#c2410c", rx=2)
        else: f.rect(x, y, 12, 22, fill="#fef3c7", stroke="#92400e", rx=4)
    f.text(160, 178, "麻袋、木桶、箱子大小不一，一件件搬", fs=11.5)
    f.text(160, 198, "装卸一艘船常要好几天；货损和偷盗多", fs=11.5, fill=C["red"][0], weight=700)
    # right: after
    f.rect(330, 10, 340, 200, fill="#ecfeff", stroke=C["teal"][0], rx=8)
    f.text(500, 32, "之后：同一个箱子走全程", fs=14, weight=700, fill=C["teal"][0])
    def cont(x, y, w=56, h=22, col="teal"):
        f.rect(x, y, w, h, fill=C[col][1], stroke=C[col][0], rx=1, sw=1.4)
        for k in range(1, 6):
            f.line(x + k * w / 6, y + 2, x + k * w / 6, y + h - 2, stroke=C[col][0], sw=0.6)
    # ship
    f.path("M345,120 L475,120 L465,145 L355,145 Z", stroke=C["slate"][0], fill=C["slate"][1], sw=1.4)
    for r in range(2):
        for c in range(2): cont(352 + c * 58, 75 + r * 23)
    f.text(410, 162, "船", fs=11.5, weight=700)
    # crane
    f.line(500, 145, 500, 55, stroke=C["red"][0], sw=2.4); f.line(470, 55, 560, 55, stroke=C["red"][0], sw=2.4)
    f.line(520, 55, 520, 80, stroke=C["red"][0], sw=1); cont(505, 80, 30, 14)
    f.text(510, 162, "岸桥", fs=11.5, weight=700)
    # truck & train
    cont(570, 96); f.rect(628, 100, 22, 18, fill=C["blue"][1], stroke=C["blue"][0], rx=2)
    f.circle(585, 124, 5, fill="#374151", stroke="#111"); f.circle(640, 124, 5, fill="#374151", stroke="#111")
    f.text(605, 142, "卡车", fs=11.5, weight=700)
    cont(560, 172 - 20, 40, 16); cont(604, 172 - 20, 40, 16)
    f.line(556, 172, 652, 172, stroke=INK, sw=1.4)
    f.text(605, 198, "火车", fs=11.5, weight=700)
    f.arrow(478, 100, 498, 100, color=C["teal"][0], size=6); f.arrow(540, 108, 566, 108, color=C["teal"][0], size=6)
    # bottom spec
    f.rect(10, 222, 660, 98, fill="#fff", stroke="#d1d5db", rx=8)
    f.text(30, 246, "标准是关键", fs=13.5, weight=700, anchor="start")
    cont(30, 258, 90, 34); f.text(75, 308, "20 英尺 = 1 TEU", fs=11, weight=700)
    cont(140, 258, 180, 34); f.text(230, 308, "40 英尺 = 2 TEU", fs=11, weight=700)
    for (x, y) in ((140, 258), (314, 258), (140, 286), (314, 286)):
        f.rect(x, y, 6, 6, fill=C["red"][0], stroke=C["red"][0], rx=0)
    f.lines(500, 254, ["宽 8 英尺，八个角都有标准角件（红点）", "→ 任何港口的吊具都能抓、能堆、能锁", "→ 船、火车、卡车按同一尺寸设计", "最大的船：2.4 万 TEU 以上"], fs=11.2, lh=1.45)
    return f

# ------------------------------------------------------------------ airplane
@fig
def airplane():
    f = Fig(680, 320, "飞机的四个力与三根轴")
    # side view plane
    f.path("M60,160 C80,148 120,144 300,146 L360,150 C380,152 390,158 380,166 L300,170 L80,170 C66,170 56,166 60,160 Z", stroke=C["slate"][0], fill=C["slate"][1], sw=1.6)
    f.path("M80,148 L60,110 L80,110 L110,147 Z", stroke=C["slate"][0], fill=C["slate"][1], sw=1.4)
    f.path("M170,160 L240,160 L260,168 L170,168 Z", stroke=C["blue"][0], fill=C["blue"][1], sw=1.2)
    cx, cy = 220, 158
    f.arrow(cx, cy - 4, cx, cy - 92, color=C["blue"][0], sw=2.6, size=10); f.text(cx + 8, cy - 80, "升力", fs=13, weight=700, fill=C["blue"][0], anchor="start")
    f.arrow(cx, cy + 14, cx, cy + 92, color=C["red"][0], sw=2.6, size=10); f.text(cx + 8, cy + 86, "重力", fs=13, weight=700, fill=C["red"][0], anchor="start")
    f.arrow(388, 158, 450, 158, color=C["green"][0], sw=2.6, size=10); f.text(420, 148, "推力", fs=13, weight=700, fill=C["green"][0])
    f.arrow(56, 158, 6, 158, color=C["amber"][0], sw=2.6, size=10); f.text(26, 148, "阻力", fs=13, weight=700, fill=C["amber"][0])
    f.text(230, 290, "匀速平飞：升力 = 重力，推力 = 阻力", fs=12, weight=700)
    f.text(230, 308, "升力 ∝ 空气密度 × 机翼面积 × 速度²", fs=11, fill=MUTED)
    # top view with control surfaces
    ox, oy = 470, 30
    f.text(ox + 100, oy + 4, "三组舵面 ↔ 三根轴", fs=13, weight=700)
    f.path(f"M{ox+95},{oy+20} L{ox+105},{oy+20} L{ox+108},{oy+230} L{ox+92},{oy+230} Z", stroke=C["slate"][0], fill=C["slate"][1], sw=1.2)
    f.path(f"M{ox+100},{oy+80} L{ox+195},{oy+125} L{ox+195},{oy+140} L{ox+100},{oy+120} L{ox+5},{oy+140} L{ox+5},{oy+125} Z", stroke=C["slate"][0], fill=C["slate"][1], sw=1.2)
    f.path(f"M{ox+100},{oy+200} L{ox+145},{oy+222} L{ox+145},{oy+230} L{ox+55},{oy+230} L{ox+55},{oy+222} Z", stroke=C["slate"][0], fill=C["slate"][1], sw=1.2)
    f.rect(ox + 150, oy + 128, 40, 9, fill=C["purple"][0], stroke=C["purple"][0], rx=1); f.rect(ox + 10, oy + 128, 40, 9, fill=C["purple"][0], stroke=C["purple"][0], rx=1)
    f.rect(ox + 58, oy + 226, 84, 6, fill=C["teal"][0], stroke=C["teal"][0], rx=1)
    f.rect(ox + 97, oy + 214, 6, 18, fill=C["pink"][0], stroke=C["pink"][0], rx=1)
    f.text(ox + 170, oy + 154, "副翼 → 滚转", fs=11, fill=C["purple"][0], weight=700)
    f.text(ox + 30, oy + 154, "副翼", fs=11, fill=C["purple"][0], weight=700)
    f.text(ox + 30, oy + 252, "升降舵 → 俯仰", fs=11, fill=C["teal"][0], weight=700)
    f.text(ox + 165, oy + 252, "方向舵 → 偏航", fs=11, fill=C["pink"][0], weight=700)
    f.text(ox + 100, oy + 280, "（俯视图）", fs=10, fill=MUTED)
    return f

# ------------------------------------------------------------------ jet engine
@fig
def jet_engine():
    f = Fig(680, 280, "涡轮喷气发动机")
    top, bot = 70, 200
    f.path(f"M40,{top+10} L120,{top} L470,{top} L560,{top+25} L640,{top+40} L640,{bot-40} L560,{bot-25} L470,{bot} L120,{bot} L40,{bot-10} Z", stroke=C["slate"][0], fill="#f8fafc", sw=1.8)
    mid = (top + bot) / 2
    f.rect(110, mid - 5, 380, 10, fill="#9ca3af", stroke="#6b7280", rx=3)
    # compressor stages
    for k in range(7):
        x = 130 + k * 22; h = 52 - k * 4
        f.line(x, mid - h, x, mid + h, stroke=C["blue"][0], sw=4)
    f.box(120, bot + 10, 150, 40, "① 压气机", "blue", fs=12.5, sub="空气压强升高数倍到数十倍", sub_fs=10)
    # combustor
    f.rect(290, mid - 40, 100, 80, fill=C["red"][1], stroke=C["red"][0], rx=10)
    for k in range(3):
        x = 310 + k * 28
        f.path(f"M{x},{mid+18} C{x-8},{mid} {x+8},{mid-6} {x},{mid-24} C{x+14},{mid-6} {x+10},{mid+8} {x},{mid+18} Z", stroke=C["red"][0], fill=C["amber"][1], sw=1.2)
    f.box(270, bot + 10, 140, 40, "② 燃烧室", "red", fs=12.5, sub="喷油持续燃烧", sub_fs=10)
    # turbine
    for k in range(3):
        x = 415 + k * 20
        f.line(x, mid - 44, x, mid + 44, stroke=C["amber"][0], sw=4)
    f.box(410, bot + 10, 120, 40, "③ 涡轮", "amber", fs=12.5, sub="取能带动压气机", sub_fs=10)
    f.box(540, bot + 10, 120, 40, "④ 尾喷管", "green", fs=12.5, sub="高速喷出 → 推力", sub_fs=10)
    f.text(300, mid + 4 - 60, "", fs=10)
    # flow arrows
    for dy in (-30, 0, 30):
        f.arrow(0, mid + dy, 34, mid + dy, color=C["blue"][0], sw=2)
    for dy in (-20, 0, 20):
        f.arrow(645, mid + dy, 676, mid + dy, color=C["red"][0], sw=2.6)
    f.text(60, top - 14, "冷空气吸入", fs=11.5, fill=C["blue"][0], weight=700)
    f.text(610, top - 4, "高温燃气喷出", fs=11.5, fill=C["red"][0], weight=700)
    f.curve(470, mid + 14, 330, mid + 70, 200, mid + 14, color=C["slate"][0], sw=1.2)
    f.text(330, mid + 58, "同一根轴：涡轮带动压气机", fs=10.5, fill=C["slate"][0])
    f.text(340, 30, "吸入 → 压缩 → 燃烧 → 膨胀做功 → 喷出：空气获得向后的动量，发动机获得向前的推力", fs=11.5, weight=700)
    return f

# ------------------------------------------------------------------ aerodynamics (small)
@fig
def aerodynamics():
    f = Fig(520, 260, "攻角与失速")
    X0, Y0, W, H = 60, 30, 300, 180
    f.line(X0, Y0 + H, X0 + W, Y0 + H, stroke=INK); f.line(X0, Y0, X0, Y0 + H, stroke=INK)
    f.text(X0 + W / 2, Y0 + H + 30, "攻角（机翼与气流的夹角）", fs=11.5, fill=MUTED)
    f.text(X0 - 10, Y0 - 10, "升力", fs=11.5, fill=MUTED, anchor="start")
    pts = []
    for a in range(0, 25):
        if a <= 15: cl = 0.1 + a * 0.09
        else: cl = 1.45 - (a - 15) * 0.11
        pts.append((X0 + a / 24 * W, Y0 + H - cl / 1.6 * H))
    f.poly(pts, stroke=C["blue"][0], sw=2.6)
    sx, sy = X0 + 15 / 24 * W, Y0 + H - 1.45 / 1.6 * H
    f.circle(sx, sy, 5, fill=C["red"][0], stroke=C["red"][0])
    f.text(sx, sy - 12, "临界攻角", fs=11.5, fill=C["red"][0], weight=700)
    f.text(X0 + 4 / 24 * W, Y0 + H - 0.9 / 1.6 * H - 20, "攻角越大，升力越大", fs=10.5, fill=C["blue"][0], anchor="middle")
    f.text(X0 + 21 / 24 * W, Y0 + H - 0.9 / 1.6 * H + 34, "失速", fs=12, fill=C["red"][0], weight=700)
    # airfoils
    def foil(x, y, ang, sep):
        a = math.radians(ang)
        def rot(px, py): return (x + px * math.cos(a) - py * math.sin(a), y + px * math.sin(a) + py * math.cos(a))
        prof = []
        for k in range(31):
            t = (k / 30) ** 2
            th = 0.6 * (0.2969 * math.sqrt(t) - 0.126 * t - 0.3516 * t ** 2 + 0.2843 * t ** 3 - 0.1015 * t ** 4)
            cam = 0.04 * (1 - (2 * t - 1) ** 2)
            prof.append((t, cam + th))
        up = [(-40 + 90 * t, -90 * yy) for t, yy in prof]
        lo = [(-40 + 90 * t, -90 * (0.08 * (1 - (2 * t - 1) ** 2) - yy) * 0.5 + 0) for t, yy in prof]
        lo = [(-40 + 90 * t, 90 * (yy - 0.08 * (1 - (2 * t - 1) ** 2)) * 0.6) for t, yy in prof]
        pts = [rot(px, py) for px, py in up + lo[::-1]]
        f.poly(pts, stroke=C["slate"][0], fill=C["slate"][1], closed=True, sw=1.2)
        for k in range(3):
            yy = y - 22 - k * 10
            if sep and k < 2:
                f.path(f"M{x-60},{yy} L{x-20},{yy} C{x},{yy-4} {x+10},{yy+14} {x+30},{yy+6} C{x+40},{yy} {x+50},{yy+12} {x+64},{yy+6}", stroke=C["red"][0], sw=1.1)
            else:
                f.path(f"M{x-60},{yy} C{x-20},{yy-6} {x+20},{yy-6} {x+64},{yy+8}", stroke=C["blue"][0], sw=1.1)
    foil(440, 80, 6, False); f.text(440, 112, "小攻角：气流贴着机翼", fs=10.5)
    foil(440, 180, 20, True); f.text(440, 222, "大攻角：上表面气流分离", fs=10.5, fill=C["red"][0])
    return f

# ------------------------------------------------------------------ turbofan (small)
@fig
def turbofan():
    f = Fig(520, 230, "涡扇发动机")
    f.path("M40,30 L330,30 L380,55 L380,175 L330,200 L40,200 Z", stroke=C["slate"][0], fill="#f8fafc", sw=1.6)
    f.path("M120,80 L330,80 L420,100 L420,130 L330,150 L120,150 Z", stroke=C["red"][0], fill=C["red"][1], sw=1.4)
    f.line(70, 38, 70, 192, stroke=C["blue"][0], sw=6)
    f.text(70, 22, "大风扇", fs=11.5, weight=700, fill=C["blue"][0])
    f.text(250, 120, "核心机（小型涡喷）", fs=11.5, weight=700, fill=C["red"][0])
    for y in (50, 62, 168, 180):
        f.arrow(90, y, 400, y, color=C["blue"][0], sw=1.8, size=7)
    f.arrow(90, 115, 116, 115, color=C["red"][0], sw=1.8, size=7)
    f.arrow(422, 115, 470, 115, color=C["red"][0], sw=2.2, size=8)
    f.text(250, 222, "外涵空气 : 内涵空气 ≈ 10 : 1（现代客机）", fs=11.5, weight=700)
    f.text(452, 16, "外涵：大量冷空气", fs=10.5, fill=C["blue"][0], anchor="middle")
    f.text(452, 31, "稍微加速 → 省油安静", fs=10.5, fill=C["blue"][0], anchor="middle")
    return f

def main():
    only = set(sys.argv[1:])
    for name, fn in FIGS.items():
        if only and name not in only: continue
        fn().save(OUT / f"{name}.svg")
    print("wrote", len(FIGS) if not only else len(only), "figures to", OUT)

if __name__ == "__main__":
    main()
