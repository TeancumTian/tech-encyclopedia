#!/usr/bin/env python3
"""Generate all diagrams for 第 2 篇「电与电子」 -> assets/figs/electronics/*.svg"""
from __future__ import annotations
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from svgkit import Fig, C, INK, MUTED, tw
from figs_energy import concept_map_layout

OUT = Path(__file__).resolve().parents[1] / "assets" / "figs" / "electronics"
FIGS = {}

def fig(fn):
    FIGS[fn.__name__.replace("_", "-")] = fn
    return fn


@fig
def concept_map():
    layers = [
        ("① 驯服电与磁", "blue", ["避雷针", "电子的发现", "电磁铁", "继电器", "发电机★", "电动机★", "感应电机",
                                "无刷电机", "变压器★", "交流电", "三相电", "断路器", "电气化"]),
        ("② 电力电子：随心变换电能", "teal", ["电力电子", "逆变器", "IGBT", "碳化硅 · 氮化镓", "开关电源", "无线充电"]),
        ("③ 电子元件：控制电子流", "amber", ["真空管★", "电阻 · 电容 · 电感", "负反馈放大器", "运算放大器", "晶体振荡器", "印刷电路板"]),
        ("④ 半导体与芯片", "red", ["半导体★", "PN 结★", "晶体管★", "MOSFET★", "CMOS", "集成电路★", "平面工艺",
                                 "摩尔定律★", "登纳德缩放", "片上系统 SoC", "FPGA", "ASIC"]),
        ("⑤ 芯片制造", "purple", ["晶圆", "光刻★", "EUV", "洁净室", "掺杂", "刻蚀 · 沉积", "FinFET · GAA",
                                 "工艺节点", "代工模式", "EDA", "先进封装", "出口管制"]),
        ("⑥ 感知、显示与信号", "green", ["模拟与数字", "模数转换", "示波器", "CRT", "LCD", "LED★", "OLED", "Micro LED",
                                    "触摸屏", "电子墨水", "图像传感器", "MEMS", "传感器", "霍尔 · 压电 · 热电"]),
        ("⑦ 走进千家万户", "pink", ["微波炉", "收音机", "计算器", "石英表", "可穿戴", "遥控器", "开源硬件",
                                 "冰箱", "洗衣机", "吸尘器", "电磁炉", "电饭煲", "恒温器"]),
    ]
    hist = [("1752", "富兰克林风筝"), ("1831", "法拉第电磁感应"), ("1834", "电动机"), ("1885", "实用变压器"),
            ("1888", "交流感应电机"), ("1897", "发现电子"), ("1904", "真空二极管"), ("1927", "负反馈"),
            ("1947", "晶体管"), ("1958", "集成电路"), ("1959", "MOSFET"), ("1965", "摩尔定律"),
            ("1987", "台积电"), ("2011", "FinFET"), ("2019", "EUV 量产"), ("2025", "2 纳米量产")]
    sides = [
        ("第一性原理", "red", ["电荷与电场", "欧姆定律 U=IR", "电磁感应", "洛伦兹力", "能带与禁带", "量子隧穿"]),
        ("电子学的一条主线", "amber", ["用小信号控制大电流", "继电器 → 真空管", "→ 晶体管 → 芯片", "越做越小、越快、", "越省电、越便宜"]),
        ("一颗芯片的数字", "purple", ["1971：约 2300 个", "2024：2000 多亿个", "约每两年翻一番", "最小结构 ≈ 几十个原子"]),
    ]
    footer = ["电网 · 发电厂 · 电池 → 第 1 篇「能源与动力」　CPU · GPU · 计算机 → 第 3 篇「计算与软件」",
              "无线电 · 手机 · 光纤 → 第 4 篇「互联网与通信」　AI 芯片 → 第 5 篇「人工智能」"]
    return concept_map_layout("电与电子 · 知识地图",
                              "从上往下读：先学会发电和用电，再学会用电去控制电，最后把亿万个\u201c电开关\u201d刻进一块硅片。",
                              layers, hist, sides, footer, "↓ 同一个物理：电荷受力而运动；变化的只是控制它的尺度")


# ------------------------------------------------------------------ 电的驯服
def magnet(f, x, y, w, h, pole, col):
    f.rect(x, y, w, h, fill=C[col][0], stroke="none", rx=3)
    f.text(x + w / 2, y + h / 2 + 6, pole, fs=18, fill="#fff", weight=700)


@fig
def electric_generator():
    f = Fig(680, 300, "发电机")
    magnet(f, 30, 70, 60, 120, "N", "red"); magnet(f, 290, 70, 60, 120, "S", "blue")
    for k in range(4):
        f.arrow(95, 90 + k * 26, 285, 90 + k * 26, color="#9ca3af", sw=1, size=6)
    f.text(190, 60, "磁感线", fs=10.5, fill=MUTED)
    f.poly([(140, 95), (240, 165), (240, 180), (140, 110)], stroke=C["amber"][0], sw=4, closed=True)
    f.text(190, 210, "旋转的线圈", fs=12, weight=700, fill=C["amber"][0])
    f.curve(150, 240, 190, 270, 235, 238, color=C["slate"][0], sw=2)
    f.text(190, 290, "外力（水、蒸汽、风）带动旋转", fs=11, fill=MUTED)
    # sine graph
    gx, gy, gw = 400, 150, 250
    f.line(gx, gy, gx + gw, gy, stroke=INK); f.line(gx, 60, gx, 240, stroke=INK)
    pts = [(gx + i, gy - 70 * math.sin(i / gw * 4 * math.pi)) for i in range(0, gw + 1, 3)]
    f.poly(pts, stroke=C["amber"][0], sw=2.4)
    f.text(gx + gw / 2, 262, "时间 →", fs=10.5, fill=MUTED)
    f.text(gx + 4, 52, "感应电压", fs=10.5, fill=MUTED, anchor="start")
    f.text(gx + gw / 2, 30, "磁通量周期变化 → 正弦交流电", fs=13, weight=700, fill=INK)
    f.text(gx + gw / 2, 286, "转得越快、磁场越强、匝数越多 → 电压越高", fs=11, fill=MUTED)
    return f


