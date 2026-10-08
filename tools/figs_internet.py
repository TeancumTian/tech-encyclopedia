#!/usr/bin/env python3
"""Generate all diagrams for 第 4 篇「互联网与通信」 -> assets/figs/internet/*.svg"""
from __future__ import annotations
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from svgkit import Fig, C, INK, MUTED, tw
from figs_energy import concept_map_layout

OUT = Path(__file__).resolve().parents[1] / "assets" / "figs" / "internet"
FIGS = {}

def fig(fn):
    FIGS[fn.__name__.replace("_", "-")] = fn
    return fn


@fig
def concept_map():
    layers = [
        ("① 有线通信：电流跑过导线", "slate", ["电报★", "摩尔斯电码", "跨大西洋电缆", "电话★", "电话交换机", "传真"]),
        ("② 无线电与卫星：电磁波穿过天空", "amber", ["无线电★", "天线", "调制与解调", "调幅 · 调频", "广播", "复用",
                                            "超外差", "微波中继", "通信卫星", "卫星互联网", "相控阵"]),
        ("③ 光纤：光在玻璃里奔跑", "teal", ["光纤通信★", "光纤放大器", "海底光缆", "宽带接入"]),
        ("④ 移动通信：把电话装进口袋", "green", ["移动电话★", "蜂窝网络★", "2G/GSM", "短信", "3G", "4G/LTE", "5G", "6G",
                                            "MIMO", "频谱", "SIM 卡", "智能手机★", "Wi-Fi", "蓝牙", "RFID/NFC"]),
        ("⑤ 互联网：网络的网络", "blue", ["分组交换★", "阿帕网", "TCP/IP★", "互联网★", "分层模型", "以太网", "IP/IPv6",
                                        "DNS", "路由器", "BGP", "CDN", "调制解调器", "VPN", "Tor", "DDoS"]),
        ("⑥ Web 与应用：人在网上做什么", "purple", ["电子邮件", "超文本", "万维网★", "HTTP/HTML", "浏览器", "HTTPS",
                                              "搜索引擎★", "PageRank", "电商", "广告", "Cookie", "社交媒体", "维基百科",
                                              "P2P", "即时通讯", "流媒体", "短视频", "移动互联网", "物联网", "网络中立"]),
    ]
    hist = [("1837", "电报"), ("1866", "跨洋电缆"), ("1876", "电话"), ("1895", "无线电"), ("1920", "广播电台"),
            ("1962", "通信卫星"), ("1969", "阿帕网"), ("1970", "低损耗光纤"), ("1973", "手机 · 以太网"),
            ("1974", "TCP/IP"), ("1983", "互联网诞生"), ("1989", "万维网"), ("1998", "谷歌"), ("2007", "iPhone"),
            ("2019", "5G 商用"), ("2025", "全球 60 亿人上网")]
    sides = [
        ("第一性原理", "red", ["电磁波：光速传播", "香农极限：带宽+噪声", "  决定最快速度", "冗余与纠错", "抽象与分层", "网络效应", "标准化"]),
        ("载体越来越快", "amber", ["电报：每分钟几十字", "拨号：56 千比特/秒", "光纤：单纤数十太比特", "5G：峰值每秒数吉比特"]),
        ("数据怎么走", "blue", ["手机 → 基站 → 核心网", "→ 运营商 → 骨干网", "→ 海底光缆 → 数据中心"]),
    ]
    footer = ["晶体管 · 天线 · 芯片 → 第 2 篇「电与电子」　服务器 · 数据库 · 云 → 第 3 篇「计算与软件」",
              "加密 · 网络攻击 → 第 13 篇「安全与国防」　卫星导航 → 第 9 篇「航天」　电视 · 媒体 → 第 16 篇"]
    return concept_map_layout("互联网与通信 · 知识地图",
                              "从上往下读：载体从电流到电磁波再到光；网络从\u201c接通一条线\u201d变成\u201c把数据切成包\u201d；最后人们在网上生活。",
                              layers, hist, sides, footer, "↓ 下层负责把比特送到，上层负责让比特有用（抽象与分层）")


