#!/usr/bin/env python3
"""Diagrams for 第 14 篇「金融与商业科技」 -> assets/figs/fintech/*.svg"""
from __future__ import annotations
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from svgkit import Fig, C, INK, MUTED, tw
from mapkit_d11_17 import concept_map as cmap

OUT = Path(__file__).resolve().parents[1] / "assets" / "figs" / "fintech"
FIGS = {}
def fig(fn):
    FIGS[fn.__name__.replace("_", "-")] = fn; return fn

@fig
def concept_map():
    return cmap("金融与商业科技", "从上往下读：先让商品能被机器读出，再让钱跟着信息跑，最后用算法撮合交易、用密码学记账。",
        [("商业基础设施：让商品可被机器读取", "slate", ["收银机", "股票报价机", "条形码", "二维码", "自动售货机", "POS 终端", "电子数据交换", "自助收银", "钞票防伪"]),
         ("银行与支付：钱跟着信息跑", "blue", ["信用卡", "银行卡清算网络", "ATM", "芯片卡", "SWIFT", "银行电子化", "清算与结算", "网上银行", "在线支付", "移动支付", "M-Pesa", "实时支付", "开放银行"]),
         ("风险与信用：用数据判断人", "teal", ["信用评分", "风控与反欺诈"]),
         ("交易市场：算法撮合与定价", "purple", ["电子交易", "量化金融", "高频交易", "智能投顾", "众筹与网贷"]),
         ("加密货币与区块链：不靠中心记账", "amber", ["比特币", "区块链", "工作量证明/权益证明", "智能合约", "稳定币", "DeFi", "NFT", "央行数字货币"])],
        [("1867", "股票报价机"), ("1879", "收银机"), ("1950", "大来卡"), ("1959", "ERMA 读支票"), ("1967", "第一台 ATM"),
         ("1971", "纳斯达克"), ("1973", "期权定价公式"), ("1974", "首次扫码"), ("1977", "SWIFT 上线"), ("1994", "QR 码 · EMV"),
         ("2007", "M-Pesa"), ("2009", "比特币"), ("2011", "扫码支付"), ("2015", "以太坊"), ("2016", "印度 UPI")],
        [("根原理", "amber", ["信息与编码", "标准与互操作", "网络效应", "单向函数", "激励与博弈", "概率与统计"]),
         ("同一个问题", "red", ["陌生人之间", "如何互相信任？", "银行、卡组织、平台", "或者共识算法"]),
         ("一组数字", "slate", ["刷卡授权：一两秒", "比特币上限 2100 万", "UPI：每月上百亿笔"])],
        ["哈希与公钥密码 → 第 13 篇「安全与国防」　电子商务、API、平台经济 → 第 4 篇「互联网与通信」",
         "智能手机与 NFC → 第 2 篇「电与电子」　风控与推荐的机器学习 → 第 5 篇「人工智能」"],
        arrow="down", center_note="↓ 记账工具在变，核心问题始终是信任")

L = ["0001101","0011001","0010011","0111101","0100011","0110001","0101111","0111011","0110111","0001011"]
G = ["0100111","0110011","0011011","0100001","0011101","0111001","0000101","0010001","0001001","0010111"]
R = ["1110010","1100110","1101100","1000010","1011100","1001110","1010000","1000100","1001000","1110100"]
PAR = ["LLLLLL","LLGLGG","LLGGLG","LLGGGL","LGLLGG","LGGLLG","LGGGLL","LGLGLG","LGLGGL","LGGLGL"]

