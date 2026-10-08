#!/usr/bin/env python3
"""Typeset 《近现代科技百科全书》 into an A4 Chinese PDF.

Toolchain inherited from the sister book repo b2b-zero-to-one (tools/build_pdf.py) (WeasyPrint + markdown-it +
Noto CJK; inline ```svg``` blocks -> <figure>). Entry metadata comes from data/entries.json;
entry bodies come from domains/NN-<domain>.md (format: see PUBLISHING_STANDARD.md §4).

Usage:
  python3 tools/build_pdf.py --sample computing   # build/样章.pdf
  python3 tools/build_pdf.py                      # build/近现代科技百科全书-全书.pdf（缺稿词条以短条目占位并警告）
  python3 tools/build_pdf.py --list               # 打印阅读顺序（role<TAB>path<TAB>title）
"""
from __future__ import annotations

import argparse, html, json, re, sys
from collections import defaultdict
from pathlib import Path

from markdown_it import MarkdownIt
from weasyprint import HTML

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"
DATA = json.loads((ROOT / "data" / "entries.json").read_text(encoding="utf-8"))
ENT = {e["id"]: e for e in DATA["entries"]}
PRIN = {p["id"]: p for p in DATA["principles"]}
DOM = {d["id"]: d for d in DATA["domains"]}
BOOK_TITLE = "近现代科技百科全书"
BOOK_SUBTITLE = "An Illustrated Encyclopedia of Modern Technology · 1700–2026"
BOOK_READER = "从工业革命到大模型 · 17 个领域、近 1000 个关键词\n每个词条讲清：是什么、为什么行、怎么工作、谁何时、改变了什么"

MD = MarkdownIt("commonmark", {"html": True, "linkify": False, "typographer": False}).enable("table")
SVG_STYLE = "<style><![CDATA[text,tspan{font-family:'Noto Sans CJK SC','Noto Sans CJK JP',sans-serif;}]]></style>"
FIELDS = ["是什么", "原理", "怎么工作", "年份人物", "改变了", "注意", "图注"]
LABEL = {"怎么工作": "怎么工作", "年份人物": "关键年份与人物", "改变了": "改变了什么", "注意": "常见误解"}

