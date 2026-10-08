#!/usr/bin/env python3
"""Generate all diagrams for 第 3 篇「计算与软件」 -> assets/figs/computing/*.svg"""
from __future__ import annotations
import math, random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from svgkit import Fig, C, INK, MUTED, tw

OUT = Path(__file__).resolve().parents[1] / "assets" / "figs" / "computing"
FIGS = {}

def fig(fn):
    FIGS[fn.__name__.replace("_", "-")] = fn
    return fn

# ------------------------------------------------------------------ concept map
@fig
def concept_map():
    f = Fig(680, 940, "计算与软件 知识地图")
    f.text(340, 30, "计算与软件 · 知识地图", fs=21, weight=700)
    f.text(340, 52, "中间是一座“抽象之塔”：越往上离人越近、离硬件越远。左边是历史，右边是贯穿各层的理论与方法。", fs=11.5, fill=MUTED)
    # center tower
    X, W = 168, 344
    layers = [  # bottom -> top
        ("硬件：从开关到芯片", "blue", ["比特与字节", "逻辑门", "触发器", "CPU / 指令集", "RISC · ARM", "流水线 · 多核", "GPU", "存储层次", "缓存 · DRAM", "闪存 · SSD", "超级计算机"]),
        ("程序与算法", "purple", ["汇编", "编译器 / 解释器", "编程语言", "C · Python · Java · JS", "面向对象 · 函数式", "算法", "数据结构", "大 O", "排序 · 递归 · 动态规划"]),
        ("系统软件", "green", ["操作系统", "分时", "Unix → Linux", "Windows · macOS · 安卓", "进程与线程", "并发", "虚拟内存", "文件系统", "虚拟化 → 容器 → K8s"]),
        ("数据", "amber", ["数据库 · SQL", "事务 ACID", "NoSQL", "大数据", "数据仓库", "哈希", "压缩", "纠错码", "Unicode"]),
        ("云与现代计算", "teal", ["客户端—服务器", "数据中心", "云计算 IaaS/PaaS/SaaS", "无服务器", "边缘计算", "科学计算"]),
        ("交互与应用", "pink", ["命令行", "图形界面 · 鼠标", "电子表格 · 文字处理", "计算机图形学", "游戏 · 游戏引擎", "应用商店", "千年虫"]),
    ]
    top, bottom = 80, 800
    lh = (bottom - top) / len(layers)
    for i, (name, col, items) in enumerate(layers):
        y = bottom - (i + 1) * lh
        dark, light = C[col]
        f.rect(X, y + 6, W, lh - 12, fill=light, stroke=dark, sw=1.4, rx=8)
        f.text(X + 12, y + 26, name, fs=14, fill=dark, weight=700, anchor="start")
        # chips in rows
        cx, cy = X + 12, y + 36
        for it in items:
            w = tw(it, 11) + 12
            if cx + w > X + W - 10:
                cx, cy = X + 12, cy + 24
            f.rect(cx, cy, w, 19, fill="#fff", stroke=dark, sw=0.8, rx=9)
            f.text(cx + w / 2, cy + 13.5, it, fs=11)
            cx += w + 6
        if i < len(layers) - 1:
            f.arrow(X + W / 2, y + 8, X + W / 2, y - 4, color=dark, sw=2.2, size=10)
    f.text(X + W / 2, bottom + 22, "↑ 每一层把下面的细节藏起来，只留简单接口（抽象与分层）", fs=11.5, fill=C["blue"][0], weight=700)
    # left: history
    LX = 10
    f.text(LX + 70, 92, "计算的源头", fs=14, weight=700, fill=C["slate"][0])
    hist = [("1822", "差分机"), ("1890", "穿孔卡片制表"), ("1936", "图灵机"), ("1943", "巨人计算机"),
            ("1945", "ENIAC"), ("1945", "冯·诺依曼结构"), ("1964", "大型机 S/360"), ("1965", "小型机"),
            ("1971", "微处理器"), ("1977", "个人电脑"), ("1991", "Linux"), ("2006", "云计算"), ("2008", "应用商店")]
    y0, step = 116, (bottom - 130) / (len(hist) - 1)
    f.line(LX + 18, y0 - 6, LX + 18, y0 + step * (len(hist) - 1) + 6, stroke=C["slate"][0], sw=2)
    for k, (yr, nm) in enumerate(hist):
        y = y0 + k * step
        f.circle(LX + 18, y, 4.5, fill=C["slate"][0], stroke="#fff", sw=1)
        f.text(LX + 28, y + 4, yr, fs=10.5, fill=MUTED, anchor="start", weight=700)
        f.text(LX + 60, y + 4, nm, fs=11.5, anchor="start")
    # right: cross-cutting
    RX = 524
    def side(y, title, col, items):
        dark, light = C[col]
        h = 34 + 22 * len(items)
        f.rect(RX, y, 148, h, fill=light, stroke=dark, sw=1.2, rx=8)
        f.text(RX + 74, y + 22, title, fs=13.5, fill=dark, weight=700)
        for k, it in enumerate(items):
            f.text(RX + 12, y + 44 + 22 * k, "· " + it, fs=11.5, anchor="start")
        return y + h
    y = side(84, "计算理论（上限）", "red", ["图灵机与可计算性", "停机问题", "P 与 NP", "大 O 复杂度"])
    y = side(y + 16, "软件工程（协作）", "slate", ["版本控制 Git", "测试 · 调试", "开源 · GNU", "敏捷 · DevOps", "API · 微服务"])
    y = side(y + 16, "分布式（规模）", "teal", ["分布式系统", "CAP 定理", "共识算法", "备份与 RAID"])
    # links to other domains
    f.rect(10, 860, 660, 66, fill="#f9fafb", stroke="#d1d5db", rx=8)
    f.text(340, 882, "和其他篇的接口", fs=12.5, weight=700)
    f.text(340, 904, "芯片怎么造 → 第 2 篇「电与电子」（晶体管、集成电路、摩尔定律）　网络与 Web → 第 4 篇「互联网与通信」", fs=11, fill=MUTED)
    f.text(340, 921, "机器学习与大模型 → 第 5 篇「人工智能」　加密与安全 → 第 13 篇「安全与国防」", fs=11, fill=MUTED)
    return f

# ------------------------------------------------------------------ 计算的源头
@fig
def turing_machine():
    f = Fig(680, 285, "图灵机")
    cells = ["…", "", "1", "1", "0", "1", "", "", "…"]
    x0, y0, cw = 70, 40, 60
    f.text(30, y0 + 34, "纸带", fs=13, weight=700, anchor="start", fill=C["slate"][0])
    for i, s in enumerate(cells):
        hl = i == 4
        f.rect(x0 + i * cw, y0, cw, 50, fill=C["amber"][1] if hl else "#fff", stroke=C["amber"][0] if hl else INK, sw=2 if hl else 1.2, rx=0)
        f.text(x0 + i * cw + cw / 2, y0 + 33, s, fs=20, weight=700, mono=True)
    hx = x0 + 4 * cw + cw / 2
    f.poly([(hx, y0 + 56), (hx - 14, y0 + 80), (hx + 14, y0 + 80)], fill=C["blue"][0], stroke=C["blue"][0], closed=True)
    f.box(hx - 70, y0 + 84, 140, 44, "读写头", "blue", fs=13, sub="当前状态：q₁", solid=True)
    f.arrow(hx - 90, y0 + 106, hx - 150, y0 + 106, color=C["blue"][0], label="左移", loff=(0, -6))
    f.arrow(hx + 90, y0 + 106, hx + 150, y0 + 106, color=C["blue"][0], label="右移", loff=(0, -6))
    # rule table
    tx, ty = 120, 190
    hdr = ["当前状态", "读到", "写入", "移动", "下一状态"]
    rows = [["q₁", "0", "1", "右", "q₂"], ["q₁", "1", "1", "右", "q₁"]]
    cwid = 88
    f.text(tx - 12, ty + 20, "规则表", fs=13, weight=700, anchor="end", fill=C["purple"][0])
    for j, h in enumerate(hdr):
        f.rect(tx + j * cwid, ty, cwid, 22, fill=C["purple"][1], stroke=C["purple"][0], rx=0, sw=0.8)
        f.text(tx + j * cwid + cwid / 2, ty + 15.5, h, fs=11.5, weight=700)
    for r, row in enumerate(rows):
        for j, v in enumerate(row):
            hl = r == 0
            f.rect(tx + j * cwid, ty + 22 * (r + 1), cwid, 22, fill="#fffbeb" if hl else "#fff", stroke=C["purple"][0], rx=0, sw=0.8)
            f.text(tx + j * cwid + cwid / 2, ty + 22 * (r + 1) + 15.5, v, fs=12)
    f.text(tx + 220, ty + 84, "高亮这一行此刻生效：读到 0 → 写 1 → 右移 → 转入状态 q₂", fs=11.5, fill=C["amber"][0], weight=700)
    return f