@fig
def electric_motor():
    f = Fig(680, 300, "直流电动机")
    magnet(f, 30, 80, 60, 120, "N", "red"); magnet(f, 330, 80, 60, 120, "S", "blue")
    for k in range(4):
        f.arrow(95, 100 + k * 26, 325, 100 + k * 26, color="#d1d5db", sw=1, size=6)
    f.rect(150, 110, 120, 60, fill="none", stroke=C["amber"][0], sw=4, rx=2)
    f.arrow(150, 140, 150, 70, color=C["green"][0], sw=2.6); f.text(140, 66, "受力↑", fs=11.5, fill=C["green"][0], weight=700, anchor="end")
    f.arrow(270, 140, 270, 210, color=C["green"][0], sw=2.6); f.text(280, 222, "受力↓", fs=11.5, fill=C["green"][0], weight=700, anchor="start")
    f.curve(300, 60, 330, 30, 360, 60, color=C["purple"][0], sw=2)
    f.text(372, 46, "线圈转起来", fs=11.5, fill=C["purple"][0], weight=700, anchor="start")
    # commutator
    f.path("M195,235 A15,15 0 0 1 210,220 L210,235 Z", fill=C["slate"][0], stroke="none")
    f.path("M225,235 A15,15 0 0 0 210,220 L210,235 Z", fill="#9ca3af", stroke="none")
    f.line(210, 170, 210, 220, stroke=C["amber"][0], sw=2)
    f.text(232, 234, "换向器：每半圈翻转电流", fs=11, fill=MUTED, anchor="start")
    f.box(30, 250, 120, 36, "电池 / 电源", "amber", fs=12)
    f.line(150, 268, 195, 240, stroke=INK, sw=1.4)
    f.rect(430, 60, 230, 170, fill="#fff", stroke=C["blue"][0], rx=10)
    f.lines(545, 86, ["电流在磁场中受力", "F = B · I · L", "（洛伦兹力）", "", "线圈两边电流方向相反", "→ 一边向上、一边向下", "→ 形成转矩"], fs=12, fill=INK)
    f.text(545, 260, "发电机反过来用就是电动机", fs=11.5, weight=700, fill=C["blue"][0])
    return f


@fig
def transformer_electrical():
    f = Fig(680, 280, "变压器")
    f.path("M200,50 L480,50 L480,230 L200,230 Z M240,90 L440,90 L440,190 L240,190 Z", fill="#cbd5e1", stroke=C["slate"][0], sw=1.4)
    f.path("M200,50 L480,50 L480,230 L200,230 Z", fill="none", stroke=C["slate"][0], sw=1.4)
    f.rect(240, 90, 200, 100, fill="#fff", stroke=C["slate"][0], rx=0, sw=1.4)
    f.text(340, 75, "铁芯（引导磁通）", fs=11.5, fill=C["slate"][0], weight=700)
    for k in range(5):
        y = 100 + k * 18
        f.rect(190, y, 60, 10, fill=C["red"][0], stroke="none", rx=5)
    for k in range(10):
        y = 96 + k * 9.5
        f.rect(430, y, 60, 6, fill=C["blue"][0], stroke="none", rx=3)
    f.arrow(300, 140, 380, 140, color=C["purple"][0], sw=2, both=True)
    f.text(340, 132, "交变磁场", fs=11, fill=C["purple"][0], weight=700)
    f.text(340, 160, "", fs=10)
    f.line(190, 105, 120, 105, stroke=C["red"][0], sw=2); f.line(190, 177, 120, 177, stroke=C["red"][0], sw=2)
    f.line(490, 99, 560, 99, stroke=C["blue"][0], sw=2); f.line(490, 181, 560, 181, stroke=C["blue"][0], sw=2)
    f.lines(70, 136, ["初级", "5 匝", "220 伏"], fs=12, weight=700, fill=C["red"][0])
    f.lines(610, 136, ["次级", "10 匝", "440 伏"], fs=12, weight=700, fill=C["blue"][0])
    f.text(340, 258, "电压之比 = 匝数之比；只对交流电有效（直流不产生变化的磁场）", fs=12, weight=700, fill=INK)
    return f