CSS = r"""
@page { size: A4; margin: 17mm 16mm 17mm 16mm;
  @bottom-center { content: counter(page); font-family: "Noto Sans CJK SC", sans-serif; font-size: 9pt; color: #4b5563; } }
@page :right { @top-right { content: string(book-title); font-family: "Noto Sans CJK SC", sans-serif; font-size: 8pt; color: #6b7280; } @top-left { content: none; } }
@page :left { @top-left { content: string(part-name); font-family: "Noto Sans CJK SC", sans-serif; font-size: 8pt; color: #6b7280; } @top-right { content: none; } }
@page cover { margin: 20mm; @top-left { content: none; } @top-right { content: none; } @bottom-center { content: none; } }
@page part-open { @top-left { content: none; } @top-right { content: none; } }
* { print-color-adjust: exact; }
html { font-size: 10.6pt; }
body { font-family: "Noto Serif CJK SC", "Noto Sans CJK SC", serif; color: #1a1a1a; line-height: 1.66; hyphens: none;
  string-set: book-title "近现代科技百科全书", part-name ""; }
a { color: inherit; text-decoration: none; }
.title-page { page: cover; break-after: page; padding-top: 46mm; text-align: center; }
.book-title { font-family: "Noto Serif CJK SC", serif; font-weight: 700; font-size: 30pt; line-height: 1.35; margin: 0 0 8mm; color: #111827; }
.subtitle { font-family: "Noto Sans CJK SC", sans-serif; font-size: 12.5pt; margin: 0 0 8mm; color: #1f2937; }
.reader { font-family: "Noto Sans CJK SC", sans-serif; font-size: 10.5pt; color: #4b5563; margin: 0 auto; max-width: 30em; line-height: 1.75; }
.cover-rule { width: 48mm; border: none; border-top: 1.2pt solid #1d4ed8; margin: 9mm auto; }
.sample-note { font-family: "Noto Sans CJK SC", sans-serif; font-size: 9.6pt; color: #1e3a8a; border: 0.8pt solid #93c5fd; background: #eff6ff; padding: 3mm 4mm; margin: 12mm auto 0; max-width: 33em; text-align: left; }
.cover-art { margin: 10mm auto 0; width: 120mm; }
/* TOC */
.toc { break-after: page; }
.toc-title { font-family: "Noto Serif CJK SC", serif; font-size: 22pt; font-weight: 700; margin: 0 0 6mm; }
.toc a { display: block; }
.toc a::after { content: leader(".") target-counter(attr(href), page); color: #9ca3af; }
.toc .lv0 { font-family: "Noto Sans CJK SC", sans-serif; font-weight: 700; font-size: 11.5pt; margin: 0.8em 0 0.2em; color: #1d4ed8; }
.toc .lv1 { font-family: "Noto Sans CJK SC", sans-serif; font-size: 9.8pt; font-weight: 700; margin: 0.35em 0 0.05em 0.8em; color: #1f2937; }
.toc .entries { columns: 2; column-gap: 8mm; margin: 0 0 0 1.6em; }
.toc .lv2 { font-family: "Noto Sans CJK SC", sans-serif; font-size: 8.4pt; margin: 0.02em 0; color: #374151; break-inside: avoid; }
/* headings */
h1.part { font-family: "Noto Serif CJK SC", serif; font-size: 24pt; color: #1d4ed8; margin: 26mm 0 2mm; break-before: page; bookmark-level: 1; }
.part-en { font-family: "Noto Sans CJK SC", sans-serif; font-size: 11pt; color: #6b7280; margin: 0 0 6mm; }
.part-tag { font-family: "Noto Sans CJK SC", sans-serif; font-size: 12pt; color: #111827; border-left: 4pt solid #1d4ed8; padding-left: 3mm; margin-bottom: 8mm; }
h1.front { font-family: "Noto Serif CJK SC", serif; font-size: 20pt; color: #1d4ed8; break-before: page; margin: 0 0 0.6em; bookmark-level: 1; }
h2 { font-family: "Noto Sans CJK SC", sans-serif; font-size: 13.5pt; margin: 1.1em 0 0.4em; break-after: avoid; bookmark-level: 2; }
h2.sub { font-size: 14pt; color: #fff; background: #1d4ed8; padding: 1.6mm 3mm; margin: 6mm 0 3mm; break-before: auto; }
h3 { font-family: "Noto Sans CJK SC", sans-serif; font-size: 11.5pt; margin: 0.9em 0 0.3em; break-after: avoid; bookmark-level: 3; }
p { margin: 0.3em 0 0.5em; orphans: 2; widows: 2; text-align: left; }  /* justify stretches only spaces in WeasyPrint -> big gaps around Latin words in CJK text */
ul, ol { margin: 0.25em 0 0.5em; padding-left: 1.3em; }
li { margin: 0.08em 0; }
blockquote { margin: 0.6em 0; padding: 0.25em 0.85em; border-left: 3pt solid #1d4ed8; background: #eff6ff; }
table { width: 100%; border-collapse: collapse; margin: 0.5em 0 0.9em; font-family: "Noto Sans CJK SC", sans-serif; font-size: 9pt; }
th, td { border: 0.5pt solid #d1d5db; padding: 0.22em 0.4em; text-align: left; vertical-align: top; }
th { background: #f3f4f6; }
tr { break-inside: avoid; }
code { font-family: "Noto Sans Mono CJK SC", monospace; font-size: 0.92em; background: #f3f4f6; padding: 0 0.15em; }
pre { font-size: 8.6pt; background: #f8fafc; border: 0.5pt solid #e5e7eb; padding: 2mm 3mm; white-space: pre-wrap; }
/* diagrams */
figure.diagram { margin: 0.6em 0 0.8em; break-inside: avoid; text-align: center; }
figure.diagram svg { display: block; width: 100%; height: auto; margin: 0 auto; }
figure.diagram.small svg { width: 78%; }
figcaption { font-family: "Noto Sans CJK SC", sans-serif; font-size: 8.6pt; color: #4b5563; margin-top: 0.3em; }
figure.map { break-before: page; }
/* entries */
section.entry { margin: 0 0 3.2mm; padding-top: 2.4mm; border-top: 0.6pt solid #e5e7eb; }
section.entry h3.eh { margin: 0 0 0.15em; font-size: 12.4pt; color: #111827; break-after: avoid; }
section.entry.tier-A { border-top: 1.4pt solid #1d4ed8; }
section.entry.tier-C h3.eh { font-size: 11.2pt; }
.eh .en { font-weight: 400; font-size: 9.4pt; color: #4b5563; margin-left: 0.4em; }
.eh .yr { font-weight: 700; font-size: 8.4pt; color: #fff; background: #64748b; border-radius: 2pt; padding: 0 0.35em; margin-left: 0.45em; }
.eh .star { color: #1d4ed8; margin-right: 0.15em; }
p.def { font-family: "Noto Sans CJK SC", sans-serif; font-weight: 700; font-size: 10.4pt; color: #1f2937; margin: 0.15em 0 0.35em; break-after: avoid; }
div.fp { background: #fffbeb; border-left: 3pt solid #f59e0b; padding: 1.2mm 3mm; margin: 0.3em 0 0.45em; break-inside: avoid; }
div.fp p { margin: 0.1em 0; }
.fp .lab, .lab { font-family: "Noto Sans CJK SC", sans-serif; font-weight: 700; color: #1d4ed8; margin-right: 0.35em; }
.fp .lab { color: #b45309; }
.chip { font-family: "Noto Sans CJK SC", sans-serif; font-size: 8pt; color: #92400e; border: 0.5pt solid #f59e0b; border-radius: 6pt; padding: 0 0.4em; margin-left: 0.25em; white-space: nowrap; }
.chip::after, a.xr::after { content: " " target-counter(attr(href), page); color: #9ca3af; font-size: 0.85em; }
p.xref { font-family: "Noto Sans CJK SC", sans-serif; font-size: 8.6pt; color: #374151; margin: 0.3em 0 0; }
p.xref .lab { color: #6b7280; }
a.xr { border-bottom: 0.4pt solid #cbd5e1; }  /* solid, not dotted: WeasyPrint draws dotted borders as thousands of tiny circles (~20 MB over the full book) */
a.xr.out { color: #6b7280; }
p.warn { font-family: "Noto Sans CJK SC", sans-serif; font-size: 9pt; color: #9a3412; }
/* principle index */
.pr { margin: 0 0 2.6mm; break-inside: avoid; }
.pr h3 { margin: 0.5em 0 0.1em; font-size: 11pt; color: #b45309; }
.pr .st { margin: 0.05em 0 0.1em; }
.pr .uses { font-family: "Noto Sans CJK SC", sans-serif; font-size: 8.2pt; color: #4b5563; line-height: 1.5; }
.pr .uses a { margin-right: 0.5em; }
/* master list */
.master table { font-size: 7.6pt; }
.master td:nth-child(1) { width: 19%; } .master td:nth-child(2) { width: 22%; } .master td:nth-child(3) { width: 5%; }
.master h2 { break-before: auto; }
/* appendices: timeline, sources, keyword indexes */
.tl-era { font-family: "Noto Sans CJK SC", sans-serif; font-size: 12pt; color: #1d4ed8; margin: 4mm 0 1.5mm; break-after: avoid; }
.tl { columns: 2; column-gap: 7mm; font-family: "Noto Sans CJK SC", sans-serif; font-size: 7.9pt; line-height: 1.42; }
.tl a { display: block; break-inside: avoid; }
.tl a::after, .kidx a::after { content: leader(".") target-counter(attr(href), page); color: #9ca3af; }
.tl .y { display: inline-block; width: 2.6em; font-weight: 700; color: #374151; }
.tl .dm { color: #9ca3af; font-size: 0.9em; margin-left: 0.3em; }
.tl a.A { font-weight: 700; color: #111827; }
.kidx { columns: 3; column-gap: 5mm; font-family: "Noto Sans CJK SC", sans-serif; font-size: 7.6pt; line-height: 1.38; }
.kidx h3.lt { font-size: 11pt; color: #1d4ed8; margin: 2.2mm 0 0.6mm; break-after: avoid; border-bottom: 0.6pt solid #93c5fd; bookmark-level: none; }
.kidx a { display: block; break-inside: avoid; }
.kidx .en2 { color: #6b7280; font-size: 0.92em; margin-left: 0.25em; }
.kidx .zh2 { color: #374151; margin-left: 0.25em; }
.srcs { font-size: 8.8pt; line-height: 1.55; }
.srcs h2.src-d { font-size: 12.5pt; color: #1d4ed8; border-bottom: 0.8pt solid #93c5fd; margin-top: 7mm; break-before: auto; }
.srcs h3 { font-size: 10pt; color: #374151; bookmark-level: none; }
.srcs h4 { font-size: 9.4pt; bookmark-level: none; }
.srcs table { font-size: 7.8pt; }
.srcs p, .srcs li { text-align: left; overflow-wrap: anywhere; }
.badge { font-size: 7pt; color: #fff; background: #1d4ed8; border-radius: 2pt; padding: 0 0.25em; }
"""


