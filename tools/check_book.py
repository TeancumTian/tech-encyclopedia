#!/usr/bin/env python3
"""Book source checker (portable, no network, no browser).

Checks every Markdown chapter:
  * each ```svg``` block (inline, or a path like figs/<domain>/x.svg under assets/) is well-formed XML and has a viewBox
  * no absolute machine paths (box workspace, home or tmp dirs, Windows user dirs) leaked into the text
  * reports CJK character count (excluding code/SVG blocks) and SVG count
Also validates that every *.json data file parses.

Usage:
  python tools/check_book.py                 # default: chapters/ + *.json in repo
  python tools/check_book.py chapters/001-*.md
  python tools/check_book.py --quiet         # only print problems + summary
Exit code 1 if any hard error (bad SVG XML / leaked path / bad JSON).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER_DIRS = ['domains', 'front']
SVG_RE = re.compile(r"^```svg[^\n]*\n(.*?)^```", re.S | re.M)
CODE_RE = re.compile(r"```.*?```", re.S)
CJK_RE = re.compile(r"[\u4e00-\u9fff]")
PATH_RE = re.compile(r"(?<![\w.\-/])/(?:work" + r"space|ho" + r"me/[a-z]\w*|t" + r"mp)/|C:\\Us" + r"ers\\")


def check_md(path: Path, quiet: bool) -> tuple[int, int, int, list[str]]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    svgs = SVG_RE.findall(text)
    for k, block in enumerate(svgs, 1):
        ref = block.strip()
        if ref.endswith(".svg") and "\n" not in ref and not ref.startswith("<"):
            fp = ROOT / "assets" / ref
            if not fp.exists():
                errors.append(f"{path.relative_to(ROOT)} svg#{k}: missing figure file assets/{ref}")
                continue
            block = fp.read_text(encoding="utf-8")
        try:
            el = ET.fromstring(block.strip())
        except ET.ParseError as exc:
            errors.append(f"{path.relative_to(ROOT)} svg#{k}: XML error: {exc}")
            continue
        if "viewBox" not in el.attrib:
            errors.append(f"{path.relative_to(ROOT)} svg#{k}: missing viewBox (figure will not scale)")
    for n, line in enumerate(text.splitlines(), 1):
        if PATH_RE.search(line):
            errors.append(f"{path.relative_to(ROOT)}:{n}: absolute machine path: {line.strip()[:100]}")
    cjk = len(CJK_RE.findall(CODE_RE.sub("", text)))
    if not quiet:
        print(f"{path.relative_to(ROOT)}\tCJK={cjk}\tSVG={len(svgs)}")
    return cjk, len(svgs), len(errors), errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()
    if args.files:
        files = [Path(f).resolve() for f in args.files]
    else:
        files = sorted(p for d in CHAPTER_DIRS for p in (ROOT / d).glob("*.md"))
    all_errors: list[str] = []
    total_cjk = total_svg = 0
    for f in files:
        cjk, nsvg, _n, errs = check_md(f, args.quiet)
        total_cjk += cjk
        total_svg += nsvg
        all_errors += errs
    if not args.files:
        for j in sorted(ROOT.rglob("*.json")):
            if any(part in {"node_modules", ".git", "build"} for part in j.parts):
                continue
            try:
                json.loads(j.read_text(encoding="utf-8"))
            except Exception as exc:  # noqa: BLE001
                all_errors.append(f"{j.relative_to(ROOT)}: invalid JSON: {exc}")
    for e in all_errors:
        print("ERROR:", e, file=sys.stderr)
    print(f"# files={len(files)} CJK={total_cjk} SVG={total_svg} errors={len(all_errors)}")
    return 1 if all_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