@fig
def von_neumann_architecture():
    f = Fig(680, 300, "冯·诺依曼结构")
    # CPU
    f.rect(30, 40, 270, 200, fill=C["blue"][1], stroke=C["blue"][0], sw=1.6, rx=10)
    f.text(165, 64, "CPU 中央处理器", fs=15, weight=700, fill=C["blue"][0])
    f.box(48, 80, 112, 62, "控制单元", "blue", fs=13, sub="取指 · 译码\n程序计数器 PC")
    f.box(172, 80, 112, 62, "运算单元 ALU", "blue", fs=13, sub="加减 · 比较\n逻辑运算")
    f.box(48, 156, 236, 40, "寄存器（最快的小存储）", "slate", fs=12.5, weight=400)
    f.text(165, 224, "取指 → 译码 → 执行 → 写回 → 再取指…", fs=11.5, fill=C["blue"][0], weight=700)
    # memory
    f.rect(450, 40, 200, 200, fill=C["amber"][1], stroke=C["amber"][0], sw=1.6, rx=10)
    f.text(550, 64, "存储器（内存）", fs=15, weight=700, fill=C["amber"][0])
    for k, (lab, col) in enumerate([("指令：LOAD 7", "purple"), ("指令：ADD 8", "purple"), ("指令：STORE 9", "purple"), ("数据：25", "green"), ("数据：17", "green")]):
        f.box(470, 78 + k * 30, 160, 24, lab, col, fs=11.5, weight=400, rx=3)
    f.text(550, 236, "程序和数据放在同一个地方", fs=11, fill=MUTED)
    # bus
    f.rect(300, 120, 150, 40, fill=C["red"][1], stroke=C["red"][0], sw=1.4, rx=4)
    f.text(375, 137, "总线", fs=13, weight=700, fill=C["red"][0])
    f.text(375, 153, "一次只能搬一点", fs=10.5, fill=C["red"][0])
    f.arrow(305, 112, 445, 112, color=C["red"][0], both=True, sw=1.4)
    f.text(375, 104, "冯·诺依曼瓶颈", fs=11, weight=700, fill=C["red"][0])
    # IO
    f.box(30, 256, 130, 34, "输入：键盘 / 磁盘", "green", fs=11.5, weight=400)
    f.box(170, 256, 130, 34, "输出：屏幕 / 打印", "green", fs=11.5, weight=400)
    f.arrow(95, 254, 95, 242, color=C["green"][0]); f.arrow(235, 242, 235, 254, color=C["green"][0])
    return f

@fig
def personal_computer():
    f = Fig(680, 230, "个人电脑的关键几步")
    ev = [("1975", "Altair 8800", "爱好者套件\n自己焊接、拨开关编程", "slate"),
          ("1977", "Apple II 等", "开箱即用的整机\n起价 1298 美元", "green"),
          ("1981", "IBM PC", "开放架构\n兼容机成为标准", "blue"),
          ("1984", "Macintosh", "图形界面 + 鼠标\n走进大众", "purple"),
          ("1995", "Windows 95", "开始菜单 + 上网\n电脑进入千家万户", "amber")]
    y = 70
    f.line(30, y, 650, y, stroke="#9ca3af", sw=3)
    f.arrow(640, y, 662, y, color="#9ca3af", sw=3, size=11)
    for i, (yr, nm, desc, col) in enumerate(ev):
        x = 80 + i * 130
        dark, light = C[col]
        f.circle(x, y, 9, fill=dark, stroke="#fff", sw=2)
        f.text(x, y - 20, yr, fs=15, weight=700, fill=dark)
        f.rect(x - 60, y + 22, 120, 104, fill=light, stroke=dark, rx=8)
        f.text(x, y + 46, nm, fs=13.5, weight=700)
        f.lines(x, y + 72, desc.split("\n"), fs=11, fill="#374151", lh=1.45)
    f.text(340, 222, "价格每跌破一道门槛，用户和软件就多一个数量级", fs=11.5, fill=MUTED)
    return f

# ------------------------------------------------------------------ 硬件
@fig
def bit_byte():
    f = Fig(520, 230, "一个字节")
    bits = "01000001"; vals = [128, 64, 32, 16, 8, 4, 2, 1]
    x0, cw = 60, 50
    f.text(260, 26, "1 字节 = 8 个比特", fs=14, weight=700)
    for i, b in enumerate(bits):
        on = b == "1"
        f.rect(x0 + i * cw, 40, cw, 48, fill=C["blue"][0] if on else "#fff", stroke=C["blue"][0], rx=0, sw=1.4)
        f.text(x0 + i * cw + cw / 2, 72, b, fs=22, weight=700, fill="#fff" if on else INK, mono=True)
        f.text(x0 + i * cw + cw / 2, 106, str(vals[i]), fs=11, fill=C["blue"][0] if on else MUTED, weight=700 if on else 400)
    f.text(30, 106, "位值", fs=11, fill=MUTED, anchor="start")
    f.box(40, 140, 200, 70, "当作整数", "green", fs=13, sub="64 + 1 = 65", sub_fs=16)
    f.box(280, 140, 200, 70, "当作 ASCII 字符", "amber", fs=13, sub="“A”", sub_fs=20)
    f.arrow(200, 116, 150, 136, color=C["green"][0]); f.arrow(320, 116, 370, 136, color=C["amber"][0])
    f.text(260, 226, "比特本身没有意义，意义来自“怎么解读”", fs=11, fill=MUTED)
    return f

def gate_and(f, x, y, s=1.0, col=INK):
    w, h = 40 * s, 36 * s
    f.path(f"M{x},{y} L{x+w*0.5},{y} A{h/2},{h/2} 0 0 1 {x+w*0.5},{y+h} L{x},{y+h} Z", stroke=col, sw=1.6, fill="#fff")
    return x + w * 0.5 + h / 2, y + h / 2

def gate_or(f, x, y, s=1.0, col=INK, xor=False):
    w, h = 44 * s, 36 * s
    f.path(f"M{x},{y} Q{x+w*0.55},{y} {x+w},{y+h/2} Q{x+w*0.55},{y+h} {x},{y+h} Q{x+w*0.28},{y+h/2} {x},{y} Z", stroke=col, sw=1.6, fill="#fff")
    if xor:
        f.path(f"M{x-6},{y} Q{x+w*0.28-6},{y+h/2} {x-6},{y+h}", stroke=col, sw=1.6)
    return x + w, y + h / 2

def gate_not(f, x, y, s=1.0, col=INK):
    w, h = 34 * s, 30 * s
    f.poly([(x, y), (x + w, y + h / 2), (x, y + h)], stroke=col, sw=1.6, fill="#fff", closed=True)
    f.circle(x + w + 4, y + h / 2, 4, fill="#fff", stroke=col, sw=1.4)
    return x + w + 8, y + h / 2

def truth(f, x, y, hdr, rows, col="blue", cw=26):
    dark, light = C[col]
    for j, h in enumerate(hdr):
        f.rect(x + j * cw, y, cw, 18, fill=light, stroke=dark, rx=0, sw=0.7)
        f.text(x + j * cw + cw / 2, y + 13, h, fs=11, weight=700)
    for r, row in enumerate(rows):
        for j, v in enumerate(row):
            last = j == len(row) - 1
            f.rect(x + j * cw, y + 18 * (r + 1), cw, 18, fill="#fffbeb" if (last and v == "1") else "#fff", stroke=dark, rx=0, sw=0.7)
            f.text(x + j * cw + cw / 2, y + 18 * (r + 1) + 13, v, fs=11, mono=True, weight=700 if last else 400)

