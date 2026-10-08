#!/usr/bin/env python3
"""Diagrams for 第 17 篇「量子与前沿」 -> assets/figs/frontier/*.svg"""
from __future__ import annotations
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from svgkit import Fig, C, INK, MUTED, tw
from mapkit_d11_17 import concept_map as cmap

OUT = Path(__file__).resolve().parents[1] / "assets" / "figs" / "frontier"
FIGS = {}
def fig(fn):
    FIGS[fn.__name__.replace("_", "-")] = fn; return fn

@fig
def concept_map():
    return cmap("量子与前沿", "从上往下读：量子技术 → 物理前沿装置 → 计算与材料前沿。越往下离日常产品越近，但都还在路上。",
        [("量子技术：叠加与纠缠变成工具", "purple", ["量子比特", "量子计算机", "技术路线", "量子纠错", "量子优越性", "Shor 算法", "后量子密码", "量子通信", "量子传感", "量子模拟"]),
         ("物理前沿装置：看得更深、测得更准", "blue", ["超导", "高温超导", "粒子加速器", "同步辐射光源", "引力波探测器", "激光冷却与冷原子", "超快激光与阿秒"]),
         ("计算前沿：摩尔定律之后", "teal", ["类脑计算", "忆阻器与存内计算", "硅光与光计算", "自旋电子学", "磁阻存储器", "DNA 存储", "E 级超算", "自动化实验室"]),
         ("材料前沿：设计到原子级", "amber", ["量子点", "分子机器", "金属有机框架", "拓扑材料", "人工光合作用"])],
        [("1911", "发现超导"), ("1931", "回旋加速器"), ("1972", "光催化分解水"), ("1981", "费曼：量子模拟"), ("1984", "BB84 协议"),
         ("1985", "啁啾脉冲放大"), ("1986", "高温超导"), ("1988", "巨磁阻"), ("1994", "Shor 算法"), ("1995", "玻色-爱因斯坦凝聚"),
         ("2015", "探测到引力波"), ("2019", "量子优越性"), ("2022", "E 级超算"), ("2024", "后量子标准 · Willow")],
        [("根原理", "amber", ["叠加与纠缠", "量子隧穿", "能级", "冗余纠错", "局部性", "结构决定性质"]),
         ("读本篇要问", "red", ["原理清楚吗？", "还差工程、成本", "还是规模？", "离产品多远？"]),
         ("近年诺贝尔奖", "slate", ["2016 拓扑 · 分子机器", "2018 超快激光", "2023 阿秒 · 量子点", "2025 超导电路 · MOF"])],
        ["晶体管、芯片与摩尔定律 → 第 2 篇「电与电子」　RSA 与公钥密码 → 第 13 篇「安全与国防」",
         "AI 芯片与 AI for Science → 第 5 篇　核聚变 → 第 1 篇　激光与原子钟 → 第 16 篇"],
        arrow="down", center_note="↓ 从实验室到工厂：差的往往是工程和成本，而不是原理")