@fig
def barcode():
    f = Fig(520, 230, "EAN-13 条码结构")
    body = "690123456789"
    s = sum(int(c) * (3 if i % 2 else 1) for i, c in enumerate(body)); chk = (10 - s % 10) % 10
    code = body + str(chk)
    first, left, right = int(code[0]), code[1:7], code[7:]
    bits = [("101", "guard")]
    for d, p in zip(left, PAR[first]):
        bits.append(((L if p == "L" else G)[int(d)], "left"))
    bits.append(("01010", "guard"))
    for i, d in enumerate(right):
        bits.append((R[int(d)], "chk" if i == 5 else "right"))
    bits.append(("101", "guard"))
    x0, mw, y0 = 70, 3.4, 40
    x = x0
    seg_x = []
    for b, kind in bits:
        sx = x
        for c in b:
            if c == "1":
                h = 120 if kind == "guard" else 108
                col = C["red"][0] if kind == "chk" else INK
                f.rect(x, y0, mw, h, fill=col, stroke="none", sw=0, rx=0)
            x += mw
        seg_x.append((sx, x, kind))
    # digits
    f.text(x0 - 12, y0 + 122, code[0], fs=14, mono=True)
    k = 0
    for (sx, ex, kind) in seg_x:
        if kind in ("left", "right", "chk"):
            k += 1
            f.text((sx + ex) / 2, y0 + 124, code[k], fs=14, mono=True, fill=C["red"][0] if kind == "chk" else INK, weight=700 if kind == "chk" else 400)
    xe = x
    # labels
    g = [s for s in seg_x if s[2] == "guard"]
    for (sx, ex, _), lab in zip(g, ["起始符", "中间分隔", "终止符"]):
        f.arrow((sx + ex) / 2, 22, (sx + ex) / 2, 36, color=C["blue"][0], sw=1.2, size=5)
        f.text((sx + ex) / 2, 18, lab, fs=10.5, fill=C["blue"][0], weight=700)
    f.text(x0 - 12, 196, "前 3 位：国家/地区前缀（690–699 为中国）", fs=11, anchor="start")
    f.text(x0 - 12, 214, "中间：厂商代码 + 商品代码　最后一位：校验码", fs=11, anchor="start")
    rx = xe + 24
    f.rect(rx, 44, 520 - rx - 8, 112, fill=C["amber"][1], stroke=C["amber"][0], rx=8)
    f.text(rx + (520 - rx - 8) / 2, 64, "1 位 = 7 个模块", fs=11.5, weight=700, fill=C["amber"][0])
    f.text(rx + 10, 86, "两黑两白四段", fs=11, anchor="start")
    f.text(rx + 10, 104, "宽度组合不同", fs=11, anchor="start")
    f.text(rx + 10, 126, "校验：奇偶位", fs=11, anchor="start")
    f.text(rx + 10, 144, "加权求和取余", fs=11, anchor="start")
    return f

@fig
def credit_card():
    f = Fig(520, 250, "四方模式")
    pos = {"持卡人": (30, 30, "blue"), "商户": (370, 30, "green"), "发卡行": (30, 170, "purple"), "收单行": (370, 170, "teal")}
    for k, (x, y, col) in pos.items():
        f.box(x, y, 120, 46, k, col, fs=14)
    f.box(200, 100, 120, 50, "卡组织", "amber", fs=14, sub="Visa · 银联…", solid=False)
    f.arrow(150, 53, 368, 53, color=INK, sw=1.8, label="① 刷卡", fs=11)
    f.arrow(430, 76, 430, 168, color=INK, sw=1.8)
    f.text(436, 126, "② 请求授权", fs=11, anchor="start")
    f.arrow(368, 182, 322, 140, color=INK, sw=1.8)
    f.arrow(200, 140, 152, 182, color=INK, sw=1.8)
    f.text(160, 204, "③ 转给发卡行", fs=10.5, anchor="start")
    f.arrow(90, 168, 90, 78, color=C["red"][0], sw=1.6, dash="5,3")
    f.text(84, 126, "④ 查额度", fs=11, anchor="end", fill=C["red"][0])
    f.text(84, 142, "批准/拒绝", fs=11, anchor="end", fill=C["red"][0])
    f.text(260, 236, "批准信息原路返回；资金在日终清算时由发卡行 → 收单行 → 商户", fs=11, fill=MUTED)
    return f