# ------------------------------------------------------------------ 有线
@fig
def telegraph():
    f = Fig(680, 290, "电报")
    f.text(110, 26, "发报端", fs=14, weight=700, fill=C["slate"][0])
    f.rect(40, 120, 140, 14, fill="#d6d3d1", stroke=INK, rx=2)
    f.line(60, 110, 160, 92, stroke=INK, sw=4)
    f.circle(160, 88, 9, fill=C["slate"][0], stroke="none")
    f.text(110, 160, "电键：按下 = 接通", fs=11, fill=INK)
    f.box(50, 190, 120, 36, "电池", "amber", fs=12)
    f.path("M180,127 L250,127 L250,60 L520,60 L520,100", stroke=C["red"][0], sw=2)
    f.text(385, 50, "导线（几百公里）", fs=11.5, weight=700, fill=C["red"][0])
    f.path("M110,226 L110,256 L560,256 L560,200", stroke=MUTED, sw=1.6, dash="5 4")
    f.text(335, 274, "大地作为回路", fs=10.5, fill=MUTED)
    f.text(560, 26, "收报端", fs=14, weight=700, fill=C["slate"][0])
    f.rect(500, 100, 50, 80, fill=C["blue"][1], stroke=C["blue"][0], rx=4)
    for k in range(6):
        f.line(500, 110 + k * 12, 550, 116 + k * 12, stroke=C["amber"][0], sw=2)
    f.text(525, 196, "电磁铁", fs=11, fill=C["blue"][0], weight=700)
    f.line(500, 92, 640, 92, stroke=INK, sw=4)
    f.circle(640, 92, 5, fill=INK, stroke="none")
    f.arrow(580, 66, 580, 86, color=C["blue"][0], sw=1.6, size=6)
    f.path("M40,127 L28,127 L28,208 L50,208", stroke=C["red"][0], sw=2)
    f.text(600, 120, "衔铁被吸下", fs=10.5, anchor="start", fill=INK)
    f.text(600, 136, "\u201c嗒\u201d", fs=11, anchor="start", weight=700)
    # morse sample
    f.rect(250, 140, 200, 60, fill="#fff", stroke=C["purple"][0], rx=8)
    f.text(350, 160, "S O S", fs=12, weight=700, fill=C["purple"][0])
    x = 270
    for s in "... --- ...":
        if s == " ": x += 12; continue
        w = 6 if s == "." else 18
        f.rect(x, 176, w, 8, fill=C["purple"][0], stroke="none", rx=2); x += w + 5
    return f


@fig
def telephone():
    f = Fig(680, 280, "电话")
    f.text(100, 26, "话筒", fs=14, weight=700, fill=C["blue"][0])
    for k in range(3):
        f.path(f"M{30 + k * 14},90 q10,20 0,40", stroke=C["blue"][0], sw=1.6)
    f.text(30, 150, "声波", fs=10.5, fill=C["blue"][0])
    f.rect(80, 70, 14, 80, fill=C["slate"][0], stroke="none", rx=2)
    f.text(87, 168, "振膜", fs=10.5)
    f.rect(100, 80, 50, 60, fill=C["amber"][1], stroke=C["amber"][0], rx=4)
    f.text(125, 115, "碳粒", fs=10.5, weight=700)
    f.text(125, 190, "振动 → 电阻变化", fs=10.5, fill=MUTED)
    f.text(125, 206, "→ 电流起伏", fs=10.5, fill=MUTED)
    pts = [(160 + i, 110 - 18 * math.sin(i / 9) * math.sin(i / 40)) for i in range(0, 120, 2)]
    f.poly(pts, stroke=C["red"][0], sw=2)
    f.text(220, 76, "起伏的电流", fs=11, fill=C["red"][0], weight=700)
    f.box(290, 80, 110, 60, "交换机", "slate", fs=13, sub="接通两条线", solid=True)
    pts = [(410 + i, 110 - 18 * math.sin(i / 9) * math.sin(i / 40)) for i in range(0, 110, 2)]
    f.poly(pts, stroke=C["red"][0], sw=2)
    f.text(580, 26, "听筒", fs=14, weight=700, fill=C["green"][0])
    f.rect(530, 80, 40, 60, fill=C["blue"][1], stroke=C["blue"][0], rx=4)
    f.text(550, 115, "电磁铁", fs=9.5, weight=700)
    f.rect(578, 70, 10, 80, fill=C["slate"][0], stroke="none", rx=2)
    for k in range(3):
        f.path(f"M{600 + k * 14},90 q10,20 0,40", stroke=C["green"][0], sw=1.6)
    f.text(580, 190, "电流变化 → 吸力变化", fs=10.5, fill=MUTED)
    f.text(580, 206, "→ 振膜振动 → 声音", fs=10.5, fill=MUTED)
    f.text(340, 250, "电话传的是声音的\u201c形状\u201d（模拟信号）：电流的起伏和声波的起伏一模一样", fs=12, weight=700, fill=INK)
    return f