@fig
def quantum_computer():
    f = Fig(680, 360, "比特与量子比特")
    # classical bit
    f.text(110, 28, "经典比特", fs=14, weight=700, fill=C["slate"][0])
    f.box(40, 46, 60, 50, "0", "slate", fs=20, solid=False)
    f.text(110, 76, "或", fs=12, fill=MUTED)
    f.box(120, 46, 60, 50, "1", "slate", fs=20, solid=True)
    f.text(110, 116, "任一时刻只取一个值", fs=11, fill=MUTED)
    # bloch sphere
    cx, cy, R = 340, 108, 56
    f.text(cx, 28, "量子比特（布洛赫球）", fs=14, weight=700, fill=C["purple"][0])
    f.circle(cx, cy, R, fill=C["purple"][1], stroke=C["purple"][0], sw=1.4)
    f.path(f"M{cx-R},{cy} A{R},{R*0.3} 0 0 0 {cx+R},{cy}", stroke=C["purple"][0], sw=1, dash="3,3")
    f.path(f"M{cx-R},{cy} A{R},{R*0.3} 0 0 1 {cx+R},{cy}", stroke=C["purple"][0], sw=1)
    f.text(cx, cy - R - 6, "|0⟩", fs=13, weight=700)
    f.text(cx, cy + R + 16, "|1⟩", fs=13, weight=700)
    ang = math.radians(50)
    px, py = cx + R * 0.85 * math.sin(ang), cy - R * 0.85 * math.cos(ang)
    f.arrow(cx, cy, px, py, color=C["red"][0], sw=2.4, size=9)
    f.circle(cx, cy, 3, fill=INK, stroke="none", sw=0)
    f.text(px + 8, py - 4, "α|0⟩ + β|1⟩", fs=12, anchor="start", fill=C["red"][0], weight=700)
    f.text(570, 180, "球面上任意一点都是合法状态", fs=11, fill=MUTED)
    # measurement
    f.rect(470, 46, 200, 112, fill=C["amber"][1], stroke=C["amber"][0], rx=8)
    f.text(570, 68, "测量时", fs=13, weight=700, fill=C["amber"][0])
    f.text(484, 94, "以 |α|² 的概率得到 0", fs=11.5, anchor="start")
    f.text(484, 116, "以 |β|² 的概率得到 1", fs=11.5, anchor="start")
    f.text(484, 140, "测完叠加就消失了", fs=11.5, anchor="start", weight=700)
    # bottom: 2^n and interference
    f.line(20, 196, 660, 196, stroke="#e5e7eb", sw=1)
    f.text(180, 222, "n 个量子比特 → 2ⁿ 个概率幅", fs=13.5, weight=700, fill=C["blue"][0])
    rows = [("10", "1024 个数"), ("50", "约 10¹⁵ 个数"), ("300", "比宇宙中的原子还多")]
    for k, (a, b) in enumerate(rows):
        y = 248 + k * 26
        f.text(60, y, f"{a} 个比特", fs=12, anchor="start")
        f.arrow(130, y - 4, 166, y - 4, color=C["blue"][0], sw=1.4, size=6)
        f.text(176, y, b, fs=12, anchor="start", weight=700)
    f.text(180, 340, "经典计算机光是存下它们就不可能", fs=11, fill=MUTED)
    # interference bars
    f.text(510, 222, "算法：让答案通过干涉“脱颖而出”", fs=13.5, weight=700, fill=C["red"][0])
    X0, Y0 = 380, 320
    before = [0.35] * 8
    after = [0.08, 0.06, 0.1, 0.92, 0.07, 0.05, 0.09, 0.06]
    for k in range(8):
        f.rect(X0 + k * 14, Y0 - 70 * before[k], 10, 70 * before[k], fill=C["slate"][1], stroke=C["slate"][0], rx=1, sw=0.8)
        col = C["red"][0] if k == 3 else C["slate"][0]
        f.rect(X0 + 150 + k * 14, Y0 - 70 * after[k], 10, 70 * after[k], fill=C["red"][1] if k == 3 else C["slate"][1], stroke=col, rx=1, sw=0.8)
    f.line(X0 - 4, Y0, X0 + 116, Y0, stroke=INK, sw=1); f.line(X0 + 146, Y0, X0 + 266, Y0, stroke=INK, sw=1)
    f.arrow(X0 + 120, Y0 - 30, X0 + 142, Y0 - 30, color=INK, sw=1.6, size=7)
    f.text(X0 + 56, Y0 + 16, "开始：均匀叠加", fs=11, fill=MUTED)
    f.text(X0 + 206, Y0 + 16, "结束：正确答案最可能", fs=11, fill=C["red"][0])
    f.text(X0 + 131, Y0 - 40, "干涉", fs=10.5, fill=MUTED)
    return f

