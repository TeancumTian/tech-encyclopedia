#!/usr/bin/env python3
"""Diagrams for 第 12 篇「建筑与城市」 -> assets/figs/building/*.svg"""
from __future__ import annotations
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from svgkit import Fig, C, INK, MUTED, tw
from mapkit_d11_17 import concept_map as cmap

OUT = Path(__file__).resolve().parents[1] / "assets" / "figs" / "building"
FIGS = {}
def fig(fn):
    FIGS[fn.__name__.replace("_", "-")] = fn; return fn

@fig
def concept_map():
    return cmap("建筑与城市", "从下往上读：材料与结构托起建筑，建筑连成基础设施，基础设施再组成能安全生活的城市。",
        [("材料与结构：对抗重力", "slate", ["波特兰水泥", "钢筋混凝土", "预应力混凝土", "钢结构", "工程木", "有限元分析", "地基与深基础"]),
         ("建筑：向高处和大跨度发展", "blue", ["摩天大楼", "安全电梯", "自动扶梯", "玻璃幕墙", "大跨度空间结构", "抗震与隔震", "装配式建筑", "BIM", "工程机械"]),
         ("基础设施：跨越与治水", "teal", ["铸铁桥与桁架桥", "悬索桥与斜拉桥", "盾构与隧道掘进机", "跨海通道", "现代大坝", "现代防洪", "填海造地"]),
         ("城市系统：看不见的生命线", "green", ["现代下水道", "自来水处理", "抽水马桶", "集中供暖", "自动喷淋", "烟雾报警器", "雨洪管理 · 海绵城市"]),
         ("规划与管理：让城市更好住", "purple", ["现代城市规划", "绿色建筑与被动房", "地理信息系统", "智慧城市"])],
        [("1775", "抽水马桶"), ("1779", "铸铁桥"), ("1824", "波特兰水泥"), ("1825", "泰晤士河盾构"), ("1854", "安全电梯"),
         ("1865", "伦敦下水道"), ("1867", "钢筋混凝土"), ("1874", "自动喷淋"), ("1883", "布鲁克林大桥"), ("1885", "第一座摩天楼"),
         ("1928", "预应力混凝土"), ("1936", "胡佛大坝"), ("1956", "有限元分析"), ("1994", "英法海底隧道"), ("2010", "哈利法塔 828 米")],
        [("根原理", "amber", ["应力与材料强度", "平方—立方定律", "重力与流体压力", "病原体学说", "传热的三种方式"]),
         ("三个敌人", "red", ["重力：自重累加", "风：越高越难", "地震：惯性与共振"]),
         ("一组数字", "slate", ["城市人口：一成 → 过半", "水泥约占 CO₂ 排放 7–8%", "建筑约占终端能耗三成"])],
        ["钢铁、玻璃与水泥生产 → 第 6 篇「材料与化工」　地铁、高速公路、运河 → 第 8 篇「交通运输」",
         "空调与热泵 → 第 1 篇「能源与动力」　低碳水泥与建筑减排 → 第 15 篇「环境与气候技术」"],
        arrow="up", center_note="↑ 每一层都建立在下一层之上：先能立得住，才谈得上住得好")