@fig
def logic_gate():
    f = Fig(680, 340, "逻辑门与半加器")
    # three gates
    specs = [("与门 AND", "两个都为 1 才输出 1", gate_and, [["0","0","0"],["0","1","0"],["1","0","0"],["1","1","1"]], ["A","B","Y"]),
             ("或门 OR", "有一个为 1 就输出 1", gate_or, [["0","0","0"],["0","1","1"],["1","0","1"],["1","1","1"]], ["A","B","Y"]),
             ("非门 NOT", "输出与输入相反", gate_not, [["0","1"],["1","0"]], ["A","Y"])]
    for i, (nm, desc, g, rows, hdr) in enumerate(specs):
        x = 30 + i * 215
        f.text(x + 90, 24, nm, fs=14, weight=700, fill=C["blue"][0])
        f.text(x + 90, 42, desc, fs=10.5, fill=MUTED)
        gx, gy = x + 30, 60
        ox, oy = g(f, gx, gy)
        if g is gate_not:
            f.line(gx - 22, gy + 15, gx, gy + 15)
            f.text(gx - 26, gy + 19, "A", fs=11, anchor="end")
        else:
            f.line(gx - 22, gy + 9, gx + (6 if g is gate_or else 0), gy + 9); f.line(gx - 22, gy + 27, gx + (6 if g is gate_or else 0), gy + 27)
            f.text(gx - 26, gy + 13, "A", fs=11, anchor="end"); f.text(gx - 26, gy + 31, "B", fs=11, anchor="end")
        f.line(ox, oy, ox + 22, oy); f.text(ox + 26, oy + 4, "Y", fs=11, anchor="start")
        truth(f, x + 112, 52, hdr, rows)
    # half adder
    f.rect(20, 160, 640, 172, fill="#f8fafc", stroke="#cbd5e1", rx=10)
    f.text(40, 184, "把门组合起来：半加器（一位二进制加法）", fs=13.5, weight=700, anchor="start", fill=C["purple"][0])
    ax, ay = 230, 212
    ox1, oy1 = gate_or(f, ax, ay, xor=True)
    ox2, oy2 = gate_and(f, ax + 4, ay + 60)
    yA, yB = ay + 9, ay + 27
    f.text(92, yA + 5, "A", fs=13, weight=700); f.text(92, yB + 5, "B", fs=13, weight=700)
    f.line(102, yA, ax + 6, yA); f.line(102, yB, ax + 6, yB)
    f.line(150, yA, 150, ay + 69); f.line(150, ay + 69, ax + 4, ay + 69); f.circle(150, yA, 3, fill=INK)
    f.line(180, yB, 180, ay + 87); f.line(180, ay + 87, ax + 4, ay + 87); f.circle(180, yB, 3, fill=INK)
    f.text(ax + 22, ay - 6, "异或 XOR", fs=10.5, fill=MUTED); f.text(ax + 22, ay + 112, "与 AND", fs=10.5, fill=MUTED)
    f.line(ox1, oy1, ox1 + 40, oy1); f.text(ox1 + 46, oy1 + 5, "和 S", fs=13, weight=700, anchor="start")
    f.line(ox2, oy2, ox1 + 40, oy2); f.text(ox1 + 46, oy2 + 5, "进位 C", fs=13, weight=700, anchor="start")
    truth(f, 430, 196, ["A", "B", "C", "S"], [["0","0","0","0"],["0","1","0","1"],["1","0","0","1"],["1","1","1","0"]], col="purple", cw=30)
    f.text(560, 290, "1 + 1 = 二进制 10", fs=11.5, fill=C["purple"][0], weight=700, anchor="start")
    f.text(560, 306, "进位 1，和 0", fs=11, fill=MUTED, anchor="start")
    return f

@fig
def cpu():
    f = Fig(680, 290, "CPU 的指令循环")
    cx, cy, r = 250, 150, 92
    steps = [("① 取指", "按 PC 地址从内存\n读出下一条指令", "blue", -90), ("② 译码", "看懂指令：做什么、\n操作哪些数据", "purple", 0),
             ("③ 执行", "ALU 计算，\n或跳转、读写内存", "amber", 90), ("④ 写回", "结果存进寄存器，\nPC 指向下一条", "green", 180)]
    f.circle(cx, cy, r, fill="none", stroke="#cbd5e1", sw=10)
    for k in range(4):
        a1 = math.radians(-90 + k * 90 + 18); a2 = math.radians(-90 + (k + 1) * 90 - 18)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        x2, y2 = cx + r * math.cos(a2), cy + r * math.sin(a2)
        f.path(f"M{x1:.1f},{y1:.1f} A{r},{r} 0 0 1 {x2:.1f},{y2:.1f}", stroke="#64748b", sw=2.4)
        f.head(x2, y2, a2 + math.pi / 2, "#64748b", 10)
    for nm, desc, col, ang in steps:
        a = math.radians(ang)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        f.box(x - 52, y - 17, 104, 34, nm, col, fs=13.5, solid=True)
        dx = {-90: (0, -30), 0: (60, 0), 90: (0, 30), 180: (-60, 0)}[ang]
        anchor = "middle" if ang in (-90, 90) else ("start" if ang == 0 else "end")
        rows = desc.split("\n")
        if ang == -90: f.lines(x + 125, y - 6, rows, fs=11, fill="#374151", anchor="start")
        elif ang == 90: f.lines(x + 62, y + 2, rows, fs=11, fill="#374151", anchor="start")
        elif ang == 0: f.lines(x + 58, y - 3, rows, fs=11, fill="#374151", anchor="start")
        else: f.lines(x - 58, y - 3, rows, fs=11, fill="#374151", anchor="end")
    f.text(cx, cy - 4, "每秒循环", fs=12, fill=MUTED); f.text(cx, cy + 16, "数十亿次", fs=15, weight=700, fill=C["blue"][0])
    # memory sidebar
    f.rect(520, 40, 140, 210, fill=C["amber"][1], stroke=C["amber"][0], rx=8)
    f.text(590, 62, "内存", fs=13.5, weight=700, fill=C["amber"][0])
    prog = ["100: LOAD R1, [200]", "101: ADD R1, 5", "102: STORE R1, [201]", "103: JUMP 100", "…", "200: 37", "201: 42"]
    for k, p in enumerate(prog):
        hl = k == 1
        f.rect(530, 74 + k * 24, 120, 20, fill="#fff7ed" if hl else "#fff", stroke=C["amber"][0] if hl else "#e5e7eb", rx=2, sw=1.4 if hl else 0.8)
        f.text(536, 88 + k * 24, p, fs=9.6, anchor="start", mono=True, weight=700 if hl else 400)
    f.text(590, 268, "PC = 101", fs=12, weight=700, fill=C["blue"][0], mono=True)
    f.arrow(440, 98, 526, 98, color=C["blue"][0], dash="4 3")
    return f

@fig
def pipeline():
    f = Fig(680, 280, "五级流水线")
    st = [("取指", "blue"), ("译码", "purple"), ("执行", "amber"), ("访存", "teal"), ("写回", "green")]
    x0, y0, cw, rh = 110, 50, 58, 30
    for c in range(9):
        f.text(x0 + c * cw + cw / 2, y0 - 10, f"周期 {c+1}", fs=10.5, fill=MUTED)
    for i in range(5):
        f.text(x0 - 10, y0 + i * (rh + 6) + 20, f"指令 {i+1}", fs=12, anchor="end", weight=700)
        for k, (nm, col) in enumerate(st):
            c = i + k
            f.box(x0 + c * cw + 2, y0 + i * (rh + 6), cw - 4, rh, nm, col, fs=11.5, weight=700, rx=4)
    xc = x0 + 4 * cw
    f.rect(xc, y0 - 4, cw, 5 * (rh + 6) + 2, fill="none", stroke=C["red"][0], sw=2, rx=4, dash="5 3")
    f.text(xc + cw / 2, y0 + 5 * (rh + 6) + 18, "这一刻 5 条指令同时在不同阶段", fs=11, fill=C["red"][0], weight=700)
    f.text(340, 272, "单条指令仍需 5 个周期，但从第 5 个周期起每个周期都“出厂”一条——吞吐量提高约 5 倍", fs=11, fill=MUTED)
    return f

