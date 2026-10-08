#!/usr/bin/env python3
"""Generate all diagrams for 第 10 篇「生物与医学」 -> assets/figs/biomed/*.svg"""
from __future__ import annotations
import json, math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from svgkit import Fig, C, INK, MUTED, tw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "figs" / "biomed"
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
        if f is not None:
            f.rect(cx, cy, cw, fs * 1.6, fill=dark if s else "#fff", stroke=dark, sw=0.9, rx=fs * 0.8)
            f.text(cx + cw / 2, cy + fs * 1.13, it, fs=fs, fill="#fff" if s else INK, weight=700 if s else 400)
        cx += cw + gap
    return cy + fs * 1.6

def ellipse(f, cx, cy, rx, ry, stroke=INK, sw=1.4, fill="none", dash=None):
    d = f"M{cx-rx},{cy} A{rx},{ry} 0 1,0 {cx+rx},{cy} A{rx},{ry} 0 1,0 {cx-rx},{cy} Z"
    f.path(d, stroke=stroke, sw=sw, fill=fill, dash=dash)

BASE_COL = {"A": "#dc2626", "T": "#d97706", "G": "#059669", "C": "#1d4ed8"}
PAIR = {"A": "T", "T": "A", "G": "C", "C": "G"}

def strand(f, x, y, seq, dx=16, col=INK, up=True, fs=10, show=True, sw=2.2):
    """horizontal DNA strand: backbone line + base ticks (+letters)."""
    f.line(x, y, x + dx * (len(seq) - 1) + 8, y, stroke=col, sw=sw)
    for i, b in enumerate(seq):
        bx = x + 4 + i * dx
        y2 = y + (8 if up else -8)
        f.line(bx, y, bx, y2, stroke=BASE_COL.get(b, MUTED), sw=2.4, cap="butt")
        if show:
            f.text(bx, y2 + (10 if up else -3), b, fs=fs - 1, fill=BASE_COL.get(b, MUTED), weight=700)

# ------------------------------------------------------------------ concept map
SECTIONS = [
    ("① 认识敌人：公共卫生与疫苗", "病原体学说 · 分子识别 · 指数增长 · 概率与统计推断", "green", "vaccine", "ems-ambulance"),
    ("② 修补身体：外科与人工器官", "稳态与负反馈 · 应力与材料强度 · 反馈与控制", "red", "anesthesia", "modern-dentistry"),
    ("③ 看进身体：影像与诊断", "电磁波 · 干涉、衍射与共振 · 量子化能级 · 采样与数字化", "blue", "stethoscope", "cancer-screening"),
    ("④ 对症下药：药物与疗法", "分子识别 · 概率与统计推断 · 自然选择 · 激励与博弈", "amber", "aspirin", "psychiatric-drugs"),
    ("⑤ 读写生命代码：基因与生物技术", "中心法则 · 结构决定性质 · 指数增长 · 自然选择", "purple", "dna-double-helix", "directed-evolution"),
]

def _biomed_entries():
    d = json.loads((ROOT / "data" / "entries.json").read_text(encoding="utf-8"))
    E = d["entries"] if isinstance(d, dict) else d
    return [e for e in E if e.get("domain") in (10, "10", "biomed")]

@fig
def concept_map():
    f = Fig(680, 940, "生物与医学 知识地图")
    f.text(340, 30, "生物与医学 · 知识地图", fs=21, weight=700)
    f.text(340, 52, "五个部分按“认识病因 → 修补 → 诊断 → 治疗 → 改写基因”排列。实心为核心词条（★）。", fs=11, fill=MUTED)
    ents = _biomed_entries()
    ids = [e["id"] for e in ents]
    name = {e["id"]: (e.get("zh") or e.get("name")) for e in ents}
    core = {name[e["id"]] for e in ents if e.get("tier") == "A"}
    X, W, FS = 8, 664, 10
    y = 66
    for title, roots, col, a, b in SECTIONS:
        items = [name[i] for i in ids[ids.index(a): ids.index(b) + 1]]
        bottom = chips(None, X + 10, y + 50, W - 20, items, col, fs=FS, gap=4)
        h = bottom - y + 10
        dark, light = C[col]
        f.rect(X, y, W, h, fill="#fff", stroke=dark, sw=1.4, rx=8)
        f.rect(X, y, W, 26, fill=dark, stroke=dark, rx=8)
        f.rect(X, y + 16, W, 10, fill=dark, stroke=dark, rx=0)
        f.text(X + 12, y + 18, title, fs=13, weight=700, fill="#fff", anchor="start")
        f.text(X + W - 12, y + 18, f"{len(items)} 条", fs=11, fill="#fff", anchor="end")
        f.text(X + 12, y + 43, "根原理：" + roots, fs=10.5, fill=dark, anchor="start", weight=700)
        chips(f, X + 10, y + 50, W - 20, items, col, fs=FS, gap=4, solid=core)
        y += h + 8
    # timeline
    ty = y + 14
    f.text(340, ty, "时间线", fs=13, weight=700)
    ev = [(1796, "牛痘"), (1846, "乙醚麻醉"), (1895, "X 射线"), (1928, "青霉素"), (1948, "随机对照"), (1953, "双螺旋"),
          (1971, "CT"), (1978, "试管婴儿"), (1983, "PCR"), (2003, "基因组"), (2012, "CRISPR"), (2020, "mRNA 疫苗")]
    x0, x1 = 40, 630
    f.line(x0 - 10, ty + 40, x1 + 10, ty + 40, stroke=INK, sw=1.6)
    for k, (yr, lab) in enumerate(ev):
        x = x0 + k * (x1 - x0) / (len(ev) - 1)
        f.circle(x, ty + 40, 4, fill=C["red"][0], stroke=C["red"][0])
        up = k % 2 == 0
        f.text(x, ty + (26 if up else 60), str(yr), fs=10.5, weight=700)
        f.text(x, ty + (14 if up else 74), lab, fs=10, fill=MUTED)
    y = ty + 88
    f.rect(8, y, 664, 62, fill="#f9fafb", stroke="#d1d5db", rx=8)
    f.text(340, y + 20, "和其他篇的接口", fs=12, weight=700)
    f.text(340, y + 38, "转基因作物、精准发酵 → 第 11 篇　AI 预测蛋白质结构 → 第 5 篇　激光、电子显微镜 → 第 16 篇", fs=10.8, fill=MUTED)
    f.text(340, y + 54, "X 射线晶体学 → 第 16 篇　放射性同位素 → 第 1 篇　超导磁体（MRI）→ 第 6 篇　数据隐私 → 第 13 篇", fs=10.8, fill=MUTED)
    f.text(340, min(y + 86, 930), "一句话：医学的进步一半靠“看得见”（病菌、体内、基因），一半靠“算得清”（随机对照试验）。", fs=11.5, weight=700)
    return f