@fig
def quantum_communication():
    f = Fig(520, 240, "BB84")
    cols = ["发送方的比特", "发送方的方式", "光子偏振", "接收方的方式", "方式一致？", "保留的密钥"]
    data = [("1", "+", "|", "+", True, "1"), ("0", "×", "\\", "+", False, ""), ("1", "×", "/", "×", True, "1"),
            ("0", "+", "—", "×", False, ""), ("0", "+", "—", "+", True, "0"), ("1", "×", "/", "×", True, "1")]
    X0, Y0, cw = 130, 30, 62
    for r, name in enumerate(cols):
        f.text(X0 - 12, Y0 + 24 + r * 30, name, fs=11, anchor="end", weight=700)
    for c, row in enumerate(data):
        x = X0 + c * cw + cw / 2
        ok = row[4]
        f.rect(X0 + c * cw + 4, Y0 + 6, cw - 8, 30 * 6 - 4, fill=C["green"][1] if ok else "#f9fafb", stroke=C["green"][0] if ok else "#e5e7eb", rx=6, sw=1)
        vals = [row[0], row[1], None, row[3], "✓" if ok else "✗", row[5]]
        for r, v in enumerate(vals):
            y = Y0 + 24 + r * 30
            if r == 2:
                s = row[2]; L = 9
                if s == "|": f.line(x, y - L - 4, x, y + L - 4, stroke=C["purple"][0], sw=2.4)
                elif s == "—": f.line(x - L, y - 4, x + L, y - 4, stroke=C["purple"][0], sw=2.4)
                elif s == "/": f.line(x - L * 0.7, y + L * 0.7 - 4, x + L * 0.7, y - L * 0.7 - 4, stroke=C["purple"][0], sw=2.4)
                else: f.line(x - L * 0.7, y - L * 0.7 - 4, x + L * 0.7, y + L * 0.7 - 4, stroke=C["purple"][0], sw=2.4)
            else:
                colr = (C["green"][0] if ok else C["red"][0]) if r == 4 else INK
                f.text(x, y, v, fs=13, weight=700 if r in (4, 5) else 400, fill=colr)
    f.text(260, 232, "+ 表示横竖偏振，× 表示斜向偏振；方式不一致的比特全部丢弃", fs=10.5, fill=MUTED)
    return f

@fig
def superconductivity():
    f = Fig(520, 220, "超导的两个标志")
    X0, Y0, W, H = 50, 170, 200, 120
    f.line(X0, Y0, X0 + W, Y0, stroke=INK, sw=1.2); f.line(X0, Y0, X0, Y0 - H, stroke=INK, sw=1.2)
    Tc = X0 + 70
    f.poly([(X0, Y0 - 2), (Tc, Y0 - 2)], stroke=C["blue"][0], sw=2.4)
    f.poly([(Tc, Y0 - 2), (Tc, Y0 - 60)] + [(Tc + i, Y0 - 60 - i * 0.35) for i in range(0, 130, 5)], stroke=C["blue"][0], sw=2.4)
    f.line(Tc, Y0, Tc, Y0 - H + 10, stroke="#9ca3af", sw=1, dash="3,3")
    f.text(Tc, Y0 + 14, "临界温度", fs=10.5, fill=MUTED)
    f.text(X0 + W, Y0 + 14, "温度 →", fs=10.5, fill=MUTED, anchor="end")
    f.text(X0 - 6, Y0 - H + 8, "电阻", fs=10.5, fill=MUTED, anchor="end")
    f.text(X0 + 30, Y0 - 12, "精确为零", fs=11, weight=700, fill=C["blue"][0])
    f.text(150, 24, "① 电阻突然消失", fs=12.5, weight=700, fill=C["blue"][0])
    # Meissner
    f.text(390, 24, "② 迈斯纳效应：排出磁场", fs=12.5, weight=700, fill=C["purple"][0])
    sx, sy, sw_, sh = 320, 130, 140, 30
    f.rect(sx, sy, sw_, sh, fill=C["slate"][1], stroke=C["slate"][0], rx=4)
    f.text(sx + sw_ / 2, sy + 20, "超导体（冷却中）", fs=11, weight=700)
    mx, my = 390, 80
    f.rect(mx - 25, my - 14, 50, 22, fill=C["red"][1], stroke=C["red"][0], rx=3)
    f.text(mx, my + 2, "磁铁", fs=11, weight=700, fill=C["red"][0])
    for k, dx in enumerate((-40, -20, 20, 40)):
        x0 = mx + dx * 0.5
        side = -1 if dx < 0 else 1
        f.path(f"M{x0},{my+8} Q{x0 + side*abs(dx)*1.4},{sy - 4} {x0 + side*(abs(dx)*2.2+20)},{sy+sh/2}", stroke=C["purple"][0], sw=1.2, dash="4,3")
    f.text(390, 186, "磁感线绕开超导体，磁铁被稳稳托起", fs=11, fill=C["purple"][0])
    f.text(260, 212, "原因：电子结成“库珀对”，凝聚成同一个量子态，不再被晶格散射", fs=10.5, fill=MUTED)
    return f

def main():
    only = set(sys.argv[1:])
    for name, fn in FIGS.items():
        if only and name not in only: continue
        fn().save(OUT / f"{name}.svg")
    print("wrote", len(only or FIGS), "figures to", OUT)

if __name__ == "__main__":
    main()