@fig
def reinforced_concrete():
    f = Fig(680, 300, "钢筋混凝土梁")
    x0, x1, yt, yb = 40, 420, 90, 150
    f.rect(x0, yt, x1 - x0, yb - yt, fill="#e5e7eb", stroke="#6b7280", sw=1.4, rx=2)
    f.poly([(x0 + 10, yb), (x0 - 4, yb + 26), (x0 + 24, yb + 26)], fill=C["slate"][1], stroke=C["slate"][0], closed=True)
    f.poly([(x1 - 10, yb), (x1 - 24, yb + 26), (x1 + 4, yb + 26)], fill=C["slate"][1], stroke=C["slate"][0], closed=True)
    f.arrow((x0 + x1) / 2, 30, (x0 + x1) / 2, yt - 4, color=INK, sw=2.4, size=11)
    f.text((x0 + x1) / 2 + 8, 40, "荷载", fs=12, anchor="start", weight=700)
    # compression zone
    f.text(x0 + 8, yt + 18, "上部：受压", fs=12, anchor="start", weight=700, fill=C["blue"][0])
    for k in range(3):
        cx = 150 + k * 70
        f.arrow(cx - 22, yt + 14, cx - 4, yt + 14, color=C["blue"][0], sw=1.6, size=6); f.arrow(cx + 22, yt + 14, cx + 4, yt + 14, color=C["blue"][0], sw=1.6, size=6)
    f.text(x1 - 8, yt + 18, "混凝土负责", fs=11, anchor="end", fill=C["blue"][0])
    # rebar
    for yy in (yb - 12, yb - 7):
        f.line(x0 + 6, yy, x1 - 6, yy, stroke=C["red"][0], sw=3)
    f.text(x0 + 8, yb - 22, "下部：受拉", fs=12, anchor="start", weight=700, fill=C["red"][0])
    for k in range(3):
        cx = 150 + k * 70
        f.arrow(cx - 4, yb - 26, cx - 24, yb - 26, color=C["red"][0], sw=1.6, size=6); f.arrow(cx + 4, yb - 26, cx + 24, yb - 26, color=C["red"][0], sw=1.6, size=6)
    f.text(x1 - 8, yb - 22, "钢筋负责", fs=11, anchor="end", fill=C["red"][0])
    # plain concrete crack inset
    f.text(230, 210, "如果没有钢筋：底部一受拉就开裂", fs=12, weight=700, fill=MUTED)
    f.rect(120, 222, 220, 34, fill="#e5e7eb", stroke="#6b7280", rx=2)
    f.path("M230,256 L226,246 L234,238 L229,229", stroke=C["red"][0], sw=2)
    f.text(230, 274, "混凝土抗拉强度只有抗压的约 1/10", fs=11, fill=MUTED)
    # conditions
    f.rect(450, 30, 220, 236, fill=C["amber"][1], stroke=C["amber"][0], rx=10, sw=1.4)
    f.text(560, 54, "两者能“合作”的三个条件", fs=13, weight=700, fill=C["amber"][0])
    rows = [("① 热膨胀几乎一样", "冷热变化时不互相撕裂"), ("② 黏结牢固", "螺纹钢让混凝土“咬”住钢筋"), ("③ 碱性保护", "混凝土包裹，钢筋不易生锈")]
    for k, (a, b) in enumerate(rows):
        y = 84 + k * 60
        f.text(466, y, a, fs=12.5, anchor="start", weight=700)
        f.text(466, y + 20, b, fs=11, anchor="start", fill="#374151")
    f.text(340, 294, "抗压交给混凝土、抗拉交给钢筋：各取所长，成本又低", fs=11, fill=MUTED)
    return f

@fig
def skyscraper():
    f = Fig(680, 360, "超高层的受力")
    gx, gy = 160, 330
    f.line(40, gy, 320, gy, stroke="#92400e", sw=2)
    bx, bw, bt = 110, 100, 40
    f.rect(bx, bt, bw, gy - bt, fill=C["slate"][1], stroke=C["slate"][0], sw=1.4, rx=2)
    f.rect(bx + 35, bt, 30, gy - bt, fill=C["blue"][1], stroke=C["blue"][0], sw=1.4, rx=0)
    for k, ch in enumerate("核心筒"): f.text(bx + 50, 276 + 14 * k, ch, fs=11, weight=700, fill=C["blue"][0])
    for y in range(bt + 24, gy, 24):
        f.line(bx, y, bx + bw, y, stroke="#cbd5e1", sw=0.7)
    for y in (130, 230):
        f.rect(bx, y - 5, bw, 10, fill=C["purple"][1], stroke=C["purple"][0], sw=1, rx=0)
    f.text(bx + bw + 6, 134, "伸臂桁架", fs=10.5, anchor="start", fill=C["purple"][0])
    # damper
    f.line(bx + 50, bt + 6, bx + 50, bt + 26, stroke=INK, sw=1.2)
    f.circle(bx + 50, bt + 32, 8, fill=C["amber"][0], stroke=INK)
    f.text(bx + bw + 6, bt + 30, "阻尼器（反向摆动）", fs=10.5, anchor="start", fill=C["amber"][0])
    # wind
    for k, y in enumerate((70, 120, 170, 220, 270)):
        L = 26 + (5 - k) * 8
        f.arrow(bx - 10 - L, y, bx - 6, y, color=C["teal"][0], sw=2, size=8)
    f.text(28, 56, "风：越高越强", fs=12, anchor="start", weight=700, fill=C["teal"][0])
    # gravity accumulating
    for k, y in enumerate((90, 170, 250)):
        f.arrow(bx + bw + 30, y, bx + bw + 30, y + 30 + k * 6, color=C["red"][0], sw=1.6 + k * 0.8, size=7 + k)
    f.text(bx + bw + 40, 300, "重力向下累加", fs=11, anchor="start", fill=C["red"][0], weight=700)
    # right panel
    rx = 360
    f.text(rx, 40, "超高层要同时解决三件事", fs=14, weight=700, anchor="start")
    items = [("承重", "核心筒 + 外框把重量传到深基础", "slate"), ("抗风", "外形收进、扭转、开槽；顶部阻尼器减晃", "teal"),
             ("上下楼", "高速电梯、分区转乘、避难层与防火分区", "blue")]
    for k, (a, b, col) in enumerate(items):
        y = 62 + k * 62
        f.box(rx, y, 70, 46, a, col, fs=13, solid=True)
        f.text(rx + 82, y + 28, b, fs=11.5, anchor="start")
    f.rect(rx, 256, 300, 66, fill="#fff7ed", stroke=C["amber"][0], rx=8)
    f.text(rx + 150, 278, "为什么风比重力难？", fs=12.5, weight=700, fill=C["amber"][0])
    f.text(rx + 150, 298, "风推倒楼的力矩 ≈ 风力 × 高度", fs=11, fill=INK)
    f.text(rx + 150, 314, "高度翻倍，力矩约增长 4 倍以上", fs=11, fill=INK)
    return f