# ------------------------------------------------------------------ vaccine
@fig
def vaccine():
    f = Fig(680, 300, "疫苗：初次与再次免疫应答")
    ox, oy, W, H = 70, 250, 440, 200
    f.arrow(ox, oy, ox + W + 10, oy, color=INK, sw=1.4)
    f.arrow(ox, oy, ox, oy - H - 10, color=INK, sw=1.4)
    f.text(ox + W + 8, oy + 18, "时间（天）", fs=11, anchor="end", fill=MUTED)
    f.lines(ox - 10, oy - H + 4, ["抗体", "水平"], fs=11, fill=MUTED, anchor="end")
    def X(d): return ox + 14 + d * (W - 14) / 70
    for d in (0, 14, 35, 49):
        f.line(X(d), oy, X(d), oy + 4, stroke=INK, sw=1)
        f.text(X(d), oy + 16, str(d if d < 35 else d - 35), fs=9.5, fill=MUTED)
    # primary: lag 5 days, peak ~d14 at 0.22, decay
    def prim(t):
        if t < 5: return 0
        return 0.25 * (1 - math.exp(-(t - 5) / 3.5)) * math.exp(-max(0, t - 14) / 10)
    def sec(t):
        if t < 2: return 0.03
        return 0.03 + 0.85 * (1 - math.exp(-(t - 2) / 2.2)) * math.exp(-max(0, t - 10) / 40)
    pts = [(X(t / 2), oy - H * prim(t / 2)) for t in range(0, 70)]
    f.poly(pts, stroke=C["blue"][0], sw=2.4)
    pts2 = [(X(35 + t / 2), oy - H * sec(t / 2)) for t in range(0, 71)]
    f.poly(pts2, stroke=C["red"][0], sw=2.6)
    f.poly([(X(35 - 0.5), oy - H * prim(34.5)), pts2[0]], stroke=MUTED, sw=1.2, dash="3 3")
    # protection level
    yl = oy - H * 0.4
    f.line(ox, yl, ox + W, yl, stroke=C["green"][0], sw=1.2, dash="5 4")
    f.text(ox + 4, yl - 5, "足以挡住感染的水平", fs=10, fill=C["green"][0], anchor="start")
    for d, t, col in ((0, "接种疫苗", "blue"), (35, "遇到真病原体", "red")):
        f.arrow(X(d), oy - H - 6, X(d), oy - H * 0.06 - 6, color=C[col][0], sw=1.6, size=7)
        f.text(X(d) + (4 if d else 6), oy - H - 10, t, fs=11, weight=700, fill=C[col][0], anchor="start" if d else "start")
    f.text(X(13), oy - H * 0.3, "初次应答：慢、少", fs=10.5, fill=C["blue"][0], weight=700)
    f.text(X(52), oy - H * 0.95 + 12, "再次应答：快、多、持久", fs=10.5, fill=C["red"][0], weight=700, anchor="start")
    # side notes
    bx = 540
    f.box(bx, 50, 130, 80, "初次", "blue", fs=12.5, sub="要 1–2 周\n抗体量少\n留下记忆细胞", sub_fs=10.5)
    f.box(bx, 145, 130, 80, "再次", "red", fs=12.5, sub="几天内反击\n抗体多、结合更牢\n病还没发起来就被压住", sub_fs=10)
    f.text(bx + 65, 250, "疫苗＝无害的“演习”", fs=11, weight=700, fill=INK)
    return f

# ------------------------------------------------------------------ x-ray
@fig
def x_ray():
    f = Fig(680, 300, "X 射线成像")
    # tube (glass envelope)
    ellipse(f, 120, 80, 95, 38, stroke=C["slate"][0], sw=1.4, fill="#f8fafc")
    # cathode
    f.rect(36, 68, 18, 24, fill=C["slate"][1], stroke=C["slate"][0], rx=2)
    f.path("M54,74 q5,3 0,6 q5,3 0,6 q5,3 0,6", stroke=C["red"][0], sw=1.4)
    f.text(45, 130, "阴极（灯丝）", fs=10, fill=MUTED)
    # anode target angled
    f.poly([(176, 58), (200, 58), (200, 102), (160, 102)], stroke=C["amber"][0], fill=C["amber"][1], closed=True)
    f.text(222, 84, "钨靶（阳极）", fs=10, fill=MUTED, anchor="start")
    # electron beam
    for dy in (-4, 0, 4):
        f.arrow(62, 80 + dy, 162, 80 + dy, color=C["blue"][0], sw=1.2, size=6)
    f.text(110, 66, "电子 e⁻", fs=10.5, fill=C["blue"][0], weight=700)
    f.text(120, 30, "几万～十几万伏高压加速", fs=10.5, fill=MUTED)
    # x-ray fan downward then right? -> rays go down to body
    sx, sy = 175, 104
    body_y = 200
    # arm cross-section
    ellipse(f, 175, body_y, 70, 30, stroke=C["pink"][0], fill=C["pink"][1], sw=1.3)
    ellipse(f, 175, body_y, 20, 14, stroke=C["slate"][0], fill="#e5e7eb", sw=1.6)
    f.text(255, body_y - 18, "软组织：吸收少", fs=10.5, fill=C["pink"][0], anchor="start", weight=700)
    f.text(255, body_y + 2, "骨骼（钙）：吸收多", fs=10.5, fill=C["slate"][0], anchor="start", weight=700)
    # rays
    for k in range(-5, 6):
        ex = 175 + k * 16
        f.line(sx, sy, ex, 262, stroke=C["purple"][0], sw=0.9, dash="4 3")
    f.text(100, 150, "X 射线", fs=11, fill=C["purple"][0], weight=700)
    # detector
    f.rect(80, 262, 190, 14, fill="#111827", stroke=INK, rx=1)
    # bright spot = bone shadow
    f.rect(158, 262, 34, 14, fill="#f9fafb", stroke="none", rx=1)
    f.rect(108, 262, 50, 14, fill="#6b7280", stroke="none", rx=0)
    f.rect(192, 262, 50, 14, fill="#6b7280", stroke="none", rx=0)
    f.text(175, 292, "探测器：骨头处射线少 → 白；空处射线多 → 黑", fs=10.5, fill=INK)
    # right: absorption ladder
    rx = 440
    f.text(rx + 105, 40, "谁挡得多？（越往右越“白”）", fs=12, weight=700)
    items = [("空气（肺）", "#111827", "#fff"), ("脂肪", "#4b5563", "#fff"), ("肌肉、血液", "#9ca3af", INK),
             ("骨骼", "#e5e7eb", INK), ("金属", "#ffffff", INK)]
    for i, (t, fill, tc) in enumerate(items):
        y = 56 + i * 34
        w = 60 + i * 30
        f.rect(rx, y, w, 26, fill=fill, stroke=INK, sw=0.8, rx=3)
        f.text(rx + w + 6, y + 18, t, fs=11, anchor="start")
    f.text(rx + 105, 250, "原子越重、越厚，吸收越多", fs=10.5, fill=MUTED)
    f.text(rx + 105, 268, "一张胸片约 0.02–0.1 毫希沃特", fs=10.5, fill=MUTED)
    return f

# ------------------------------------------------------------------ antibiotic
def _rod(f, x, y, w, h, wall=C["green"][0], fill=C["green"][1], dash=None, sw=3):
    f.rect(x, y, w, h, fill=fill, stroke=wall, sw=sw, rx=h / 2, dash=dash)

