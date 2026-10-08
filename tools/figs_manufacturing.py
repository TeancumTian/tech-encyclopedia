#!/usr/bin/env python3
"""Generate all diagrams for 第 7 篇「制造与自动化」 -> assets/figs/manufacturing/*.svg"""
from __future__ import annotations
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from svgkit import Fig, C, INK, MUTED, tw

OUT = Path(__file__).resolve().parents[1] / "assets" / "figs" / "manufacturing"
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
    f = Fig(680, 940, "制造与自动化 知识地图")
    f.text(340, 30, "制造与自动化 · 知识地图", fs=21, weight=700)
    f.text(340, 52, "中间自下而上：先有机器动力，再有组织方式和精密工艺，最后机器学会了反馈与自主。", fs=11.5, fill=MUTED)
    layers = [
        ("工业革命", "机器代替肌肉", "slate", ["珍妮纺纱机", "水力纺纱机", "动力织布机", "提花织机", "轧棉机", "缝纫机", "工厂制度", "第二次工业革命"]),
        ("生产方式", "怎样组织人和机器", "amber", ["可互换零件", "螺纹标准", "科学管理", "流水线", "大规模生产", "丰田生产方式 · 精益", "统计质量控制", "六西格玛", "ERP"]),
        ("机床与工艺", "怎样把材料变成零件", "blue", ["机床", "精密测量与公差", "液压机", "铸造 · 锻造", "焊接", "注塑", "数控机床", "CAD/CAM", "3D 打印", "激光加工", "连续造纸机", "滚动轴承"]),
        ("自动化与控制", "测量—比较—纠正", "green", ["离心调速器", "PID 控制", "控制论", "PLC", "SCADA", "机器视觉", "数字孪生", "系统工程", "工业 4.0"]),
        ("机器人", "会动的自动化", "purple", ["工业机器人", "伺服系统", "协作机器人", "移动机器人", "物流自动化", "人形机器人"]),
    ]
    layered_map(f, layers, 76, 812, footer="↑ 从“人操作机器”到“机器自己感知、决策、执行”")
    timeline(f, "生产方式的里程碑", [("1764", "珍妮纺纱机"), ("1769", "水力纺纱机"), ("1771", "第一座工厂"), ("1788", "离心调速器"),
             ("1800", "螺纹车床"), ("1804", "提花织机"), ("1841", "螺纹标准"), ("1870", "第二次工业革命"), ("1911", "科学管理"),
             ("1913", "福特流水线"), ("1924", "控制图"), ("1950s", "丰田生产方式"), ("1952", "数控机床"), ("1961", "Unimate"),
             ("1969", "PLC"), ("1984", "3D 打印专利"), ("2008", "协作机器人"), ("2011", "工业 4.0"), ("2025", "在役机器人 500 万台")], 90, 812)
    y = side(f, 84, "根原理", "green", ["能量与机械增益", "分工与标准化", "规模效应", "反馈与控制", "抽象：把手艺写成程序"])
    y = side(f, y + 14, "五种生产方式", "amber", ["手工作坊", "工厂", "流水线大批量", "精益 · 准时化", "智能工厂"])
    y = side(f, y + 14, "代价与争论", "red", ["童工与劳动强度", "单调重复的工作", "自动化与就业", "供应链脆弱"])
    y = side(f, y + 14, "看一条产线时问", "slate", ["瓶颈在哪道工序？", "误差怎么控制？", "换产品要多久？"])
    f.rect(10, 862, 660, 66, fill="#f9fafb", stroke="#d1d5db", rx=8)
    f.text(340, 884, "和其他篇的接口", fs=12.5, weight=700)
    f.text(340, 905, "蒸汽机与电动机 → 第 1 篇「能源与动力」　钢铁与塑料 → 第 6 篇「材料与化工」", fs=11, fill=MUTED)
    f.text(340, 922, "AI 与具身智能 → 第 5 篇「人工智能」　T 型车与集装箱 → 第 8 篇「交通与运载」", fs=11, fill=MUTED)
    return f