@fig
def gpu():
    f = Fig(680, 270, "CPU 与 GPU")
    # CPU
    f.rect(30, 40, 280, 190, fill="#f8fafc", stroke=C["blue"][0], sw=1.6, rx=10)
    f.text(170, 30, "CPU：少数“全能”大核", fs=14, weight=700, fill=C["blue"][0])
    for i in range(2):
        for j in range(2):
            f.box(44 + j * 90, 52 + i * 62, 82, 54, "核心", "blue", fs=12, sub="复杂控制\n分支预测", solid=True)
    f.box(228, 52, 70, 116, "大缓存", "amber", fs=12)
    f.box(44, 182, 254, 36, "控制逻辑", "slate", fs=12)
    # GPU
    f.rect(370, 40, 280, 190, fill="#f8fafc", stroke=C["green"][0], sw=1.6, rx=10)
    f.text(510, 30, "GPU：成千上万个简单小核", fs=14, weight=700, fill=C["green"][0])
    for i in range(10):
        for j in range(16):
            f.rect(382 + j * 16.5, 52 + i * 14.5, 13, 11, fill=C["green"][0], stroke="none", rx=1.5)
    f.box(382, 200, 256, 22, "共享缓存 / 显存接口", "amber", fs=11, weight=400, rx=3)
    f.text(170, 254, "擅长：复杂、前后依赖的逻辑", fs=11.5, fill=MUTED)
    f.text(510, 254, "擅长：同一种运算做一百万遍（像素、矩阵）", fs=11.5, fill=MUTED)
    return f

@fig
def memory_hierarchy():
    f = Fig(680, 310, "存储层次")
    lv = [("寄存器", "< 1 ns", "数百字节", "blue"), ("缓存 L1–L3", "1–40 ns", "KB–MB", "purple"),
          ("内存 DRAM", "≈100 ns", "GB", "teal"), ("固态硬盘 SSD", "≈10–100 µs", "TB", "amber"), ("机械硬盘 / 磁带", "≈5–10 ms", "数 TB 起", "slate")]
    cx, top, h = 230, 30, 50
    for i, (nm, lat, cap, col) in enumerate(lv):
        y = top + i * h
        hw1, hw2 = 30 + i * 38, 30 + (i + 1) * 38
        dark, light = C[col]
        f.poly([(cx - hw1, y), (cx + hw1, y), (cx + hw2, y + h - 3), (cx - hw2, y + h - 3)], fill=light, stroke=dark, sw=1.4, closed=True)
        f.text(cx, y + h / 2 + 4, nm, fs=12.5 if i else 11.5, weight=700)
        f.text(450, y + h / 2 + 4, lat, fs=12.5, weight=700, fill=dark, anchor="start")
        f.text(560, y + h / 2 + 4, cap, fs=12, fill="#374151", anchor="start")
    f.text(450, 20, "延迟", fs=11.5, fill=MUTED, anchor="start", weight=700)
    f.text(560, 20, "容量", fs=11.5, fill=MUTED, anchor="start", weight=700)
    f.arrow(30, 270, 30, 40, color=C["red"][0], sw=2)
    f.lines(42, 150, ["更快", "更贵"], fs=11, fill=C["red"][0], anchor="start", weight=700)
    f.text(340, 300, "上下相邻两层速度常差 10–1000 倍；靠局部性，常用数据总在上层", fs=11, fill=MUTED)
    return f

# ------------------------------------------------------------------ 程序与算法
@fig
def algorithm():
    f = Fig(680, 270, "线性查找与二分查找")
    n, x0, cw = 16, 70, 30
    vals = [3, 8, 12, 17, 21, 25, 30, 34, 41, 47, 52, 58, 63, 70, 76, 88]
    target = 63
    def row(y, hl_fn, label, col):
        f.text(x0 - 10, y + 20, label, fs=12.5, weight=700, anchor="end", fill=C[col][0])
        for i, v in enumerate(vals):
            st = hl_fn(i)
            fill = {"done": "#e5e7eb", "hit": C["green"][0], "cur": C[col][1], None: "#fff"}[st]
            f.rect(x0 + i * cw, y, cw - 3, 30, fill=fill, stroke=C["green"][0] if st == "hit" else "#9ca3af", rx=3, sw=1)
            f.text(x0 + i * cw + (cw - 3) / 2, y + 20, str(v), fs=12, weight=700 if st == "hit" else 400, fill="#fff" if st == "hit" else (MUTED if st == "done" else INK))
    f.text(340, 24, f"在有序数组里找 {target}", fs=14, weight=700)
    idx = vals.index(target)
    row(44, lambda i: "hit" if i == idx else ("done" if i < idx else None), "逐个找", "red")
    f.arrow(x0 + 4, 86, x0 + idx * cw + 12, 86, color=C["red"][0], sw=1.8)
    f.text(x0 + idx * cw + 22, 90, f"第 {idx+1} 次才找到", fs=11.5, fill=C["red"][0], anchor="start", weight=700)
    # binary
    lo, hi, steps = 0, n - 1, []
    while lo <= hi:
        mid = (lo + hi) // 2; steps.append((lo, hi, mid))
        if vals[mid] == target: break
        if vals[mid] < target: lo = mid + 1
        else: hi = mid - 1
    y = 116
    for k, (lo, hi, mid) in enumerate(steps):
        yy = y + k * 34
        f.text(x0 - 10, yy + 15, f"第 {k+1} 步", fs=11, anchor="end", fill=C["blue"][0], weight=700)
        f.rect(x0 + lo * cw - 2, yy, (hi - lo + 1) * cw + 1, 24, fill=C["blue"][1], stroke=C["blue"][0], rx=4, sw=1)
        hit = vals[mid] == target
        f.rect(x0 + mid * cw, yy + 2, cw - 3, 20, fill=C["green"][0] if hit else C["blue"][0], stroke="none", rx=3)
        f.text(x0 + mid * cw + (cw - 3) / 2, yy + 16, str(vals[mid]), fs=11, fill="#fff", weight=700)
        msg = "找到！" if hit else (f"{vals[mid]} < {target}，丢掉左半" if vals[mid] < target else f"{vals[mid]} > {target}，丢掉右半")
        f.text(x0 + n * cw + 6, yy + 16, msg, fs=10.5, anchor="start", fill=C["green"][0] if hit else MUTED)
    f.text(340, 262, "16 个元素：逐个找最坏 16 次，二分最多 4 次；100 万个：100 万次 vs 20 次", fs=11.5, weight=700, fill=C["blue"][0])
    return f