def esc(s): return html.escape(s, quote=True)

def load_svgfile(path: str) -> str:
    fp = ROOT / "assets" / path.strip()
    if not fp.exists():
        print("WARNING missing figure", fp, file=sys.stderr)
        return f'<svg viewBox="0 0 600 60"><text x="300" y="35" text-anchor="middle" fill="#9a3412">[缺图 {html.escape(path.strip())}]</text></svg>'
    return fp.read_text(encoding="utf-8")

def fix_svg(raw: str) -> str:
    raw = raw.strip()
    if not raw.startswith("<"):
        raw = load_svgfile(raw).strip()
    raw = re.sub(r"^<\?xml[^>]*>\s*", "", raw)
    m = re.match(r"<svg\b([^>]*)>", raw, flags=re.I)
    if not m:
        return "<pre>" + esc(raw) + "</pre>"
    attrs = re.sub(r'\s(?:width|height)\s*=\s*"[^"]*"', "", m.group(1))
    return f"<svg{attrs}>{SVG_STYLE}{raw[m.end():]}"

def md_inline(text: str) -> str:
    text = re.sub(r"\*\*([^\n*]+?)\*\*", "\uE000\\1\uE001", text)
    out = MD.renderInline(text).replace("\uE000", "<strong>").replace("\uE001", "</strong>")
    return link_mentions(out)

