#!/usr/bin/env python3
"""Diagrams for 第 11 篇「农业与食品」 -> assets/figs/agri/*.svg"""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from svgkit import Fig, C, INK, MUTED, tw
from mapkit_d11_17 import concept_map as cmap

OUT = Path(__file__).resolve().parents[1] / "assets" / "figs" / "agri"
FIGS = {}
def fig(fn):
    FIGS[fn.__name__.replace("_", "-")] = fn; return fn

@fig
def concept_map():
    return cmap("农业与食品", "从上往下读：先有阳光、水和氮，再靠机器和良种把它们变成粮食，最后经加工和冷链送上餐桌。",
        [("投入：阳光 · 水 · 氮", "amber", ["光合作用", "化肥（氮磷钾）", "合成氨", "现代灌溉 · 滴灌", "轮作固氮", "保护性耕作"]),
         ("机械化：用机器换人力", "slate", ["条播机", "机械收割机", "拖拉机", "联合收割机", "精准农业", "植保无人机", "铁丝网"]),
         ("育种与植保：提单产", "green", ["现代育种", "杂交玉米", "杂交水稻", "绿色革命", "转基因作物", "基因编辑作物", "家畜育种", "种子库", "农药", "综合虫害管理"]),
         ("养殖与新型生产", "teal", ["集约化养殖", "水产养殖", "设施农业 · 垂直农场", "无土栽培", "细胞培养肉", "植物肉", "精密发酵"]),
         ("加工 · 保存 · 运输", "blue", ["罐头", "速冻食品", "冷链物流", "方便面", "食品添加剂", "HACCP 食品安全"])],
        [("1701", "条播机"), ("1730s", "诺福克轮作"), ("1810", "罐头"), ("1831", "机械收割机"), ("1842", "过磷酸钙"),
         ("1892", "汽油拖拉机"), ("1900", "重新发现孟德尔"), ("1913", "合成氨投产"), ("1925", "速冻食品"), ("1939", "DDT 杀虫"),
         ("1966", "IR8 奇迹稻"), ("1973", "杂交水稻配套"), ("1996", "转基因作物种植"), ("2013", "培养肉汉堡")],
        [("根原理", "amber", ["光合作用与能量流", "自然选择（育种）", "病原体学说（保鲜）", "规模效应"]),
         ("代价与约束", "red", ["富营养化", "农药与抗药性", "地下水超采", "细菌耐药", "温室气体"]),
         ("一组数字", "slate", ["人口：10 亿 → 80 亿", "约一半人口靠合成氮肥", "灌溉地两成 → 粮食四成"])],
        ["合成氨工艺 → 第 6 篇「材料与化工」　制冷 → 第 1 篇「能源与动力」　基因工程 → 第 10 篇「生物与医学」",
         "无人机与卫星导航 → 第 8、9 篇　富营养化与污水处理 → 第 15 篇「环境与气候技术」"],
        arrow="down", center_note="↓ 每往下一层，都在提高“阳光、水、氮 → 食物”的转化效率")