@fig
def big_o():
    f = Fig(680, 340, "复杂度增长曲线")
    X0, Y0, W, H = 60, 290, 380, 250
    nmax, ymax = 20, 80
    f.line(X0, Y0, X0 + W, Y0, sw=1.4); f.line(X0, Y0, X0, Y0 - H, sw=1.4)
    f.text(X0 + W, Y0 + 32, "数据规模 n →", fs=11.5, anchor="end", fill=MUTED)
    f.text(X0 - 8, Y0 - H - 8, "步数", fs=11.5, anchor="start", fill=MUTED)
    for t in range(0, nmax + 1, 5):
        f.text(X0 + W * t / nmax, Y0 + 14, str(t), fs=10, fill=MUTED)
    curves = [("O(1)", lambda n: 2, "green"), ("O(log n)", lambda n: math.log2(max(n, 1)) * 2, "teal"),
              ("O(n)", lambda n: n, "blue"), ("O(n log n)", lambda n: n * math.log2(max(n, 1)) / 1.0, "purple"),
              ("O(n²)", lambda n: n * n, "amber"), ("O(2ⁿ)", lambda n: 2 ** n, "red")]
    for k, (nm, fn, col) in enumerate(curves):
        pts = []
        for i in range(0, 401):
            n = 0.5 + i * (nmax - 0.5) / 400
            v = fn(n)
            if v > ymax:
                pts.append((X0 + W * n / nmax, Y0 - H)); break
            pts.append((X0 + W * n / nmax, Y0 - H * v / ymax))
        f.poly(pts, stroke=C[col][0], sw=2.4)
        ex, ey = pts[-1]
        if ey <= Y0 - H + 1: f.text(ex, ey - 6, nm, fs=12, fill=C[col][0], weight=700)
        else: f.text(ex + 5, ey + 4, nm, fs=12, fill=C[col][0], weight=700, anchor="start")
    # table
    tx = 520
    f.text(tx + 70, 50, "n = 100 万时", fs=12.5, weight=700)
    rows = [("O(1)", "1", "green"), ("O(log n)", "≈20", "teal"), ("O(n)", "10⁶", "blue"), ("O(n log n)", "≈2×10⁷", "purple"), ("O(n²)", "10¹²", "amber"), ("O(2ⁿ)", "天文数字", "red")]
    for k, (nm, v, col) in enumerate(rows):
        y = 64 + k * 30
        f.rect(tx, y, 150, 26, fill=C[col][1], stroke=C[col][0], rx=4, sw=0.9)
        f.text(tx + 8, y + 18, nm, fs=11.5, anchor="start", weight=700, fill=C[col][0])
        f.text(tx + 142, y + 18, v, fs=11.5, anchor="end")
    f.text(tx + 75, 268, "电脑每秒约 10⁹ 步：", fs=10.5, fill=MUTED)
    f.text(tx + 75, 284, "n² 要十几分钟，2ⁿ 永远算不完", fs=10.5, fill=MUTED)
    return f

@fig
def graph_algorithms():
    f = Fig(520, 260, "最短路径")
    P = {"A": (60, 130), "B": (180, 50), "C": (210, 200), "D": (340, 120), "E": (460, 160)}
    E = [("A", "B", 2), ("A", "C", 6), ("B", "C", 1), ("B", "D", 5), ("C", "D", 2), ("D", "E", 2), ("C", "E", 5)]
    best = {("A", "B"), ("B", "C"), ("C", "D"), ("D", "E")}
    for a, b, w in E:
        (x1, y1), (x2, y2) = P[a], P[b]
        on = (a, b) in best
        f.line(x1, y1, x2, y2, stroke=C["blue"][0] if on else "#cbd5e1", sw=5 if on else 2)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        f.circle(mx, my, 11, fill="#fff", stroke=C["blue"][0] if on else "#cbd5e1", sw=1)
        f.text(mx, my + 4.5, str(w), fs=12, weight=700, fill=C["blue"][0] if on else MUTED)
    dist = {"A": 0, "B": 2, "C": 3, "D": 5, "E": 7}
    for k, (x, y) in P.items():
        col = "green" if k in "AE" else "blue"
        f.circle(x, y, 20, fill=C[col][0], stroke="#fff", sw=2)
        f.text(x, y + 6, k, fs=16, weight=700, fill="#fff")
        if k == "C": f.text(x - 26, y + 5, f"距 A：{dist[k]}", fs=10.5, fill=C["amber"][0], weight=700, anchor="end")
        else: f.text(x, y - 26, f"距 A：{dist[k]}", fs=10.5, fill=C["amber"][0], weight=700)
    f.text(260, 250, "A → B → C → D → E，总长 2 + 1 + 2 + 2 = 7", fs=12, weight=700, fill=C["blue"][0])
    return f

@fig
def programming_language():
    f = Fig(680, 310, "抽象的阶梯")
    rungs = [("Python", "total = price * qty", "人最容易读", "green"),
             ("C 语言", "int total = price * qty;", "接近硬件，但仍可移植", "teal"),
             ("汇编", "mov eax,[price] ; imul eax,[qty] ; mov [total],eax", "与 CPU 指令一一对应", "purple"),
             ("机器码", "8B 05 …  0F AF 05 …  89 05 …", "CPU 真正执行的数字", "blue"),
             ("电路", "数十亿个晶体管开关：1 = 通，0 = 断", "物理世界", "slate")]
    for i, (nm, code, desc, col) in enumerate(rungs):
        y = 20 + i * 56
        x = 30 + i * 24
        dark, light = C[col]
        f.rect(x, y, 470 - i * 24, 44, fill=light, stroke=dark, rx=6, sw=1.4)
        f.text(x + 12, y + 27, nm, fs=13.5, weight=700, fill=dark, anchor="start")
        f.text(x + 82, y + 27, code, fs=11, anchor="start", mono=True)
        f.text(530, y + 27, desc, fs=11.5, fill="#374151", anchor="start")
        if i < 4:
            f.arrow(x + 40, y + 46, x + 58, y + 56, color=dark, sw=1.6, size=7)
    f.text(20, 305, "↓ 编译器 / 汇编器自动完成每一级翻译；越往上，一行代码能表达的事越多", fs=11.5, fill=C["blue"][0], weight=700, anchor="start")
    return f

@fig
def compiler():
    f = Fig(680, 270, "编译器的阶段")
    st = [("源代码", "x = a + 2 * b", "slate"), ("词法分析", "x  =  a  +  2  *  b\n（切成单词）", "blue"),
          ("语法分析", "语法树", "purple"), ("语义分析", "类型检查：\na、b 都是整数 ✓", "teal"),
          ("优化", "2*b → b+b\n删掉无用代码", "amber"), ("代码生成", "目标 CPU 指令", "green")]
    w, gap, y = 98, 12, 40
    for i, (nm, ex, col) in enumerate(st):
        x = 12 + i * (w + gap)
        f.box(x, y, w, 36, nm, col, fs=12.5, solid=True)
        if i < len(st) - 1:
            f.arrow(x + w + 1, y + 18, x + w + gap - 1, y + 18, size=7)
        dark, light = C[col]
        f.rect(x, y + 46, w, 100, fill=light, stroke=dark, rx=6, sw=0.9)
        if nm == "语法分析":
            # tiny tree
            cx = x + w / 2
            nodes = {"=": (cx, y + 64), "x": (cx - 26, y + 92), "+": (cx + 22, y + 92), "a": (cx + 2, y + 120), "*": (cx + 40, y + 120)}
            for a, b in [("=", "x"), ("=", "+"), ("+", "a"), ("+", "*")]:
                f.line(*nodes[a], *nodes[b], stroke=dark, sw=1)
            for k, (nx, ny) in nodes.items():
                f.circle(nx, ny, 9, fill="#fff", stroke=dark, sw=1); f.text(nx, ny + 4, k, fs=11, mono=True, weight=700)
            f.text(cx + 40, y + 140, "2  b", fs=9, fill=MUTED, mono=True)
        else:
            f.lines(x + w / 2, y + 80, ex.split("\n"), fs=10.5 if nm != "源代码" else 10.2, mono=nm in ("源代码",), fill="#1f2937", lh=1.5)
    f.text(160, 218, "前端：理解语言", fs=12, weight=700, fill=C["purple"][0])
    f.path("M24,200 L24,206 L312,206 L312,200", stroke=C["purple"][0], sw=1.4)
    f.text(510, 218, "后端：适配机器", fs=12, weight=700, fill=C["green"][0])
    f.path("M354,200 L354,206 L668,206 L668,200", stroke=C["green"][0], sw=1.4)
    f.text(340, 250, "LLVM 等框架让“多种语言前端 × 多种 CPU 后端”共用中间的优化器", fs=11.5, fill=MUTED)
    return f

