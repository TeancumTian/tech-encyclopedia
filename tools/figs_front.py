#!/usr/bin/env python3
"""Front-matter diagrams: book map (17 domains in 5 clusters)."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from svgkit import Fig, C, INK, MUTED, tw
ROOT = Path(__file__).resolve().parents[1]
D = {d["id"]: d for d in json.loads((ROOT / "data" / "entries.json").read_text())["domains"]}

def book_map():
    f = Fig(680, 584, "全书地图")
    f.text(340, 28, "17 个领域 · 5 大板块", fs=19, weight=700)
    f.text(340, 50, "方块左上角是篇号，右上角是该领域的词条数", fs=11.5, fill=MUTED)
    clusters = [
        ("能量与物质：让东西动起来、造出来", "amber", 20, 70, 640, 120, ["energy", "materials", "manufacturing", "building", "environment"]),
        ("信息：把世界变成比特", "blue", 20, 206, 640, 120, ["electronics", "computing", "internet", "ai", "media", "frontier"]),
        ("移动：把人和货送到远方", "teal", 20, 342, 300, 120, ["transport", "space"]),
        ("生命：吃饱、治病、长寿", "green", 360, 342, 300, 120, ["biomed", "agri"]),
        ("社会：安全与金钱", "slate", 20, 478, 640, 96, ["security", "fintech"]),
    ]
    pos = {}
    for title, col, x, y, w, h, ids in clusters:
        dark, light = C[col]
        f.rect(x, y, w, h, fill=light, stroke=dark, rx=10, sw=1.4)
        f.text(x + 12, y + 22, title, fs=13, weight=700, fill=dark, anchor="start")
        n = len(ids); gap = 8; tw_ = (w - 24 - gap * (n - 1)) / n
        th = h - 44
        for k, i in enumerate(ids):
            d = D[i]; tx = x + 12 + k * (tw_ + gap); ty = y + 32
            f.rect(tx, ty, tw_, th, fill="#fff", stroke=dark, rx=7, sw=1)
            f.text(tx + 8, ty + 17, f"{d['num']:02d}", fs=11, fill=dark, weight=700, anchor="start")
            f.text(tx + tw_ - 8, ty + 17, str(d["count"]), fs=12, fill=dark, weight=700, anchor="end")
            name = d["zh"]
            fs = 13 if tw_ > tw(name, 13) + 10 else 11.5
            if tw(name, fs) > tw_ - 8 and "、" in name:
                a, b = name.split("、", 1)
                f.text(tx + tw_ / 2, ty + th / 2 + 6, a + "、", fs=fs, weight=700)
                f.text(tx + tw_ / 2, ty + th / 2 + 6 + fs * 1.25, b, fs=fs, weight=700)
            else:
                f.text(tx + tw_ / 2, ty + th / 2 + 10, name, fs=fs, weight=700)
            pos[i] = (tx + tw_ / 2, ty, ty + th)
    total = sum(d["count"] for d in D.values())
    f.text(660, 28, f"共 {total} 个词条", fs=12, fill=C["blue"][0], weight=700, anchor="end")
    return f

if __name__ == "__main__":
    out = ROOT / "assets" / "figs" / "front"; out.mkdir(parents=True, exist_ok=True)
    book_map().save(out / "book-map.svg"); print("ok")

def cover():
    f = Fig(600, 230, "封面")
    ev = [(1712, "纽科门\n蒸汽机", "amber"), (1837, "电报", "blue"), (1879, "电灯", "amber"), (1903, "飞机", "teal"),
          (1928, "青霉素", "green"), (1947, "晶体管", "blue"), (1969, "阿波罗\n与阿帕网", "purple"), (2007, "智能\n手机", "blue"), (2022, "大模型", "pink")]
    x0, x1, y = 30, 570, 120
    def X(yr): return x0 + (yr - 1700) / (2026 - 1700) * (x1 - x0)
    f.rect(x0, y - 3, x1 - x0, 6, fill="#e5e7eb", stroke="none", rx=3)
    # exponential-ish curve suggesting acceleration
    pts = [(X(1700 + t), y - 8 - 90 * ((1.0 + t / 326) ** 7 - 1) / (2 ** 7 - 1)) for t in range(0, 327, 4)]
    f.poly(pts, stroke="#1d4ed8", sw=2.2, opacity=0.5)
    for k, (yr, nm, col) in enumerate(ev):
        x = X(yr); dark, light = C[col]
        f.circle(x, y, 7, fill=dark, stroke="#fff", sw=2)
        up = k % 2 == 0
        f.text(x, y + 26 if up else y - 16, str(yr), fs=11, weight=700, fill=dark)
        rows = nm.split("\n")
        if up: f.lines(x, y + 44, rows, fs=11.5, fill="#374151")
        else: f.lines(x, y - 34 - 14 * (len(rows) - 1), rows, fs=11.5, fill="#374151")
    f.text(x0, y + 96, "1700", fs=11, fill=MUTED, anchor="start"); f.text(x1, y + 96, "2026", fs=11, fill=MUTED, anchor="end")
    return f

if __name__ == "__main__":
    cover().save(ROOT / "front" / "cover.svg")