# ------------------------------------------------------------------ 无线
@fig
def radio():
    f = Fig(680, 280, "无线电通信")
    f.box(20, 100, 110, 60, "声音 / 数据", "amber", fs=12.5)
    f.arrow(132, 130, 160, 130, color=INK)
    f.box(162, 100, 110, 60, "发射机", "red", fs=13, sub="调制到载波上")
    f.line(290, 130, 290, 50, stroke=INK, sw=2.4)
    f.poly([(278, 50), (290, 30), (302, 50)], stroke=INK, sw=2)
    f.line(272, 130, 290, 130, stroke=INK, sw=2)
    f.text(290, 22, "", fs=10)
    for k in range(4):
        r = 30 + k * 26
        f.path(f"M{300 + r * 0.5},{60 - r * 0.6} A{r},{r} 0 0 1 {300 + r * 0.5},{60 + r * 0.6}", stroke=C["purple"][0], sw=1.6)
        f.path(f"M{430 - r * 0.5},{60 - r * 0.6} A{r},{r} 0 0 0 {430 - r * 0.5},{60 + r * 0.6}", stroke=C["purple"][0], sw=1.6, opacity=0.6)
    f.text(365, 150, "电磁波以光速传播", fs=11.5, weight=700, fill=C["purple"][0])
    f.line(440, 130, 440, 50, stroke=INK, sw=2.4)
    f.poly([(428, 50), (440, 30), (452, 50)], stroke=INK, sw=2)
    f.line(440, 130, 458, 130, stroke=INK, sw=2)
    f.box(458, 100, 100, 60, "接收机", "blue", fs=13, sub="调谐 → 解调")
    f.arrow(560, 130, 584, 130, color=INK)
    f.box(586, 100, 80, 60, "还原", "green", fs=12.5)
    f.rect(40, 190, 600, 70, fill="#fff", stroke=C["slate"][0], rx=10)
    f.text(340, 212, "天线里来回振荡的电流 → 向四周辐射电磁波；电磁波扫过接收天线 → 感应出微弱电流", fs=11.5, fill=INK)
    f.text(340, 234, "不同电台用不同频率（载波）；调谐 = 只挑出你想听的那个频率", fs=11.5, fill=INK)
    f.text(340, 252, "频率越高，能携带的信息越多，但越容易被遮挡", fs=10.5, fill=MUTED)
    return f


@fig
def am_fm():
    f = Fig(520, 270, "调幅与调频")
    rows = [("声音信号", "slate"), ("调幅 AM：改变振幅", "red"), ("调频 FM：改变频率", "blue")]
    for k, (t, col) in enumerate(rows):
        y = 45 + k * 80
        f.text(20, y - 22, t, fs=12, weight=700, fill=C[col][0], anchor="start")
        f.line(20, y, 500, y, stroke="#e5e7eb", sw=1)
        pts = []
        for i in range(0, 481):
            m = math.sin(i / 480 * 2 * math.pi * 1.5)
            if k == 0: v = 22 * m
            elif k == 1: v = (14 + 10 * m) * math.sin(i / 3.2)
            else:
                ph = sum(1 / 3.2 + 0.16 * math.sin(j / 480 * 2 * math.pi * 1.5) for j in range(i))
                v = 22 * math.sin(ph)
            pts.append((20 + i, y - v))
        f.poly(pts, stroke=C[col][0], sw=1.4 if k else 2)
    f.text(260, 262, "FM 抗干扰更好、音质更佳；AM 传得更远（中波可沿地面绕射）", fs=11, fill=MUTED)
    return f


@fig
def communication_satellite():
    f = Fig(520, 270, "通信卫星轨道")
    cx, cy = 150, 150
    f.circle(cx, cy, 48, fill=C["blue"][1], stroke=C["blue"][0], sw=2)
    f.text(cx, cy + 5, "地球", fs=12, weight=700, fill=C["blue"][0])
    f.circle(cx, cy, 64, fill="none", stroke=C["green"][0], sw=1.4, dash="3 3")
    for a in range(0, 360, 30):
        r = math.radians(a)
        f.circle(cx + 64 * math.cos(r), cy + 64 * math.sin(r), 3, fill=C["green"][0], stroke="none")
    f.circle(cx, cy, 118, fill="none", stroke=C["amber"][0], sw=1.4, dash="6 4")
    for a in (90, 210, 330):
        r = math.radians(a)
        f.rect(cx + 118 * math.cos(r) - 6, cy + 118 * math.sin(r) - 6, 12, 12, fill=C["amber"][0], stroke="none", rx=2)
    f.text(cx, 18, "静止轨道（示意，未按比例）", fs=10, fill=C["amber"][0])
    f.box(300, 30, 205, 100, "静止轨道 GEO", "amber", fs=13, sub="高约 36000 公里\n3 颗即可覆盖除两极外的全球\n往返延迟约 0.5 秒")
    f.box(300, 145, 205, 100, "低轨星座 LEO", "green", fs=13, sub="高约 300–2000 公里\n延迟约 20–50 毫秒\n需要成千上万颗组网")
    return f