# ------------------------------------------------------------------ A figures
@fig
def industrial_revolution():
    f = Fig(680, 380, "工业革命：互相推动的创新链")
    nodes = [(110, 60, "纺纱机", "珍妮机 · 水力纺纱", "amber"), (330, 60, "织布成瓶颈", "→ 动力织布机", "amber"),
             (550, 60, "需要铁与煤", "焦炭炼铁 · 采矿", "slate"), (550, 160, "矿井要排水", "→ 蒸汽机", "red"),
             (330, 160, "蒸汽驱动工厂", "工厂不必建在河边", "red"), (110, 160, "铁路与轮船", "运来原料 · 运走产品", "blue")]
    for x, y, t, s, col in nodes:
        f.box(x - 90, y - 26, 180, 52, t, col, fs=13.5, sub=s)
    f.arrow(202, 60, 238, 60); f.arrow(422, 60, 458, 60); f.arrow(550, 88, 550, 132)
    f.arrow(458, 160, 422, 160); f.arrow(238, 160, 202, 160); f.arrow(110, 132, 110, 88)
    f.text(330, 112, "一个环节变快，就逼着下一个环节创新", fs=12, weight=700, fill=C["purple"][0])
    # GDP curve
    ox, oy, w, h = 70, 230, 560, 110
    f.line(ox, oy + h, ox + w, oy + h); f.line(ox, oy, ox, oy + h)
    def X(yr): return ox + (yr - 1000) / (2020 - 1000) * w
    pts = [(1000, 4), (1300, 5), (1500, 6), (1700, 8), (1760, 9), (1820, 12), (1870, 18), (1913, 30), (1950, 40), (1980, 70), (2000, 85), (2020, 105)]
    f.poly([(X(a), oy + h - v) for a, v in pts], stroke=C["blue"][0], sw=2.4)
    for yr in (1000, 1200, 1400, 1600, 1800, 2000):
        f.line(X(yr), oy + h, X(yr), oy + h + 4); f.text(X(yr), oy + h + 16, str(yr), fs=10, fill=MUTED)
    f.rect(X(1760), oy, X(1840) - X(1760), h, fill=C["amber"][1], stroke="none", rx=0, opacity=0.7)
    f.poly([(X(a), oy + h - v) for a, v in pts], stroke=C["blue"][0], sw=2.4)
    f.text(X(1800), oy + 14, "工业革命", fs=11, weight=700, fill=C["amber"][0])
    f.text(ox + 8, oy + 12, "世界人均产出（示意）", fs=11, weight=700, fill=C["blue"][0], anchor="start")
    f.text(X(1400), oy + h - 18, "近千年几乎是平的", fs=11, fill=MUTED)
    f.text(X(1640), oy + 40, "1800 年后才开始持续增长 →", fs=11, fill=MUTED)
    return f

@fig
def assembly_line():
    f = Fig(680, 360, "流水线装配")
    def car(x, y, col="blue"):
        f.rect(x, y, 70, 22, fill=C[col][1], stroke=C[col][0], rx=6)
        f.rect(x + 14, y - 12, 38, 14, fill=C[col][1], stroke=C[col][0], rx=4)
        f.circle(x + 15, y + 24, 6, fill=INK); f.circle(x + 55, y + 24, 6, fill=INK)
    def worker(x, y, col="amber"):
        f.circle(x, y - 14, 6, fill=C[col][0], stroke="none")
        f.line(x, y - 8, x, y + 8, stroke=C[col][0], sw=3)
        f.line(x - 6, y, x + 6, y, stroke=C[col][0], sw=2.5)
    f.text(160, 26, "以前：车不动，人围着车转", fs=13.5, weight=700, fill=C["slate"][0])
    car(125, 90, "slate")
    for k, (dx, dy) in enumerate([(-40, 0), (0, -40), (70, -40), (110, 0), (35, 50)]):
        worker(125 + dx + 20, 90 + dy + 10, "slate")
    f.curve(90, 140, 160, 175, 240, 120, color=C["slate"][0], sw=1.2, dash="4 3")
    f.text(160, 186, "每个工人要会很多道工序，来回取零件", fs=11, fill=MUTED)
    f.line(340, 20, 340, 196, stroke="#e5e7eb")
    f.text(510, 26, "1913 年起：车在动，人站定", fs=13.5, weight=700, fill=C["blue"][0])
    f.rect(360, 112, 300, 10, fill="#d1d5db", stroke="#6b7280", rx=5)
    for k in range(3):
        car(372 + k * 100, 86)
        worker(407 + k * 100, 150)
        f.text(407 + k * 100, 180, ["装车轴", "装发动机", "装车身"][k], fs=11, fill=C["amber"][0], weight=700)
    f.arrow(380, 60, 640, 60, color=C["blue"][0], sw=2, label="传送带按固定节拍移动", loff=(0, -8), lcolor=C["blue"][0])
    f.line(20, 206, 660, 206, stroke="#e5e7eb")
    f.text(20, 232, "福特 T 型车底盘装配时间", fs=13.5, weight=700, anchor="start")
    for k, (lab, hrs, col) in enumerate([("1913 年以前（静止装配）", 12.5, "slate"), ("1914 年初（移动装配线）", 1.5, "blue")]):
        y = 252 + k * 42
        f.text(210, y + 19, lab, fs=12, anchor="end")
        ww = 340 * hrs / 12.5
        f.rect(220, y + 4, ww, 22, fill=C[col][1], stroke=C[col][0], rx=3)
        f.text(226 + ww, y + 20, f"约 {hrs:g} 小时", fs=12, weight=700, anchor="start", fill=C[col][0])
    f.text(340, 348, "装配时间缩短约 8 倍；T 型车价格随之从 850 美元降到 300 美元以下", fs=11, fill=MUTED)
    return f

