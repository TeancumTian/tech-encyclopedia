#!/usr/bin/env python3
"""Diagrams for 第 15 篇「环境与气候技术」 -> assets/figs/environment/*.svg"""
from __future__ import annotations
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from svgkit import Fig, C, INK, MUTED, tw
from mapkit_d11_17 import concept_map as cmap

OUT = Path(__file__).resolve().parents[1] / "assets" / "figs" / "environment"
FIGS = {}
def fig(fn):
    FIGS[fn.__name__.replace("_", "-")] = fn; return fn

@fig
def concept_map():
    return cmap("环境与气候技术", "从上往下读：先测量和理解，再减少排放、治理污染，最后让物质循环起来。",
        [("认识气候：测量与模拟", "blue", ["温室效应", "基林曲线", "冰芯与古气候", "Argo 浮标", "温室气体监测", "气候模型", "数值天气预报", "IPCC 评估", "灾害预警", "生命周期评价"]),
         ("减排与清除：改变能源和工业", "green", ["能源转型", "碳中和与净零", "碳定价与碳交易", "碳捕集与封存", "直接空气捕集", "碳移除", "绿色钢铁与低碳水泥", "可持续航空燃料", "地球工程"]),
         ("污染治理：空气、水和土", "teal", ["静电除尘", "烟气脱硫", "烟气脱硝", "三元催化器", "淘汰含铅汽油", "臭氧层保护", "HEPA 过滤", "空气质量监测", "污水处理", "海水淡化", "富营养化治理", "生物修复"]),
         ("循环经济：废物变资源", "amber", ["资源回收", "塑料回收与微塑料", "垃圾焚烧发电", "沼气", "卫生填埋"])],
        [("1856", "富特：CO₂ 吸热"), ("1896", "阿伦尼乌斯估算"), ("1907", "静电除尘"), ("1914", "活性污泥法"), ("1950", "首次数值预报"),
         ("1958", "基林曲线"), ("1960", "反渗透膜"), ("1967", "真锅气候模型"), ("1975", "汽车催化器"), ("1987", "蒙特利尔议定书"),
         ("1988", "IPCC 成立"), ("2005", "欧盟碳市场"), ("2015", "巴黎协定"), ("2021", "含铅汽油终结")],
        [("根原理", "amber", ["电磁辐射与能量平衡", "熵：分开要花能量", "催化与氧化还原", "微生物", "激励与协作"]),
         ("四种手段", "green", ["测量：看清问题", "减排：少产生", "清除：拿回来", "适应：躲得开"]),
         ("一组数字", "slate", ["CO₂：280 → 420+ ppm", "长期升温约 1.3–1.4 °C", "海洋吸收九成余热"])],
        ["风电、光伏、储能、核电 → 第 1 篇「能源与动力」　电动汽车 → 第 8 篇　气象与遥感卫星 → 第 9 篇",
         "化肥与农业排放 → 第 11 篇「农业与食品」　下水道、自来水、海绵城市 → 第 12 篇「建筑与城市」"],
        arrow="down", center_note="↓ 修补比制造难：少排几乎总是比事后清除便宜")

@fig
def greenhouse_effect():
    f = Fig(680, 330, "地球的能量收支")
    # sun
    f.circle(60, 50, 30, fill="#fde68a", stroke=C["amber"][0], sw=1.6)
    f.text(60, 55, "太阳", fs=12, weight=700, fill=C["amber"][0])
    # ground
    f.rect(20, 260, 640, 40, fill="#d9f99d", stroke="#65a30d", rx=0)
    f.text(340, 286, "地面：吸收阳光变暖，再以红外线散热", fs=12, weight=700, fill="#3f6212")
    # atmosphere band
    f.rect(20, 120, 640, 60, fill=C["blue"][1], stroke=C["blue"][0], rx=6, dash="5,4")
    f.text(650, 140, "大气中的温室气体", fs=12, weight=700, fill=C["blue"][0], anchor="end")
    f.text(650, 158, "CO₂ · H₂O · CH₄", fs=11, fill=C["blue"][0], anchor="end")
    # incoming shortwave
    for x in (100, 140, 180):
        f.arrow(x, 82, x + 40, 254, color=C["amber"][0], sw=2.4, size=9)
    f.text(228, 226, "可见光（短波）", fs=11.5, weight=700, fill=C["amber"][0], anchor="start")
    f.text(228, 242, "大部分直接穿过", fs=11, fill=C["amber"][0], anchor="start")
    # reflected
    f.arrow(130, 120, 100, 92, color="#9ca3af", sw=1.6, size=7)
    f.text(96, 110, "约 3 成被反射", fs=10.5, fill=MUTED, anchor="end")
    # outgoing IR
    def wavy(x1, y1, x2, y2, col, sw=2):
        L = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / L, (y2 - y1) / L; px, py = -uy, ux
        pts = [(x1 + ux * L * i / 80 + px * 4 * math.sin(i / 80 * 2 * math.pi * 6), y1 + uy * L * i / 80 + py * 4 * math.sin(i / 80 * 2 * math.pi * 6)) for i in range(81)]
        f.poly(pts, stroke=col, sw=sw)
        f.arrow(pts[-3][0], pts[-3][1], x2 + ux * 6, y2 + uy * 6, color=col, sw=sw, size=8)
    wavy(330, 256, 330, 150, C["red"][0])
    wavy(390, 256, 390, 150, C["red"][0])
    wavy(450, 256, 450, 60, C["red"][0])
    f.text(468, 70, "一部分红外线逃向太空", fs=11, fill=C["red"][0], anchor="start")
    # re-emission
    for x in (330, 390):
        f.arrow(x, 150, x - 30, 112, color=C["red"][0], sw=1.4, size=6, dash="4,3")
        f.arrow(x + 4, 160, x + 30, 240, color=C["purple"][0], sw=1.8, size=7)
    f.text(345, 98, "被吸收后向四面八方重新辐射", fs=11, fill=C["red"][0])
    f.text(520, 220, "一部分返回地面", fs=11.5, weight=700, fill=C["purple"][0], anchor="start")
    f.text(520, 238, "→ 地表更暖", fs=11.5, weight=700, fill=C["purple"][0], anchor="start")
    f.text(340, 320, "没有温室气体：约 −18 °C　　有天然温室效应：约 15 °C　　气体增多：地表还要继续变暖才能重新平衡", fs=11, fill=MUTED)
    return f