@fig
def chemical_fertilizer():
    f = Fig(680, 320, "氮从空气到餐桌")
    f.box(20, 40, 120, 64, "空气中的氮气 N₂", "slate", fs=12.5, sub="约占空气 78%\n植物不能直接用", sub_fs=10.5)
    f.box(20, 130, 120, 54, "天然气 / 煤", "slate", fs=12.5, sub="提供氢 H₂", sub_fs=10.5)
    f.rect(190, 60, 150, 110, fill=C["amber"][1], stroke=C["amber"][0], sw=1.6, rx=10)
    f.text(265, 86, "合成氨工厂", fs=14, weight=700, fill=C["amber"][0])
    f.lines(265, 108, ["N₂ + 3H₂ → 2NH₃", "高温高压 + 铁催化剂", "（哈伯—博施法，1913）"], fs=10.5, fill=INK, lh=1.5)
    f.arrow(142, 72, 188, 96, color=C["slate"][0]); f.arrow(142, 157, 188, 136, color=C["slate"][0])
    f.box(380, 80, 110, 70, "氮肥", "amber", fs=13.5, sub="尿素 · 硝酸铵\n铵盐", sub_fs=10.5, solid=True)
    f.arrow(342, 115, 378, 115, color=C["amber"][0], sw=2)
    f.rect(530, 40, 130, 150, fill=C["green"][1], stroke=C["green"][0], sw=1.6, rx=10)
    f.text(595, 64, "农田", fs=14, weight=700, fill=C["green"][0])
    f.lines(595, 90, ["根系吸收铵和硝酸盐", "→ 合成蛋白质", "→ 籽粒增产"], fs=10.5, lh=1.5)
    f.arrow(492, 115, 528, 115, color=C["amber"][0], sw=2)
    # outcomes
    f.box(530, 222, 130, 62, "进入作物：约四到五成", "green", fs=11.5, sub="→ 粮食 · 饲料 → 人", sub_fs=10.5)
    f.arrow(595, 192, 595, 220, color=C["green"][0], sw=2)
    f.box(250, 222, 250, 62, "流失：其余部分", "red", fs=12, sub="淋溶入河湖（富营养化）· 挥发成氨\n变成氧化亚氮（强温室气体）", sub_fs=10.5)
    f.arrow(540, 180, 502, 236, color=C["red"][0], sw=1.6, dash="5,3")
    f.text(20, 244, "全球平均：施入的氮", fs=11.5, anchor="start", weight=700)
    f.text(20, 262, "只有不到一半进了粮食", fs=11.5, anchor="start", weight=700)
    f.text(20, 282, "（各地差异很大）", fs=10.5, anchor="start", fill=MUTED)
    f.text(340, 312, "把惰性的 N≡N 三键拆开要很多能量：合成氨消耗了全球约 1–2% 的能源", fs=11, fill=MUTED)
    return f

def plant(f, x, base, h, head, tilt=0, col=C["green"][0]):
    import math
    tx = x + h * math.sin(math.radians(tilt)); ty = base - h * math.cos(math.radians(tilt))
    f.path(f"M{x},{base} Q{x + (tx - x) * 0.2},{base - h * 0.6} {tx:.1f},{ty:.1f}", stroke=col, sw=3)
    f.raw(f'<ellipse cx="{tx:.1f}" cy="{ty:.1f}" rx="{head * 0.45:.1f}" ry="{head:.1f}" fill="{C["amber"][1]}" stroke="{C["amber"][0]}" stroke-width="1.4" transform="rotate({tilt} {tx:.1f} {ty:.1f})"/>')
    for k in (0.35, 0.6):
        yy = base - h * k * math.cos(math.radians(tilt)); xx = x + h * k * math.sin(math.radians(tilt)) * 0.6
        f.path(f"M{xx:.1f},{yy:.1f} q-16,-6 -22,-18", stroke=col, sw=1.6); f.path(f"M{xx:.1f},{yy:.1f} q16,-6 22,-18", stroke=col, sw=1.6)

@fig
def green_revolution():
    f = Fig(680, 330, "绿色革命")
    f.text(170, 24, "传统高秆品种 + 大量施肥", fs=13, weight=700, fill=C["red"][0])
    f.line(30, 170, 310, 170, stroke="#92400e", sw=2)
    for x in (70, 150): plant(f, x, 170, 120, 14, tilt=62)
    plant(f, 240, 170, 135, 13, tilt=8)
    f.text(170, 192, "秆长得又高又细 → 一阵风雨就倒伏减产", fs=11, fill=C["red"][0])
    f.text(510, 24, "半矮秆品种 + 大量施肥", fs=13, weight=700, fill=C["green"][0])
    f.line(370, 170, 650, 170, stroke="#92400e", sw=2)
    for x in (420, 510, 600): plant(f, x, 170, 78, 20)
    f.text(510, 192, "秆短而粗，养分进了穗 → 穗大不倒", fs=11, fill=C["green"][0])
    # 4 pillars
    items = [("矮秆高产品种", "博洛格小麦\nIR8 水稻", "green"), ("化肥", "尤其是氮肥", "amber"), ("灌溉", "水渠 · 机井", "blue"), ("农药与政策", "植保 · 贷款\n收购价 · 推广", "slate")]
    for i, (a, b, col) in enumerate(items):
        x = 30 + i * 138
        f.box(x, 218, 118, 66, a, col, fs=12.5, sub=b, sub_fs=10.5)
        if i < 3: f.text(x + 128, 256, "+", fs=20, weight=700, fill=INK)
    f.arrow(580, 251, 600, 251, color=INK, sw=2)
    f.box(604, 222, 66, 58, "单产", "red", fs=13, sub="约翻倍", sub_fs=11, solid=True)
    f.text(340, 312, "缺任何一件，产量都上不去：只引进种子而没有水和肥，新品种并不比老品种强", fs=11, fill=MUTED)
    return f

