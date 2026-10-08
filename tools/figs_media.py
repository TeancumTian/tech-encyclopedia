#!/usr/bin/env python3
"""Diagrams for 第 16 篇「光学、成像与媒体」 -> assets/figs/media/*.svg"""
from __future__ import annotations
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from svgkit import Fig, C, INK, MUTED, tw
from mapkit_d11_17 import concept_map as cmap

OUT = Path(__file__).resolve().parents[1] / "assets" / "figs" / "media"
FIGS = {}
def fig(fn):
    FIGS[fn.__name__.replace("_", "-")] = fn; return fn

@fig
def concept_map():
    return cmap("光学、成像与媒体", "从上往下读：记录光与声 → 传播与复制 → 印刷与办公 → 看得更清、量得更准。",
        [("记录影像", "blue", ["摄影", "胶卷与平价相机", "彩色摄影", "数码相机", "手机与计算摄影", "像素", "红外热成像"]),
         ("记录声音", "teal", ["留声机", "麦克风与扬声器", "磁性录音", "随身听", "数字音频与 CD", "MP3"]),
         ("活动影像与传播", "purple", ["电影", "有声电影", "电视", "彩色电视", "录像机", "数字电视", "JPEG", "视频编码", "VR / AR", "元宇宙"]),
         ("印刷与办公", "amber", ["轮转印刷机", "打字机", "键盘与输入法", "复印机", "激光打印", "喷墨打印", "电子书", "数字排版"]),
         ("光学与精密测量", "red", ["激光", "全息术", "光谱学", "X 射线晶体学", "电子显微镜", "扫描隧道显微镜", "现代光学显微术", "射电望远镜", "大型光学望远镜", "自适应光学", "原子钟", "国际单位制", "标准时间", "碳-14 定年", "盖革计数器", "地震仪"])],
        [("1814", "蒸汽印报"), ("1839", "银版摄影"), ("1859", "光谱分析"), ("1877", "留声机"), ("1888", "柯达相机"),
         ("1895", "卢米埃尔电影"), ("1912", "晶体衍射"), ("1926", "电视演示"), ("1931", "电子显微镜"), ("1955", "铯原子钟"),
         ("1960", "激光器"), ("1975", "数码相机"), ("1982", "CD"), ("1993", "MP3 标准"), ("2019", "SI 重新定义")],
        [("根原理", "amber", ["透镜成像", "光电效应", "采样定理", "信息与压缩", "能级与光谱", "波动与衍射"]),
         ("三次跃迁", "blue", ["化学/机械记录", "→ 电信号传播", "→ 数字化"]),
         ("一组数字", "slate", ["CD：44100 次/秒", "MP3 ≈ CD 的 1/11", "电影：24 格/秒"])],
        ["图像传感器、显示屏 → 第 2 篇「电与电子」　光纤与流媒体 → 第 4 篇「互联网与通信」",
         "图像识别与生成 → 第 5 篇「人工智能」　太空望远镜 → 第 9 篇　X 光与 CT → 第 10 篇「生物与医学」"],
        arrow="down", center_note="↓ 记录 → 传播 → 测量：同一套光学原理，向外看星系，向内看原子")