# ------------------------------------------------------------------ 系统软件
@fig
def operating_system():
    f = Fig(680, 320, "操作系统的分层")
    def band(y, h, col, label, items, lab_fs=13):
        dark, light = C[col]
        f.rect(30, y, 620, h, fill=light, stroke=dark, rx=8, sw=1.4)
        f.text(44, y + h / 2 + 5, label, fs=lab_fs, weight=700, fill=dark, anchor="start")
        n = len(items); bw = (480 - (n - 1) * 10) / n
        for k, it in enumerate(items):
            f.box(158 + k * (bw + 10), y + 9, bw, h - 18, it, col, fs=12, weight=400, rx=5)
    band(20, 54, "pink", "应用程序", ["浏览器", "微信", "游戏", "代码编辑器"])
    f.rect(30, 84, 620, 26, fill="#fff", stroke=C["red"][0], rx=4, sw=1.4, dash="5 3")
    f.text(340, 102, "系统调用：open() · read() · write() · fork() …（应用和内核之间唯一的门）", fs=11.5, fill=C["red"][0], weight=700)
    f.rect(30, 120, 620, 106, fill=C["green"][1], stroke=C["green"][0], rx=8, sw=1.6)
    f.text(44, 178, "内核", fs=15, weight=700, fill=C["green"][0], anchor="start")
    ks = [("进程调度", "谁用 CPU"), ("内存管理", "虚拟内存"), ("文件系统", "文件与目录"), ("网络协议栈", "TCP/IP")]
    for k, (a, b) in enumerate(ks):
        f.box(110 + k * 132, 130, 122, 44, a, "green", fs=12.5, sub=b, solid=True)
    f.box(110, 182, 518, 36, "设备驱动程序：把“读一块数据”翻译成具体硬件的命令", "green", fs=11.5, weight=400)
    band(236, 54, "slate", "硬件", ["CPU", "内存", "磁盘 / SSD", "网卡 · 显卡"])
    f.arrow(660, 30, 660, 280, color="#9ca3af", both=True, sw=1.2)
    f.text(340, 312, "应用不能直接碰硬件——必须请内核代办：既保证安全，也让同一程序跑在不同硬件上", fs=11, fill=MUTED)
    return f

@fig
def virtual_memory():
    f = Fig(680, 370, "虚拟内存")
    def proc(x, y, nm, col):
        dark, light = C[col]
        f.text(x + 50, y - 8, nm, fs=12.5, weight=700, fill=dark)
        for k in range(4):
            f.box(x, y + k * 30, 100, 26, f"虚拟页 {k}", col, fs=11.5, weight=400, rx=3)
        return [(x + 100, y + k * 30 + 13) for k in range(4)]
    a = proc(30, 46, "进程 A 看到的内存", "blue")
    b = proc(30, 210, "进程 B 看到的内存", "purple")
    f.box(170, 40, 100, 130, "A 的页表", "blue", fs=12, sub="由 MMU\n硬件自动查", rx=6)
    f.box(170, 204, 100, 130, "B 的页表", "purple", fs=12, sub="与 A 的\n互不相通", rx=6)
    f.text(460, 26, "物理内存", fs=13, weight=700)
    frames = []
    for k in range(8):
        y = 38 + k * 36
        f.rect(410, y, 100, 30, fill="#fff", stroke="#9ca3af", rx=3)
        f.text(460, y + 20, f"页框 {k}", fs=11, fill=MUTED)
        frames.append((410, y + 15))
    f.rect(560, 130, 105, 110, fill=C["slate"][1], stroke=C["slate"][0], rx=6)
    f.text(612, 156, "磁盘", fs=13, weight=700, fill=C["slate"][0]); f.text(612, 176, "（换出的页）", fs=10.5, fill=MUTED)
    f.text(612, 204, "A 的页 3", fs=10.5, fill=C["blue"][0], weight=700); f.text(612, 222, "B 的页 3", fs=10.5, fill=C["purple"][0], weight=700)
    mapA = {0: 2, 1: 5, 2: 0, 3: "disk"}; mapB = {0: 4, 1: 1, 2: 7, 3: "disk"}
    for mp, src, col, nm in ((mapA, a, "blue", "A"), (mapB, b, "purple", "B")):
        for k, dst in mp.items():
            sx, sy = src[k]
            f.line(sx, sy, 170, sy, stroke=C[col][0], sw=1, dash="2 2")
            if dst == "disk":
                f.curve(270, sy, 520, sy + (40 if nm == "A" else -60), 560, 185 + (-15 if nm == "A" else 25), color=C[col][0], sw=1.3, dash="4 3")
            else:
                fx, fy = frames[dst]
                f.arrow(270, sy, fx, fy, color=C[col][0], sw=1.3, size=7)
                f.rect(411, fy - 14, 98, 28, fill=C[col][1], stroke="none", rx=3)
                f.text(460, fy + 4, f"{nm} 的页 {k}", fs=11, fill=C[col][0], weight=700)
    f.text(340, 362, "每个进程都以为自己从地址 0 开始独占内存；实际页面散落各处，甚至暂存在磁盘上", fs=11, fill=MUTED)
    return f

@fig
def virtualization():
    f = Fig(680, 290, "虚拟机与容器")
    def stack(x0, title, col, cols, mid_label, mid_col, guest_os):
        f.text(x0 + 145, 24, title, fs=14, weight=700, fill=C[col][0])
        bw = 280 / cols - 8
        for k in range(cols):
            x = x0 + k * (bw + 8)
            f.box(x, 36, bw, 34, f"应用 {chr(65+k)}", "pink", fs=12)
            f.box(x, 74, bw, 30, "依赖库", "amber", fs=11, weight=400)
            if guest_os:
                f.box(x, 108, bw, 40, "完整的\n操作系统", "purple", fs=10.5)
        y = 152 if guest_os else 110
        f.box(x0, y, 288, 34, mid_label, mid_col, fs=12, solid=True)
        if guest_os:
            f.box(x0, y + 40, 288, 30, "宿主操作系统 / 硬件", "slate", fs=12)
        else:
            f.box(x0, y + 40, 288, 34, "宿主操作系统（共享一个内核）", "slate", fs=12)
            f.box(x0, y + 78, 288, 30, "硬件", "slate", fs=12)
    stack(20, "虚拟机", "purple", 3, "虚拟机监视器 Hypervisor", "purple", True)
    stack(372, "容器", "teal", 4, "容器运行时（如 Docker）", "teal", False)
    f.text(165, 252, "每台约 GB 级 · 启动数十秒到分钟 · 隔离最强", fs=11.5, fill=MUTED)
    f.text(516, 252, "每个约 MB 级 · 启动约秒级 · 更轻更密", fs=11.5, fill=MUTED)
    f.line(340, 30, 340, 260, stroke="#e5e7eb", sw=1.4)
    f.text(340, 282, "共同点：都把“一台机器”切给多个互相隔离的应用", fs=11.5, fill=C["blue"][0], weight=700)
    return f

# ------------------------------------------------------------------ 数据
@fig
def database():
    f = Fig(680, 310, "关系数据库")
    def table(x, y, name, hdr, rows, col, widths, hl=()):
        dark, light = C[col]
        f.text(x, y - 8, name, fs=12.5, weight=700, fill=dark, anchor="start")
        cx = x
        for j, h in enumerate(hdr):
            f.rect(cx, y, widths[j], 22, fill=dark, stroke=dark, rx=0, sw=0.8)
            f.text(cx + widths[j] / 2, y + 15.5, h, fs=11, fill="#fff", weight=700)
            cx += widths[j]
        for r, row in enumerate(rows):
            cx = x
            for j, v in enumerate(row):
                on = r in hl
                f.rect(cx, y + 22 * (r + 1), widths[j], 22, fill="#fef9c3" if on else "#fff", stroke=dark, rx=0, sw=0.6)
                f.text(cx + widths[j] / 2, y + 22 * (r + 1) + 15.5, v, fs=11, weight=700 if on else 400)
                cx += widths[j]
    table(20, 40, "customers 客户表", ["id", "name", "city"], [["1", "王芳", "北京"], ["2", "李雷", "上海"], ["3", "赵敏", "北京"]], "blue", [40, 70, 60], hl=(0, 2))
    table(210, 40, "orders 订单表", ["no", "cust_id", "amount"], [["101", "1", "¥88"], ["102", "2", "¥45"], ["103", "3", "¥120"], ["104", "1", "¥19"]], "amber", [50, 70, 70], hl=(0, 2, 3))
    f.curve(40, 130, 160, 200, 295, 152, color=C["green"][0], sw=1.4, dash="4 3")
    f.text(170, 192, "通过“键”关联：订单的 cust_id 指向客户的 id", fs=10.5, fill=C["green"][0], weight=700)
    # SQL
    f.rect(440, 30, 220, 122, fill="#0f172a", stroke="#0f172a", rx=8)
    sql = ["SELECT c.name, o.amount", "FROM customers c", "JOIN orders o", "  ON o.cust_id = c.id", "WHERE c.city = '北京';"]
    for k, s in enumerate(sql):
        f.text(452, 54 + k * 20, s, fs=10.6, fill="#e2e8f0", anchor="start", mono=True)
    f.text(550, 170, "只说“要什么”，不说“怎么找”", fs=11, fill=MUTED)
    f.arrow(550, 178, 550, 200, color=C["green"][0])
    table(470, 210, "结果", ["name", "amount"], [["王芳", "¥88"], ["赵敏", "¥120"], ["王芳", "¥19"]], "green", [80, 80])
    f.text(20, 236, "数据库替你决定：先查索引、再连表、再过滤——", fs=11, fill=MUTED, anchor="start")
    f.text(20, 254, "十亿行里找几行，也只需几次磁盘读取", fs=11, fill=MUTED, anchor="start")
    return f