@fig
def hybrid_rice():
    f = Fig(520, 250, "三系杂交水稻")
    f.box(20, 30, 130, 58, "不育系 A", "red", fs=13, sub="花粉不育\n只能当母本", sub_fs=10.5)
    f.box(20, 150, 130, 58, "不育系 A", "red", fs=13, sub="（同上）", sub_fs=10.5)
    f.box(200, 30, 120, 58, "保持系 B", "blue", fs=13, sub="授粉后代仍不育", sub_fs=10.5)
    f.box(200, 150, 120, 58, "恢复系 R", "green", fs=13, sub="授粉后代可育", sub_fs=10.5)
    f.text(175, 64, "×", fs=20, weight=700); f.text(175, 184, "×", fs=20, weight=700)
    f.arrow(322, 59, 368, 59, color=C["blue"][0], sw=1.8); f.arrow(322, 179, 368, 179, color=C["green"][0], sw=1.8)
    f.box(372, 30, 130, 58, "新的不育系 A", "red", fs=12.5, sub="用来繁殖母本", sub_fs=10.5)
    f.box(372, 150, 130, 58, "杂交种 F1", "green", fs=13, sub="种到大田，增产约两成", sub_fs=10.5, solid=True)
    f.text(260, 120, "关键：找到雄性不育的母本，水稻才能大批量杂交制种", fs=11, fill=MUTED)
    f.text(260, 238, "杂种优势只在第一代最强，所以每年都要重新制种", fs=11, fill=MUTED)
    return f

@fig
def cold_chain():
    f = Fig(520, 222, "冷链温度带")
    steps = ["产地预冷", "冷库", "冷藏运输", "超市冷柜", "家庭冰箱"]
    for i, s in enumerate(steps):
        x = 14 + i * 100
        f.box(x, 26, 88, 40, s, "blue", fs=12)
        if i < 4: f.arrow(x + 89, 46, x + 99, 46, color=C["blue"][0], sw=1.4, size=6)
    bands = [("冷冻食品", "≤ −18 ℃", "purple"), ("鲜肉 · 乳品", "0 ～ 4 ℃", "blue"), ("多数疫苗", "2 ～ 8 ℃", "teal"), ("部分 mRNA 疫苗（早期）", "约 −70 ℃", "red")]
    for i, (a, b, col) in enumerate(bands):
        y = 84 + i * 28
        f.rect(60, y, 400, 22, fill=C[col][1], stroke=C[col][0], rx=4, sw=1)
        f.text(72, y + 15.5, a, fs=11.5, anchor="start", weight=700)
        f.text(448, y + 15.5, b, fs=11.5, anchor="end", weight=700, fill=C[col][0])
    f.text(260, 214, "整条链的可靠性取决于最弱的一环：断冷一次，前面的努力可能白费", fs=11, fill=MUTED)
    return f

def main():
    only = set(sys.argv[1:])
    for name, fn in FIGS.items():
        if only and name not in only: continue
        fn().save(OUT / f"{name}.svg")
    print("wrote", len(only or FIGS), "figures to", OUT)

if __name__ == "__main__":
    main()