@fig
def suspension_bridge():
    f = Fig(520, 210, "悬索桥的力流")
    dy = 140
    f.line(10, dy, 510, dy, stroke=INK, sw=4)
    t1, t2, th = 150, 370, 50
    for tx in (t1, t2):
        f.rect(tx - 6, th, 12, 160 - th, fill=C["slate"][1], stroke=C["slate"][0], sw=1.4, rx=1)
    pts = []
    for i in range(41):
        x = t1 + (t2 - t1) * i / 40
        y = th + (dy - 18 - th) * (1 - ((x - (t1 + t2) / 2) / ((t2 - t1) / 2)) ** 2)
        pts.append((x, y))
    f.poly(pts, stroke=C["red"][0], sw=2.6)
    f.poly([(t1, th), (40, dy + 30)], stroke=C["red"][0], sw=2.6); f.poly([(t2, th), (480, dy + 30)], stroke=C["red"][0], sw=2.6)
    for x, y in pts[2:-1:3]:
        f.line(x, y, x, dy, stroke=C["red"][0], sw=0.9)
    f.rect(18, dy + 24, 40, 24, fill="#9ca3af", stroke=INK, rx=2); f.rect(462, dy + 24, 40, 24, fill="#9ca3af", stroke=INK, rx=2)
    f.text(38, dy + 62, "锚碇", fs=11, weight=700); f.text(482, dy + 62, "锚碇", fs=11, weight=700)
    f.text(260, 72, "主缆：受拉", fs=12, weight=700, fill=C["red"][0])
    f.text(t1 - 12, 46, "塔：受压", fs=11.5, weight=700, fill=C["slate"][0], anchor="end")
    f.text(260, 160, "吊索把桥面挂在主缆上", fs=10.5, fill=MUTED)
    f.arrow(t1 - 16, 60, t1 - 16, 120, color=C["slate"][0], sw=1.6, size=7)
    f.text(260, 200, "桥面重量 → 吊索 → 主缆 → 塔顶与锚碇 → 大地", fs=11.5, fill=INK, weight=700)
    return f

@fig
def flush_toilet():
    f = Fig(520, 230, "存水弯")
    # pipe S-trap
    w = 26
    outer = "M120,40 L120,120 Q120,190 190,190 Q260,190 260,120 L260,110 Q260,80 290,80 L420,80"
    f.path(outer, stroke="#94a3b8", sw=w + 6)
    f.path(outer, stroke="#f8fafc", sw=w)
    # water in U
    f.path("M120,120 Q120,190 190,190 Q260,190 260,120", stroke=C["blue"][1], sw=w - 2)
    f.path("M107,120 L133,120", stroke=C["blue"][0], sw=1.4); f.path("M247,120 L273,120", stroke=C["blue"][0], sw=1.4)
    f.text(190, 194, "水封", fs=12.5, weight=700, fill=C["blue"][0])
    f.text(120, 30, "便池", fs=12, weight=700)
    f.text(430, 84, "通往下水道", fs=12, anchor="start", weight=700)
    for x in (330, 370):
        f.path(f"M{x},64 q-6,-10 0,-20 q6,-10 0,-20", stroke=C["amber"][0], sw=1.6)
    f.text(350, 30, "臭气被水封挡住", fs=11, fill=C["amber"][0], weight=700)
    f.rect(20, 200, 480, 26, fill="#fff", stroke="#fff")
    f.text(260, 222, "冲水时水位越过弯顶 → 虹吸把污物整段吸走 → 水箱补水，水封重新形成", fs=11, fill=MUTED)
    return f

def main():
    only = set(sys.argv[1:])
    for name, fn in FIGS.items():
        if only and name not in only: continue
        fn().save(OUT / f"{name}.svg")
    print("wrote", len(only or FIGS), "figures to", OUT)

if __name__ == "__main__":
    main()