# ------------------------------------------------------------------ 光纤与移动
@fig
def fiber_optic():
    f = Fig(680, 300, "光纤通信")
    f.text(240, 26, "全反射：光被\u201c关\u201d在纤芯里", fs=14, weight=700, fill=C["teal"][0])
    f.rect(30, 50, 420, 110, fill=C["teal"][1], stroke=C["teal"][0], rx=50)
    f.rect(30, 80, 420, 50, fill="#ecfeff", stroke=C["teal"][0], rx=0, dash="4 3")
    f.text(460, 70, "包层（折射率低）", fs=11, anchor="start", fill=C["teal"][0], weight=700)
    f.text(460, 110, "纤芯（折射率高）", fs=11, anchor="start", fill=C["blue"][0], weight=700)
    f.text(460, 126, "直径约 9 微米", fs=10.5, anchor="start", fill=MUTED)
    zig = [(40, 105), (90, 82), (150, 128), (210, 82), (270, 128), (330, 82), (390, 128), (440, 100)]
    f.poly(zig, stroke=C["red"][0], sw=2)
    f.head(440, 100, math.atan2(100 - 128, 440 - 390), C["red"][0])
    f.text(240, 180, "光以很斜的角度碰到边界时会全部反射回来，几乎不漏", fs=11, fill=INK)
    # WDM
    f.text(340, 214, "波分复用：多种颜色的光同时走一根光纤", fs=13, weight=700, fill=C["purple"][0])
    cols = ["#ef4444", "#f59e0b", "#22c55e", "#3b82f6", "#8b5cf6"]
    for k, c in enumerate(cols):
        f.line(40, 232 + k * 10, 150, 262, stroke=c, sw=2.4)
        f.line(530, 262, 640, 232 + k * 10, stroke=c, sw=2.4)
    f.rect(150, 252, 380, 20, fill="#f1f5f9", stroke=C["slate"][0], rx=10)
    for k, c in enumerate(cols):
        f.line(160, 256 + k * 3, 520, 256 + k * 3, stroke=c, sw=1.2)
    f.text(95, 292, "合波", fs=10.5, fill=MUTED); f.text(585, 292, "分波", fs=10.5, fill=MUTED)
    f.text(340, 292, "每种颜色一路信号，单根光纤可达每秒数十太比特", fs=10.5, fill=MUTED)
    return f


@fig
def mobile_phone():
    f = Fig(680, 290, "移动电话的演进")
    items = [(60, "1973", "\u201c砖头\u201d原型", "约 1.1 千克", 70, 170, "slate"),
             (240, "1990s", "功能手机", "打电话 · 发短信", 56, 120, "blue"),
             (420, "2007 后", "智能手机", "触摸屏 · 应用 · 移动互联网", 74, 140, "purple")]
    for x, yr, name, sub, w, h, col in items:
        dark, light = C[col]
        base = 210
        f.rect(x + 50 - w / 2, base - h, w, h, fill=light, stroke=dark, sw=2, rx=10 if col != "slate" else 6)
        if col == "slate":
            f.rect(x + 50 - 6, base - h - 30, 12, 32, fill=dark, stroke="none", rx=3)
            for r in range(4):
                for c in range(3):
                    f.rect(x + 30 + c * 14, base - 80 + r * 16, 10, 10, fill="#fff", stroke=dark, sw=0.8, rx=2)
        elif col == "blue":
            f.rect(x + 50 - w / 2 + 6, base - h + 10, w - 12, 36, fill="#fff", stroke=dark, sw=1, rx=2)
            for r in range(4):
                for c in range(3):
                    f.rect(x + 34 + c * 12, base - 64 + r * 13, 8, 8, fill="#fff", stroke=dark, sw=0.8, rx=2)
        else:
            f.rect(x + 50 - w / 2 + 5, base - h + 10, w - 10, h - 20, fill="#fff", stroke=dark, sw=1, rx=4)
            for r in range(4):
                for c in range(3):
                    f.rect(x + 23 + c * 19, base - h + 20 + r * 24, 14, 14, fill=C[["red", "amber", "green", "teal"][(r + c) % 4]][0], stroke="none", rx=3)
        f.text(x + 50, base + 24, yr, fs=13, weight=700, fill=dark)
        f.text(x + 50, base + 42, name, fs=12, weight=700)
        f.text(x + 50, base + 58, sub, fs=10.5, fill=MUTED)
        if x < 400: f.arrow(x + 120, 150, x + 165, 150, color=MUTED, sw=1.6)
    f.rect(560, 60, 110, 150, fill="#fff", stroke=C["green"][0], rx=8)
    f.lines(615, 82, ["1G 模拟语音", "2G 数字 · 短信", "3G 上网", "4G 视频", "5G 万物互联"], fs=11, fill=INK, lh=2.2)
    return f


@fig
def cellular_network():
    f = Fig(680, 320, "蜂窝网络")
    R = 38
    cols = ["blue", "amber", "green", "red", "purple", "teal", "pink"]
    # 7-cell reuse pattern on hex grid
    def hexpts(cx, cy):
        return [(cx + R * math.cos(math.radians(60 * k)), cy + R * math.sin(math.radians(60 * k))) for k in range(6)]
    centers = []
    for q in range(-3, 4):
        for r in range(-3, 4):
            x = 230 + 1.5 * R * q
            y = 160 + math.sqrt(3) * R * (r + q / 2)
            if 20 < x < 440 and 20 < y < 300:
                centers.append((q, r, x, y))
    for q, r, x, y in centers:
        idx = (q + 3 * r) % 7
        dark, light = C[cols[idx]]
        f.poly(hexpts(x, y), fill=light, stroke=dark, sw=1, closed=True)
        f.text(x, y + 4, f"f{idx + 1}", fs=10, fill=dark, weight=700)
    # handover
    f.circle(200, 150, 4, fill=INK, stroke="none")
    f.path("M120,200 Q170,150 280,130", stroke=INK, sw=2, dash="5 3")
    f.head(280, 130, math.atan2(130 - 140, 280 - 230), INK)
    f.rect(84, 212, 136, 20, fill="#fff", stroke=INK, sw=0.8, rx=4)
    f.text(152, 226, "边走边打：自动切换基站", fs=11, weight=700, fill=INK)
    f.rect(460, 40, 205, 240, fill="#fff", stroke=C["slate"][0], rx=10)
    f.lines(562, 66, ["把城市切成许多小区", "每个小区一个基站，功率小", "", "相邻小区用不同频率", "（不同颜色）避免干扰", "", "隔得够远就重复使用", "同一频率（同色）", "", "→ 有限的频谱", "服务无限多的人"], fs=11.5, fill=INK)
    return f