@fig
def three_phase_power():
    f = Fig(520, 240, "三相交流电")
    gx, gy, gw = 40, 110, 440
    f.line(gx, gy, gx + gw, gy, stroke=INK); f.line(gx, 30, gx, 190, stroke=INK)
    for k, col in enumerate(["red", "amber", "blue"]):
        pts = [(gx + i, gy - 70 * math.sin(i / gw * 4 * math.pi - k * 2 * math.pi / 3)) for i in range(0, gw + 1, 3)]
        f.poly(pts, stroke=C[col][0], sw=2.2)
        f.text(gx + gw + 6, 40 + k * 18, ["A 相", "B 相", "C 相"][k], fs=11, fill=C[col][0], weight=700, anchor="start")
    f.text(gx + gw / 2, 210, "三条波依次错开 120°：任意时刻三者之和为零，可共用回线", fs=11.5, fill=INK)
    f.text(gx + gw / 2, 230, "接入电机后合成一个匀速旋转的磁场", fs=11, fill=MUTED)
    return f


# ------------------------------------------------------------------ 电子元件
@fig
def vacuum_tube():
    f = Fig(680, 300, "真空三极管")
    f.path("M120,270 L120,80 C120,20 280,20 280,80 L280,270 Z", fill="#f8fafc", stroke=C["slate"][0], sw=2)
    f.text(200, 290, "玻璃管内抽成真空", fs=11, fill=MUTED)
    f.rect(150, 60, 100, 14, fill=C["red"][0], stroke="none", rx=2)
    f.text(300, 72, "阳极（+，收集电子）", fs=11.5, anchor="start", weight=700, fill=C["red"][0])
    for k in range(7):
        f.circle(158 + k * 14, 150, 3, fill=C["amber"][0], stroke="none")
    f.line(150, 150, 250, 150, stroke=C["amber"][0], sw=1, dash="2 4")
    f.text(300, 154, "栅极（小电压控制）", fs=11.5, anchor="start", weight=700, fill=C["amber"][0])
    f.rect(150, 230, 100, 14, fill=C["slate"][0], stroke="none", rx=2)
    f.path("M160,252 l10,8 l10,-8 l10,8 l10,-8 l10,8 l10,-8 l10,8 l10,-8", stroke=C["red"][0], sw=1.4)
    f.text(300, 242, "阴极（加热后发射电子）", fs=11.5, anchor="start", weight=700, fill=C["slate"][0])
    for k in range(5):
        x = 165 + k * 18
        f.arrow(x, 224, x, 80, color=C["blue"][0], sw=1.2, size=6, dash="3 3")
    f.text(200, 196, "e⁻", fs=12, fill=C["blue"][0], weight=700)
    f.rect(470, 110, 190, 120, fill="#fff", stroke=C["blue"][0], rx=10)
    f.lines(565, 134, ["栅极电压略负 → 电子被推回", "栅极电压略正 → 电子涌过", "", "栅极上微小的变化", "→ 阳极电流大幅变化", "= 放大 / 开关"], fs=11, fill=INK)
    return f


# ------------------------------------------------------------------ 半导体
@fig
def semiconductor():
    f = Fig(680, 300, "能带")
    cols = [("金属（导体）", "green", 0, "能带重叠：电子随意流动"), ("半导体", "amber", 40, "禁带约 1 电子伏：加热、掺杂、光照就能导电"),
            ("绝缘体", "red", 120, "禁带太宽：电子跳不过去")]
    for k, (name, col, gap, note) in enumerate(cols):
        x = 40 + k * 215
        f.text(x + 85, 28, name, fs=14, weight=700, fill=C[col][0])
        top_y = 60
        cb_bottom = 115 if gap == 0 else 105
        gap = {0: 0, 40: 40, 120: 90}[gap]
        vb_top = cb_bottom + gap - (20 if gap == 0 else 0)
        f.rect(x + 30, top_y, 110, cb_bottom - top_y, fill=C["blue"][1], stroke=C["blue"][0], rx=2)
        f.text(x + 85, top_y + 20, "导带", fs=11, fill=C["blue"][0], weight=700)
        f.rect(x + 30, vb_top, 110, 55, fill=C["slate"][1] if gap else C["green"][1], stroke=C["slate"][0], rx=2, opacity=0.9)
        f.text(x + 85, vb_top + 44, "价带", fs=11, fill=C["slate"][0], weight=700)
        if gap:
            f.arrow(x + 150, cb_bottom, x + 150, vb_top, color=C[col][0], both=True, sw=1.4, size=6)
            f.text(x + 156, (cb_bottom + vb_top) / 2 + 4, "禁带", fs=10.5, anchor="start", fill=C[col][0])
        for j in range(5):
            f.circle(x + 45 + j * 20, vb_top + 16, 4, fill=C["blue"][0], stroke="none")
        if gap == 0:
            for j in range(3):
                f.circle(x + 55 + j * 25, top_y + 42, 4, fill=C["blue"][0], stroke="none")
        if gap == 40:
            f.circle(x + 85, top_y + 40, 4, fill=C["blue"][0], stroke="none")
            f.curve(x + 65, vb_top + 14, x + 60, 120, x + 81, top_y + 44, color=C["amber"][0], sw=1.4, size=6)
        f.lines(x + 85, 274, [note] if len(note) < 16 else [note[:note.index("：") + 1], note[note.index("：") + 1:]], fs=10.5, fill=INK)
    f.text(20, 60, "能量↑", fs=10.5, fill=MUTED, anchor="start")
    return f