@fig
def keeling_curve():
    f = Fig(520, 230, "基林曲线")
    X0, Y0, W, H = 60, 190, 430, 150
    def X(t): return X0 + (t - 1958) / (2024 - 1958) * W
    def Y(c): return Y0 - (c - 310) / (430 - 310) * H
    f.line(X0, Y0, X0 + W, Y0, stroke=INK, sw=1.2); f.line(X0, Y0, X0, Y0 - H - 6, stroke=INK, sw=1.2)
    for c in (320, 360, 400):
        f.line(X0, Y(c), X0 + W, Y(c), stroke="#e5e7eb", sw=0.8)
        f.text(X0 - 6, Y(c) + 4, str(c), fs=10.5, anchor="end", fill=MUTED)
    for t in (1960, 1980, 2000, 2020):
        f.text(X(t), Y0 + 16, str(t), fs=10.5, fill=MUTED)
    pts, trend = [], []
    for i in range(0, 66 * 12 + 1):
        t = 1958 + i / 12
        base = 315 + 0.8 * (t - 1958) + 0.0128 * (t - 1958) ** 2
        c = base + 3.2 * math.sin(2 * math.pi * (t - 1958) + 1.2)
        pts.append((X(t), Y(c))); trend.append((X(t), Y(base)))
    f.poly(pts, stroke=C["red"][0], sw=1.1)
    f.poly(trend, stroke=INK, sw=1.6, dash="5,3")
    f.text(X0 - 40, Y0 - H - 12, "CO₂（ppm）", fs=10.5, anchor="start", fill=MUTED)
    f.text(X(1958) + 6, Y(318) - 10, "1958：约 315", fs=11, anchor="start", weight=700)
    f.text(X(2024) - 4, Y(424) - 10, "今天：420 以上", fs=11, anchor="end", weight=700, fill=C["red"][0])
    f.text(X(1995), Y(330), "锯齿：植物夏吸冬放", fs=11, fill=C["red"][0])
    f.text(X(1995), Y(318), "虚线：长期趋势", fs=11, fill=INK)
    f.text(260, 225, "测点：夏威夷莫纳罗亚观测站（示意，按实测趋势绘制）", fs=10.5, fill=MUTED)
    return f

@fig
def desalination():
    f = Fig(520, 220, "渗透与反渗透")
    def tank(x, title, rev):
        f.text(x + 80, 22, title, fs=13, weight=700, fill=C["red"][0] if rev else C["blue"][0])
        f.rect(x, 40, 210, 120, fill="#fff", stroke=INK, sw=1.4, rx=2)
        lw, rw = (70, 90) if not rev else (95, 60)
        f.rect(x + 2, 160 - rw, 102, rw - 2, fill="#bfdbfe", stroke="none", sw=0, rx=0)
        f.rect(x + 106, 160 - lw, 102, lw - 2, fill="#93c5fd", stroke="none", sw=0, rx=0)
        f.line(x + 105, 40, x + 105, 160, stroke=C["amber"][0], sw=2.4, dash="3,3")
        f.text(x + 52, 176, "淡水", fs=11); f.text(x + 158, 176, "盐水", fs=11)
        import random
        random.seed(1 + rev)
        for _ in range(12):
            f.circle(x + 115 + random.random() * 84, 160 - random.random() * (lw - 10) - 5, 2.6, fill=C["slate"][0], stroke="none", sw=0)
        if not rev:
            f.arrow(x + 80, 120, x + 130, 120, color=C["blue"][0], sw=2.2, size=8)
            f.text(x + 105, 194, "水自发流向盐水一侧", fs=11, fill=C["blue"][0])
        else:
            f.rect(x + 112, 160 - lw - 14, 90, 10, fill="#9ca3af", stroke=INK, rx=1)
            f.arrow(x + 157, 46, x + 157, 160 - lw - 16, color=C["red"][0], sw=2.4, size=8)
            f.text(x + 190, 37, "加压", fs=11, weight=700, fill=C["red"][0])
            f.arrow(x + 130, 130, x + 80, 130, color=C["red"][0], sw=2.2, size=8)
            f.text(x + 105, 194, "压力 > 渗透压：水被挤出", fs=11, fill=C["red"][0])
    tank(20, "渗透", False)
    tank(290, "反渗透", True)
    f.text(260, 214, "黄线是半透膜：水分子能过，盐离子（灰点）过不去", fs=10.5, fill=MUTED)
    return f

def main():
    only = set(sys.argv[1:])
    for name, fn in FIGS.items():
        if only and name not in only: continue
        fn().save(OUT / f"{name}.svg")
    print("wrote", len(only or FIGS), "figures to", OUT)

if __name__ == "__main__":
    main()