def md_block(text: str, fi: int = 0) -> str:
    lines, blocks, out, i = text.split("\n"), [], [], 0
    while i < len(lines):
        if lines[i].startswith("```"):
            lang = lines[i][3:].strip().lower(); i += 1; buf = []
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i]); i += 1
            i += 1
            blocks.append((lang, "\n".join(buf))); out += ["", f"XBLOCK{len(blocks)-1:04d}X", ""]
        else:
            out.append(lines[i]); i += 1
    t = re.sub(r"\*\*([^\n*]+?)\*\*", "\uE000\\1\uE001", "\n".join(out))
    body = MD.render(t).replace("\uE000", "<strong>").replace("\uE001", "</strong>")
    def rep(m):
        lang, content = blocks[int(m.group(1))]
        if lang.startswith("svg"):
            cls = "diagram" + (" small" if "small" in lang else "") + (" map" if "map" in lang else "")
            return f'<figure class="{cls}">{fix_svg(content)}</figure>'
        return f"<pre><code>{esc(content)}</code></pre>"
    body = re.sub(r"<p>\s*XBLOCK(\d{4})X\s*</p>", rep, body)
    body = re.sub(r"XBLOCK(\d{4})X", rep, body)
    return link_mentions(body)

INCLUDED: set[str] = set()

def href(eid: str) -> str:
    return f"#e-{eid}" if eid in INCLUDED else f"#x-{eid}"

def link_mentions(h: str) -> str:
    """[[id]] or [[id|显示文字]] -> cross-reference link with page number."""
    def rep(m):
        eid, label = m.group(1), m.group(2)
        if eid.startswith("p:"):
            p = PRIN[eid[2:]]
            return f'<a class="chip" href="#p-{p["id"]}">{esc(label or p["zh"])}</a>'
        if eid not in ENT:
            print("WARNING unknown mention", eid, file=sys.stderr); return esc(label or eid)
        cls = "xr" if eid in INCLUDED else "xr out"
        return f'<a class="{cls}" href="{href(eid)}">{esc(label or ENT[eid]["zh"])}</a>'
    return re.sub(r"\[\[([a-z0-9:\-]+)(?:\|([^\]]+))?\]\]", rep, h)

# ---------------- domain source parsing ----------------

def parse_domain(path: Path):
    text = path.read_text(encoding="utf-8")
    parts = re.split(r"^@(intro|entry [a-z0-9\-]+|outro)\s*$", text, flags=re.M)
    intro, outro, entries = "", "", {}
    for tag, body in zip(parts[1::2], parts[2::2]):
        if tag == "intro": intro = body.strip()
        elif tag == "outro": outro = body.strip()
        else:
            eid = tag.split()[1]
            if eid in entries: sys.exit(f"duplicate entry body {eid}")
            entries[eid] = parse_entry(body)
    return intro, entries, outro

def parse_entry(body: str):
    fields, cur, svgs, captions = defaultdict(str), None, [], []
    lines, i = body.strip("\n").split("\n"), 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("```svg"):
            lang = ln[3:].strip(); buf = []; i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i]); i += 1
            i += 1; svgs.append((lang, "\n".join(buf))); cur = None; continue
        m = re.match(r"^(" + "|".join(FIELDS) + r")[：:]\s*(.*)$", ln)
        if m:
            cur = m.group(1)
            if cur == "图注": captions.append(m.group(2).strip()); cur = None
            else: fields[cur] = m.group(2).strip()
        elif cur and ln.strip():
            fields[cur] += "\n" + ln
        i += 1
    return dict(fields=dict(fields), svgs=svgs, captions=captions)

def cjk_count(s: str) -> int:
    """字数 as Word counts it: each CJK char / CJK punctuation = 1, each Latin word or number = 1."""
    s = re.sub(r"\[\[[^\]|]+\|([^\]]+)\]\]", r"\1", s)
    s = re.sub(r"\[\[([^\]]+)\]\]", r"\1", s)
    return (len(re.findall(r"[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]", s))
            + len(re.findall(r"[A-Za-z0-9][A-Za-z0-9.\-+']*", s)))