@fig
def data_compression():
    f = Fig(520, 290, "哈夫曼编码")
    f.text(260, 22, "原文：AAAAAABBCD（10 个字母）", fs=13, weight=700)
    # tree
    N = {"r": (190, 60, "10"), "A": (110, 120, "A×6"), "n1": (270, 120, "4"), "B": (210, 180, "B×2"), "n2": (330, 180, "2"), "C": (280, 240, "C×1"), "D": (380, 240, "D×1")}
    Ed = [("r", "A", "0"), ("r", "n1", "1"), ("n1", "B", "0"), ("n1", "n2", "1"), ("n2", "C", "0"), ("n2", "D", "1")]
    for a, b, bit in Ed:
        x1, y1, _ = N[a]; x2, y2, _ = N[b]
        f.line(x1, y1, x2, y2, stroke="#94a3b8", sw=1.6)
        f.text((x1 + x2) / 2 + (-10 if x2 < x1 else 10), (y1 + y2) / 2, bit, fs=12, weight=700, fill=C["red"][0])
    for k, (x, y, lab) in N.items():
        leaf = k in "ABCD"
        if leaf:
            f.box(x - 28, y - 15, 56, 30, lab, "blue", fs=12, solid=True, rx=6)
        else:
            f.circle(x, y, 15, fill="#fff", stroke="#94a3b8", sw=1.4); f.text(x, y + 4, lab, fs=11, fill=MUTED)
    # code table
    tx = 400
    rows = [("A", "0"), ("B", "10"), ("C", "110"), ("D", "111")]
    f.text(tx + 50, 56, "编码表", fs=12, weight=700)
    for k, (s, c) in enumerate(rows):
        f.rect(tx, 66 + k * 24, 100, 22, fill="#fff", stroke="#cbd5e1", rx=3)
        f.text(tx + 16, 82 + k * 24, s, fs=12, weight=700, anchor="start")
        f.text(tx + 88, 82 + k * 24, c, fs=12, mono=True, anchor="end", fill=C["red"][0])
    f.text(20, 280, "定长编码：10 × 2 = 20 位　→　哈夫曼：6×1 + 2×2 + 1×3 + 1×3 = 16 位", fs=11.5, weight=700, fill=C["green"][0], anchor="start")
    return f

@fig
def hashing():
    f = Fig(520, 250, "哈希表")
    keys = [("张三", 2), ("李四", 0), ("王五", 2), ("赵六", 4)]
    for k, (nm, b) in enumerate(keys):
        f.box(20, 30 + k * 46, 80, 32, nm, "blue", fs=12.5)
        f.arrow(102, 46 + k * 46, 168, 120, color="#94a3b8", sw=1.1, size=6)
    f.box(170, 92, 110, 56, "哈希函数", "amber", fs=13, sub="h(名字) mod 5", solid=True)
    for i in range(5):
        y = 20 + i * 42
        f.rect(340, y, 44, 34, fill=C["slate"][1], stroke=C["slate"][0], rx=3)
        f.text(362, y + 22, str(i), fs=13, weight=700, fill=C["slate"][0])
        items = [nm for nm, b in keys if b == i]
        for j, nm in enumerate(items):
            col = "red" if len(items) > 1 else "green"
            f.box(394 + j * 60, y + 3, 54, 28, nm, col, fs=11.5, weight=400, rx=4)
        if not items:
            f.line(388, y + 17, 410, y + 17, stroke="#cbd5e1", sw=1, dash="2 2")
    for i in (0, 2, 4):
        f.arrow(282, 120, 338, 37 + i * 42, color=C["amber"][0], sw=1.2, size=6)
    f.text(430, 240, "桶 2 发生“碰撞”：用链表挂在一起", fs=10.5, fill=C["red"][0])
    return f

# ------------------------------------------------------------------ 软件工程
@fig
def version_control():
    f = Fig(520, 200, "Git 分支")
    y1, y2 = 70, 140
    f.text(20, y1 + 5, "main", fs=12.5, weight=700, fill=C["blue"][0], anchor="start")
    f.text(20, y2 + 5, "feature", fs=12.5, weight=700, fill=C["green"][0], anchor="start")
    xs = [100, 170, 240, 380, 450]
    f.line(100, y1, 470, y1, stroke=C["blue"][0], sw=3)
    f.path(f"M170,{y1} C200,{y1} 200,{y2} 230,{y2} L330,{y2} C360,{y2} 360,{y1} 380,{y1}", stroke=C["green"][0], sw=3)
    for x in xs:
        f.circle(x, y1, 9, fill=C["blue"][0], stroke="#fff", sw=2)
    for x in (240, 300):
        f.circle(x, y2, 9, fill=C["green"][0], stroke="#fff", sw=2)
    f.circle(380, y1, 12, fill=C["purple"][0], stroke="#fff", sw=2)
    f.text(170, y1 - 18, "分出分支", fs=11, fill=MUTED)
    f.text(270, y2 + 30, "在分支上提交（不影响主线）", fs=11, fill=C["green"][0])
    f.text(380, y1 - 20, "合并 merge", fs=11.5, weight=700, fill=C["purple"][0])
    f.text(240, y1 - 18, "别人也在提交", fs=10.5, fill=MUTED)
    f.text(260, 194, "每个圆点都是一次“提交”快照：随时可以回到任何一个", fs=11, fill=MUTED)
    return f

@fig
def open_source():
    f = Fig(680, 225, "开源协作流程")
    st = [("原始仓库", "维护者\n负责把关", "slate"), ("① Fork", "复制一份\n到自己名下", "blue"), ("② 修改", "改代码\n提交 commit", "purple"),
          ("③ 合并请求", "Pull Request\n请求合并", "amber"), ("④ 评审", "讨论、测试\n再修改", "teal"), ("⑤ 合并", "进入主线\n人人受益", "green")]
    w, gap, y = 98, 14, 70
    for i, (nm, sub, col) in enumerate(st):
        x = 14 + i * (w + gap)
        f.box(x, y, w, 66, nm, col, fs=13, sub=sub, solid=(i in (0, 5)), sub_fs=10.5)
        if i < len(st) - 1:
            f.arrow(x + w + 1, y + 31, x + w + gap - 1, y + 31, size=7)
    f.path(f"M{14+5*(w+gap)+w/2},{y+64} C{14+5*(w+gap)+w/2},{y+120} {14+w/2},{y+120} {14+w/2},{y+70}", stroke=C["green"][0], sw=1.6, dash="5 3")
    f.head(14 + w / 2, y + 66, -math.pi / 2, C["green"][0], 9)
    f.text(340, y + 140, "新版本发布 → 更多人使用 → 更多人发现问题和贡献改进", fs=11.5, fill=C["green"][0], weight=700)
    f.text(340, 30, "全世界的人都可以参与，但由维护者决定什么进入主线", fs=12.5, weight=700)
    return f