@fig
def antibiotic():
    f = Fig(680, 300, "青霉素如何杀菌")
    titles = ["① 正常细菌：边长边修细胞壁", "② 青霉素卡住“砌墙酶”", "③ 墙上出现缺口，细菌被撑破"]
    for i, t in enumerate(titles):
        f.text(115 + i * 225, 28, t, fs=11.5, weight=700)
    # panel 1
    _rod(f, 30, 60, 170, 70)
    f.text(115, 100, "细菌（内部压力高）", fs=10.5, fill=C["green"][0])
    # zoomed mesh
    mx, my = 40, 160
    f.rect(mx - 6, my - 8, 162, 92, fill="#fff", stroke="#d1d5db", rx=6)
    for r in range(4):
        f.line(mx, my + r * 22, mx + 150, my + r * 22, stroke=C["green"][0], sw=2.2)
    for r in range(3):
        for c in range(6):
            f.line(mx + 12 + c * 25, my + r * 22, mx + 12 + c * 25, my + r * 22 + 22, stroke=C["amber"][0], sw=1.8)
    f.text(115, my + 96, "细胞壁＝糖链（绿）＋交联（橙）的网", fs=10, fill=MUTED)
    # panel 2
    _rod(f, 255, 60, 170, 70)
    mx = 265
    f.rect(mx - 6, my - 8, 162, 92, fill="#fff", stroke="#d1d5db", rx=6)
    for r in range(4):
        f.line(mx, my + r * 22, mx + 150, my + r * 22, stroke=C["green"][0], sw=2.2)
    for r in range(3):
        for c in range(6):
            if (r + c) % 3 == 0: continue
            f.line(mx + 12 + c * 25, my + r * 22, mx + 12 + c * 25, my + r * 22 + 22, stroke=C["amber"][0], sw=1.8)
    # enzyme + penicillin
    f.circle(mx + 62, my + 33, 10, fill=C["blue"][1], stroke=C["blue"][0])
    f.text(mx + 62, my + 37, "酶", fs=9.5, fill=C["blue"][0], weight=700)
    f.poly([(mx + 70, my + 22), (mx + 82, my + 16), (mx + 86, my + 28)], stroke=C["red"][0], fill=C["red"][0], closed=True)
    f.text(mx + 92, my + 16, "青霉素", fs=10, fill=C["red"][0], weight=700, anchor="start")
    f.text(340, my + 96, "交联砌不上，网上出现空洞", fs=10, fill=MUTED)
    f.text(340, 100, "仍在生长、分裂", fs=10.5, fill=C["green"][0])
    # panel 3: bursting
    cx = 565
    f.path(f"M{cx-85},95 C{cx-85},55 {cx-40},58 {cx-10},62 L{cx},72 L{cx+10},60 C{cx+50},56 {cx+85},60 {cx+85},95 C{cx+85},130 {cx+40},134 {cx+12},130 L{cx},118 L{cx-12},132 C{cx-50},134 {cx-85},130 {cx-85},95 Z",
           stroke=C["green"][0], sw=3, fill=C["green"][1], dash="10 5")
    for a in range(0, 360, 45):
        r1, r2 = 30, 46
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        f.arrow(cx + r1 * ca * 1.6, 95 + r1 * sa * 0.7, cx + r2 * ca * 1.9, 95 + r2 * sa * 0.95, color=C["red"][0], sw=1.4, size=6)
    f.text(cx, 99, "水涌入", fs=10.5, fill=C["red"][0], weight=700)
    # human cell
    f.circle(cx, 205, 34, fill=C["pink"][1], stroke=C["pink"][0], sw=1.2)
    f.circle(cx, 205, 11, fill="#fff", stroke=C["pink"][0], sw=1)
    f.text(cx, 256, "人体细胞：只有细胞膜、没有细胞壁", fs=10.5, fill=C["pink"][0], weight=700)
    f.text(cx, 272, "→ 青霉素无处下手", fs=10.5, fill=C["pink"][0], weight=700)
    f.text(340, 292, "原理：专打细菌有、人没有的结构（分子识别）", fs=11, weight=700)
    return f

# ------------------------------------------------------------------ drug discovery
@fig
def drug_discovery():
    f = Fig(680, 360, "新药研发漏斗")
    stages = [
        ("靶点发现 · 苗头筛选", "上万个候选分子", "blue", "2–4 年"),
        ("先导化合物优化", "几百个", "blue", ""),
        ("临床前：细胞和动物实验", "十几个", "teal", "1–2 年"),
        ("一期：几十名健康志愿者 · 安全吗", "约 10 个", "green", ""),
        ("二期：几百名患者 · 有效吗、多大剂量", "", "green", "5–7 年"),
        ("三期：上千名患者 · 随机对照", "", "green", ""),
        ("审批上市", "1 个", "amber", "约 1 年"),
    ]
    cx, top, H = 240, 24, 38
    w0, w1 = 420, 100
    n = len(stages)
    for i, (t, cnt, col, dur) in enumerate(stages):
        y = top + i * H
        wa = w0 - (w0 - w1) * i / n
        wb = w0 - (w0 - w1) * (i + 1) / n
        dark, light = C[col]
        f.poly([(cx - wa / 2, y), (cx + wa / 2, y), (cx + wb / 2, y + H - 4), (cx - wb / 2, y + H - 4)], stroke=dark, fill=light, sw=1.2, closed=True)
        f.text(cx, y + 22, t, fs=11.5 if i < 5 else 11, weight=700)
        if cnt:
            f.text(cx + wa / 2 + 10, y + 22, cnt, fs=11, anchor="start", fill=dark, weight=700)
    # bracket for clinical
    y1, y2 = top + 3 * H, top + 6 * H - 4
    bx = 560
    f.line(bx, y1, bx, y2, stroke=C["green"][0], sw=1.4)
    f.line(bx, y1, bx - 6, y1, stroke=C["green"][0], sw=1.4)
    f.line(bx, y2, bx - 6, y2, stroke=C["green"][0], sw=1.4)
    f.lines(bx + 8, (y1 + y2) / 2 - 6, ["临床试验", "约九成在这里失败"], fs=10.5, fill=C["green"][0], anchor="start", weight=700)
    f.text(cx, top + n * H + 14, "↓ 上市后继续监测罕见副作用（四期）", fs=10.5, fill=MUTED)
    # totals
    f.rect(480, 272, 190, 56, fill="#f9fafb", stroke="#d1d5db", rx=8)
    f.text(575, 294, "总计约 10–15 年", fs=12.5, weight=700)
    f.text(575, 316, "花费十亿美元级别", fs=12.5, weight=700, fill=C["red"][0])
    f.text(340, 352, "每一层都在问同一个问题：它能精准结合靶点、又不伤及其他吗？最后由统计说了算。", fs=10.5, fill=MUTED)
    return f