def render_entry(e, body):
    f = body["fields"] if body else {}
    tier = e["tier"]
    star = '<span class="star">★</span>' if tier == "A" else ""
    yr = f'<span class="yr">{e["year"]}</span>' if e["year"] else ""
    out = [f'<section class="entry tier-{tier}" id="e-{e["id"]}">',
           f'<h3 class="eh">{star}{esc(e["zh"])}<span class="en">{esc(e["en"])}</span>{yr}</h3>',
           f'<p class="def">{md_inline(f.get("是什么", e["definition"]))}</p>']
    chips = "".join(f'<a class="chip" href="#p-{p}">{esc(PRIN[p]["zh"])}</a>' for p in e["principles"])
    if f.get("原理"):
        out.append(f'<div class="fp"><p><span class="lab">第一性原理</span>{md_inline(f["原理"])}{chips}</p></div>')
    for key in ["怎么工作", "年份人物", "改变了", "注意"]:
        if f.get(key):
            paras = [x.strip() for x in f[key].split("\n") if x.strip()]
            first = f'<p><span class="lab">{LABEL[key]}</span>{md_inline(paras[0])}</p>'
            out.append(first + "".join(f"<p>{md_inline(p)}</p>" for p in paras[1:]))
    for k, (lang, svg) in enumerate(body["svgs"] if body else []):
        cap = body["captions"][k] if k < len(body["captions"]) else ""
        cls = "diagram" + (" small" if "small" in lang else "")
        capx = f"<figcaption>图：{md_inline(cap)}</figcaption>" if cap else ""
        out.append(f'<figure class="{cls}">{fix_svg(svg)}{capx}</figure>')
    rel = list(dict.fromkeys(e["related"] + e["cited_by"][:max(0, 7 - len(e["related"]))]))
    links = "、".join(f'<a class="xr{"" if r in INCLUDED else " out"}" href="{href(r)}">{esc(ENT[r]["zh"])}</a>' for r in rel)
    out.append(f'<p class="xref"><span class="lab">相关词条</span>{links}</p>')
    if not body:
        out.insert(3, '<p class="warn">（正文待写）</p>')
    out.append("</section>")
    return "\n".join(out)

# ---------------- generated front/back matter ----------------

def principles_index_html():
    uses = defaultdict(list)
    for e in DATA["entries"]:
        for p in e["principles"]:
            uses[p].append(e["id"])
    h = ['<section class="front-sec"><h1 class="front" id="principles-index">第一性原理索引</h1>',
         md_block((ROOT / "front" / "principles-intro.md").read_text(encoding="utf-8")) if (ROOT / "front" / "principles-intro.md").exists() else ""]
    for g in DATA["principle_groups"]:
        h.append(f'<h2 id="pg-{esc(g)}">{esc(g)}</h2>')
        for p in DATA["principles"]:
            if p["group"] != g: continue
            ids = uses[p["id"]]
            lst = "".join(f'<a href="{href(i)}">{esc(ENT[i]["zh"])}</a>' for i in ids)
            h.append(f'<div class="pr" id="p-{p["id"]}"><h3>{esc(p["zh"])} <span class="en" style="font-weight:400;color:#6b7280;font-size:9pt">{esc(p["en"])}</span></h3>'
                     f'<p class="st">{esc(p["statement"])}</p><p class="uses">用到它的词条（{len(ids)}）：{lst}</p></div>')
    h.append("</section>")
    return "\n".join(h)

def master_list_html():
    h = ['<section class="master"><h1 class="front" id="master-list">附录　全书词条总表</h1>',
         '<p>按领域与子类排列。<span class="badge">样</span> 表示本样章已写出正文；年份为该技术的关键起点年份（发明、首次演示或首次商用，以词条正文为准）；A/B/C 为篇幅级别。</p>']
    for d in DATA["domains"]:
        h.append(f'<h2 id="m-{d["id"]}">{d["num"]:02d}　{esc(d["zh"])}（{d["count"]} 条）</h2>')
        for sub in d["subcategories"]:
            rows = [e for e in DATA["entries"] if e["domain"] == d["id"] and e["subcategory"] == sub]
            h.append(f'<table><thead><tr><th colspan="4">{esc(sub)}（{len(rows)}）</th></tr></thead><tbody>')
            for e in rows:
                b = ' <span class="badge">样</span>' if e["id"] in INCLUDED else ""
                h.append(f'<tr id="x-{e["id"]}"><td>{esc(e["zh"])}{b}　<b style="color:#9ca3af">{e["tier"]}</b></td><td>{esc(e["en"])}</td>'
                         f'<td>{e["year"] or ""}</td><td>{esc(e["definition"])}</td></tr>')
            h.append("</tbody></table>")
    h.append("</section>")
    return "\n".join(h)

