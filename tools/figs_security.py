#!/usr/bin/env python3
"""Diagrams for 第 13 篇「安全与国防」 -> assets/figs/security/*.svg  (conceptual, non-operational)"""
from __future__ import annotations
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from svgkit import Fig, C, INK, MUTED, tw
from mapkit_d11_17 import concept_map as cmap

OUT = Path(__file__).resolve().parents[1] / "assets" / "figs" / "security"
FIGS = {}
def fig(fn):
    FIGS[fn.__name__.replace("_", "-")] = fn; return fn

@fig
def concept_map():
    return cmap("安全与国防", "从上往下读：火力与机动 → 核与导弹 → 看见与隐藏 → 信息战场。每一种矛都催生了新的盾。",
        [("火力与机动：工业化的战争", "red", ["线膛枪与后装枪", "机枪", "突击步枪", "现代炸药", "无烟火药", "坦克", "化学武器", "防弹衣"]),
         ("海空力量", "blue", ["铁甲舰与无畏舰", "鱼雷", "潜艇", "航空母舰", "战斗机"]),
         ("核与导弹：毁灭与威慑", "amber", ["核武器", "氢弹", "洲际弹道导弹", "巡航导弹", "精确制导武器", "导弹防御", "高超声速武器", "核不扩散", "生物武器"]),
         ("看见与隐藏：传感器战争", "teal", ["雷达", "声呐", "预警机", "隐身技术", "夜视", "电子战", "军用无人机", "定向能武器", "视频监控"]),
         ("信息战场：密码与网络安全", "purple", ["恩尼格玛与密码破译", "密码学", "对称加密", "公钥密码", "RSA 算法", "数字签名与证书", "身份认证", "生物识别", "端到端加密", "网络安全", "恶意软件", "勒索软件", "漏洞与零日攻击", "防火墙", "零信任架构", "震网病毒", "网络钓鱼与社会工程"])],
        [("1849", "米涅弹"), ("1867", "达纳炸药"), ("1884", "马克沁机枪"), ("1906", "无畏舰"), ("1916", "坦克"),
         ("1932", "破解恩尼格玛"), ("1935", "雷达演示"), ("1945", "首次核试验"), ("1957", "洲际导弹"), ("1968", "核不扩散条约"),
         ("1976", "公钥密码"), ("1988", "莫里斯蠕虫"), ("2010", "震网病毒"), ("2017", "WannaCry")],
        [("根原理", "amber", ["电磁波与回波", "质能等价", "动量与弹道", "单向函数", "反馈控制"]),
         ("攻防循环", "red", ["机枪 → 坦克", "轰炸机 → 雷达", "雷达 → 隐身", "加密 → 破译", "漏洞 → 补丁"]),
         ("本篇的边界", "slate", ["只讲原理与历史", "不涉及制造与使用", "军控条约同样是技术史"])],
        ["喷气发动机、火箭 → 第 8、9 篇　磁控管、相控阵 → 第 2 篇「电与电子」　核裂变与浓缩 → 第 1 篇",
         "哈希与 HTTPS → 第 4 篇「互联网与通信」　量子计算对密码的威胁 → 第 17 篇「量子与前沿」"],
        arrow="down", center_note="↓ 从拼火力到拼信息：今天最激烈的攻防往往发生在看不见的地方")

