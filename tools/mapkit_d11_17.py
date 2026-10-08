"""Shared concept-map layout for domains 11–17 (same look as figs_computing.concept_map)."""
from __future__ import annotations
from svgkit import Fig, C, INK, MUTED, tw

def _rows(items, width, fs=11):
    rows, cx = 1, 0
    for it in items:
        w = tw(it, fs) + 12
        if cx and cx + w > width - 22:
            rows, cx = rows + 1, 0
        cx += w + 6
    return rows

def concept_map(title, subtitle, groups, hist, side, footer, arrow="up", hist_title="关键年份", center_note=None, H=940):
    """groups: [(name, color, [items])] drawn bottom->top if arrow=='up' else top->bottom."""
    f = Fig(680, H, title + " 知识地图")
    f.text(340, 30, title + " · 知识地图", fs=21, weight=700)
    f.text(340, 52, subtitle, fs=11.5, fill=MUTED)
    X, W = 168, 344
    top, bottom = 80, H - 140
    need = [34 + 24 * _rows(it, W) for _, _, it in groups]
    gap = 14
    scale = (bottom - top - gap * (len(groups) - 1)) / sum(need)
    hs = [n * scale for n in need]
    order = list(range(len(groups)))
    seq = order if arrow == "down" else order[::-1]  # draw from top
    y = top
    pos = {}
    for i in seq:
        pos[i] = (y, hs[i]); y += hs[i] + gap
    for i, (name, col, items) in enumerate(groups):
        y, h = pos[i]
        dark, light = C[col]
        f.rect(X, y, W, h, fill=light, stroke=dark, sw=1.4, rx=8)
        f.text(X + 12, y + 20, name, fs=14, fill=dark, weight=700, anchor="start")
        cx, cy = X + 12, y + 30
        for it in items:
            w = tw(it, 11) + 12
            if cx + w > X + W - 10:
                cx, cy = X + 12, cy + 24
            f.rect(cx, cy, w, 19, fill="#fff", stroke=dark, sw=0.8, rx=9)
            f.text(cx + w / 2, cy + 13.5, it, fs=11)
            cx += w + 6
    # arrows between consecutive groups (seq is top->bottom)
    for a, b in zip(seq, seq[1:]):
        ya, ha = pos[a]; yb, _ = pos[b]
        if arrow == "down":
            f.arrow(X + W / 2, ya + ha - 1, X + W / 2, yb + 3, color=C[groups[a][1]][0], sw=2.2, size=10)
        elif arrow == "up":
            f.arrow(X + W / 2, yb + 1, X + W / 2, ya + ha - 3, color=C[groups[b][1]][0], sw=2.2, size=10)
    if center_note:
        f.text(X + W / 2, bottom + 24, center_note, fs=11.5, fill=C["blue"][0], weight=700)
    # left timeline
    LX = 10
    f.text(LX + 70, 92, hist_title, fs=14, weight=700, fill=C["slate"][0])
    y0 = 116; step = (bottom - 130) / max(1, len(hist) - 1)
    f.line(LX + 18, y0 - 6, LX + 18, y0 + step * (len(hist) - 1) + 6, stroke=C["slate"][0], sw=2)
    for k, (yr, nm) in enumerate(hist):
        yy = y0 + k * step
        f.circle(LX + 18, yy, 4.5, fill=C["slate"][0], stroke="#fff", sw=1)
        f.text(LX + 28, yy + 4, yr, fs=10.5, fill=MUTED, anchor="start", weight=700)
        fs = 11.5 if tw(nm, 11.5) < 98 else 10.5
        f.text(LX + 60, yy + 4, nm, fs=fs, anchor="start")
    # right side boxes
    RX = 524; y = 84
    for stitle, col, items in side:
        dark, light = C[col]
        h = 34 + 22 * len(items)
        f.rect(RX, y, 148, h, fill=light, stroke=dark, sw=1.2, rx=8)
        f.text(RX + 74, y + 22, stitle, fs=13.5, fill=dark, weight=700)
        for k, it in enumerate(items):
            fs = 11.5 if tw("· " + it, 11.5) < 134 else 10.5
            f.text(RX + 10, y + 44 + 22 * k, "· " + it, fs=fs, anchor="start")
        y += h + 16
    # footer
    fy = H - 80
    f.rect(10, fy, 660, 22 + 17 * len(footer) + 10, fill="#f9fafb", stroke="#d1d5db", rx=8)
    f.text(340, fy + 22, "和其他篇的接口", fs=12.5, weight=700)
    for k, ln in enumerate(footer):
        f.text(340, fy + 42 + 17 * k, ln, fs=11, fill=MUTED)
    return f