@fig
def smartphone():
    f = Fig(680, 320, "智能手机的组成")
    f.rect(250, 20, 180, 290, fill="#f8fafc", stroke=INK, sw=2.4, rx=26)
    f.rect(262, 44, 156, 242, fill=C["slate"][1], stroke=C["slate"][0], rx=6)
    parts = [(270, 54, 140, 40, "片上系统 SoC", "red", "CPU · GPU · AI · 基带"), (270, 100, 66, 36, "内存", "amber", None),
             (344, 100, 66, 36, "闪存", "amber", None), (270, 142, 140, 80, "电池", "green", "锂离子 约 4000–5000 毫安时"),
             (270, 228, 66, 50, "摄像头", "purple", None), (344, 228, 66, 50, "传感器", "teal", None)]
    for x, y, w, h, lab, col, sub in parts:
        f.box(x, y, w, h, lab, col, fs=11.5, sub=sub, sub_fs=9.5)
    left = [("触摸屏", "电容式多点触控", 70), ("多种无线电", "蜂窝 4G/5G · Wi-Fi · 蓝牙 · NFC", 150), ("卫星定位", "GPS / 北斗等", 230)]
    for t, s, y in left:
        f.text(230, y, t, fs=12.5, weight=700, anchor="end", fill=C["blue"][0])
        f.text(230, y + 18, s, fs=10.5, anchor="end", fill=MUTED)
        f.line(234, y, 262, y, stroke=C["blue"][0], sw=1, dash="3 3")
    right = [("加速度计 · 陀螺仪", "转屏、计步", 240), ("指纹 / 人脸识别", "解锁与支付", 170), ("麦克风 · 扬声器", "", 100)]
    for t, s, y in right:
        f.text(450, y, t, fs=12, weight=700, anchor="start", fill=C["teal"][0])
        if s: f.text(450, y + 18, s, fs=10.5, anchor="start", fill=MUTED)
        f.line(418, y - 4, 446, y - 4, stroke=C["teal"][0], sw=1, dash="3 3")
    f.text(560, 40, "操作系统 + 应用商店", fs=12, weight=700, fill=C["purple"][0])
    f.text(560, 58, "让硬件变成无数种工具", fs=10.5, fill=MUTED)
    return f


# ------------------------------------------------------------------ 互联网基础
@fig
def packet_switching():
    f = Fig(680, 320, "电路交换与分组交换")
    def nodes(y0):
        pos = {"A": (40, y0 + 55), "1": (170, y0 + 20), "2": (170, y0 + 95), "3": (330, y0 + 20), "4": (330, y0 + 95), "B": (460, y0 + 55)}
        edges = [("A", "1"), ("A", "2"), ("1", "3"), ("2", "4"), ("1", "4"), ("2", "3"), ("3", "B"), ("4", "B"), ("1", "2"), ("3", "4")]
        return pos, edges
    # circuit
    f.text(20, 24, "电路交换（电话）：通话期间独占整条线路", fs=13, weight=700, fill=C["slate"][0], anchor="start")
    pos, edges = nodes(30)
    for a, b in edges:
        f.line(*pos[a], *pos[b], stroke="#d1d5db", sw=2)
    for a, b in [("A", "1"), ("1", "3"), ("3", "B")]:
        f.line(*pos[a], *pos[b], stroke=C["slate"][0], sw=6)
    for n, (x, y) in pos.items():
        f.circle(x, y, 12 if n in "AB" else 9, fill=C["slate"][0] if n in "AB" else "#fff", stroke=C["slate"][0], sw=2)
        if n in "AB": f.text(x, y + 4, n, fs=11, fill="#fff", weight=700)
    f.text(560, 70, "别人用不了这条线", fs=11, fill=MUTED)
    f.text(560, 88, "哪怕你一言不发", fs=11, fill=MUTED)
    # packet
    f.text(20, 180, "分组交换（互联网）：切成小包，各自寻路，共享线路", fs=13, weight=700, fill=C["blue"][0], anchor="start")
    pos, edges = nodes(186)
    for a, b in edges:
        f.line(*pos[a], *pos[b], stroke="#cbd5e1", sw=2)
    for n, (x, y) in pos.items():
        f.circle(x, y, 12 if n in "AB" else 9, fill=C["blue"][0] if n in "AB" else "#fff", stroke=C["blue"][0], sw=2)
        if n in "AB": f.text(x, y + 4, n, fs=11, fill="#fff", weight=700)
    def pkt(x, y, s, col):
        f.rect(x - 9, y - 8, 18, 16, fill=C[col][0], stroke="#fff", sw=1, rx=2)
        f.text(x, y + 4, s, fs=9.5, fill="#fff", weight=700)
    pkt(105, 222, "1", "amber"); pkt(250, 206, "2", "amber"); pkt(250, 281, "3", "amber"); pkt(395, 260, "4", "amber")
    pkt(250, 245, "x", "pink"); pkt(170 + 80 * 0.5, 206 + 75 * 0.5 + 20, "y", "teal")
    f.text(560, 220, "橙色：A 发给 B 的包", fs=11, fill=C["amber"][0], weight=700)
    f.text(560, 238, "其他颜色：别人的包", fs=11, fill=MUTED)
    f.text(560, 262, "到达后按序号重组", fs=11, fill=INK)
    f.text(560, 280, "某条线断了就绕道", fs=11, fill=INK)
    f.text(340, 312, "代价：包可能延迟、乱序、丢失 → 交给 TCP 来补救", fs=11, fill=MUTED)
    return f