# ------------------------------------------------------------------ mRNA vaccine
@fig
def mrna_vaccine():
    f = Fig(680, 320, "mRNA 疫苗的工作流程")
    # LNP
    lx, ly = 60, 150
    f.circle(lx, ly, 32, fill=C["amber"][1], stroke=C["amber"][0], sw=2)
    for a in range(0, 360, 30):
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        f.circle(lx + 32 * ca, ly + 32 * sa, 3, fill=C["amber"][0], stroke=C["amber"][0])
    f.path(f"M{lx-18},{ly} q6,-10 12,0 t12,0 t12,0", stroke=C["red"][0], sw=2)
    f.lines(lx, ly + 52, ["① 脂质纳米颗粒", "包着 mRNA"], fs=10.5, weight=700, fill=C["amber"][0])
    # cell
    ellipse(f, 330, 155, 200, 115, stroke=C["slate"][0], sw=1.6, fill="#f8fafc")
    f.text(330, 30, "人体细胞（如注射部位的肌肉细胞、免疫细胞）", fs=10.5, fill=MUTED)
    f.arrow(96, 150, 150, 150, color=C["amber"][0], sw=2, size=8)
    # nucleus
    f.circle(250, 200, 36, fill=C["slate"][1], stroke=C["slate"][0], sw=1.2)
    f.lines(250, 196, ["细胞核", "（DNA）"], fs=10, fill=C["slate"][0], weight=700)
    f.text(250, 252, "mRNA 不进细胞核", fs=10, fill=C["red"][0], weight=700)
    # mRNA released + ribosome
    f.path("M170,120 q8,-10 16,0 t16,0 t16,0 t16,0 t16,0 t16,0", stroke=C["red"][0], sw=2.2)
    f.text(218, 104, "② mRNA＝蛋白“图纸”", fs=10.5, fill=C["red"][0], weight=700)
    ellipse(f, 280, 122, 15, 11, stroke=C["purple"][0], fill=C["purple"][1], sw=1.4)
    f.text(282, 145, "核糖体", fs=10, fill=C["purple"][0], weight=700)
    # protein chain
    for k in range(6):
        f.circle(300 + k * 11, 110 - k * 3, 5, fill=C["blue"][1], stroke=C["blue"][0], sw=1)
    f.text(345, 132, "③ 造出病毒蛋白", fs=10.5, fill=C["blue"][0], weight=700, anchor="start")
    # display on surface
    for k, (sx, sy) in enumerate([(470, 110), (490, 150), (478, 192)]):
        f.poly([(sx + 18, sy), (sx, sy - 8), (sx, sy + 8)], stroke=C["blue"][0], fill=C["blue"][0], closed=True)
    f.text(420, 230, "④ 展示 / 分泌出去", fs=10.5, fill=C["blue"][0], weight=700)
    f.text(330, 286, "几天后 mRNA 被分解，不改变 DNA", fs=10.5, fill=MUTED)
    # immune response
    bx = 556
    f.box(bx, 54, 116, 44, "B 细胞", "green", fs=11.5, sub="产生抗体", sub_fs=10)
    f.box(bx, 108, 116, 44, "T 细胞", "teal", fs=11.5, sub="清除被感染细胞", sub_fs=10)
    f.box(bx, 162, 116, 44, "记忆细胞", "red", fs=11.5, sub="下次快速反击", sub_fs=10, solid=True)
    f.arrow(514, 150, 552, 80, color=C["green"][0], sw=1.4, size=7)
    f.arrow(514, 150, 552, 130, color=C["teal"][0], sw=1.4, size=7)
    f.arrow(514, 150, 552, 184, color=C["red"][0], sw=1.4, size=7)
    f.lines(bx + 58, 232, ["⑤ 免疫系统", "学会认这个蛋白"], fs=10.5, weight=700)
    return f

# ------------------------------------------------------------------ DNA double helix
@fig
def dna_double_helix():
    f = Fig(680, 340, "DNA 双螺旋与复制")
    # helix (vertical) on left
    cx, y0, y1, amp = 120, 40, 300, 46
    seq = "ATGCGTACCATGGA"
    N = 120
    def xa(t): return cx + amp * math.sin(t)
    ts = [y0 + (y1 - y0) * i / N for i in range(N + 1)]
    ph = lambda y: (y - y0) / (y1 - y0) * 2.5 * 2 * math.pi
    # rungs
    for k, b in enumerate(seq):
        y = y0 + 8 + k * (y1 - y0 - 16) / (len(seq) - 1)
        x1, x2 = xa(ph(y)), xa(ph(y) + math.pi)
        mid = (x1 + x2) / 2
        f.line(x1, y, mid, y, stroke=BASE_COL[b], sw=3.2, cap="butt")
        f.line(mid, y, x2, y, stroke=BASE_COL[PAIR[b]], sw=3.2, cap="butt")
    f.poly([(xa(ph(y)), y) for y in ts], stroke=C["slate"][0], sw=3.6)
    f.poly([(xa(ph(y) + math.pi), y) for y in ts], stroke=C["purple"][0], sw=3.6)
    f.text(cx, 24, "双螺旋", fs=13, weight=700)
    f.line(cx - amp, 318, cx + amp, 318, stroke=MUTED, sw=1)
    f.text(cx, 334, "直径约 2 纳米", fs=10, fill=MUTED)
    f.lines(cx + 58, 70, ["糖—磷酸", "骨架"], fs=10.5, fill=C["slate"][0], anchor="start", weight=700)
    f.lines(cx + 58, 150, ["碱基对", "（横档）"], fs=10.5, fill=INK, anchor="start", weight=700)
    f.lines(cx + 58, 230, ["约 10 对", "转一圈"], fs=10.5, fill=MUTED, anchor="start")
    # pairing legend
    lx, ly = 260, 50
    f.text(lx + 70, ly - 18, "配对规则", fs=12.5, weight=700)
    for i, (a, b, hb) in enumerate((("A", "T", 2), ("G", "C", 3))):
        y = ly + i * 52
        f.box(lx, y, 40, 30, a, "red" if a == "A" else "green", fs=15, solid=True)
        f.box(lx + 100, y, 40, 30, b, "amber" if b == "T" else "blue", fs=15, solid=True)
        for h in range(hb):
            yy = y + 15 + (h - (hb - 1) / 2) * 7
            f.line(lx + 44, yy, lx + 96, yy, stroke=MUTED, sw=1.2, dash="3 3")
        f.text(lx + 70, y + 46, f"{hb} 个氢键", fs=10, fill=MUTED)
    f.text(lx + 70, 170, "知道一条链", fs=11, weight=700)
    f.text(lx + 70, 186, "就能推出另一条", fs=11, weight=700)
    # replication fork on right
    rx, ry = 400, 70
    f.text(560, 24, "半保留复制", fs=13, weight=700)
    top = "ATGCGT"
    bot = "".join(PAIR[b] for b in top)
    # parental double region (left)
    dx = 16
    strand(f, rx, ry + 100, top, dx=dx, col=C["slate"][0], up=True, show=False)
    strand(f, rx, ry + 124, bot, dx=dx, col=C["purple"][0], up=False, show=False)
    # fork: upper strand goes up-right, lower goes down-right
    fx = rx + dx * 6
    up_seq, dn_seq = "CATGA", "GTACT"
    for i in range(5):
        x = fx + 8 + i * 18
        yu = ry + 100 - (i + 1) * 14
        yd = ry + 124 + (i + 1) * 14
        b = up_seq[i]
        # old strands
        f.line(x - 18, yu + 14, x, yu, stroke=C["slate"][0], sw=2.2)
        f.line(x - 18, yd - 14, x, yd, stroke=C["purple"][0], sw=2.2)
        # base ticks
        f.line(x, yu, x + 6, yu + 8, stroke=BASE_COL[b], sw=2.4)
        f.line(x, yd, x + 6, yd - 8, stroke=BASE_COL[dn_seq[i]], sw=2.4)
        if i < 4:  # new strand partners
            f.line(x + 6, yu + 8, x + 12, yu + 16, stroke=BASE_COL[PAIR[b]], sw=2.4)
            f.line(x + 6, yd - 8, x + 12, yd - 16, stroke=BASE_COL[PAIR[dn_seq[i]]], sw=2.4)
    f.poly([(fx + 20, ry + 108), (fx + 74, ry + 64)], stroke=C["red"][0], sw=2.4)
    f.poly([(fx + 20, ry + 116), (fx + 74, ry + 160)], stroke=C["red"][0], sw=2.4)
    f.text(rx + 48, ry + 160, "旧双链", fs=10.5, fill=MUTED)
    f.text(fx + 96, ry + 24, "旧链（模板）", fs=10.5, fill=C["slate"][0], anchor="start", weight=700)
    f.text(fx + 70, ry + 52, "新链", fs=10.5, fill=C["red"][0], anchor="start", weight=700)
    f.text(fx + 96, ry + 206, "旧链（模板）", fs=10.5, fill=C["purple"][0], anchor="start", weight=700)
    f.text(fx + 70, ry + 182, "新链", fs=10.5, fill=C["red"][0], anchor="start", weight=700)
    f.text(560, 312, "结果：两份一样的 DNA，各含一条旧链", fs=10.5, weight=700)
    return f