@fig
def pn_junction():
    f = Fig(680, 300, "PN 结")
    X = 120
    f.rect(X, 50, 190, 120, fill=C["red"][1], stroke=C["red"][0], rx=0)
    f.rect(X + 190, 50, 60, 120, fill="#fff", stroke=C["purple"][0], rx=0, dash="4 3")
    f.rect(X + 250, 50, 190, 120, fill=C["blue"][1], stroke=C["blue"][0], rx=0)
    f.text(X + 95, 40, "P 型（掺硼，多空穴 ⊕）", fs=12, weight=700, fill=C["red"][0])
    f.text(X + 345, 40, "N 型（掺磷，多电子 ⊖）", fs=12, weight=700, fill=C["blue"][0])
    for r in range(3):
        for c in range(5):
            f.circle(X + 25 + c * 35, 80 + r * 30, 7, fill="#fff", stroke=C["red"][0], sw=1.4)
            f.circle(X + 275 + c * 35, 80 + r * 30, 6, fill=C["blue"][0], stroke="none")
    f.text(X + 220, 100, "耗尽层", fs=11, weight=700, fill=C["purple"][0])
    f.arrow(X + 240, 125, X + 200, 125, color=C["purple"][0], sw=1.6, size=7)
    f.text(X + 220, 150, "内建电场", fs=10, fill=C["purple"][0])
    # forward / reverse
    f.box(40, 200, 290, 80, "正向偏置：P 接正、N 接负", "green", fs=12.5, sub="耗尽层变薄 → 电流畅通（约 0.7 伏起）")
    f.box(350, 200, 290, 80, "反向偏置：P 接负、N 接正", "red", fs=12.5, sub="耗尽层变厚 → 几乎没有电流")
    f.text(340, 296, "所以 PN 结像一道只许电流单向通过的阀门：二极管", fs=11, fill=MUTED)
    return f


@fig
def transistor():
    f = Fig(680, 300, "晶体管")
    # point contact sketch
    f.text(110, 26, "1947 点接触晶体管", fs=12.5, weight=700, fill=C["slate"][0])
    f.rect(40, 200, 140, 40, fill=C["slate"][1], stroke=C["slate"][0], rx=2)
    f.text(110, 226, "锗晶体", fs=11, fill=C["slate"][0], weight=700)
    f.poly([(80, 80), (110, 196), (140, 80)], fill=C["purple"][1], stroke=C["purple"][0], closed=True)
    f.line(103, 194, 103, 60, stroke=C["amber"][0], sw=2); f.line(117, 194, 117, 60, stroke=C["amber"][0], sw=2)
    f.text(110, 54, "两根金触点", fs=10.5, fill=C["amber"][0])
    f.line(110, 240, 110, 262, stroke=INK, sw=2); f.text(110, 280, "底座", fs=10.5, fill=MUTED)
    # amplifier
    f.rect(220, 40, 210, 220, fill=C["green"][1], stroke=C["green"][0], rx=10)
    f.text(325, 64, "用法一：放大", fs=14, weight=700, fill=C["green"][0])
    pts = [(240 + i, 130 - 8 * math.sin(i / 12)) for i in range(0, 60, 2)]
    f.poly(pts, stroke=C["blue"][0], sw=2)
    f.box(305, 110, 50, 40, "晶体管", "slate", fs=10, solid=True)
    pts = [(365 + i, 130 - 40 * math.sin(i / 12)) for i in range(0, 60, 2)]
    f.poly(pts, stroke=C["red"][0], sw=2.4)
    f.text(325, 200, "小信号 → 同样形状的大信号", fs=11, fill=INK)
    f.text(325, 220, "收音机、音响、传感器", fs=10.5, fill=MUTED)
    # switch
    f.rect(450, 40, 210, 220, fill=C["blue"][1], stroke=C["blue"][0], rx=10)
    f.text(555, 64, "用法二：开关", fs=14, weight=700, fill=C["blue"][0])
    f.box(475, 90, 70, 50, "1", "blue", fs=20, solid=True, sub="导通")
    f.box(565, 90, 70, 50, "0", "slate", fs=20, sub="截止")
    f.text(555, 175, "控制端的电压决定通还是断", fs=11, fill=INK)
    f.text(555, 195, "亿万个开关组合 → 计算", fs=11, fill=INK)
    f.text(555, 220, "CPU、内存、所有数字芯片", fs=10.5, fill=MUTED)
    f.text(440, 290, "共同点：用一个小的电信号控制一个大的电流", fs=12, weight=700, fill=INK)
    return f