@fig
def radar():
    f = Fig(680, 300, "雷达测距与测速")
    # antenna
    ax, ay = 70, 200
    f.path(f"M{ax-30},{ay-30} Q{ax},{ay+10} {ax+30},{ay-30}", stroke=INK, sw=2.4)
    f.line(ax, ay - 12, ax, ay + 40, stroke=INK, sw=2)
    f.line(ax - 24, ay + 40, ax + 24, ay + 40, stroke=INK, sw=2)
    f.text(ax, ay + 60, "雷达天线", fs=12, weight=700)
    # target plane
    tx, ty = 470, 90
    f.poly([(tx + 40, ty), (tx - 40, ty), (tx - 50, ty - 4), (tx - 40, ty - 8), (tx + 40, ty - 8)], fill=C["slate"][1], stroke=C["slate"][0], closed=True)
    f.poly([(tx + 6, ty - 8), (tx - 10, ty - 30), (tx - 18, ty - 8)], fill=C["slate"][1], stroke=C["slate"][0], closed=True)
    f.text(tx, ty + 22, "目标", fs=12, weight=700)
    # outgoing pulse (wavy) and echo
    def wave(x1, y1, x2, y2, col, n=9, amp=6):
        L = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / L, (y2 - y1) / L; px, py = -uy, ux
        pts = []
        for i in range(121):
            s = L * i / 120
            a = amp * math.sin(2 * math.pi * n * i / 120)
            pts.append((x1 + ux * s + px * a, y1 + uy * s + py * a))
        f.poly(pts, stroke=col, sw=1.8)
    wave(ax + 20, ay - 40, tx - 60, ty + 4, C["blue"][0])
    f.arrow(tx - 70, ty + 6, tx - 56, ty + 2, color=C["blue"][0], sw=2, size=9)
    wave(tx - 60, ty + 30, ax + 40, ay - 22, C["red"][0], n=12, amp=4)
    f.arrow(ax + 52, ay - 26, ax + 38, ay - 20, color=C["red"][0], sw=2, size=9)
    f.text(250, 112, "发射脉冲", fs=12, weight=700, fill=C["blue"][0])
    f.text(300, 186, "反射回波", fs=12, weight=700, fill=C["red"][0])
    f.arrow(tx + 110, ty - 4, tx + 60, ty - 4, color=C["slate"][0], sw=1.8, size=8)
    f.text(tx + 85, ty - 14, "飞近", fs=11, fill=C["slate"][0])
    # formulas
    f.rect(400, 160, 270, 120, fill=C["amber"][1], stroke=C["amber"][0], rx=10)
    f.text(535, 184, "两个读数", fs=13, weight=700, fill=C["amber"][0])
    f.text(414, 210, "距离 d = c × t ÷ 2", fs=13, anchor="start", weight=700)
    f.text(414, 228, "t 是往返时间；1 微秒 ≈ 150 米", fs=11, anchor="start", fill="#374151")
    f.text(414, 252, "速度：多普勒频移", fs=13, anchor="start", weight=700)
    f.text(414, 270, "目标靠近 → 回波频率升高", fs=11, anchor="start", fill="#374151")
    f.text(200, 292, "方位：天线指向哪里，回波就来自哪里", fs=11, fill=MUTED)
    return f

@fig
def nuclear_weapon():
    f = Fig(680, 320, "链式反应：k 的大小决定一切")
    def gen_tree(x0, y0, k_branch, gens, col, w):
        # draws generations as columns of dots
        counts = []
        n = 1
        for g in range(gens):
            counts.append(n); n = n * k_branch
        for g, c in enumerate(counts):
            x = x0 + g * w
            for j in range(c):
                yy = y0 + (j - (c - 1) / 2) * (min(16, 120 / max(c, 1)))
                f.circle(x, yy, 4.2 if c < 9 else 3.2, fill=col, stroke="#fff", sw=0.6)
        return counts
    # left: reactor k=1
    f.text(170, 34, "反应堆：k ≈ 1", fs=15, weight=700, fill=C["blue"][0])
    f.rect(20, 50, 300, 170, fill=C["blue"][1], stroke=C["blue"][0], rx=10)
    for g in range(6):
        x = 50 + g * 50
        f.circle(x, 135, 6, fill=C["blue"][0], stroke="#fff")
        if g < 5:
            f.arrow(x + 8, 135, x + 40, 135, color=C["blue"][0], sw=1.6, size=7)
            # absorbed extra neutrons
            f.line(x + 6, 129, x + 18, 108, stroke="#94a3b8", sw=1.2, dash="3,3")
            f.text(x + 22, 104, "×", fs=11, fill=MUTED)
    f.text(170, 76, "多余的中子被控制棒吸收或逃逸", fs=11, fill=MUTED)
    f.text(170, 180, "每代 1 次裂变 → 功率平稳", fs=12, weight=700)
    f.text(170, 202, "可连续运行数年发电", fs=11, fill="#374151")
    # right: k>1
    f.text(510, 34, "核武器：k 远大于 1", fs=15, weight=700, fill=C["red"][0])
    f.rect(350, 50, 320, 170, fill=C["red"][1], stroke=C["red"][0], rx=10)
    counts = gen_tree(380, 130, 2, 6, C["red"][0], 52)
    for g, c in enumerate(counts):
        f.text(380 + g * 52, 210, str(c), fs=11, weight=700, fill=C["red"][0])
    f.text(510, 70, "裂变数每代翻倍（指数增长）", fs=11, fill=MUTED)
    # bottom notes
    f.rect(20, 236, 650, 72, fill="#f9fafb", stroke="#d1d5db", rx=8)
    f.text(345, 258, "一次裂变释放约 2 亿电子伏特；每一代只需极短时间，几十代后能量在瞬间释放", fs=11.5)
    f.text(345, 278, "同样的物理，两种用法：差别在材料浓度与“k”是否被控制", fs=11.5, weight=700)
    f.text(345, 297, "（示意图，只表达指数增长的概念，不代表任何具体设计）", fs=10.5, fill=MUTED)
    return f

