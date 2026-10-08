#!/usr/bin/env python3
"""Insert entry lines into data/src files at the end of a named subcategory (creates it if absent).
Input: a text file with blocks:
  @@ <file> :: <subcategory>
  id | zh | en | tier | year | def | related | principles
"""
import sys
from pathlib import Path
SRC = Path(__file__).resolve().parents[1] / "data" / "src"
blocks, cur = [], None
for line in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines():
    if line.startswith("@@ "):
        f, sub = [x.strip() for x in line[3:].split("::")]
        cur = (f, sub, []); blocks.append(cur)
    elif line.strip():
        cur[2].append(line)
for f, sub, lines in blocks:
    fp = SRC / f
    rows = fp.read_text(encoding="utf-8").splitlines()
    idx = None
    for i, r in enumerate(rows):
        if r.strip() == f"## {sub}":
            idx = i
    if idx is None:
        rows += [f"## {sub}"] + lines
    else:
        j = idx + 1
        while j < len(rows) and not rows[j].startswith("## "):
            j += 1
        while j > idx + 1 and not rows[j - 1].strip():
            j -= 1
        rows[j:j] = lines
    fp.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"{f} :: {sub} +{len(lines)}")