@fig
def mosfet():
    f = Fig(680, 300, "MOSFET")
    f.rect(80, 120, 520, 140, fill=C["red"][1], stroke=C["red"][0], rx=0)
    f.text(340, 245, "P 型硅衬底", fs=12, weight=700, fill=C["red"][0])
    f.rect(110, 120, 140, 50, fill=C["blue"][1], stroke=C["blue"][0], rx=0)
    f.text(180, 150, "N⁺ 源极", fs=12, weight=700, fill=C["blue"][0])
    f.rect(430, 120, 140, 50, fill=C["blue"][1], stroke=C["blue"][0], rx=0)
    f.text(500, 150, "N⁺ 漏极", fs=12, weight=700, fill=C["blue"][0])
    f.rect(250, 108, 180, 12, fill="#fef9c3", stroke=C["amber"][0], rx=0)
    f.text(440, 112, "绝缘层（二氧化硅等）", fs=10, anchor="start", fill=C["amber"][0])
    f.rect(250, 70, 180, 38, fill=C["slate"][0], stroke="none", rx=0)
    f.text(340, 94, "栅极 G（+）", fs=12, fill="#fff", weight=700)
    # channel
    f.rect(250, 121, 180, 12, fill=C["blue"][0], stroke="none", rx=0, opacity=0.8)
    for k in range(8):
        f.circle(262 + k * 22, 127, 2.6, fill="#fff", stroke="none")
    f.text(340, 188, "电场吸出电子 → 形成导电沟道", fs=11.5, weight=700, fill=C["blue"][0])
    f.arrow(200, 205, 480, 205, color=C["blue"][0], sw=1.8, label="电子从源极流向漏极", loff=(0, 18), lcolor=C["blue"][0])
    for x, lab in ((150, "源极 S"), (548, "漏极 D")):
        f.line(x, 120, x, 50, stroke=INK, sw=2); f.text(x, 42, lab, fs=11.5, weight=700)
    f.line(340, 70, 340, 40, stroke=INK, sw=2)
    f.text(340, 286, "栅极不加电压：没有沟道，关；加正电压：沟道出现，开。栅极几乎不耗电流。", fs=11.5, fill=INK)
    return f


@fig
def cmos():
    f = Fig(520, 280, "CMOS 非门")
    f.text(130, 26, "VDD（电源，1）", fs=11.5, weight=700, fill=C["red"][0])
    f.line(60, 34, 200, 34, stroke=C["red"][0], sw=2.4)
    f.box(90, 60, 80, 50, "P 管", "red", fs=12.5, sub="输入 0 时通")
    f.box(90, 160, 80, 50, "N 管", "blue", fs=12.5, sub="输入 1 时通")
    f.line(130, 34, 130, 60, stroke=INK, sw=2); f.line(130, 110, 130, 160, stroke=INK, sw=2)
    f.line(130, 210, 130, 240, stroke=INK, sw=2)
    f.line(60, 240, 200, 240, stroke=C["slate"][0], sw=2.4)
    f.text(130, 262, "GND（地，0）", fs=11.5, weight=700, fill=C["slate"][0])
    f.line(30, 135, 70, 135, stroke=INK, sw=2); f.line(70, 85, 70, 185, stroke=INK, sw=2)
    f.line(70, 85, 90, 85, stroke=INK, sw=2); f.line(70, 185, 90, 185, stroke=INK, sw=2)
    f.text(24, 130, "输入", fs=11.5, anchor="end", weight=700)
    f.line(130, 135, 220, 135, stroke=INK, sw=2); f.text(228, 140, "输出", fs=11.5, anchor="start", weight=700)
    # truth table
    tx, ty = 320, 70
    for j, h in enumerate(["输入", "导通的管", "输出"]):
        f.rect(tx + j * 60, ty, 60, 26, fill=C["purple"][1], stroke=C["purple"][0], rx=0, sw=0.8)
        f.text(tx + j * 60 + 30, ty + 18, h, fs=11, weight=700)
    for r, row in enumerate([["0", "P 管", "1"], ["1", "N 管", "0"]]):
        for j, v in enumerate(row):
            f.rect(tx + j * 60, ty + 26 * (r + 1), 60, 26, fill="#fff", stroke=C["purple"][0], rx=0, sw=0.8)
            f.text(tx + j * 60 + 30, ty + 26 * (r + 1) + 18, v, fs=12)
    f.lines(410, 180, ["两只管子总是一开一关", "电源到地不会直接导通", "→ 只在翻转瞬间耗电"], fs=11, fill=INK)
    return f


@fig
def integrated_circuit():
    f = Fig(680, 300, "从晶圆到芯片")
    f.circle(110, 150, 95, fill="#e5e7eb", stroke=C["slate"][0], sw=2)
    for i in range(-5, 6):
        for j in range(-5, 6):
            x, y = 110 + i * 16, 150 + j * 16
            if (i * 16) ** 2 + (j * 16) ** 2 < 84 ** 2:
                f.rect(x - 7, y - 7, 14, 14, fill=C["purple"][1], stroke=C["purple"][0], sw=0.6, rx=1)
    f.rect(110 + 2 * 16 - 7, 150 - 1 * 16 - 7, 14, 14, fill=C["amber"][0], stroke="none", rx=1)
    f.text(110, 268, "晶圆（直径 300 毫米）", fs=11.5, weight=700)
    f.text(110, 286, "一次造出数百颗芯片", fs=10.5, fill=MUTED)
    f.arrow(150, 134, 250, 100, color=C["amber"][0], sw=1.6)
    # die
    f.rect(255, 40, 170, 170, fill=C["purple"][1], stroke=C["purple"][0], sw=2, rx=4)
    for (x, y, w, h, lab, col) in [(265, 50, 70, 60, "CPU 核", "blue"), (345, 50, 70, 60, "GPU", "green"), (265, 120, 150, 36, "缓存", "amber"), (265, 164, 70, 36, "I/O", "slate"), (345, 164, 70, 36, "AI 单元", "red")]:
        f.box(x, y, w, h, lab, col, fs=11)
    f.text(340, 232, "一颗芯片（裸片）", fs=11.5, weight=700)
    f.arrow(425, 120, 470, 120, color=C["amber"][0], sw=1.6)
    # cross section
    f.text(570, 30, "剖面：层层叠叠", fs=12, weight=700)
    for k in range(6):
        y = 50 + k * 22
        f.rect(480, y, 180, 10, fill="#fcd34d" if k % 2 == 0 else "#fde68a", stroke="none", rx=0)
        for v in range(5):
            f.rect(495 + v * 34, y + 10, 5, 12, fill="#b45309", stroke="none", rx=0)
    f.text(570, 196, "十几层金属连线", fs=10.5, fill=C["amber"][0], weight=700)
    f.rect(480, 206, 180, 30, fill=C["slate"][1], stroke=C["slate"][0], rx=0)
    for v in range(6):
        f.rect(490 + v * 28, 200, 14, 10, fill=C["red"][0], stroke="none", rx=1)
    f.text(570, 228, "硅：晶体管在最底层", fs=10.5, fill=C["slate"][0], weight=700)
    f.text(570, 268, "晶体管和导线一起\u201c印\u201d出来，", fs=11, fill=INK)
    f.text(570, 286, "而不是一个个焊上去", fs=11, fill=INK)
    return f