@fig
def tcp_ip():
    f = Fig(680, 360, "TCP 三次握手与确认重传")
    LX, RX = 140, 540
    f.box(LX - 60, 14, 120, 34, "客户端（你的手机）", "blue", fs=11.5)
    f.box(RX - 60, 14, 120, 34, "服务器", "green", fs=11.5)
    f.line(LX, 50, LX, 350, stroke=C["blue"][0], sw=2); f.line(RX, 50, RX, 350, stroke=C["green"][0], sw=2)
    msgs = [(70, ">", "SYN：能听到吗？", "purple"), (105, "<", "SYN-ACK：能，你呢？", "purple"), (140, ">", "ACK：能。", "purple"),
            (190, ">", "数据段 1", "amber"), (225, "<", "ACK 1：收到 1", "slate"), (260, ">", "数据段 2", "amber"),
            (325, ">", "数据段 2（重发）", "amber")]
    for y, d, lab, col in msgs:
        if d == ">": f.arrow(LX, y, RX, y + 14, color=C[col][0], sw=1.8, label=lab, loff=(0, -4), lcolor=C[col][0], fs=11.5)
        else: f.arrow(RX, y, LX, y + 14, color=C[col][0], sw=1.8, label=lab, loff=(0, -4), lcolor=C[col][0], fs=11.5)
    f.rect(390, 264, 152, 14, fill="#fff", stroke="none", rx=0)
    f.line(RX, 262, RX, 278, stroke=C["green"][0], sw=2)
    f.text(392, 272, "✕ 丢失", fs=12, weight=700, fill=C["red"][0])
    f.path(f"M{LX},{260} L{340},{267}", stroke=C["red"][0], sw=0)
    f.rect(LX - 130, 66, 120, 90, fill=C["purple"][1], stroke=C["purple"][0], rx=6)
    f.lines(LX - 70, 96, ["三次握手", "建立连接"], fs=12, weight=700, fill=C["purple"][0])
    f.rect(LX - 130, 256, 120, 76, fill=C["red"][1], stroke=C["red"][0], rx=6)
    f.lines(LX - 70, 280, ["超时没收到", "ACK 2", "→ 重发"], fs=11, fill=C["red"][0], weight=700)
    f.rect(RX + 10, 170, 125, 110, fill="#fff", stroke=C["slate"][0], rx=6)
    f.lines(RX + 72, 194, ["IP：只管寄", "（尽力而为）", "", "TCP：编号、确认、", "重发、排序"], fs=11, fill=INK)
    return f


@fig
def internet():
    f = Fig(680, 330, "网络的网络")
    f.rect(230, 120, 220, 80, fill=C["blue"][1], stroke=C["blue"][0], sw=2, rx=40)
    f.text(340, 152, "骨干网 · 交换中心", fs=14, weight=700, fill=C["blue"][0])
    f.text(340, 172, "大型运营商互联", fs=11, fill=C["blue"][0])
    isps = [(110, 60, "运营商 A", "amber"), (570, 60, "运营商 B", "amber"), (110, 260, "移动运营商", "green"), (570, 260, "云服务商", "purple")]
    for x, y, lab, col in isps:
        f.box(x - 65, y - 22, 130, 44, lab, col, fs=12.5)
        f.line(x + (60 if x < 340 else -60), y + (20 if y < 160 else -20), 340 + (-90 if x < 340 else 90), 160 + (-30 if y < 160 else 30), stroke=C[col][0], sw=3)
    ends = [(20, 10, "家庭宽带", 110, 60), (200, 10, "企业网", 110, 60), (20, 300, "手机 · 基站", 110, 260), (190, 300, "物联网设备", 110, 260),
            (480, 10, "大学 · 研究网", 570, 60), (480, 300, "数据中心", 570, 260), (600, 300, "CDN 节点", 570, 260)]
    for x, y, lab, px, py in ends:
        w = tw(lab, 11) + 14
        f.rect(x, y, w, 22, fill="#fff", stroke=C["slate"][0], rx=11)
        f.text(x + w / 2, y + 15, lab, fs=11)
        f.line(x + w / 2, y + (22 if y < 160 else 0), px, py + (-22 if y < 160 else 22), stroke=MUTED, sw=1.2)
    f.line(175, 60, 505, 60, stroke=C["amber"][0], sw=1.6, dash="5 4")
    f.text(340, 54, "运营商之间也可直接\u201c对等互联\u201d", fs=10.5, fill=C["amber"][0])
    f.rect(210, 220, 260, 56, fill="#fff", stroke=C["red"][0], rx=8)
    f.lines(340, 242, ["各网络独立管理，没有总开关", "靠 TCP/IP · BGP · DNS 统一互通"], fs=11.5, fill=INK)
    return f