# ------------------------------------------------------------------ recombinant DNA
@fig
def recombinant_dna():
    f = Fig(680, 300, "重组 DNA 的基本步骤")
    # step 1: gene from human DNA
    f.text(90, 26, "① 剪：同一把“剪刀”", fs=11.5, weight=700)
    f.rect(20, 46, 140, 12, fill=C["slate"][1], stroke=C["slate"][0], rx=2)
    f.rect(60, 46, 60, 12, fill=C["red"][0], stroke=C["red"][0], rx=1)
    f.text(90, 74, "人的 DNA：目标基因（红）", fs=10, fill=MUTED)
    f.text(90, 92, "限制酶在 GAATTC 处切开", fs=10, fill=C["blue"][0], weight=700)
    # cut gene with sticky ends
    f.rect(62, 104, 56, 12, fill=C["red"][0], stroke=C["red"][0], rx=1)
    f.rect(56, 104, 6, 6, fill=C["red"][0], stroke=C["red"][0], rx=0)
    f.rect(118, 110, 6, 6, fill=C["red"][0], stroke=C["red"][0], rx=0)
    f.text(90, 132, "带“黏性末端”的基因片段", fs=10, fill=C["red"][0])
    # plasmid
    pcx, pcy = 90, 205
    f.path(f"M{pcx+10},{pcy-44} A44,44 0 1,1 {pcx-10},{pcy-44}", stroke=C["blue"][0], sw=6)
    f.path(f"M{pcx+40},{pcy+18} A44,44 0 0,1 {pcx+14},{pcy+42}", stroke=C["green"][0], sw=6)
    f.text(pcx, pcy + 4, "质粒", fs=11.5, fill=C["blue"][0], weight=700)
    f.text(pcx + 58, pcy + 50, "抗药基因", fs=10, fill=C["green"][0], anchor="start", weight=700)
    f.text(pcx, pcy - 56, "切口", fs=10, fill=C["blue"][0])
    f.text(pcx, 290, "细菌里的环状小 DNA", fs=10, fill=MUTED)
    f.arrow(176, 150, 214, 150, color=INK, sw=1.8)
    # step 2: ligate
    f.text(280, 26, "② 贴：连接酶缝合", fs=11.5, weight=700)
    c2x, c2y = 280, 150
    f.path(f"M{c2x+14},{c2y-44} A44,44 0 1,1 {c2x-14},{c2y-44}", stroke=C["blue"][0], sw=6)
    f.path(f"M{c2x-14},{c2y-44} A44,44 0 0,1 {c2x+14},{c2y-44}", stroke=C["red"][0], sw=6)
    f.path(f"M{c2x+40},{c2y+18} A44,44 0 0,1 {c2x+14},{c2y+42}", stroke=C["green"][0], sw=6)
    f.text(c2x, c2y + 4, "重组质粒", fs=11.5, weight=700)
    f.text(c2x, c2y + 76, "基因被“缝”进质粒", fs=10, fill=MUTED)
    f.arrow(338, 150, 376, 150, color=INK, sw=1.8)
    # step 3: into bacteria + select
    f.text(452, 26, "③ 导入细菌，抗生素筛选", fs=11.5, weight=700)
    for k, ok in enumerate((True, False, True, False)):
        x, y = 392 + (k % 2) * 66, 70 + (k // 2) * 74
        _rod(f, x, y, 54, 28, wall=C["green"][0] if ok else C["gray"][0], fill=C["green"][1] if ok else "#fff", sw=2, dash=None if ok else "4 3")
        if ok:
            f.circle(x + 27, y + 14, 7, fill="none", stroke=C["red"][0], sw=2)
        else:
            f.line(x + 14, y + 6, x + 40, y + 22, stroke=C["gray"][0], sw=1.6)
    f.lines(452, 236, ["含抗生素的培养基里", "只有拿到质粒的细菌活下来"], fs=10, fill=MUTED)
    f.arrow(526, 150, 560, 150, color=INK, sw=1.8)
    # step 4: produce
    f.text(620, 26, "④ 繁殖并生产", fs=11.5, weight=700)
    f.rect(578, 60, 84, 130, fill=C["blue"][1], stroke=C["blue"][0], rx=10)
    for k in range(9):
        _rod(f, 588 + (k % 3) * 24, 76 + (k // 3) * 22, 18, 10, sw=1.2)
    for k in range(6):
        f.circle(592 + (k % 3) * 24, 150 + (k // 3) * 16, 4, fill=C["red"][0], stroke=C["red"][0])
    f.text(620, 210, "发酵罐", fs=10.5, fill=C["blue"][0], weight=700)
    f.lines(620, 232, ["目标蛋白", "（如人胰岛素）"], fs=10.5, fill=C["red"][0], weight=700)
    return f

# ------------------------------------------------------------------ PCR
@fig
def pcr():
    f = Fig(680, 320, "PCR 聚合酶链式反应")
    steps = [("① 变性 约 95°C", "双链解开", "red"), ("② 退火 约 55–65°C", "引物贴到两端", "blue"), ("③ 延伸 约 72°C", "聚合酶补齐新链", "green")]
    for i, (t, s, col) in enumerate(steps):
        x0 = 20 + i * 220
        f.rect(x0, 18, 200, 136, fill=C[col][1], stroke=C[col][0], sw=1, rx=8)
        f.text(x0 + 100, 38, t, fs=12, weight=700, fill=C[col][0])
        f.text(x0 + 100, 144, s, fs=10.5, fill=INK)
        L = 160
        xs = x0 + 20
        if i == 0:
            f.line(xs, 70, xs + L, 70, stroke=C["slate"][0], sw=3)
            f.line(xs, 110, xs + L, 110, stroke=C["purple"][0], sw=3)
            for k in range(8):
                f.arrow(xs + 10 + k * 20, 82, xs + 10 + k * 20, 74, color=C["red"][0], sw=1, size=5)
                f.arrow(xs + 10 + k * 20, 98, xs + 10 + k * 20, 106, color=C["red"][0], sw=1, size=5)
        else:
            f.line(xs, 70, xs + L, 70, stroke=C["slate"][0], sw=3)
            f.line(xs, 110, xs + L, 110, stroke=C["purple"][0], sw=3)
            f.rect(xs + L - 34, 76, 30, 7, fill=C["blue"][0], stroke=C["blue"][0], rx=1)
            f.rect(xs + 4, 97, 30, 7, fill=C["blue"][0], stroke=C["blue"][0], rx=1)
            if i == 2:
                f.line(xs + 8, 79.5, xs + L - 34, 79.5, stroke=C["green"][0], sw=3.5)
                f.line(xs + 34, 100.5, xs + L - 8, 100.5, stroke=C["green"][0], sw=3.5)
                f.head(xs + 8, 79.5, math.pi, C["green"][0], 8)
                f.head(xs + L - 8, 100.5, 0, C["green"][0], 8)
                ellipse(f, xs + 30, 79.5, 12, 8, stroke=C["amber"][0], fill=C["amber"][1], sw=1.2)
                f.text(xs + 30, 64, "Taq 酶", fs=9.5, fill=C["amber"][0], weight=700)
            else:
                f.text(xs + L - 19, 94, "引物", fs=9.5, fill=C["blue"][0], weight=700)
        if i < 2:
            f.arrow(x0 + 202, 86, x0 + 218, 86, color=INK, sw=1.6, size=7)
    # bottom: temperature profile
    f.text(170, 182, "温度曲线：一个循环几分钟，重复约 30 次", fs=11, weight=700)
    gx, gy = 30, 290
    f.line(gx, gy, gx + 290, gy, stroke=INK, sw=1)
    f.line(gx, gy, gx, gy - 92, stroke=INK, sw=1)
    def T(v): return gy - (v - 40) * 1.5
    pts = []
    x = gx + 4
    for c in range(3):
        for v, w in ((95, 22), (60, 22), (72, 30)):
            pts += [(x, T(v)), (x + w, T(v))]
            x += w + 6
    f.poly(pts, stroke=C["red"][0], sw=2)
    for v in (95, 72, 60):
        f.text(gx - 4, T(v) + 4, f"{v}°", fs=9, fill=MUTED, anchor="end")
    f.text(gx + 290, gy + 14, "时间", fs=9.5, fill=MUTED, anchor="end")
    # bottom right: doubling
    f.text(500, 182, "每个循环翻一倍", fs=11, weight=700)
    bx, by = 360, 290
    for k, (lab, n) in enumerate((("第 0 轮", 1), ("1", 2), ("2", 4), ("3", 8), ("4", 16))):
        x = bx + k * 46
        for j in range(n):
            col = j % 4
            f.line(x, by - 8 - j * 5, x + 30, by - 8 - j * 5, stroke=[C["slate"][0], C["green"][0], C["purple"][0], C["green"][0]][col], sw=2.4)
        f.text(x + 15, by + 12, lab, fs=9.5, fill=MUTED)
    f.text(bx + 238, by - 40, "…", fs=16, weight=700)
    f.lines(bx + 282, by - 64, ["第 30 轮", "约 10 亿份", "（2³⁰）"], fs=11, weight=700, fill=C["red"][0])
    return f

# ------------------------------------------------------------------ DNA sequencing
@fig
def dna_sequencing():
    f = Fig(680, 380, "桑格测序与测序成本")
    f.text(170, 24, "① 合成新链，随机在某个碱基处“刹车”", fs=11.5, weight=700)
    seq = "ACGTTAGC"
    x0, y0, dx = 40, 46, 26
    f.text(x0 - 8, y0 + 5, "模板", fs=10, anchor="end", fill=MUTED)
    f.line(x0, y0, x0 + dx * len(seq), y0, stroke=C["slate"][0], sw=2.4)
    for i, b in enumerate(seq):
        f.text(x0 + 13 + i * dx, y0 + 18, PAIR[b], fs=11, fill=MUTED, mono=True)
    # fragments
    for L in range(1, len(seq) + 1):
        y = y0 + 24 + L * 13
        f.line(x0, y, x0 + dx * L - 10, y, stroke=MUTED, sw=2)
        f.circle(x0 + dx * L - 6, y, 5, fill=BASE_COL[seq[L - 1]], stroke=BASE_COL[seq[L - 1]])
    f.text(x0 + 110, y0 + 24 + 9 * 13 + 4, "带荧光的终止剂（每种碱基一个颜色）", fs=10, fill=MUTED)
    # gel/capillary reading
    gx = 330
    f.text(gx + 90, 24, "② 按长度排队，从短到长读颜色", fs=11.5, weight=700)
    f.rect(gx, 40, 30, 150, fill="#111827", stroke=INK, rx=4)
    for L in range(1, len(seq) + 1):
        y = 190 - L * 17
        f.rect(gx + 4, y, 22, 6, fill=BASE_COL[seq[L - 1]], stroke="none", rx=1)
        f.text(gx + 42, y + 7, seq[L - 1], fs=12, fill=BASE_COL[seq[L - 1]], weight=700, anchor="start", mono=True)
    f.arrow(gx - 10, 184, gx - 10, 48, color=MUTED, sw=1.2, size=6)
    f.lines(gx - 16, 120, ["短", "→", "长"], fs=9.5, fill=MUTED, anchor="end")
    f.lines(gx + 80, 90, ["读出：", "A C G T T A G C"], fs=12, weight=700, anchor="start")
    f.lines(gx + 80, 140, ["毛细管电泳 + 激光", "自动读取，一次几百个碱基"], fs=10, fill=MUTED, anchor="start")
    # cost curve (NHGRI data)
    cy0, ch, cx0, cw = 360, 130, 70, 560
    f.text(340, 218, "③ 测一个人类基因组的成本（美元，对数坐标；数据：NHGRI）", fs=11.5, weight=700)
    f.line(cx0, cy0, cx0 + cw, cy0, stroke=INK, sw=1)
    f.line(cx0, cy0, cx0, cy0 - ch, stroke=INK, sw=1)
    def X(yr): return cx0 + (yr - 2001) / 21.5 * cw
    def Y(v): return cy0 - (math.log10(v) - 2) / 6 * ch
    for e, lab in ((2, "100"), (4, "1 万"), (6, "100 万"), (8, "1 亿")):
        f.text(cx0 - 6, Y(10 ** e) + 4, lab, fs=9.5, fill=MUTED, anchor="end")
        f.line(cx0, Y(10 ** e), cx0 + cw, Y(10 ** e), stroke="#e5e7eb", sw=0.8)
    for yr in (2001, 2005, 2010, 2015, 2020):
        f.text(X(yr), cy0 + 14, str(yr), fs=9.5, fill=MUTED)
    data = [(2001.75, 95.3e6), (2002.25, 70.2e6), (2003.25, 53.8e6), (2004.5, 19.9e6), (2005.5, 16.2e6), (2006.5, 11.5e6),
            (2007.5, 8.9e6), (2008.5, 7.5e5), (2009.5, 1.08e5), (2010.5, 3.1e4), (2011.5, 1.05e4), (2012.5, 6.0e3),
            (2013.5, 5.6e3), (2014.5, 4.9e3), (2015.5, 1.36e3), (2016.9, 1.36e3), (2017.9, 1.84e3), (2018.9, 1.39e3),
            (2019.9, 695), (2020.9, 512), (2022.4, 525)]
    f.poly([(X(a), Y(b)) for a, b in data], stroke=C["red"][0], sw=2.4)
    # Moore's law reference: halve every 2 years from 2001
    f.poly([(X(2001.75), Y(95.3e6)), (X(2022.4), Y(95.3e6 / 2 ** (20.65 / 2)))], stroke=C["blue"][0], sw=1.4, dash="5 4")
    f.text(X(2016), Y(95.3e6 / 2 ** (14.25 / 2)) - 8, "若按摩尔定律（两年减半）", fs=10, fill=C["blue"][0])
    f.text(X(2001.75) + 4, Y(95.3e6) + 18, "约 1 亿", fs=10, fill=C["red"][0], anchor="start", weight=700)
    f.text(X(2008.5) + 6, Y(7.5e5) - 2, "高通量测序登场", fs=10, fill=C["red"][0], anchor="start", weight=700)
    f.text(X(2022.4), Y(525) - 8, "约 500", fs=10, fill=C["red"][0], weight=700)
    return f

# ------------------------------------------------------------------ CRISPR
@fig
def crispr():
    f = Fig(680, 320, "CRISPR-Cas9 基因编辑")
    f.text(200, 24, "① 向导 RNA 找到匹配的位置，Cas9 剪断双链", fs=11.5, weight=700)
    # Cas9 blob
    f.path("M60,70 C40,40 120,30 200,38 C300,30 360,50 352,90 C360,140 300,160 200,154 C110,160 40,140 60,70 Z",
           stroke=C["blue"][0], fill=C["blue"][1], sw=1.6)
    f.text(80, 60, "Cas9 蛋白", fs=11, fill=C["blue"][0], weight=700, anchor="start")
    target = "GACGTTAGCATTCGAT"
    pam = "TGG"
    x0, dx = 40, 16
    top = target + pam + "CA"
    strand(f, x0, 96, top, dx=dx, col=C["slate"][0], up=False, show=True)
    bot = "".join(PAIR[b] for b in top)
    strand(f, x0, 132, bot, dx=dx, col=C["purple"][0], up=True, show=False)
    # guide RNA under top strand region (pairs with bottom? simplify: pairs with target)
    gx = x0 + 4 * dx
    f.path(f"M{x0 + 4},{112} L{x0 + 4 + dx * 15},{112} q30,0 40,30 q10,26 -20,30", stroke=C["red"][0], sw=2.6)
    f.text(x0 + 4 + dx * 7, 122, "向导 RNA（约 20 个碱基，与目标配对）", fs=9.5, fill=C["red"][0], weight=700)
    # PAM box
    px = x0 + 4 + dx * 16 - 6
    f.rect(px - 2, 74, dx * 3, 30, fill="none", stroke=C["amber"][0], sw=1.6, rx=3, dash="3 2")
    f.text(px + dx * 1.5 - 2, 184 - 116, "PAM", fs=10, fill=C["amber"][0], weight=700)
    # cut marks (3 bp upstream of PAM)
    cx = x0 + 4 + dx * 12.5
    for yy in (96, 132):
        f.line(cx - 6, yy - 8, cx + 6, yy + 8, stroke=C["red"][0], sw=2.4)
        f.line(cx + 6, yy - 8, cx - 6, yy + 8, stroke=C["red"][0], sw=2.4)
    f.text(cx - 10, 176, "✂ 在 PAM 前约 3 个碱基处双链断裂", fs=10.5, fill=C["red"][0], weight=700, anchor="end")
    f.text(520, 50, "换一段向导 RNA", fs=12, weight=700, fill=C["red"][0])
    f.text(520, 68, "＝换一个目标", fs=12, weight=700, fill=C["red"][0])
    f.lines(520, 98, ["以往：每个目标要", "重新设计一种蛋白", "CRISPR：只需合成", "一段新 RNA"], fs=10.5, fill=MUTED)
    # outcomes
    f.text(340, 202, "② 细胞修复断口：两种结果", fs=11.5, weight=700)
    f.box(30, 214, 300, 90, "直接粘回（常出错）", "slate", fs=12.5, sub="多出或少掉几个碱基\n→ 基因读错，被“敲除”\n用于研究基因功能、关掉致病基因", sub_fs=10.5)
    f.box(350, 214, 300, 90, "照模板修复", "green", fs=12.5, sub="同时提供一段正确序列\n→ 按模板改写\n用于“修正”突变（效率较低）", sub_fs=10.5)
    return f

# ------------------------------------------------------------------ small: antibiotic resistance
@fig
def antibiotic_resistance():
    f = Fig(520, 250, "耐药菌是怎样被“选”出来的")
    import random
    rnd = random.Random(7)
    def dish(cx, cy, n_s, n_r, dead=0):
        f.circle(cx, cy, 62, fill="#f9fafb", stroke=C["slate"][0], sw=1.6)
        pts = []
        while len(pts) < n_s + n_r + dead:
            x, y = rnd.uniform(-48, 48), rnd.uniform(-48, 48)
            if x * x + y * y < 48 * 48 and all((x - a) ** 2 + (y - b) ** 2 > 150 for a, b in pts):
                pts.append((x, y))
        for i, (x, y) in enumerate(pts):
            if i < n_r:
                _rod(f, cx + x - 7, cy + y - 4, 14, 8, wall=C["red"][0], fill=C["red"][1], sw=1.4)
            elif i < n_r + n_s:
                _rod(f, cx + x - 7, cy + y - 4, 14, 8, wall=C["green"][0], fill=C["green"][1], sw=1.4)
            else:
                f.line(cx + x - 5, cy + y - 4, cx + x + 5, cy + y + 4, stroke=C["gray"][0], sw=1.4)
                f.line(cx + x + 5, cy + y - 4, cx + x - 5, cy + y + 4, stroke=C["gray"][0], sw=1.4)
    dish(85, 110, 22, 2)
    dish(260, 110, 0, 2, dead=22)
    dish(435, 110, 0, 24)
    f.arrow(152, 110, 192, 110, color=INK, sw=1.6)
    f.text(172, 98, "用抗生素", fs=10, fill=C["red"][0], weight=700)
    f.arrow(327, 110, 367, 110, color=INK, sw=1.6)
    f.text(347, 98, "繁殖", fs=10, fill=MUTED, weight=700)
    f.lines(85, 196, ["用药前：多数敏感（绿）", "偶有耐药突变（红）"], fs=10.5)
    f.lines(260, 196, ["敏感菌被杀死", "耐药菌活了下来"], fs=10.5)
    f.lines(435, 196, ["耐药菌成了主流", "这种药不再管用"], fs=10.5, weight=700, fill=C["red"][0])
    f.text(260, 24, "药没有“制造”耐药，而是把本来就有的耐药菌“筛”了出来", fs=11, weight=700)
    f.text(260, 244, "耐药基因还能借质粒在细菌之间传递", fs=10, fill=MUTED)
    return f

# ------------------------------------------------------------------ small: clinical trial
@fig
def clinical_trial():
    f = Fig(520, 260, "随机对照试验")
    def people(x, y, n, col, cols=5):
        for i in range(n):
            px, py = x + (i % cols) * 14, y + (i // cols) * 18
            f.circle(px, py, 4, fill=C[col][0], stroke=C[col][0])
            f.path(f"M{px-5},{py+12} Q{px},{py+3} {px+5},{py+12} Z", stroke=C[col][0], fill=C[col][0], sw=1)
    people(20, 100, 15, "slate")
    f.text(48, 168, "符合条件的患者", fs=10.5)
    f.box(110, 104, 70, 40, "随机\n分组", "amber", fs=11.5, solid=True)
    f.arrow(92, 124, 108, 124, color=INK, sw=1.4, size=6)
    f.arrow(182, 114, 222, 70, color=INK, sw=1.4, size=6)
    f.arrow(182, 134, 222, 178, color=INK, sw=1.4, size=6)
    f.rect(226, 34, 160, 76, fill=C["blue"][1], stroke=C["blue"][0], rx=8)
    people(236, 52, 7, "blue", cols=7)
    f.text(306, 98, "试验组：新疗法", fs=11, weight=700, fill=C["blue"][0])
    f.rect(226, 142, 160, 76, fill=C["slate"][1], stroke=C["slate"][0], rx=8)
    people(236, 160, 8, "slate", cols=8)
    f.text(306, 206, "对照组：安慰剂或标准疗法", fs=10.5, weight=700, fill=C["slate"][0])
    f.rect(214, 24, 184, 204, fill="none", stroke=C["purple"][0], sw=1.4, rx=10, dash="5 4")
    f.text(306, 246, "双盲：患者和医生都不知道谁在哪组", fs=10.5, fill=C["purple"][0], weight=700)
    f.arrow(390, 72, 420, 110, color=INK, sw=1.4, size=6)
    f.arrow(390, 180, 420, 142, color=INK, sw=1.4, size=6)
    f.box(424, 96, 88, 60, "比较结果", "green", fs=11.5, sub="差别是否大于\n偶然的波动？", sub_fs=9.5)
    f.text(260, 14, "两组唯一的系统差别是疗法本身，结果的差异才能归功于它", fs=10.5, weight=700)
    return f

# ------------------------------------------------------------------ small: CT
@fig
def ct_scan():
    f = Fig(520, 260, "CT 计算机断层扫描")
    cx, cy, R = 130, 135, 92
    f.circle(cx, cy, R + 14, fill="#f1f5f9", stroke=C["slate"][0], sw=1.4)
    f.circle(cx, cy, R - 14, fill="#fff", stroke=C["slate"][0], sw=1.4)
    ellipse(f, cx, cy, 46, 30, stroke=C["pink"][0], fill=C["pink"][1], sw=1.3)
    f.circle(cx - 14, cy + 2, 8, fill="#e5e7eb", stroke=C["slate"][0], sw=1.2)
    f.circle(cx + 18, cy - 6, 6, fill=C["red"][1], stroke=C["red"][0], sw=1.2)
    a = math.radians(-120)
    tx, ty = cx + R * math.cos(a), cy + R * math.sin(a)
    f.rect(tx - 12, ty - 8, 24, 16, fill=C["amber"][1], stroke=C["amber"][0], rx=3)
    f.text(tx - 18, ty - 10, "X 光管", fs=10, fill=C["amber"][0], weight=700, anchor="end")
    # detector arc opposite
    b0, b1 = math.radians(30), math.radians(90)
    dx0, dy0 = cx + R * math.cos(b0), cy + R * math.sin(b0)
    dx1, dy1 = cx + R * math.cos(b1), cy + R * math.sin(b1)
    f.path(f"M{dx0:.1f},{dy0:.1f} A{R},{R} 0 0,1 {dx1:.1f},{dy1:.1f}", stroke=C["blue"][0], sw=7)
    f.text(cx + 78, cy + 92, "探测器", fs=10, fill=C["blue"][0], weight=700, anchor="start")
    for t in range(0, 7):
        bb = b0 + (b1 - b0) * t / 6
        f.line(tx, ty, cx + R * math.cos(bb), cy + R * math.sin(bb), stroke=C["purple"][0], sw=0.8, dash="3 3")
    f.path(f"M{cx - 60},{cy - 108} A118,118 0 0,1 {cx + 60},{cy - 108}", stroke=C["red"][0], sw=1.6)
    f.head(cx + 60, cy - 108, math.radians(35), C["red"][0], 8)
    f.text(cx + 70, 22, "一起旋转，从几百个角度拍", fs=10.5, fill=C["red"][0], weight=700, anchor="start")
    f.arrow(250, 135, 300, 135, color=INK, sw=1.6)
    f.text(275, 124, "计算机", fs=10, fill=MUTED)
    f.text(275, 154, "反推", fs=10, fill=MUTED)
    # reconstructed slice
    gx, gy, n, s = 320, 60, 10, 15
    for i in range(n):
        for j in range(n):
            x, y = (i - 4.5) / 4.6, (j - 4.5) / 3.2
            inside = x * x + y * y < 1
            v = 0
            if inside: v = 1
            if (i - 3) ** 2 + (j - 4.6) ** 2 < 1.6: v = 3
            if (i - 6.2) ** 2 + (j - 4) ** 2 < 1.0: v = 2
            fill = {0: "#111827", 1: "#9ca3af", 2: "#d1d5db", 3: "#f9fafb"}[v]
            f.rect(gx + i * s, gy + j * s, s, s, fill=fill, stroke="#374151", sw=0.4, rx=0)
    f.lines(gx + 75, gy + 172, ["算出每个小方格吸收了多少", "→ 一张“切片”图像"], fs=10.5, weight=700)
    return f

def main():
    only = set(sys.argv[1:])
    for name, fn in FIGS.items():
        if only and name not in only: continue
        fn().save(OUT / f"{name}.svg")
    print("wrote", len(only) if only else len(FIGS), "figures to", OUT)

if __name__ == "__main__":
    main()