def front_md(name: str, hid: str, title: str):
    p = ROOT / "front" / name
    if not p.exists():
        print("WARNING missing", p, file=sys.stderr); return ""
    txt = p.read_text(encoding="utf-8")
    txt = re.sub(r"^# .*\n", "", txt, count=1)
    if "@@STATS@@" in txt:
        from collections import Counter as _C
        tc = _C(e["tier"] for e in DATA["entries"])
        txt = txt.replace("@@STATS@@", f'{len(DATA["domains"])} 个领域、{len(DATA["entries"])} 个词条（★ 核心 {tc["A"]} 条、标准 {tc["B"]} 条、短词条 {tc["C"]} 条）、{len(DATA["principles"])} 条第一性原理')
    if "@@DOMAIN_TABLE@@" in txt:
        rows = []
        for d in DATA["domains"]:
            tgt = f"#d-{d['id']}" if d["id"] in {e["domain"] for e in DATA["entries"] if e["id"] in INCLUDED} else f"#m-{d['id']}"
            rows.append(f'| {d["num"]:02d} | <a class="xr" href="{tgt}">{d["zh"]}</a> | {d["count"]} | {d["tagline"]} |')
        rows.append(f'| | **合计** | **{len(DATA["entries"])}** | 另有 {len(DATA["principles"])} 条第一性原理 |')
        txt = txt.replace("@@DOMAIN_TABLE@@", "\n".join(rows))
    return f'<section class="front-sec"><h1 class="front" id="{hid}">{esc(title)}</h1>{md_block(txt)}</section>'

ERAS = [(1700, 1799, "1700–1799　第一次工业革命：蒸汽与机器"), (1800, 1869, "1800–1869　铁路、电报与电的驯服"),
        (1870, 1913, "1870–1913　第二次工业革命：电力、内燃机与化工"), (1914, 1945, "1914–1945　两次世界大战与大众技术"),
        (1946, 1969, "1946–1969　晶体管、原子能与太空竞赛"), (1970, 1999, "1970–1999　个人电脑、互联网与基因工程"),
        (2000, 2100, "2000–2026　移动互联网、新能源与人工智能")]

def timeline_html():
    ents = sorted((e for e in DATA["entries"] if e["year"] and e["id"] in INCLUDED), key=lambda e: (e["year"], DOM[e["domain"]]["num"], e["order"]))
    h = ['<section class="appendix"><h1 class="front" id="timeline">附录一　大事年表</h1>',
         f'<p>按词条标题中的"关键起点"年份（发明、首次演示或首次商用）排列，共 {len(ents)} 条；没有单一起点年份的词条（如"可再生能源"这类总称）不列入。'
         '<b>粗体</b>为 ★ 核心词条，右侧灰字为所属领域，末尾是页码。年份只标起点，完整经过见词条正文。</p>']
    for lo, hi, name in ERAS:
        rows = [e for e in ents if lo <= e["year"] <= hi]
        if not rows: continue
        h.append(f'<h2 class="tl-era">{esc(name)}（{len(rows)}）</h2><div class="tl">')
        h += [f'<a class="{e["tier"]}" href="#e-{e["id"]}"><span class="y">{e["year"]}</span>{esc(e["zh"])}<span class="dm">{esc(DOM[e["domain"]]["zh"])}</span></a>' for e in rows]
        h.append("</div>")
    h.append("</section>")
    return "\n".join(h)

def sources_all_html(doms):
    h = ['<section class="appendix srcs"><h1 class="front" id="sources">附录二　资料来源与核实记录</h1>',
         '<p>各篇的核实记录按篇排列，格式相同：一、按原始来源核对的最新数据（附访问时间）；二、用维基百科正文批量核对年份与人物，并逐条处理未通过项；'
         '三、收词范围的对照来源；四、延伸阅读。2025–2026 年的数据都注明了时间点，标"终校时核对"的条目是 2026 年 10 月全书终校时重新查证或更正过的。</p>']
    for d in doms:
        fp = ROOT / "front" / f'sources-{d["id"]}.md'
        if not fp.exists():
            print("WARNING missing", fp, file=sys.stderr); continue
        txt = fp.read_text(encoding="utf-8")
        txt = re.sub(r"^# .*\n", "", txt, count=1)
        txt = re.sub(r"^(#{2,5}) ", lambda m: "#" + m.group(1) + " ", txt, flags=re.M)
        h.append(f'<h2 class="src-d" id="src-{d["id"]}">第 {d["num"]} 篇　{esc(d["zh"])}</h2>{md_block(txt)}')
    h.append("</section>")
    return "\n".join(h)

def _index_keys():
    fp = ROOT / "data" / "index_keys.json"
    return json.loads(fp.read_text(encoding="utf-8")) if fp.exists() else {}