@fig
def enigma_codebreaking():
    f = Fig(520, 230, "恩尼格玛的信号路径")
    xs = [("键盘", 30, "slate"), ("接线板", 120, "amber"), ("转子 1", 210, "blue"), ("转子 2", 280, "blue"), ("转子 3", 350, "blue"), ("反射器", 430, "purple")]
    for name, x, col in xs:
        w = 60 if name.startswith("转子") else 70
        f.box(x, 50, w, 90, name, col, fs=12)
    # forward path
    y1, y2 = 78, 116
    f.arrow(100, y1, 120, y1, color=C["red"][0], sw=2, size=7)
    for a, b in ((190, 210), (270, 280), (340, 350), (410, 430)):
        f.arrow(a, y1, b, y1, color=C["red"][0], sw=2, size=7)
    f.path(f"M465,{y1} L480,{y1} L480,{y2} L465,{y2}", stroke=C["red"][0], sw=2)
    for a, b in ((430, 410), (350, 340), (280, 270), (210, 190), (120, 100)):
        f.arrow(a, y2, b, y2, color=C["teal"][0], sw=2, size=7)
    f.text(255, 36, "去程（红）→ 反射器折返 → 回程（绿）", fs=11.5, weight=700)
    f.text(65, 160, "按下 A", fs=11, fill=C["red"][0], weight=700)
    f.text(65, 176, "灯亮 R", fs=11, fill=C["teal"][0], weight=700)
    f.path("M210,152 Q245,170 280,152", stroke=C["blue"][0], sw=1.6)
    f.arrow(276, 155, 282, 151, color=C["blue"][0], sw=1.6, size=6)
    f.text(320, 170, "每按一键，转子转一格 → 规则改变", fs=11, fill=C["blue"][0], weight=700, anchor="start")
    f.text(260, 210, "反射器带来致命弱点：任何字母都不会被加密成它自己", fs=11, fill=MUTED)
    return f

@fig
def cryptography():
    f = Fig(680, 300, "密码学的基本场景")
    f.box(30, 60, 100, 56, "Alice", "blue", fs=15, sub="发送方", solid=False)
    f.box(550, 60, 100, 56, "Bob", "green", fs=15, sub="接收方")
    f.box(290, 170, 100, 52, "Eve", "red", fs=15, sub="窃听者")
    f.box(170, 66, 80, 44, "加密", "amber", fs=13, solid=True)
    f.box(430, 66, 80, 44, "解密", "amber", fs=13, solid=True)
    f.arrow(130, 88, 168, 88, color=INK, sw=1.8)
    f.arrow(250, 88, 428, 88, color=INK, sw=1.8)
    f.arrow(510, 88, 548, 88, color=INK, sw=1.8)
    f.text(150, 52, "明文", fs=11, fill=MUTED); f.text(530, 52, "明文", fs=11, fill=MUTED)
    f.text(340, 78, "密文：x7#Qf…", fs=12, weight=700, fill=C["purple"][0], mono=True)
    f.arrow(340, 92, 340, 166, color=C["red"][0], sw=1.6, dash="4,3")
    f.text(352, 154, "截获的只是乱码", fs=11, fill=C["red"][0], anchor="start")
    f.text(210, 128, "密钥", fs=11, weight=700, fill=C["amber"][0]); f.text(470, 128, "密钥", fs=11, weight=700, fill=C["amber"][0])
    rows = [("保密性", "别人看不懂", "加密", "blue"), ("完整性", "改动会被发现", "哈希、MAC", "teal"), ("真实性", "确认是谁发的", "数字签名、证书", "purple")]
    for k, (a, b, c, col) in enumerate(rows):
        x = 30 + k * 220
        f.rect(x, 240, 200, 50, fill=C[col][1], stroke=C[col][0], rx=8)
        f.text(x + 100, 260, a + "：" + b, fs=12, weight=700, fill=C[col][0])
        f.text(x + 100, 280, "工具：" + c, fs=11)
    return f