@fig
def photography():
    f = Fig(680, 340, "照相机与胶片")
    # object (tree)
    f.line(60, 150, 60, 110, stroke="#92400e", sw=5)
    f.circle(60, 92, 22, fill="#bbf7d0", stroke="#15803d", sw=1.4)
    f.text(60, 172, "物体", fs=11.5, weight=700)
    # camera box
    f.rect(240, 60, 200, 120, fill="#f3f4f6", stroke=INK, sw=1.6, rx=4)
    f.text(340, 52, "暗箱", fs=12, weight=700)
    # lens
    f.path("M240,92 Q252,120 240,148 Q228,120 240,92 Z", fill=C["blue"][1], stroke=C["blue"][0], sw=1.4)
    f.text(240, 196, "透镜", fs=11.5, weight=700, fill=C["blue"][0])
    # rays from top and bottom of object to inverted image
    f.line(60, 72, 240, 106, stroke=C["amber"][0], sw=1.4); f.line(240, 106, 434, 160, stroke=C["amber"][0], sw=1.4)
    f.line(60, 72, 240, 134, stroke=C["amber"][0], sw=1.4); f.line(240, 134, 434, 160, stroke=C["amber"][0], sw=1.4)
    f.line(60, 150, 240, 110, stroke=C["teal"][0], sw=1.4); f.line(240, 110, 434, 80, stroke=C["teal"][0], sw=1.4)
    f.line(60, 150, 240, 132, stroke=C["teal"][0], sw=1.4); f.line(240, 132, 434, 80, stroke=C["teal"][0], sw=1.4)
    f.rect(434, 66, 8, 108, fill=C["red"][1], stroke=C["red"][0], rx=1)
    f.text(452, 100, "胶片", fs=11.5, weight=700, fill=C["red"][0], anchor="start")
    f.text(452, 118, "（倒立的像）", fs=10.5, fill=MUTED, anchor="start")
    # inverted tree icon
    f.circle(410, 150, 8, fill="#bbf7d0", stroke="#15803d", sw=1); f.line(410, 142, 410, 128, stroke="#92400e", sw=2)
    f.rect(530, 60, 140, 120, fill=C["amber"][1], stroke=C["amber"][0], rx=8)
    f.text(600, 82, "曝光量", fs=12.5, weight=700, fill=C["amber"][0])
    f.text(600, 106, "= 光强 × 时间", fs=11.5)
    f.text(600, 130, "光圈：进光多少", fs=11)
    f.text(600, 150, "快门：曝光多久", fs=11)
    # bottom process
    f.line(20, 214, 660, 214, stroke="#e5e7eb", sw=1)
    steps = [("① 曝光", "卤化银晶体吸收光子", "析出微量银 = 潜影", "slate"), ("② 显影 · 定影", "潜影处整颗变成黑银粒", "洗掉未感光的卤化银", "purple"), ("③ 负片 → 正片", "亮处在负片上变黑", "透过负片印到相纸上", "green")]
    for k, (a, b, c, col) in enumerate(steps):
        x = 20 + k * 222
        f.rect(x, 228, 200, 92, fill=C[col][1], stroke=C[col][0], rx=8)
        f.text(x + 100, 252, a, fs=13, weight=700, fill=C[col][0])
        f.text(x + 100, 278, b, fs=11)
        f.text(x + 100, 298, c, fs=11)
        if k < 2: f.arrow(x + 202, 274, x + 220, 274, color=INK, sw=1.6, size=7)
    return f

@fig
def digital_audio():
    f = Fig(520, 220, "采样与量化")
    X0, Y0, W, A = 50, 110, 440, 70
    for k in range(-4, 5):
        y = Y0 - k * A / 4
        f.line(X0, y, X0 + W, y, stroke="#e5e7eb", sw=0.8)
    f.line(X0, Y0 - A - 10, X0, Y0 + A + 10, stroke=INK, sw=1.2)
    f.line(X0, Y0, X0 + W, Y0, stroke=INK, sw=1)
    def s(t): return 0.75 * math.sin(2 * math.pi * t * 1.3) + 0.25 * math.sin(2 * math.pi * t * 3.1)
    pts = [(X0 + W * i / 300, Y0 - A * s(i / 300)) for i in range(301)]
    f.poly(pts, stroke=C["blue"][0], sw=2)
    n = 22
    q = []
    for i in range(n + 1):
        t = i / n; x = X0 + W * t
        v = round(s(t) * 4) / 4
        y = Y0 - A * v
        f.line(x, Y0, x, y, stroke=C["red"][0], sw=1, dash="2,2")
        f.circle(x, y, 3.2, fill=C["red"][0], stroke="#fff", sw=0.6)
        q.append((x, y))
    st = []
    for (x, y), (x2, _) in zip(q, q[1:] + [(X0 + W + W / n, 0)]):
        st += [(x, y), (min(x2, X0 + W), y)]
    f.poly(st, stroke=C["red"][0], sw=1.2, opacity=0.6)
    f.text(X0 + 6, 22, "蓝：原始声波　红点：每隔固定时间取一个值，并取整到最近的台阶", fs=11, anchor="start")
    f.text(260, 206, "CD：每秒采样 44100 次，每个值分 65536 级（16 位）——远比图中细密", fs=11, fill=MUTED)
    return f