@fig
def moores_law():
    f = Fig(680, 320, "摩尔定律")
    gx, gy, gw, gh = 80, 30, 560, 240
    f.line(gx, gy + gh, gx + gw, gy + gh, stroke=INK); f.line(gx, gy, gx, gy + gh, stroke=INK)
    def X(yr): return gx + (yr - 1970) / (2026 - 1970) * gw
    def Y(n): return gy + gh - (math.log10(n) - 3) / (12 - 3) * gh
    for e in range(3, 13):
        y = Y(10 ** e)
        f.line(gx - 4, y, gx + gw, y, stroke="#f3f4f6", sw=1)
        lab = {3: "1 千", 6: "100 万", 9: "10 亿", 12: "1 万亿"}.get(e)
        if lab: f.text(gx - 8, y + 4, lab, fs=10.5, anchor="end", fill=MUTED)
    for yr in range(1970, 2030, 10):
        f.text(X(yr), gy + gh + 18, str(yr), fs=10.5, fill=MUTED)
    # ideal line doubling every 2 years from 2300 in 1971
    f.line(X(1971), Y(2300), X(2024), Y(2300 * 2 ** ((2024 - 1971) / 2)), stroke=C["blue"][0], sw=1.4, dash="6 4")
    pts = [(1971, 2300, "Intel 4004"), (1978, 29000, "8086"), (1989, 1.2e6, "486"), (1993, 3.1e6, "奔腾"),
           (2000, 4.2e7, "奔腾 4"), (2006, 2.9e8, "酷睿 2"), (2012, 1.4e9, ""), (2017, 1.9e10, ""),
           (2020, 5.4e10, "A100"), (2024, 2.08e11, "Blackwell")]
    for yr, n, lab in pts:
        f.circle(X(yr), Y(n), 5, fill=C["red"][0], stroke="#fff", sw=1)
        if lab == "Blackwell": f.text(X(yr) - 8, Y(n) - 6, lab, fs=10.5, anchor="end", fill=INK)
        elif lab: f.text(X(yr) + 8, Y(n) + 4, lab, fs=10.5, anchor="start", fill=INK)
    f.text(X(1990), Y(1e9), "每两年翻一番（虚线）", fs=12, weight=700, fill=C["blue"][0])
    f.text(gx + 10, gy + 8, "每颗芯片的晶体管数（对数坐标，每格 ×10）", fs=11, anchor="start", fill=MUTED)
    f.text(340, 310, "约 53 年增长约 1 亿倍：2300 → 2080 亿", fs=12, weight=700, fill=INK)
    return f