def pinyin_index_html():
    keys = _index_keys()
    ents = [e for e in DATA["entries"] if e["id"] in INCLUDED]
    miss = [e["id"] for e in ents if e["id"] not in keys]
    if miss: print("WARNING index_keys.json lacks", len(miss), "ids; run tools/make_index_keys.py", file=sys.stderr)
    def k(e):
        v = keys.get(e["id"], {"key": e["zh"].lower(), "letter": "#"})
        return (v["letter"] != "#", v["letter"], v["key"], e["zh"])
    ents.sort(key=k)
    h = ['<section class="appendix"><h1 class="front" id="kw-index">附录三　中文关键词索引（按拼音）</h1>',
         f'<p>全书 {len(ents)} 个词条按汉语拼音排序（以英文字母或数字开头的词条按字母归入相应字母，数字开头的排在最前），每条附英文名，末尾是页码。'
         '想从英文查，请用附录四。</p><div class="kidx">']
    cur = None
    for e in ents:
        L = keys.get(e["id"], {"letter": "#"})["letter"]
        if L != cur:
            h.append(f'<h3 class="lt">{"0–9" if L == "#" else L}</h3>'); cur = L
        h.append(f'<a href="#e-{e["id"]}">{esc(e["zh"])}<span class="en2">{esc(e["en"])}</span></a>')
    h.append("</div></section>")
    return "\n".join(h)

def english_index_html():
    ents = [e for e in DATA["entries"] if e["id"] in INCLUDED]
    def k(e):
        s = re.sub(r"^(the|a|an)\s+", "", e["en"].strip(), flags=re.I)
        return (not s[:1].isalpha(), s.casefold())
    ents.sort(key=k)
    h = ['<section class="appendix"><h1 class="front" id="en-index">附录四　English Index（英文索引）</h1>',
         '<p>按英文名 A–Z 排序（忽略开头的 The/A/An），右侧为中文词条名与页码。</p><div class="kidx">']
    cur = None
    for e in ents:
        s = re.sub(r"^(the|a|an)\s+", "", e["en"].strip(), flags=re.I)
        L = s[:1].upper() if s[:1].isalpha() else "0–9"
        if L != cur:
            h.append(f'<h3 class="lt">{L}</h3>'); cur = L
        h.append(f'<a href="#e-{e["id"]}">{esc(e["en"])}<span class="zh2">{esc(e["zh"])}</span></a>')
    h.append("</div></section>")
    return "\n".join(h)

def domain_html(d, intro, bodies, outro):
    h = [f'<section class="domain" style="string-set: part-name \'第 {d["num"]} 篇｜{esc(d["zh"])}\'">',
         f'<h1 class="part" id="d-{d["id"]}">第 {d["num"]} 篇　{esc(d["zh"])}</h1>',
         f'<p class="part-en">{esc(d["en"])} · {d["count"]} 个词条</p>',
         f'<p class="part-tag">{esc(d["tagline"])}</p>', md_block(intro) if intro else ""]
    toc, stats = [], defaultdict(int)
    for sub in d["subcategories"]:
        sid = f's-{d["id"]}-{d["subcategories"].index(sub)}'
        h.append(f'<h2 class="sub" id="{sid}">{esc(sub)}</h2>')
        ents = [e for e in DATA["entries"] if e["domain"] == d["id"] and e["subcategory"] == sub]
        toc.append((sub, sid, ents))
        for e in ents:
            b = bodies.get(e["id"])
            if not b: stats["missing"] += 1
            h.append(render_entry(e, b))
    if outro: h.append(md_block(outro))
    h.append("</section>")
    return "\n".join(h), toc, stats

