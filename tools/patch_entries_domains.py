#!/usr/bin/env python3
"""Minimal, domain-scoped update of data/entries.json (safe when other domains are edited in parallel).
Re-reads entries.json, replaces ONLY the given domains' entries + domain records from data/src,
recomputes cited_by for those entries, validates their refs, and writes back.
usage: patch_entries_domains.py agri building ..."""
import json, sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import compile_entries as CE
ROOT = CE.ROOT
mine = set(sys.argv[1:])
_, principles = CE.load_principles(); pids = {p["id"] for p in principles}
doms, ents = CE.load_domains()
new = [e for e in ents if e["domain"] in mine]
fp = ROOT / "data" / "entries.json"
data = json.loads(fp.read_text(encoding="utf-8"))
keep = [e for e in data["entries"] if e["domain"] not in mine]
ids = {e["id"] for e in keep} | {e["id"] for e in new}
errs = []
dup = [k for k, v in Counter([e["id"] for e in keep] + [e["id"] for e in new]).items() if v > 1]
errs += [f"duplicate id {d}" for d in dup]
for e in new:
    for r in e["related"]:
        if r not in ids: errs.append(f"{e['id']}: unknown related {r}")
    for p in e["principles"]:
        if p not in pids: errs.append(f"{e['id']}: unknown principle {p}")
    if not e["principles"]: errs.append(f"{e['id']}: no principle")
if errs:
    print("\n".join(errs)); sys.exit(1)
allents = keep + new
for e in new:
    e["cited_by"] = sorted({x["id"] for x in allents if e["id"] in x["related"]} - set(e["related"]))
# keep global order by domain number then original order
order = {d["id"]: d["num"] for d in data["domains"]}
merged = sorted(allents, key=lambda e: (order[e["domain"]], 0))  # stable: keeps within-domain order
dmap = {d["id"]: d for d in doms}
for i, d in enumerate(data["domains"]):
    if d["id"] in mine:
        nd = dmap[d["id"]]
        es = [e for e in new if e["domain"] == d["id"]]
        nd["count"] = len(es); nd["tiers"] = dict(Counter(e["tier"] for e in es))
        data["domains"][i] = nd
data["entries"] = merged
data["meta"]["total_entries"] = len(merged)
fp.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
print("patched", sorted(mine), "->", {d["id"]: d["count"] for d in data["domains"] if d["id"] in mine}, "total", len(merged))