@fig
def photolithography():
    f = Fig(680, 320, "光刻")
    # light
    f.rect(190, 10, 300, 28, fill=C["purple"][0], stroke="none", rx=6)
    f.text(340, 29, "光源（深紫外 193 纳米 / 极紫外 13.5 纳米）", fs=10.5, fill="#fff", weight=700)
    for k in range(5):
        f.arrow(270 + k * 35, 40, 270 + k * 35, 62, color=C["purple"][0], sw=1.4, size=6)
    f.rect(240, 64, 200, 14, fill="#e5e7eb", stroke=INK, rx=0)
    for x in (270, 340, 395):
        f.rect(x, 64, 22, 14, fill=INK, stroke="none", rx=0)
    f.text(450, 75, "掩模（电路图形）", fs=11, anchor="start", weight=700)
    f.path("M250,100 Q340,86 430,100 Q340,114 250,100 Z", fill=C["blue"][1], stroke=C["blue"][0])
    f.text(450, 104, "透镜：缩小 4 倍投影", fs=11, anchor="start", weight=700, fill=C["blue"][0])
    f.poly([(250, 100), (300, 150)], stroke=C["purple"][0], sw=1, dash="3 3"); f.poly([(430, 100), (380, 150)], stroke=C["purple"][0], sw=1, dash="3 3")
    f.rect(260, 150, 160, 8, fill=C["amber"][1], stroke=C["amber"][0], rx=0)
    f.rect(260, 158, 160, 14, fill="#cbd5e1", stroke=C["slate"][0], rx=0)
    f.text(450, 162, "晶圆：涂光刻胶", fs=11, anchor="start", weight=700, fill=C["amber"][0])
    # steps
    steps = ["① 涂胶", "② 曝光", "③ 显影", "④ 刻蚀", "⑤ 去胶"]
    for k, s in enumerate(steps):
        x = 20 + k * 132
        f.text(x + 55, 205, s, fs=12, weight=700)
        f.rect(x, 250, 110, 26, fill="#cbd5e1", stroke=C["slate"][0], rx=0)
        if k == 0:
            f.rect(x, 236, 110, 14, fill=C["amber"][1], stroke=C["amber"][0], rx=0)
        if k == 1:
            f.rect(x, 236, 110, 14, fill=C["amber"][1], stroke=C["amber"][0], rx=0)
            f.rect(x + 40, 236, 30, 14, fill=C["purple"][1], stroke=C["purple"][0], rx=0)
            f.arrow(x + 55, 214, x + 55, 234, color=C["purple"][0], sw=1.4, size=6)
        if k == 2:
            f.rect(x, 236, 40, 14, fill=C["amber"][1], stroke=C["amber"][0], rx=0)
            f.rect(x + 70, 236, 40, 14, fill=C["amber"][1], stroke=C["amber"][0], rx=0)
        if k == 3:
            f.rect(x, 236, 40, 14, fill=C["amber"][1], stroke=C["amber"][0], rx=0)
            f.rect(x + 70, 236, 40, 14, fill=C["amber"][1], stroke=C["amber"][0], rx=0)
            f.rect(x + 40, 250, 30, 14, fill="#fff", stroke="none", rx=0)
        if k == 4:
            f.rect(x + 40, 250, 30, 14, fill="#fff", stroke="none", rx=0)
        if k < 4: f.arrow(x + 114, 256, x + 128, 256, color=INK, sw=1.4, size=6)
    f.text(340, 300, "重复几十次，一层层\u201c印\u201d出晶体管和导线。分辨率 ∝ 波长 ÷ 数值孔径", fs=11.5, fill=INK)
    return f


@fig
def finfet():
    f = Fig(520, 250, "平面、FinFET 与 GAA")
    titles = [("平面晶体管", "栅极只从上面控制"), ("FinFET（鳍式）", "栅极包住三面"), ("GAA（环绕栅极）", "栅极包住四面")]
    for k, (t, s) in enumerate(titles):
        x = 15 + k * 170
        f.text(x + 75, 26, t, fs=12.5, weight=700)
        f.rect(x + 10, 150, 130, 40, fill=C["red"][1], stroke=C["red"][0], rx=0)
        if k == 0:
            f.rect(x + 50, 136, 50, 14, fill=C["blue"][0], stroke="none", rx=0, opacity=0.7)
            f.rect(x + 45, 100, 60, 36, fill=C["slate"][0], stroke="none", rx=0)
        elif k == 1:
            f.rect(x + 63, 80, 24, 70, fill=C["blue"][0], stroke="none", rx=0, opacity=0.7)
            f.path(f"M{x+45},150 L{x+45},64 L{x+105},64 L{x+105},150 L{x+93},150 L{x+93},76 L{x+57},76 L{x+57},150 Z", fill=C["slate"][0], stroke="none")
        else:
            f.rect(x + 40, 60, 70, 90, fill=C["slate"][0], stroke="none", rx=0)
            for j in range(3):
                f.rect(x + 52, 72 + j * 26, 46, 14, fill=C["blue"][0], stroke="#fff", sw=1.4, rx=2, opacity=0.9)
        f.text(x + 75, 212, s, fs=11, fill=INK)
    f.rect(20, 222, 12, 12, fill=C["slate"][0], stroke="none", rx=0); f.text(38, 232, "栅极", fs=10.5, anchor="start")
    f.rect(90, 222, 12, 12, fill=C["blue"][0], stroke="none", rx=0, opacity=0.7); f.text(108, 232, "沟道", fs=10.5, anchor="start")
    f.text(330, 240, "包得越严，漏电越少，晶体管能做得越小", fs=11, weight=700, fill=C["blue"][0])
    return f


# ------------------------------------------------------------------ 信号与显示
@fig
def analog_digital():
    f = Fig(520, 240, "模拟与数字")
    gx, gy, gw, gh = 40, 36, 440, 146
    f.line(gx, gy + gh, gx + gw, gy + gh, stroke=INK); f.line(gx, gy, gx, gy + gh, stroke=INK)
    for q in range(1, 8):
        y = gy + gh - q * gh / 8
        f.line(gx, y, gx + gw, y, stroke="#f3f4f6", sw=1)
    def s(x): return 0.5 + 0.38 * math.sin(x / gw * 2 * math.pi * 1.4) + 0.08 * math.sin(x / 20)
    pts = [(gx + i, gy + gh - s(i) * gh) for i in range(0, gw + 1, 2)]
    f.poly(pts, stroke=C["blue"][0], sw=2.2)
    codes = []
    for i in range(10, gw, 30):
        v = round(s(i) * 8)
        y = gy + gh - v * gh / 8
        f.line(gx + i, gy + gh, gx + i, y, stroke=C["red"][0], sw=1, dash="2 2")
        f.circle(gx + i, y, 4, fill=C["red"][0], stroke="none")
        codes.append(str(v))
    f.text(gx + gw / 2, gy - 10, "蓝线：模拟信号（连续）　红点：采样值", fs=11.5, weight=700, fill=C["blue"][0])
    f.text(gx + gw / 2, 206, "采样 + 量化 → " + " ".join(codes[:10]) + " …", fs=12, weight=700, fill=C["red"][0], mono=True)
    f.text(gx + gw / 2, 228, "数字（离散）：复制、传输千万次也不失真", fs=11, fill=INK)
    return f