def build(sample: str | None):
    global INCLUDED
    domain_files = {d["id"]: ROOT / "domains" / f'{d["num"]:02d}-{d["id"]}.md' for d in DATA["domains"]}
    doms = [DOM[sample]] if sample else DATA["domains"]
    parsed = {}
    for d in doms:
        fp = domain_files[d["id"]]
        parsed[d["id"]] = parse_domain(fp) if fp.exists() else ("", {}, "")
        INCLUDED |= {e["id"] for e in DATA["entries"] if e["domain"] == d["id"]}
    # QA
    report = []
    for d in doms:
        intro, bodies, _ = parsed[d["id"]]
        extra = set(bodies) - {e["id"] for e in DATA["entries"] if e["domain"] == d["id"]}
        if extra: print("WARNING bodies for unknown entries:", extra, file=sys.stderr)
        for e in DATA["entries"]:
            if e["domain"] != d["id"]: continue
            b = bodies.get(e["id"])
            n = cjk_count(" ".join(b["fields"].values())) if b else 0
            svgs = len(b["svgs"]) if b else 0
            report.append((e["id"], e["tier"], n, svgs))
    toc_html = ['<section class="toc"><div class="toc-title">目录</div>']
    pieces = []
    fronts = [("howto.md", "howto", "怎么读这本书"), ("map.md", "bookmap", "全书地图")]
    for name, hid, title in fronts:
        pieces.append(front_md(name, hid, title)); toc_html.append(f'<a class="lv0" href="#{hid}">{title}</a>')
    pieces.append(principles_index_html()); toc_html.append('<a class="lv0" href="#principles-index">第一性原理索引</a>')
    for d in doms:
        intro, bodies, outro = parsed[d["id"]]
        dh, toc, stats = domain_html(d, intro, bodies, outro)
        pieces.append(dh)
        toc_html.append(f'<a class="lv0" href="#d-{d["id"]}">第 {d["num"]} 篇　{esc(d["zh"])}</a>')
        for sub, sid, ents in toc:
            toc_html.append(f'<a class="lv1" href="#{sid}">{esc(sub)}</a>')
            if sample:
                toc_html.append('<div class="entries">' + "".join(
                    f'<a class="lv2" href="#e-{e["id"]}">{esc(e["zh"])}</a>' for e in ents) + "</div>")
    if sample:
        srcs = ROOT / "front" / f"sources-{sample}.md"
        if srcs.exists():
            pieces.append(front_md(srcs.name, "sources", "本篇资料来源与核实记录")); toc_html.append('<a class="lv0" href="#sources">本篇资料来源与核实记录</a>')
        pieces.append(master_list_html()); toc_html.append('<a class="lv0" href="#master-list">附录　全书词条总表</a>')
    else:
        for fn, hid, title in [(timeline_html, "timeline", "附录一　大事年表"),
                               (lambda: sources_all_html(doms), "sources", "附录二　资料来源与核实记录"),
                               (pinyin_index_html, "kw-index", "附录三　中文关键词索引（按拼音）"),
                               (english_index_html, "en-index", "附录四　English Index（英文索引）")]:
            pieces.append(fn()); toc_html.append(f'<a class="lv0" href="#{hid}">{title}</a>')
    toc_html.append("</section>")
    note = (f'<p class="sample-note">样章版：收录"怎么读这本书""全书地图""第一性原理索引"（{len(DATA["principles"])} 条根原理）、'
            f'第 {DOM[sample]["num"]} 篇「{DOM[sample]["zh"]}」全部 {DOM[sample]["count"]} 个词条的正文与图解，以及全书 {len(DATA["entries"])} 个词条的总表。'
            f'其余各篇按同一标准撰写。</p>') if sample else ""
    cover_art = ROOT / "front" / "cover.svg"
    art = f'<div class="cover-art">{fix_svg(cover_art.read_text(encoding="utf-8"))}</div>' if cover_art.exists() else ""
    title_page = (f'<section class="title-page"><h1 class="book-title">近现代科技百科全书</h1><hr class="cover-rule"/>'
                  f'<p class="subtitle">{esc(BOOK_SUBTITLE)}</p><p class="reader">{esc(BOOK_READER).replace(chr(10), "<br/>")}</p>{art}{note}</section>')
    doc = (f'<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"/><title>{BOOK_TITLE}</title>'
           f'<style>{CSS}</style></head><body>{title_page}{"".join(toc_html)}{"".join(pieces)}</body></html>')
    return doc, report

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", default=None, help="domain id to build as 样章")
    ap.add_argument("--html-only", action="store_true")
    ap.add_argument("--list", action="store_true", help="print reading order and exit")
    args = ap.parse_args()
    if args.list:
        print("front\tfront/howto.md\t怎么读这本书")
        print("front\tfront/map.md\t全书地图")
        print("front\tfront/principles-intro.md\t第一性原理索引（导读）")
        for d in DATA["domains"]:
            print(f'chapter\tdomains/{d["num"]:02d}-{d["id"]}.md\t第 {d["num"]} 篇　{d["zh"]}（{d["count"]} 条）')
        return 0
    BUILD.mkdir(parents=True, exist_ok=True)
    doc, report = build(args.sample)
    stem = "样章" if args.sample else "近现代科技百科全书-全书"
    (BUILD / f"{stem}.html").write_text(doc, encoding="utf-8")
    tiers = {"A": (360, 750), "B": (220, 480), "C": (120, 320)}  # 字数, see PUBLISHING_STANDARD.md
    short = [(i, t, n) for i, t, n, s in report if n and not tiers[t][0] <= n <= tiers[t][1]]
    missing = [i for i, t, n, s in report if n == 0]
    nofig_A = [i for i, t, n, s in report if t == "A" and n and s == 0]
    total = sum(n for _, _, n, _ in report); figs = sum(s for *_, s in report)
    print(f"entries={len(report)} written={len(report)-len(missing)} 字数={total} entry_figs={figs}")
    if missing: print("MISSING:", missing)
    if short: print("LENGTH OUT OF RANGE:", short)
    if nofig_A: print("A-TIER WITHOUT FIGURE:", nofig_A)
    if args.html_only: return 0
    out = BUILD / f"{stem}.pdf"
    HTML(string=doc, base_url=str(ROOT)).write_pdf(str(out))
    print("PDF:", out.relative_to(ROOT), out.stat().st_size)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