@fig
def _3d_printing():
    f = Fig(680, 370, "3D 打印：切片与逐层堆叠")
    f.text(20, 26, "① 切片：任何形状都能切成薄层", fs=13.5, weight=700, anchor="start", fill=C["blue"][0])
    cx, cy = 110, 110
    f.path(f"M{cx-50},{cy+50} L{cx-50},{cy-10} Q{cx},{cy-70} {cx+50},{cy-10} L{cx+50},{cy+50} Z", stroke=C["blue"][0], sw=2, fill=C["blue"][1])
    f.text(cx, cy + 74, "三维模型", fs=11.5, fill=MUTED)
    f.arrow(180, 100, 230, 100, color=C["blue"][0], sw=2)
    for k in range(9):
        y = 158 - k * 12
        t = k / 8
        half = 50 if y > 108 else max(10, 50 * math.sqrt(max(0, 1 - ((108 - y) / 60) ** 2)))
        f.rect(320 - half, y, 2 * half, 9, fill=C["blue"][1], stroke=C["blue"][0], sw=0.8, rx=1)
    f.text(320, 184, "一层层薄片（常见层厚 0.05—0.3 毫米）", fs=11.5, fill=MUTED)
    f.arrow(400, 100, 450, 100, color=C["blue"][0], sw=2)
    f.box(460, 70, 200, 60, "逐层“画”出每一层", "blue", fs=13, sub="叠起来就还原成立体")
    f.line(20, 200, 660, 200, stroke="#e5e7eb")
    f.text(20, 226, "② 三种主要工艺", fs=13.5, weight=700, anchor="start", fill=C["green"][0])
    # FDM
    x = 30
    f.rect(x + 50, 250, 40, 26, fill=C["slate"][1], stroke=C["slate"][0], rx=3)
    f.poly([(x + 62, 276), (x + 78, 276), (x + 70, 290)], fill=C["slate"][0], stroke=C["slate"][0], closed=True)
    for k in range(3):
        f.rect(x + 20, 312 - k * 8, 100, 7, fill=C["amber"][1], stroke=C["amber"][0], sw=0.8, rx=3)
    f.text(x + 70, 340, "熔融沉积 FDM", fs=12, weight=700)
    f.text(x + 70, 356, "挤出熔化的塑料丝", fs=10.5, fill=MUTED)
    # SLA
    x = 250
    f.rect(x + 10, 290, 120, 32, fill="#ede9fe", stroke=C["purple"][0], rx=2)
    f.rect(x + 40, 268, 60, 10, fill=C["slate"][0], stroke="none", rx=1)
    f.line(x + 70, 248, x + 70, 268, stroke=C["slate"][0], sw=2)
    for d in (-20, 0, 20):
        f.line(x + 70 + d, 335, x + 70 + d * 0.4, 322, stroke=C["purple"][0], sw=1.5, dash="3 2")
    f.text(x + 70, 356, "紫外光逐层固化液态树脂", fs=10.5, fill=MUTED)
    f.text(x + 70, 340, "", fs=1)
    # SLS
    x = 470
    f.rect(x + 10, 286, 150, 36, fill="#e5e7eb", stroke="#6b7280", rx=0)
    for i in range(30):
        f.circle(x + 15 + (i % 15) * 10, 296 + (i // 15) * 14, 3, fill="#9ca3af", stroke="none")
    f.line(x + 85, 246, x + 85, 290, stroke=C["red"][0], sw=2)
    f.circle(x + 85, 290, 4, fill=C["red"][0], stroke="none")
    f.text(x + 85, 340, "粉末床熔融 SLS/SLM", fs=12, weight=700)
    f.text(x + 85, 356, "激光逐层熔化粉末，可打印金属", fs=10.5, fill=MUTED)
    f.text(320, 340, "光固化 SLA", fs=12, weight=700)
    return f

@fig
def industrial_robot():
    f = Fig(680, 360, "六轴工业机器人")
    gx = 200
    f.rect(gx - 70, 316, 140, 16, fill="#9ca3af", stroke="#4b5563", rx=2)
    f.rect(gx - 40, 280, 80, 36, fill=C["amber"][1], stroke=C["amber"][0], rx=6)
    J = [(gx, 266), (gx + 10, 150), (gx + 170, 110), (gx + 230, 130), (gx + 262, 160)]
    f.line(gx, 280, *J[0], stroke=C["amber"][0], sw=24, cap="round")
    f.line(*J[0], *J[1], stroke=C["amber"][0], sw=22, cap="round")
    f.line(*J[1], *J[2], stroke=C["amber"][0], sw=18, cap="round")
    f.line(*J[2], *J[3], stroke=C["amber"][0], sw=12, cap="round")
    f.line(*J[3], *J[4], stroke=C["slate"][0], sw=6)
    f.poly([(J[4][0] - 6, J[4][1] + 4), (J[4][0] + 10, J[4][1] + 26), (J[4][0] + 16, J[4][1] + 18)], stroke=C["slate"][0], sw=4)
    for (x, y) in J[:4]:
        f.circle(x, y, 11, fill="#fff", stroke=INK, sw=2)
    labels = [(gx - 60, 300, "J1 底座旋转"), (gx - 50, 268, "J2 肩"), (gx - 40, 150, "J3 肘"), (gx + 150, 84, "J4 · J5 · J6 手腕"), (gx + 300, 196, "末端工具：焊枪 / 夹爪")]
    for x, y, t in labels:
        f.text(x, y, t, fs=11.5, weight=700, anchor="end" if x < gx else "start")
    f.text(gx - 60, 300, "", fs=1)
    f.text(140, 40, "前三轴：决定“手”到哪里", fs=12.5, weight=700, fill=C["amber"][0])
    f.text(140, 58, "后三轴：决定工具朝哪个方向", fs=12.5, weight=700, fill=C["slate"][0])
    # loop inset
    X0 = 470
    f.rect(X0, 220, 196, 128, fill="#f9fafb", stroke="#d1d5db", rx=8)
    f.text(X0 + 98, 240, "每个关节都是一个反馈回路", fs=11.5, weight=700, fill=C["green"][0])
    f.box(X0 + 10, 252, 80, 30, "目标角度", "slate", fs=11, weight=400)
    f.box(X0 + 106, 252, 80, 30, "伺服电机", "green", fs=11)
    f.arrow(X0 + 90, 267, X0 + 106, 267, color=C["green"][0], size=6)
    f.box(X0 + 58, 304, 80, 30, "编码器测角", "green", fs=11, weight=400)
    f.curve(X0 + 146, 284, X0 + 160, 310, X0 + 140, 318, color=C["green"][0], sw=1.2, size=6)
    f.curve(X0 + 58, 318, X0 + 30, 310, X0 + 40, 284, color=C["green"][0], sw=1.2, size=6)
    f.text(X0 + 98, 346, "重复定位精度可达 ±0.02 毫米级", fs=9.5, fill=MUTED)
    return f

# ------------------------------------------------------------------ small figures
@fig
def toyota_production_system():
    f = Fig(520, 250, "推动与拉动")
    def row(y, title, col, arrows_dir, note, stock):
        dark, light = C[col]
        f.text(20, y - 8, title, fs=13, weight=700, fill=dark, anchor="start")
        xs = [20, 190, 360]
        for k, x in enumerate(xs):
            f.box(x, y, 130, 40, ["工序 A", "工序 B", "工序 C"][k], col, fs=12.5)
        for k in range(2):
            a, b = xs[k] + 132, xs[k + 1] - 2
            if stock:
                for i in range(5):
                    f.rect(a + 4 + (i % 3) * 11, y + 6 + (i // 3) * 13 - 4, 9, 9, fill=C["red"][1], stroke=C["red"][0], sw=0.7, rx=1)
                f.arrow(a, y + 34, b, y + 34, color=dark, size=6)
            else:
                f.arrow(b, y + 12, a, y + 12, color=dark, dash="4 2", size=6)
                f.rect(a + 12, y + 20, 14, 18, fill="#fff", stroke=dark, rx=1)
                f.arrow(a, y + 34, b, y + 34, color=dark, size=6)
        f.text(260, y + 58, note, fs=11, fill=MUTED)
    row(34, "大批量“推动”：做多少推多少", "slate", 1, "工序之间堆满库存（红块），次品和停机被库存掩盖", True)
    row(144, "丰田“拉动”：后道用看板来领", "green", -1, "虚线 = 看板信号；只补充被领走的数量，问题立刻暴露", False)
    return f

@fig
def cnc():
    f = Fig(520, 220, "数控机床的闭环")
    f.box(10, 80, 100, 50, "程序", "slate", fs=13, sub="G01 X10 Y20")
    f.arrow(112, 105, 150, 105)
    f.circle(170, 105, 18, fill="#fff", stroke=INK, sw=1.4)
    f.text(170, 110, "−", fs=16, weight=700)
    f.arrow(188, 105, 220, 105)
    f.box(222, 80, 100, 50, "数控系统", "blue", fs=13, solid=True, sub="算出误差 → 指令")
    f.arrow(324, 105, 360, 105)
    f.box(362, 80, 140, 50, "伺服电机 + 丝杠", "green", fs=12.5, sub="刀具 / 工作台移动")
    f.path("M432,132 L432,180 L170,180 L170,125", stroke=C["amber"][0], sw=1.8)
    f.head(170, 125, -math.pi / 2, C["amber"][0])
    f.text(300, 198, "位置传感器（光栅尺 / 编码器）把实际位置报告回来", fs=11.5, weight=700, fill=C["amber"][0])
    f.text(130, 92, "目标", fs=10.5, fill=MUTED)
    f.text(160, 150, "实际", fs=10.5, fill=MUTED, anchor="end")
    f.text(260, 40, "目标位置 − 实际位置 = 误差，每秒纠正成千上万次", fs=12, weight=700)
    return f

@fig
def control_theory():
    f = Fig(520, 250, "反馈控制回路")
    f.box(10, 80, 80, 44, "目标值", "slate", fs=13, sub="如 24°C")
    f.arrow(92, 102, 124, 102)
    f.circle(142, 102, 16, fill="#fff", stroke=INK, sw=1.4); f.text(142, 107, "−", fs=16, weight=700)
    f.arrow(158, 102, 186, 102, label="误差", loff=(0, -7))
    f.box(188, 66, 120, 72, "PID 控制器", "blue", fs=13, solid=True, sub="P 看现在\nI 看过去\nD 看趋势")
    f.arrow(310, 102, 338, 102)
    f.box(340, 80, 80, 44, "执行器", "green", fs=13, sub="压缩机")
    f.arrow(422, 102, 440, 102)
    f.box(442, 80, 70, 44, "房间", "amber", fs=13, sub="被控对象")
    f.path("M477,126 L477,190 L142,190 L142,120", stroke=C["red"][0], sw=1.8)
    f.head(142, 119, -math.pi / 2, C["red"][0])
    f.box(260, 172, 110, 34, "传感器", "red", fs=12.5, sub=None)
    f.text(310, 228, "测出实际温度，送回去和目标比较", fs=11.5, weight=700, fill=C["red"][0])
    f.text(260, 34, "测量 → 比较 → 纠正，周而复始", fs=13, weight=700)
    return f

def main():
    only = set(sys.argv[1:])
    for name, fn in FIGS.items():
        if only and name not in only: continue
        fn().save(OUT / f"{name}.svg")
    print("wrote", len(FIGS) if not only else len(only), "figures to", OUT)

if __name__ == "__main__":
    main()