# ------------------------------------------------------------------ 交互与云
@fig
def gui():
    f = Fig(680, 220, "图形界面简史")
    ev = [("1968", "演示之母", "恩格尔巴特：\n鼠标、窗口、超文本", "slate"), ("1973", "施乐 Alto", "第一个完整的\n图形桌面", "blue"),
          ("1984", "Macintosh", "图形界面\n走进大众", "purple"), ("1995", "Windows 95", "开始菜单、任务栏\n普及到亿万人", "amber"),
          ("2007", "iPhone", "多点触控：\n手指直接操作", "green"), ("今天", "对话式界面", "用自然语言\n“说”出需求", "pink")]
    y = 60
    f.line(20, y, 660, y, stroke="#9ca3af", sw=3)
    for i, (yr, nm, desc, col) in enumerate(ev):
        x = 70 + i * 108
        dark, light = C[col]
        f.circle(x, y, 8, fill=dark, stroke="#fff", sw=2)
        f.text(x, y - 16, yr, fs=14, weight=700, fill=dark)
        f.rect(x - 50, y + 20, 100, 104, fill=light, stroke=dark, rx=8, dash="4 3" if yr == "今天" else None)
        f.text(x, y + 44, nm, fs=12.5, weight=700)
        f.lines(x, y + 68, desc.split("\n"), fs=10.5, fill="#374151", lh=1.45)
    f.text(340, 212, "趋势：从“记住命令”到“看见就能点”，再到“说出来就行”", fs=11.5, fill=MUTED)
    return f

@fig
def cloud_computing():
    f = Fig(680, 380, "IaaS / PaaS / SaaS")
    layers = ["应用程序", "数据", "运行环境", "操作系统", "虚拟化", "服务器", "存储", "网络"]
    cols = [("自建机房", 0), ("IaaS", 4), ("PaaS", 6), ("SaaS", 8)]  # number of layers (from bottom) managed by provider
    x0, y0, cw, rh = 120, 50, 130, 30
    for j, (nm, prov) in enumerate(cols):
        x = x0 + j * (cw + 8)
        f.text(x + cw / 2, y0 - 14, nm, fs=14, weight=700)
        for i, lay in enumerate(layers):
            from_bottom = len(layers) - i
            mine = from_bottom > prov
            col = "amber" if mine else "blue"
            f.box(x, y0 + i * (rh + 3), cw, rh, lay, col, fs=11.5, weight=400, solid=not mine, rx=4)
    f.text(x0 - 12, y0 + 2 * (rh + 3), "", fs=1)
    ly = y0 + 8 * (rh + 3) + 12
    f.rect(140, ly, 18, 14, fill=C["amber"][1], stroke=C["amber"][0], rx=2); f.text(164, ly + 12, "你自己管", fs=12, anchor="start")
    f.rect(270, ly, 18, 14, fill=C["blue"][0], stroke=C["blue"][0], rx=2); f.text(294, ly + 12, "云服务商替你管", fs=12, anchor="start")
    exs = ["", "例：租虚拟机", "例：上传代码即运行", "例：网页邮箱、在线文档"]
    for j, e in enumerate(exs):
        f.text(x0 + j * (cw + 8) + cw / 2, ly + 40, e, fs=10.5, fill=MUTED)
    f.text(60, y0 + 18, "离你近", fs=11, fill=MUTED); f.text(60, y0 + 7 * (rh + 3) + 18, "离硬件近", fs=11, fill=MUTED)
    f.arrow(60, y0 + 30, 60, y0 + 7 * (rh + 3) + 2, color="#cbd5e1", both=True)
    return f

@fig
def scientific_computing():
    f = Fig(520, 300, "蒙特卡洛估算 π")
    x0, y0, s = 30, 20, 260
    f.rect(x0, y0, s, s, fill="#fff", stroke=INK, rx=0, sw=1.4)
    f.circle(x0 + s / 2, y0 + s / 2, s / 2, fill=C["blue"][1], stroke=C["blue"][0], sw=1.6)
    rnd = random.Random(9); inside = 0; N = 400
    for _ in range(N):
        u, v = rnd.random(), rnd.random()
        ins = (u - 0.5) ** 2 + (v - 0.5) ** 2 <= 0.25
        inside += ins
        f.circle(x0 + u * s, y0 + v * s, 2.1, fill=C["blue"][0] if ins else C["red"][0], stroke="none", sw=0)
    est = 4 * inside / N
    tx = 320
    f.text(tx, 50, "随机撒 400 个点", fs=13, weight=700, anchor="start")
    f.text(tx, 80, f"圆内（蓝）：{inside} 个", fs=12, fill=C["blue"][0], anchor="start", weight=700)
    f.text(tx, 102, f"圆外（红）：{N - inside} 个", fs=12, fill=C["red"][0], anchor="start", weight=700)
    f.text(tx, 140, "圆面积 / 正方形面积 = π / 4", fs=11.5, anchor="start")
    f.text(tx, 170, f"π ≈ 4 × {inside} / {N} = {est:.2f}", fs=13, anchor="start", weight=700, fill=C["green"][0])
    f.lines(tx, 210, ["点越多越准：", "误差约按 1/√N 缩小"], fs=11, fill=MUTED, anchor="start")
    return f

@fig
def halting_problem():
    f = Fig(520, 290, "停机问题")
    f.box(20, 30, 180, 60, "假想的判定程序 H", "slate", fs=12.5, sub="输入任意程序，\n回答“会停”或“不停”", sub_fs=10.5)
    f.rect(240, 20, 260, 190, fill=C["purple"][1], stroke=C["purple"][0], rx=10, sw=1.4)
    f.text(370, 42, "“唱反调”程序 D", fs=13.5, weight=700, fill=C["purple"][0])
    f.box(270, 56, 200, 34, "先问 H：“我 D 会停吗？”", "slate", fs=11.5, weight=400)
    f.arrow(200, 60, 268, 72, color=C["slate"][0], sw=1.2, size=7)
    f.box(256, 120, 110, 70, "H 说“会停”", "red", fs=11.5, sub="→ D 就进入\n死循环", sub_fs=10.5)
    f.box(376, 120, 110, 70, "H 说“不停”", "red", fs=11.5, sub="→ D 立刻\n停止", sub_fs=10.5)
    f.arrow(340, 92, 312, 118, color=C["purple"][0], sw=1.2, size=7); f.arrow(400, 92, 430, 118, color=C["purple"][0], sw=1.2, size=7)
    f.rect(40, 226, 440, 50, fill="#fff", stroke=C["red"][0], rx=8, sw=1.6)
    f.text(260, 246, "无论 H 怎么回答都是错的 → 矛盾", fs=13, weight=700, fill=C["red"][0])
    f.text(260, 266, "所以“万能判定程序”H 根本不可能存在（图灵，1936）", fs=11, fill=INK)
    return f

@fig
def p_vs_np():
    f = Fig(520, 290, "P 与 NP")
    f.path("M30,145 C30,40 450,40 450,145 C450,250 30,250 30,145 Z", stroke=C["blue"][0], sw=1.8, fill=C["blue"][1])
    f.text(240, 92, "NP：答案容易验证", fs=13.5, weight=700, fill=C["blue"][0])
    f.path("M60,160 C60,110 230,110 230,160 C230,210 60,210 60,160 Z", stroke=C["green"][0], sw=1.6, fill=C["green"][1])
    f.text(145, 145, "P：容易求解", fs=13, weight=700, fill=C["green"][0])
    f.lines(145, 168, ["排序 · 最短路径", "查找 · 判断素数"], fs=10.5, fill="#374151")
    f.path("M300,95 C390,100 425,130 420,160 C412,195 360,215 300,205 C330,180 330,120 300,95 Z", stroke=C["red"][0], sw=1.6, fill=C["red"][1])
    f.text(372, 130, "NP 完全", fs=12.5, weight=700, fill=C["red"][0])
    f.lines(370, 152, ["旅行商", "排课 · 数独", "背包问题"], fs=10.5, fill="#374151")
    f.text(240, 268, "百万美元之问：P 和 NP 其实是同一个圈吗？多数人认为不是（P ≠ NP）", fs=11.5, weight=700, fill=INK)
    f.text(490, 30, "大圈之外还有更难的：例如停机问题根本不可计算", fs=10.5, fill=MUTED, anchor="end")
    return f

def main():
    only = set(sys.argv[1:])
    for name, fn in FIGS.items():
        if only and name not in only: continue
        fn().save(OUT / f"{name}.svg")
    print("wrote", len(FIGS) if not only else len(only), "figures to", OUT)

if __name__ == "__main__":
    main()