@fig
def mobile_payment():
    f = Fig(680, 340, "扫码支付")
    f.box(20, 40, 110, 52, "顾客手机", "blue", fs=13, sub="支付 App")
    f.box(20, 210, 110, 52, "商户", "green", fs=13, sub="一张收款码")
    f.box(210, 125, 130, 56, "支付机构", "amber", fs=13, sub="余额 / 绑卡")
    f.box(210, 260, 130, 50, "清算平台", "slate", fs=13, sub="网联、银联")
    f.box(20, 280, 110, 44, "银行账户", "purple", fs=12)
    # QR code icon
    qx, qy = 60, 150
    import random
    random.seed(4)
    f.rect(qx - 2, qy - 2, 34, 34, fill="#fff", stroke=INK, sw=1, rx=1)
    for i in range(8):
        for j in range(8):
            if random.random() < 0.5: f.rect(qx + i * 3.75, qy + j * 3.75, 3.75, 3.75, fill=INK, stroke="none", sw=0, rx=0)
    for cx, cy in ((qx, qy), (qx + 22.5, qy), (qx, qy + 22.5)):
        f.rect(cx, cy, 7.5, 7.5, fill="#fff", stroke=INK, sw=1.6, rx=0)
    f.arrow(75, 94, 75, 146, color=C["blue"][0], sw=1.8)
    f.text(84, 124, "① 扫码", fs=11, anchor="start", fill=C["blue"][0], weight=700)
    f.arrow(130, 70, 208, 140, color=INK, sw=1.8)
    f.text(176, 92, "② 发起付款", fs=11, anchor="start")
    f.arrow(275, 183, 275, 258, color=C["purple"][0], sw=1.6, both=True)
    f.text(282, 228, "③ 扣款与结算", fs=11, anchor="start", fill=C["purple"][0])
    f.arrow(210, 285, 132, 300, color=C["purple"][0], sw=1.4, both=True)
    f.arrow(208, 168, 130, 226, color=C["green"][0], sw=1.8)
    f.text(186, 214, "④ 到账通知", fs=11, anchor="start", fill=C["green"][0])
    f.text(180, 26, "整个过程约 1–3 秒", fs=11.5, weight=700, fill=MUTED)
    # right: two-sided network effect
    cx, cy = 535, 170
    f.text(cx, 34, "双边网络效应", fs=14, weight=700, fill=C["red"][0])
    f.box(cx - 60, 56, 120, 46, "更多用户", "blue", fs=13, solid=True)
    f.box(cx - 60, 238, 120, 46, "更多商户", "green", fs=13, solid=True)
    f.path(f"M{cx+64},{82} Q{cx+120},{170} {cx+64},{258}", stroke=C["red"][0], sw=2)
    f.arrow(cx + 70, 252, cx + 62, 260, color=C["red"][0], sw=2, size=8)
    f.path(f"M{cx-64},{258} Q{cx-120},{170} {cx-64},{82}", stroke=C["red"][0], sw=2)
    f.arrow(cx - 70, 88, cx - 62, 80, color=C["red"][0], sw=2, size=8)
    f.text(cx + 104, 170, "值得收", fs=11, anchor="start", fill=C["red"][0])
    f.text(cx - 104, 170, "值得用", fs=11, anchor="end", fill=C["red"][0])
    f.text(cx, 160, "临界点之后", fs=11.5, weight=700)
    f.text(cx, 178, "自我加速", fs=11.5, weight=700)
    f.text(cx, 310, "中国的关键：打印一张码", fs=11, fill=MUTED)
    f.text(cx, 326, "商户接入成本几乎为零", fs=11, fill=MUTED)
    return f