@fig
def lcd():
    f = Fig(520, 260, "液晶像素")
    for k, (t, on) in enumerate([("不加电：亮", False), ("加电：暗", True)]):
        x = 15 + k * 250
        f.text(x + 100, 22, t, fs=13, weight=700, fill=C["amber"][0] if not on else C["slate"][0])
        f.rect(x, 210, 200, 16, fill="#fef9c3", stroke=C["amber"][0], rx=2); f.text(x + 100, 222, "背光", fs=10)
        f.rect(x, 186, 200, 10, fill=C["slate"][1], stroke=C["slate"][0], rx=0); f.text(x + 206, 195, "偏光片↕", fs=9.5, anchor="start")
        f.rect(x, 50, 200, 10, fill=C["slate"][1], stroke=C["slate"][0], rx=0); f.text(x + 206, 59, "偏光片↔", fs=9.5, anchor="start")
        for j in range(5):
            y = 72 + j * 22
            if not on:
                a = j * 22.5
                dx, dy = 22 * math.cos(math.radians(a)), 6 * math.sin(math.radians(a)) + 2
                f.line(x + 100 - dx, y - dy / 2, x + 100 + dx, y + dy / 2, stroke=C["purple"][0], sw=5)
            else:
                f.line(x + 100, y - 8, x + 100, y + 8, stroke=C["purple"][0], sw=5)
        if not on:
            f.arrow(x + 40, 205, x + 40, 30, color=C["amber"][0], sw=2.4)
            f.text(x + 50, 40, "光透过", fs=11, anchor="start", fill=C["amber"][0], weight=700)
        else:
            f.arrow(x + 40, 205, x + 40, 64, color=C["amber"][0], sw=2.4)
            f.text(x + 50, 40, "光被挡住", fs=11, anchor="start", fill=C["slate"][0], weight=700)
        f.text(x + 150, 130, "液晶" if True else "", fs=10.5, fill=C["purple"][0])
    f.text(260, 252, "液晶分子扭转 90° 带着偏振方向一起转；加电后竖直排列，不再转", fs=10.5, fill=MUTED)
    return f


@fig
def led():
    f = Fig(680, 300, "LED 发光")
    # band diagram
    f.text(170, 26, "电子落下，放出光子", fs=13.5, weight=700)
    f.rect(40, 50, 260, 50, fill=C["blue"][1], stroke=C["blue"][0], rx=0); f.text(70, 80, "导带", fs=11.5, fill=C["blue"][0], weight=700)
    f.rect(40, 170, 260, 50, fill=C["red"][1], stroke=C["red"][0], rx=0); f.text(70, 200, "价带", fs=11.5, fill=C["red"][0], weight=700)
    f.circle(180, 90, 7, fill=C["blue"][0], stroke="none"); f.text(180, 94, "−", fs=10, fill="#fff", weight=700)
    f.circle(180, 180, 7, fill="#fff", stroke=C["red"][0], sw=2); f.text(180, 184, "+", fs=10, fill=C["red"][0], weight=700)
    f.arrow(180, 100, 180, 170, color=INK, sw=2)
    f.text(140, 140, "禁带 Eg", fs=11, anchor="end", fill=MUTED)
    f.path("M195,135 l10,-8 l6,10 l10,-8 l6,10 l10,-8 l6,10 l12,-6", stroke=C["amber"][0], sw=2)
    f.text(270, 130, "光子", fs=11, fill=C["amber"][0], weight=700)
    f.text(170, 248, "光子能量 = 禁带宽度：禁带越宽，颜色越偏蓝", fs=11, fill=INK)
    # spectrum
    cols = [("红外", "#7f1d1d", 1.2), ("红", "#ef4444", 1.9), ("绿", "#22c55e", 2.3), ("蓝", "#3b82f6", 2.7)]
    for k, (n, c, e) in enumerate(cols):
        x = 360 + k * 70
        h = e * 50
        f.rect(x, 200 - h, 46, h, fill=c, stroke="none", rx=3)
        f.text(x + 23, 218, n, fs=11, weight=700)
        f.text(x + 23, 194 - h, f"{e} eV", fs=10, fill=MUTED)
    f.text(500, 26, "常见 LED 的禁带宽度", fs=13, weight=700)
    f.text(500, 246, "蓝光 LED（氮化镓，1990 年代）+ 黄色荧光粉 = 白光", fs=11, weight=700, fill=C["blue"][0])
    f.text(340, 284, "LED 直接把电变成光，几乎不发热：发光效率约为白炽灯的 8–10 倍", fs=11.5, fill=INK)
    return f


def main():
    only = set(sys.argv[1:])
    for name, fn in FIGS.items():
        if only and name not in only: continue
        fn().save(OUT / f"{name}.svg")
    print("wrote", len(FIGS) if not only else len(only), "figures to", OUT)

if __name__ == "__main__":
    main()
