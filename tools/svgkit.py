"""Tiny SVG drawing kit for the encyclopedia's diagrams.

All figures share one palette and one font stack so the book looks consistent.
Text width is estimated (CJK ≈ 1.0·fs, Latin ≈ 0.56·fs) to size boxes without a renderer.
"""
from __future__ import annotations
import html, math, re

C = dict(  # (stroke/dark, fill/light)
    blue=("#1d4ed8", "#dbeafe"), amber=("#d97706", "#fef3c7"), green=("#059669", "#d1fae5"),
    red=("#dc2626", "#fee2e2"), purple=("#7c3aed", "#ede9fe"), slate=("#475569", "#f1f5f9"),
    teal=("#0f766e", "#ccfbf1"), pink=("#db2777", "#fce7f3"), gray=("#9ca3af", "#f9fafb"),
)
INK, MUTED = "#111827", "#6b7280"


def tw(s: str, fs: float) -> float:
    w = 0.0
    for ch in s:
        if ord(ch) > 0x2E7F or ch in "·—“”‘’…": w += fs
        elif ch == " ": w += 0.3 * fs
        else: w += 0.56 * fs
    return w


def esc(s) -> str:
    return html.escape(str(s), quote=True)


class Fig:
    def __init__(self, w: float, h: float, title: str = ""):
        self.w, self.h, self.items = w, h, []
        self.title = title

    # ---- primitives ----
    def raw(self, s: str): self.items.append(s); return self

    def text(self, x, y, s, fs=13, fill=INK, anchor="middle", weight=400, italic=False, mono=False, opacity=1):
        fam = ' font-family="Noto Sans Mono CJK SC,monospace"' if mono else ""
        st = ' font-style="italic"' if italic else ""
        op = f' opacity="{opacity}"' if opacity != 1 else ""
        self.items.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{fs}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}"{fam}{st}{op}>{esc(s)}</text>')
        return self

    def lines(self, x, y, rows, fs=13, lh=1.3, **kw):
        """multi-line text, y is the baseline of the first line."""
        for i, r in enumerate(rows):
            self.text(x, y + i * fs * lh, r, fs=fs, **kw)
        return self

    def rect(self, x, y, w, h, fill="#fff", stroke=INK, sw=1.2, rx=6, dash=None, opacity=1):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        op = f' opacity="{opacity}"' if opacity != 1 else ""
        self.items.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}{op}/>')
        return self

    def box(self, x, y, w, h, label="", color="blue", fs=13, sub=None, sub_fs=None, weight=700, rx=6, dash=None, solid=False, txt=None):
        dark, light = C[color]
        self.rect(x, y, w, h, fill=dark if solid else light, stroke=dark, rx=rx, dash=dash)
        tc = txt or ("#fff" if solid else INK)
        rows = label.split("\n") if label else []
        subs = (sub.split("\n") if sub else [])
        sfs = sub_fs or fs * 0.78
        total = len(rows) * fs * 1.25 + len(subs) * sfs * 1.25
        yy = y + (h - total) / 2
        for r in rows:
            self.text(x + w / 2, yy + fs * 0.98, r, fs=fs, fill=tc, weight=weight); yy += fs * 1.25
        for r in subs:
            self.text(x + w / 2, yy + sfs * 0.98, r, fs=sfs, fill=("#fff" if solid else MUTED)); yy += sfs * 1.25
        return self

    def circle(self, cx, cy, r, fill="#fff", stroke=INK, sw=1.2, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.items.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')
        return self

    def line(self, x1, y1, x2, y2, stroke=INK, sw=1.4, dash=None, cap="round"):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.items.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="{cap}"{d}/>')
        return self

    def path(self, d, stroke=INK, sw=1.4, fill="none", dash=None, opacity=1):
        da = f' stroke-dasharray="{dash}"' if dash else ""
        op = f' opacity="{opacity}"' if opacity != 1 else ""
        self.items.append(f'<path d="{d}" stroke="{stroke}" stroke-width="{sw}" fill="{fill}" stroke-linejoin="round" stroke-linecap="round"{da}{op}/>')
        return self

    def poly(self, pts, stroke=INK, sw=1.4, fill="none", dash=None, opacity=1, closed=False):
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + (" Z" if closed else "")
        return self.path(d, stroke=stroke, sw=sw, fill=fill, dash=dash, opacity=opacity)

    def head(self, x, y, ang, color=INK, size=8):
        a1, a2 = ang + math.radians(152), ang - math.radians(152)
        p = [(x, y), (x + size * math.cos(a1), y + size * math.sin(a1)), (x + size * math.cos(a2), y + size * math.sin(a2))]
        self.items.append('<path d="M{:.1f},{:.1f} L{:.1f},{:.1f} L{:.1f},{:.1f} Z" fill="{}" stroke="none"/>'.format(*p[0], *p[1], *p[2], color))

    def arrow(self, x1, y1, x2, y2, color=INK, sw=1.5, dash=None, both=False, label=None, fs=11, lcolor=None, loff=(0, -5), size=8):
        ang = math.atan2(y2 - y1, x2 - x1)
        bx, by = x2 - size * 0.7 * math.cos(ang), y2 - size * 0.7 * math.sin(ang)
        sx, sy = (x1 + size * 0.7 * math.cos(ang), y1 + size * 0.7 * math.sin(ang)) if both else (x1, y1)
        self.line(sx, sy, bx, by, stroke=color, sw=sw, dash=dash, cap="butt")
        self.head(x2, y2, ang, color, size)
        if both: self.head(x1, y1, ang + math.pi, color, size)
        if label:
            self.text((x1 + x2) / 2 + loff[0], (y1 + y2) / 2 + loff[1], label, fs=fs, fill=lcolor or MUTED)
        return self

    def curve(self, x1, y1, cx, cy, x2, y2, color=INK, sw=1.5, dash=None, arrow=True, size=8):
        self.path(f"M{x1:.1f},{y1:.1f} Q{cx:.1f},{cy:.1f} {x2:.1f},{y2:.1f}", stroke=color, sw=sw, dash=dash)
        if arrow:
            self.head(x2, y2, math.atan2(y2 - cy, x2 - cx), color, size)
        return self

    def pill(self, x, y, s, color="blue", fs=11, solid=False, anchor="start", pad=6):
        w = tw(s, fs) + 2 * pad
        if anchor == "middle": x -= w / 2
        dark, light = C[color]
        self.rect(x, y, w, fs * 1.6, fill=dark if solid else light, stroke=dark, sw=0.9, rx=fs * 0.8)
        self.text(x + w / 2, y + fs * 1.13, s, fs=fs, fill="#fff" if solid else dark, weight=700)
        return w

    def svg(self) -> str:
        t = f"<title>{esc(self.title)}</title>" if self.title else ""
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
                f'font-family="Noto Sans CJK SC, sans-serif">{t}' + "".join(self.items) + "</svg>\n")

    def save(self, path):
        from pathlib import Path
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(self.svg(), encoding="utf-8")
        return path