@fig
def television():
    f = Fig(680, 330, "电视的扫描")
    # left: picture with raster lines
    f.text(110, 26, "① 摄像端：逐行扫描", fs=13, weight=700, fill=C["blue"][0])
    x0, y0, w, h = 20, 40, 180, 130
    f.rect(x0, y0, w, h, fill="#fff", stroke=INK, sw=1.4, rx=2)
    f.circle(x0 + 90, y0 + 62, 30, fill="#fde68a", stroke=C["amber"][0])
    for k in range(9):
        y = y0 + 10 + k * 14
        f.line(x0 + 8, y, x0 + w - 8, y, stroke=C["red"][0], sw=1)
        if k < 8: f.line(x0 + w - 8, y, x0 + 8, y + 14, stroke=C["red"][0], sw=0.6, dash="2,3")
    f.text(110, 188, "实线：读出亮度　虚线：回扫", fs=10.5, fill=MUTED)
    # middle: signal
    f.text(340, 26, "② 一条随时间变化的电信号", fs=13, weight=700, fill=C["purple"][0])
    sx, sy = 236, 110
    pts = []
    for i in range(200):
        x = sx + i
        line = i // 50; pos = (i % 50) / 50
        if i % 50 < 4: y = sy + 30  # sync pulse
        else:
            bright = 1 if (line in (1, 2) and 0.35 < pos < 0.75) else 0.2
            y = sy - 40 * bright
        pts.append((x, y))
    f.poly(pts, stroke=C["purple"][0], sw=1.6)
    f.text(340, 170, "低于零线的短脉冲 = 同步信号", fs=10.5, fill=MUTED)
    f.text(340, 186, "告诉接收端：新的一行开始了", fs=10.5, fill=MUTED)
    f.arrow(204, 104, 232, 104, color=INK, sw=1.6, size=7)
    f.arrow(440, 104, 470, 104, color=INK, sw=1.6, size=7)
    # right: CRT
    f.text(570, 26, "③ 显像管：电子束重画", fs=13, weight=700, fill=C["green"][0])
    f.path("M480,90 L520,90 L560,46 L660,46 L660,176 L560,176 L520,122 L480,122 Z", fill="#f3f4f6", stroke=INK, sw=1.4)
    f.rect(470, 96, 14, 20, fill=C["slate"][1], stroke=C["slate"][0], rx=2)
    f.text(477, 136, "电子枪", fs=10.5)
    f.line(484, 106, 650, 70, stroke=C["green"][0], sw=1.6, dash="4,3")
    f.circle(650, 70, 4, fill=C["green"][0], stroke="none", sw=0)
    f.rect(536, 96, 12, 20, fill=C["amber"][1], stroke=C["amber"][0], rx=2)
    f.line(540, 118, 516, 148, stroke=C["amber"][0], sw=1)
    f.text(500, 160, "偏转线圈", fs=10.5, fill=C["amber"][0])
    f.text(612, 194, "荧光屏：被击中处发光", fs=10.5, fill=MUTED)
    # bottom notes
    f.rect(20, 214, 640, 104, fill="#f9fafb", stroke="#d1d5db", rx=8)
    rows = [("为什么要扫描？", "无线电一次只能传一个数值；把二维画面变成一维信号，才能用一条信道发送。"),
            ("为什么看起来是连续的？", "每秒几十幅画面（早期 25 或 30 幅），大脑把它们连成连续的运动。"),
            ("关键是同步", "收发两端必须以同样的顺序和节奏扫描，否则画面会撕裂、滚动。")]
    for k, (a, b) in enumerate(rows):
        y = 240 + k * 28
        f.text(34, y, a, fs=12, weight=700, anchor="start")
        f.text(200, y, b, fs=11, anchor="start")
    return f

