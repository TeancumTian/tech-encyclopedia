#!/usr/bin/env python3
"""Batch fact-check: for each claim, fetch the Wikipedia article's plain text and test a regex.
Usage: factcheck.py claims.tsv  (cols: claim \t Wikipedia title \t regex)
Writes research/factcheck/<name>.result.tsv with PASS/FAIL and a context snippet."""
import json, re, sys, time, urllib.parse, urllib.request
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "research" / "factcheck" / "cache"; CACHE.mkdir(parents=True, exist_ok=True)
UA = {"User-Agent": "tech-encyclopedia-factcheck/0.1 (research use)"}

def text(title):
    fp = CACHE / (re.sub(r"[^\w\-]", "_", title) + ".txt")
    if fp.exists(): return fp.read_text()
    q = urllib.parse.urlencode({"action": "query", "prop": "extracts", "explaintext": 1, "redirects": 1, "format": "json", "titles": title})
    with urllib.request.urlopen(urllib.request.Request("https://en.wikipedia.org/w/api.php?" + q, headers=UA), timeout=30) as r:
        pages = json.load(r)["query"]["pages"]
    t = next(iter(pages.values())).get("extract", "") or ""
    fp.write_text(t); time.sleep(0.2)
    return t

src = Path(sys.argv[1]); rows = []
for ln in src.read_text().splitlines():
    if not ln.strip() or ln.startswith("#"): continue
    claim, title, rx = ln.split("\t")
    try: t = text(title)
    except Exception as e: rows.append(("ERR", claim, title, str(e))); continue
    m = re.search(rx, t, flags=re.S)
    ctx = t[max(0, m.start() - 80): m.end() + 80].replace("\n", " ") if m else ""
    rows.append(("PASS" if m else ("NOPAGE" if not t else "FAIL"), claim, title, ctx))
out = src.with_suffix(".result.tsv")
out.write_text("\n".join("\t".join(r) for r in rows))
for r in rows:
    if r[0] != "PASS": print(r[0], "|", r[1], "|", r[2])
print(sum(r[0] == "PASS" for r in rows), "/", len(rows), "pass ->", out)
