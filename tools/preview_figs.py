#!/usr/bin/env python3
"""Render assets/figs/<dir>/*.svg to PNGs (via WeasyPrint at book text width) for visual QA."""
import sys, subprocess, re
from pathlib import Path
from weasyprint import HTML
ROOT = Path(__file__).resolve().parents[1]
d = ROOT / "assets" / "figs" / sys.argv[1]
names = sys.argv[2:] or sorted(p.stem for p in d.glob("*.svg"))
out = ROOT / "build" / "preview"; out.mkdir(parents=True, exist_ok=True)
style = "<style><![CDATA[text,tspan{font-family:'Noto Sans CJK SC',sans-serif;}]]></style>"
for n in names:
    svg = (d / f"{n}.svg").read_text()
    svg = re.sub(r"(<svg[^>]*>)", r"\1" + style, svg, count=1)
    h = f'<html><head><style>@page{{size:178mm 260mm;margin:0}} svg{{width:178mm;height:auto;display:block}}</style></head><body>{svg}</body></html>'
    pdf = out / f"{n}.pdf"
    HTML(string=h).write_pdf(str(pdf))
    subprocess.run(["pdftoppm", "-png", "-r", "110", "-singlefile", str(pdf), str(out / n)], check=True)
    pdf.unlink()
print("ok", len(names))
from PIL import Image, ImageChops
for n in names:
    fp = out / f"{n}.png"
    im = Image.open(fp).convert("RGB")
    bb = ImageChops.difference(im, Image.new("RGB", im.size, (255, 255, 255))).getbbox()
    if bb: im.crop((0, 0, im.size[0], min(im.size[1], bb[3] + 10))).save(fp)