@fig
def laser():
    f = Fig(680, 320, "激光原理")
    # energy levels
    f.text(130, 26, "① 能级：泵浦与受激辐射", fs=13, weight=700, fill=C["purple"][0])
    for y, lab in ((60, "泵浦能级"), (110, "亚稳态（高能级）"), (200, "基态")):
        f.line(30, y, 200, y, stroke=INK, sw=2)
        f.text(206, y + 4, lab, fs=10.5, anchor="start", fill=MUTED)
    f.arrow(60, 198, 60, 64, color=C["blue"][0], sw=2, size=8)
    f.text(54, 140, "泵浦", fs=11, anchor="end", fill=C["blue"][0], weight=700)
    f.arrow(80, 62, 100, 106, color="#9ca3af", sw=1.4, size=6)
    f.text(96, 80, "快速落下", fs=10, fill=MUTED, anchor="start")
    for k in range(5):
        f.circle(120 + k * 16, 104, 4.5, fill=C["red"][0], stroke="#fff", sw=0.6)
    f.circle(150, 194, 4.5, fill=C["slate"][0], stroke="#fff", sw=0.6)
    f.text(120, 128, "粒子数反转：上多下少", fs=10.5, fill=C["red"][0], weight=700)
    f.arrow(186, 114, 186, 196, color=C["red"][0], sw=2, size=8)
    f.text(192, 170, "放出光子", fs=10.5, anchor="start", fill=C["red"][0])
    # stimulated emission inset
    f.text(130, 238, "受激辐射：1 个光子进去，2 个相同的光子出来", fs=11, weight=700)
    def ph(x, y, L=60, col=C["red"][0]):
        pts = [(x + i, y + 4 * math.sin(i / 6)) for i in range(L)]
        f.poly(pts, stroke=col, sw=1.6); f.arrow(x + L - 4, y + 4 * math.sin((L - 4) / 6), x + L + 4, y + 4 * math.sin((L - 4) / 6), color=col, sw=1.6, size=6)
    ph(20, 270, 50)
    f.circle(100, 270, 9, fill=C["red"][1], stroke=C["red"][0])
    f.text(100, 296, "高能级原子", fs=10, fill=MUTED)
    ph(118, 262, 60); ph(118, 280, 60)
    f.text(150, 314, "频率、方向、相位完全一样", fs=10, fill=MUTED, anchor="start")
    # cavity
    f.text(480, 26, "② 谐振腔：来回放大", fs=13, weight=700, fill=C["red"][0])
    cx0, cx1, cy = 330, 620, 120
    f.rect(cx0 + 22, cy - 30, cx1 - cx0 - 44, 60, fill=C["red"][1], stroke=C["red"][0], rx=6)
    f.text((cx0 + cx1) / 2, cy + 50, "增益介质（红宝石、气体、半导体…）", fs=11, fill=C["red"][0])
    f.rect(cx0, cy - 44, 10, 88, fill="#94a3b8", stroke=INK, rx=1)
    f.rect(cx1 - 10, cy - 44, 10, 88, fill="#cbd5e1", stroke=INK, rx=1, dash="3,2")
    f.text(cx0 + 5, cy - 52, "全反射镜", fs=10.5)
    f.text(cx1 - 5, cy - 52, "半透镜", fs=10.5)
    for k, y in enumerate((cy - 14, cy, cy + 14)):
        if k % 2 == 0:
            f.arrow(cx0 + 16, y, cx1 - 16, y, color=C["red"][0], sw=1.4 + k * 0.4, size=7)
        else:
            f.arrow(cx1 - 16, y, cx0 + 16, y, color=C["red"][0], sw=1.6, size=7)
    f.arrow(cx1 + 2, cy, 672, cy, color=C["red"][0], sw=4, size=11)
    f.text(650, cy - 12, "激光", fs=11.5, weight=700, fill=C["red"][0])
    f.arrow(590, 210, 590, cy + 34, color=C["blue"][0], sw=1.8, size=8)
    f.text(560, 226, "泵浦：闪光灯 / 电流 / 另一束光", fs=11, fill=C["blue"][0])
    f.rect(330, 248, 340, 62, fill=C["amber"][1], stroke=C["amber"][0], rx=8)
    f.text(500, 270, "结果：方向集中、颜色单一、相位一致", fs=12, weight=700, fill=C["amber"][0])
    f.text(500, 292, "→ 能会聚成极小光斑，也能传播很远不发散", fs=11)
    return f

def wl_rgb(w):
    if w < 440: r, g, b = -(w - 440) / 60, 0, 1
    elif w < 490: r, g, b = 0, (w - 440) / 50, 1
    elif w < 510: r, g, b = 0, 1, -(w - 510) / 20
    elif w < 580: r, g, b = (w - 510) / 70, 1, 0
    elif w < 645: r, g, b = 1, -(w - 645) / 65, 0
    else: r, g, b = 1, 0, 0
    fac = 0.4 + 0.6 * (w - 380) / 40 if w < 420 else (0.4 + 0.6 * (750 - w) / 50 if w > 700 else 1)
    return "#%02x%02x%02x" % tuple(int(255 * max(0, min(1, c * fac))) for c in (r, g, b))

@fig
def spectroscopy():
    f = Fig(520, 210, "氢原子光谱")
    X0, W = 40, 440
    def X(w): return X0 + (w - 380) / (750 - 380) * W
    lines = [410.2, 434.0, 486.1, 656.3]
    f.text(X0, 30, "发射光谱：炽热的氢气只发出几种颜色的光", fs=11.5, anchor="start", weight=700)
    f.rect(X0, 40, W, 40, fill="#111827", stroke="none", sw=0, rx=2)
    for w in lines:
        f.rect(X(w) - 2, 40, 4, 40, fill=wl_rgb(w), stroke="none", sw=0, rx=0)
    f.text(X0, 110, "吸收光谱：连续光穿过较冷的氢气，同样位置变暗", fs=11.5, anchor="start", weight=700)
    step = 2
    for w in range(380, 750, step):
        f.rect(X(w), 120, W / (370 / step) + 0.6, 40, fill=wl_rgb(w), stroke="none", sw=0, rx=0)
    for w in lines:
        f.rect(X(w) - 2, 120, 4, 40, fill="#111827", stroke="none", sw=0, rx=0)
    for w in (400, 500, 600, 700):
        f.text(X(w), 176, f"{w} nm", fs=10, fill=MUTED)
    for w in lines:
        f.line(X(w), 82, X(w), 118, stroke="#9ca3af", sw=0.8, dash="2,2")
    f.text(260, 200, "谱线位置由能级差决定：每种元素一套，像指纹一样独特", fs=10.5, fill=MUTED)
    return f

def main():
    only = set(sys.argv[1:])
    for name, fn in FIGS.items():
        if only and name not in only: continue
        fn().save(OUT / f"{name}.svg")
    print("wrote", len(only or FIGS), "figures to", OUT)

if __name__ == "__main__":
    main()