@fig
def bitcoin():
    f = Fig(680, 360, "挖矿与减半")
    f.text(20, 28, "① 挖矿：反复试随机数（nonce）", fs=14, weight=700, anchor="start", fill=C["amber"][0])
    f.box(20, 44, 150, 70, "区块头", "slate", fs=13, sub="前一块哈希 + 交易 + nonce")
    f.arrow(170, 79, 220, 79, color=INK, sw=1.8)
    f.box(222, 54, 90, 50, "SHA-256", "purple", fs=12, solid=True)
    f.arrow(312, 79, 350, 79, color=INK, sw=1.8)
    rows = [("nonce = 1", "8f3a91…", False), ("nonce = 2", "c71e04…", False), ("…试了上万亿次…", "", None), ("nonce = 7350…", "000000004b…", True)]
    for k, (a, b, ok) in enumerate(rows):
        y = 50 + k * 20
        f.text(356, y, a, fs=11, anchor="start", mono=True, fill=MUTED)
        if b:
            f.text(470, y, b, fs=11, anchor="start", mono=True, weight=700 if ok else 400, fill=C["green"][0] if ok else C["red"][0])
            f.text(580, y, "✓ 小于目标" if ok else "✗", fs=11, anchor="start", fill=C["green"][0] if ok else C["red"][0], weight=700)
    f.text(340, 144, "找答案：只能盲猜，平均约 10 分钟全网才找到一个　验证：别人只需算一次", fs=11.5, weight=700)
    # halving chart
    f.text(20, 184, "② 区块奖励大约每四年减半，总量趋近 2100 万枚", fs=14, weight=700, anchor="start", fill=C["blue"][0])
    X0, Y0, W, H = 70, 330, 420, 120
    f.line(X0, Y0, X0 + W, Y0, stroke=INK, sw=1.2); f.line(X0, Y0, X0, Y0 - H - 6, stroke=INK, sw=1.2)
    vals = [("2009", 50), ("2012", 25), ("2016", 12.5), ("2020", 6.25), ("2024", 3.125)]
    bw = W / 6
    for k, (yr, v) in enumerate(vals):
        h = H * v / 50
        x = X0 + 10 + k * bw
        f.rect(x, Y0 - h, bw - 14, h, fill=C["blue"][1], stroke=C["blue"][0], rx=1)
        f.text(x + (bw - 14) / 2, Y0 - h - 5, str(v), fs=10.5, weight=700)
        f.text(x + (bw - 14) / 2, Y0 + 15, yr, fs=10.5, fill=MUTED)
    f.text(X0 - 8, Y0 - H, "枚/块", fs=10.5, anchor="end", fill=MUTED)
    f.rect(510, 200, 160, 130, fill=C["amber"][1], stroke=C["amber"][0], rx=8)
    f.text(590, 222, "为什么矿工守规矩？", fs=12, weight=700, fill=C["amber"][0])
    for k, ln in enumerate(["诚实挖矿：拿奖励", "篡改账本：需过半算力", "成本远高于收益", "不如老老实实挖"]):
        f.text(522, 246 + k * 20, ln, fs=11, anchor="start")
    return f

@fig
def blockchain():
    f = Fig(680, 300, "哈希链")
    xs = [20, 240, 460]
    names = ["区块 1", "区块 2", "区块 3"]
    prev = ["0000…", "a41f…", "7c2e…"]
    own = ["a41f…", "7c2e…", "e90b…"]
    for k, x in enumerate(xs):
        f.rect(x, 40, 200, 120, fill=C["blue"][1], stroke=C["blue"][0], rx=8, sw=1.4)
        f.text(x + 100, 60, names[k], fs=13, weight=700, fill=C["blue"][0])
        f.rect(x + 10, 70, 180, 22, fill="#fff", stroke=C["slate"][0], rx=4)
        f.text(x + 16, 86, "前一块哈希：" + prev[k], fs=11, anchor="start", mono=False)
        f.rect(x + 10, 98, 180, 22, fill="#fff", stroke=C["slate"][0], rx=4)
        f.text(x + 16, 114, "交易：A→B 2 枚 …", fs=11, anchor="start")
        f.text(x + 100, 146, "本块哈希：" + own[k], fs=11, weight=700, fill=C["purple"][0])
        if k < 2:
            f.arrow(x + 160, 150, xs[k + 1] + 60, 92, color=C["purple"][0], sw=1.6)
    # tampered row
    f.text(340, 188, "如果有人篡改区块 2 的交易：", fs=12.5, weight=700, fill=C["red"][0])
    for k, x in enumerate(xs):
        col = "red" if k >= 1 else "blue"
        f.rect(x, 200, 200, 64, fill=C[col][1], stroke=C[col][0], rx=8, sw=1.4)
    f.text(120, 236, "不变", fs=12, fill=C["blue"][0], weight=700)
    f.text(340, 224, "交易改成 A→B 20 枚", fs=11.5, fill=C["red"][0], weight=700)
    f.text(340, 246, "本块哈希变成 3d9a…", fs=11.5, fill=C["red"][0])
    f.text(560, 224, "记录的仍是 7c2e…", fs=11.5, fill=C["red"][0])
    f.text(560, 246, "对不上 → 链断开", fs=11.5, fill=C["red"][0], weight=700)
    f.text(450, 236, "✗", fs=20, fill=C["red"][0], weight=700)
    f.text(340, 290, "要想不被发现，必须重算其后所有区块，并且追上全网其他节点——几乎不可能", fs=11, fill=MUTED)
    return f

def main():
    only = set(sys.argv[1:])
    for name, fn in FIGS.items():
        if only and name not in only: continue
        fn().save(OUT / f"{name}.svg")
    print("wrote", len(only or FIGS), "figures to", OUT)

if __name__ == "__main__":
    main()
