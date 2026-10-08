#!/usr/bin/env python3
"""Compile data/src/*.txt into data/entries.json + data/principles.json and validate.

Source format (one entry per line):
  id | 中文 | English | tier(A/B/C) | year | 一句话定义 | related ids (comma) | principle ids (comma)
Lines starting with '# ' declare the domain: id | 中文 | English | tagline
Lines starting with '## ' declare a subcategory.
"""
from __future__ import annotations
import json, re, sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data" / "src"

def split(line):
    return [x.strip() for x in line.split("|")]

def load_principles():
    groups, out, sub = [], [], None
    for line in (SRC / "00-principles.txt").read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("# "):
            continue
        if line.startswith("## "):
            sub = line[3:].strip(); groups.append(sub); continue
        f = split(line)
        assert len(f) == 5, line
        out.append(dict(id=f[0], zh=f[1], en=f[2], statement=f[3], group=sub,
                        examples=[x.strip() for x in f[4].split(",") if x.strip()]))
    return groups, out

def load_domains():
    domains, entries = [], []
    for fp in sorted(SRC.glob("[0-9][0-9]-*.txt")):
        if fp.name.startswith("00-"):
            continue
        dom, sub, order = None, None, 0
        for ln, line in enumerate(fp.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            if line.startswith("# "):
                f = split(line[2:])
                dom = dict(id=f[0], zh=f[1], en=f[2], tagline=f[3], file=fp.name,
                           num=int(fp.name[:2]), subcategories=[])
                domains.append(dom); continue
            if line.startswith("## "):
                sub = line[3:].strip(); dom["subcategories"].append(sub); continue
            f = split(line)
            if len(f) != 8:
                sys.exit(f"{fp.name}:{ln}: expected 8 fields, got {len(f)}: {line[:80]}")
            order += 1
            entries.append(dict(
                id=f[0], zh=f[1], en=f[2], tier=f[3], year=int(f[4]) if f[4] else None,
                definition=f[5], domain=dom["id"], subcategory=sub, order=order,
                related=[x.strip() for x in f[6].split(",") if x.strip()],
                principles=[x.strip() for x in f[7].split(",") if x.strip()],
            ))
    return domains, entries

def main():
    groups, principles = load_principles()
    domains, entries = load_domains()
    pids = {p["id"] for p in principles}
    errors, warns = [], []
    c = Counter(e["id"] for e in entries)
    errors += [f"duplicate id: {k}" for k, v in c.items() if v > 1]
    zc = Counter(e["zh"] for e in entries)
    warns += [f"duplicate zh name: {k}" for k, v in zc.items() if v > 1]
    ids = {e["id"] for e in entries}
    for e in entries:
        if e["tier"] not in "ABC":
            errors.append(f"{e['id']}: bad tier {e['tier']}")
        for r in e["related"]:
            if r not in ids: errors.append(f"{e['id']}: unknown related '{r}'")
            if r == e["id"]: errors.append(f"{e['id']}: self reference")
        for p in e["principles"]:
            if p not in pids: errors.append(f"{e['id']}: unknown principle '{p}'")
        if not e["principles"]:
            errors.append(f"{e['id']}: no principle link")
    for p in principles:
        for x in p["examples"]:
            if x not in ids: errors.append(f"principle {p['id']}: unknown example '{x}'")
    # back-links: who cites each entry
    cited = defaultdict(list)
    for e in entries:
        for r in e["related"]:
            cited[r].append(e["id"])
    for e in entries:
        e["cited_by"] = sorted(set(cited[e["id"]]) - set(e["related"]))
    puse = Counter(p for e in entries for p in e["principles"])
    for p in principles:
        p["entry_count"] = puse[p["id"]]
    for d in domains:
        es = [e for e in entries if e["domain"] == d["id"]]
        d["count"] = len(es)
        d["tiers"] = dict(Counter(e["tier"] for e in es))
    out = dict(meta=dict(title="近现代科技百科全书", version="v1-keywords",
                         generated_by="tools/compile_entries.py",
                         total_entries=len(entries), total_principles=len(principles),
                         tier_meaning={"A": "核心词条：约 380–750 字 + 1 张图", "B": "标准词条：约 220–480 字，可选小图", "C": "短词条：约 120–320 字"}),
               principle_groups=groups, principles=principles, domains=domains, entries=entries)
    (ROOT / "data" / "entries.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"principles={len(principles)} entries={len(entries)}")
    for d in domains:
        print(f"  {d['num']:02d} {d['zh']:<10} {d['count']:>4}  {d['tiers']}")
    print("tiers:", dict(Counter(e['tier'] for e in entries)))
    print("principle usage (low):", sorted(puse.items(), key=lambda x: x[1])[:8])
    unused = pids - set(puse)
    if unused: warns.append(f"principles never used: {sorted(unused)}")
    orphans = [e["id"] for e in entries if not cited[e["id"]]]
    print(f"entries never cited by another entry: {len(orphans)}")
    for w in warns: print("WARN", w)
    for er in errors: print("ERR ", er)
    return 1 if errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