@fig
def osi_layers():
    f = Fig(520, 300, "网络分层")
    layers = [("应用层", "HTTP · DNS · 邮件", "purple"), ("传输层", "TCP · UDP", "blue"), ("网络层", "IP · 路由", "green"),
              ("链路层", "以太网 · Wi-Fi", "amber"), ("物理层", "网线 · 光纤 · 无线电", "slate")]
    for k, (n, s, col) in enumerate(layers):
        y = 30 + k * 46
        f.box(20, y, 150, 38, n, col, fs=12.5, sub=s, sub_fs=9.5)
        f.box(350, y, 150, 38, n, col, fs=12.5, sub=s, sub_fs=9.5)
        # packet envelope
        hdrs = ["", "TCP头", "IP头", "帧头"][:k + 1] if k < 4 else None
        if k < 4:
            x = 185
            segs = [("数据", "purple")] + [(h, layers[j][2]) for j, h in enumerate(["TCP", "IP", "帧"], start=1) if j <= k]
            total = sum(tw(sg, 9.5) + 8 for sg, _ in segs)
            x = 260 - total / 2
            for sg, c in reversed(segs):
                w = tw(sg, 9.5) + 8
                f.rect(x, y + 10, w, 18, fill=C[c][1], stroke=C[c][0], rx=2, sw=0.8)
                f.text(x + w / 2, y + 23, sg, fs=9.5); x += w
    f.arrow(10, 40, 10, 240, color=MUTED, sw=1.4); f.text(6, 280, "发送：逐层加头", fs=10, anchor="start", fill=MUTED)
    f.arrow(510, 240, 510, 40, color=MUTED, sw=1.4); f.text(508, 280, "接收：逐层拆开", fs=10, anchor="end", fill=MUTED)
    f.line(170, 236, 350, 236, stroke=C["slate"][0], sw=3)
    f.text(260, 262, "比特流 0101…", fs=10.5, fill=C["slate"][0], weight=700)
    return f


@fig
def dns():
    f = Fig(520, 280, "DNS 查询")
    f.box(10, 110, 90, 50, "你的电脑", "slate", fs=12, sub="www.example.com?", sub_fs=8.5)
    f.box(150, 110, 100, 50, "本地解析器", "blue", fs=12, sub="运营商 / 公共 DNS")
    f.arrow(102, 128, 148, 128, color=INK, label="①", loff=(0, -5))
    f.arrow(148, 145, 102, 145, color=C["green"][0], label="⑧ IP 地址", loff=(0, 16), lcolor=C["green"][0])
    srv = [(20, "根服务器", "问 .com 找谁", "red"), (105, "顶级域 .com", "问 example.com 找谁", "amber"), (190, "权威服务器", "IP = 93.184.…", "green")]
    for y, n, s, col in srv:
        f.box(330, y, 170, 52, n, col, fs=12, sub=s)
    pairs = [(46, "②③"), (131, "④⑤"), (216, "⑥⑦")]
    for y, lab in pairs:
        f.arrow(252, 130 + (y - 131) * 0.25, 328, y - 6, color=INK, sw=1.2, size=6)
        f.arrow(328, y + 8, 252, 140 + (y - 131) * 0.25, color=MUTED, sw=1.2, size=6, dash="3 3")
        f.text(292, y - 10 + (130 - y) * 0.4, lab, fs=10, fill=MUTED)
    f.text(200, 196, "每一步结果都会缓存", fs=10.5, fill=C["blue"][0], weight=700)
    f.text(200, 212, "下次直接回答", fs=10.5, fill=C["blue"][0])
    f.text(260, 268, "名字分层管理：根 → .com → example.com → www", fs=11, fill=INK)
    return f