@fig
def public_key_crypto():
    f = Fig(680, 340, "公钥密码的两个直观类比")
    # top: padlock analogy
    f.text(340, 26, "① 挂锁：人人能锁，只有主人能开", fs=13.5, weight=700, fill=C["blue"][0])
    def lock(x, y, col, open_=True):
        f.rect(x - 16, y, 32, 26, fill=C[col][1], stroke=C[col][0], sw=1.6, rx=4)
        if open_:
            f.path(f"M{x-10},{y} L{x-10},{y-12} Q{x-10},{y-24} {x},{y-24} Q{x+10},{y-24} {x+10},{y-12} L{x+10},{y-16}", stroke=C[col][0], sw=2.4)
        else:
            f.path(f"M{x-10},{y} L{x-10},{y-12} Q{x-10},{y-24} {x},{y-24} Q{x+10},{y-24} {x+10},{y-12} L{x+10},{y}", stroke=C[col][0], sw=2.4)
    lock(90, 74, "green", True)
    f.text(90, 120, "Bob 公开发放", fs=11); f.text(90, 136, "打开的锁（公钥）", fs=11, weight=700)
    f.arrow(130, 86, 200, 86, color=INK, sw=1.6)
    f.rect(210, 66, 60, 40, fill="#fef3c7", stroke=C["amber"][0], rx=4); f.text(240, 91, "信", fs=12)
    lock(290, 74, "green", False)
    f.text(260, 128, "Alice 放信、扣上锁", fs=11)
    f.arrow(320, 86, 420, 86, color=INK, sw=1.6, label="公开传送", fs=11)
    lock(470, 74, "green", False)
    f.circle(560, 86, 10, fill=C["amber"][0], stroke=INK); f.line(570, 86, 600, 86, stroke=INK, sw=3)
    f.text(520, 128, "只有 Bob 手里的钥匙（私钥）能打开", fs=11, weight=700)
    # bottom: paint mixing DH
    f.line(20, 150, 660, 150, stroke="#e5e7eb", sw=1)
    f.text(340, 176, "② 混颜料：迪菲—赫尔曼密钥交换", fs=13.5, weight=700, fill=C["purple"][0])
    def blob(x, y, col, label):
        f.circle(x, y, 16, fill=col, stroke=INK, sw=1)
        f.text(x, y + 32, label, fs=10.5)
    Y = 220
    pub, a_sec, b_sec = "#fde68a", "#f87171", "#60a5fa"
    mixA, mixB, final = "#fb923c", "#a3e635", "#a16207"
    blob(60, Y, pub, "公共色"); blob(120, Y, a_sec, "A 的秘密色")
    f.arrow(140, Y, 175, Y, color=INK, sw=1.4); blob(200, Y, mixA, "混合后公开")
    blob(620, Y, pub, "公共色"); blob(560, Y, b_sec, "B 的秘密色")
    f.arrow(540, Y, 505, Y, color=INK, sw=1.4); blob(480, Y, mixB, "混合后公开")
    f.arrow(220, Y - 6, 460, Y - 6, color=C["slate"][0], sw=1.4, both=True)
    f.text(340, Y - 14, "交换混合色（Eve 也能看到）", fs=10.5, fill=MUTED)
    f.arrow(200, Y + 40, 300, 292, color=INK, sw=1.2); f.arrow(480, Y + 40, 380, 292, color=INK, sw=1.2)
    f.circle(340, 300, 18, fill=final, stroke=INK)
    f.text(340, 332, "各自再加入自己的秘密色 → 得到同一种颜色（共享密钥）", fs=11, weight=700)
    f.text(130, 300, "混合容易", fs=11, fill=C["green"][0], weight=700)
    f.text(550, 300, "分离极难", fs=11, fill=C["red"][0], weight=700)
    return f

@fig
def cybersecurity():
    f = Fig(680, 290, "纵深防御：瑞士奶酪模型")
    layers = [("人员培训", "teal"), ("身份认证", "blue"), ("防火墙/网络分段", "purple"), ("补丁与终端防护", "green"), ("备份与监测", "amber")]
    holes = [[50, 150], [100, 150], [70, 150], [30, 150], [110, 150]]
    for k, (name, col) in enumerate(layers):
        x = 150 + k * 92
        f.poly([(x, 50), (x + 26, 40), (x + 26, 220), (x, 230)], fill=C[col][1], stroke=C[col][0], sw=1.4, closed=True)
        for hy in holes[k]:
            f.circle(x + 13, hy + 30, 9, fill="#fff", stroke=C[col][0], sw=1)
        f.text(x + 13, 252, name, fs=10.5, weight=700, fill=C[col][0])
    # threat arrow aligned through y=180 hole (index pattern)
    f.text(70, 120, "攻击", fs=13, weight=700, fill=C["red"][0])
    f.arrow(40, 130, 140, 160, color=C["red"][0], sw=2.2)
    # blocked attempts
    f.arrow(90, 120, 156, 120, color="#9ca3af", sw=1.6)
    f.arrow(90, 80, 246, 80, color="#9ca3af", sw=1.6, dash="4,3")
    f.text(200, 34, "多数攻击被某一层挡住", fs=10.5, fill=MUTED, anchor="start")
    # passing attack through aligned holes y=180
    f.arrow(140, 180, 610, 180, color=C["red"][0], sw=2, dash="6,4")
    f.text(640, 176, "孔恰好", fs=11, fill=C["red"][0], weight=700)
    f.text(640, 192, "对齐才失守", fs=11, fill=C["red"][0], weight=700)
    f.text(340, 280, "没有哪一层是完美的；层数越多、各层越不相关，全部失守的概率越小（概率相乘）", fs=11, fill=MUTED)
    return f

def main():
    only = set(sys.argv[1:])
    for name, fn in FIGS.items():
        if only and name not in only: continue
        fn().save(OUT / f"{name}.svg")
    print("wrote", len(only or FIGS), "figures to", OUT)

if __name__ == "__main__":
    main()