# ------------------------------------------------------------------ Web
@fig
def world_wide_web():
    f = Fig(680, 330, "点击一个链接")
    # URL anatomy
    url = [("https://", "协议", "purple"), ("www.example.com", "服务器（域名）", "blue"), ("/wiki/page.html", "路径（哪个文件）", "green")]
    x = 110
    for s, lab, col in url:
        w = len(s) * 0.62 * 14 + 14
        f.rect(x, 20, w, 30, fill=C[col][1], stroke=C[col][0], rx=4)
        f.text(x + w / 2, 40, s, fs=14, weight=700, mono=True, fill=C[col][0])
        f.text(x + w / 2, 68, lab, fs=11, fill=C[col][0])
        x += w + 4
    f.text(40, 41, "URL", fs=14, weight=700)
    # flow
    steps = [(20, "浏览器", "解析 URL", "slate"), (180, "DNS", "域名 → IP", "amber"), (340, "Web 服务器", "HTTP GET", "blue"), (500, "浏览器渲染", "HTML → 页面", "green")]
    for k, (sx, n, s, col) in enumerate(steps):
        f.box(sx + 5, 92, 135, 52, n, col, fs=13, sub=s)
        if k < 3: f.arrow(sx + 142, 118, sx + 182, 118, color=INK, sw=1.6)
    # pages and links
    pages = [(60, 180, "页面 A"), (250, 196, "页面 B"), (440, 176, "页面 C"), (580, 210, "页面 D")]
    for x, y, n in pages:
        f.rect(x, y, 80, 92, fill="#fff", stroke=C["slate"][0], rx=4)
        f.text(x + 40, y + 18, n, fs=11, weight=700)
        for j in range(4):
            f.line(x + 10, y + 32 + j * 13, x + 70 - (j % 2) * 18, y + 32 + j * 13, stroke="#d1d5db", sw=3)
        f.line(x + 14, y + 58, x + 44, y + 58, stroke=C["blue"][0], sw=3)
    f.curve(104, 238, 180, 300, 250, 246, color=C["blue"][0], sw=1.6)
    f.curve(294, 254, 370, 300, 440, 230, color=C["blue"][0], sw=1.6)
    f.curve(484, 234, 540, 280, 580, 256, color=C["blue"][0], sw=1.6)
    f.curve(470, 176, 300, 140, 120, 180, color=C["blue"][0], sw=1.2, dash="4 3")
    f.text(340, 176, "", fs=10)
    f.text(340, 322, "蓝色：超链接——任何网页都能链接到任何网页，不需要谁批准", fs=11.5, fill=C["blue"][0], weight=700)
    return f


@fig
def search_engine():
    f = Fig(680, 330, "搜索引擎")
    cols = [(20, "① 爬取", "blue"), (245, "② 建索引", "amber"), (470, "③ 查询与排序", "green")]
    for x, t, col in cols:
        f.rect(x, 20, 195, 270, fill=C[col][1], stroke=C[col][0], rx=10)
        f.text(x + 97, 44, t, fs=14, weight=700, fill=C[col][0])
    # crawler web
    pts = [(60, 90), (150, 80), (110, 140), (60, 200), (170, 190), (120, 250)]
    for a, b in [(0, 1), (0, 2), (1, 2), (2, 3), (2, 4), (3, 5), (4, 5), (1, 4)]:
        f.line(*pts[a], *pts[b], stroke=C["blue"][0], sw=1.2)
    for x, y in pts:
        f.rect(x - 12, y - 14, 24, 28, fill="#fff", stroke=C["blue"][0], rx=2)
    f.text(117, 278, "爬虫顺着链接下载网页", fs=10.5, fill=INK)
    f.arrow(217, 160, 243, 160, color=INK, sw=1.6)
    # inverted index
    idx = [("电池", "3, 17, 42"), ("锂", "17, 42, 88"), ("光伏", "5, 42"), ("电网", "8, 17"), ("…", "…")]
    for k, (w, ids) in enumerate(idx):
        y = 70 + k * 36
        f.rect(258, y, 60, 26, fill="#fff", stroke=C["amber"][0], rx=3)
        f.text(288, y + 18, w, fs=12, weight=700)
        f.arrow(320, y + 13, 340, y + 13, color=C["amber"][0], sw=1.2, size=6)
        f.text(346, y + 18, "网页 " + ids, fs=11, anchor="start", mono=True)
    f.text(342, 278, "倒排索引：词 → 网页列表", fs=10.5, fill=INK)
    f.arrow(442, 160, 468, 160, color=INK, sw=1.6)
    # query
    f.rect(484, 66, 168, 28, fill="#fff", stroke=C["green"][0], rx=14)
    f.text(568, 85, "🔍 锂 电池", fs=12)
    f.text(568, 116, "交集 → 网页 17、42", fs=11, fill=C["green"][0], weight=700)
    for k, (t, s) in enumerate([("1. 网页 42", "相关度高 · 链接多"), ("2. 网页 17", "较新 · 质量好")]):
        y = 132 + k * 48
        f.rect(484, y, 168, 40, fill="#fff", stroke=C["slate"][0], rx=4)
        f.text(494, y + 17, t, fs=11.5, anchor="start", weight=700, fill=C["blue"][0])
        f.text(494, y + 32, s, fs=10, anchor="start", fill=MUTED)
    f.text(567, 248, "数百种信号打分", fs=10.5, fill=INK)
    f.text(567, 278, "零点几秒内返回", fs=10.5, fill=INK)
    f.text(340, 318, "索引提前建好，所以查询时不必翻遍几十亿网页", fs=11.5, weight=700, fill=INK)
    return f


def main():
    only = set(sys.argv[1:])
    for name, fn in FIGS.items():
        if only and name not in only: continue
        fn().save(OUT / f"{name}.svg")
    print("wrote", len(FIGS) if not only else len(only), "figures to", OUT)

if __name__ == "__main__":
    main()
