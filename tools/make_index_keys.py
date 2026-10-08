#!/usr/bin/env python3
"""Generate data/index_keys.json: pinyin sort keys for the keyword index (附录 拼音索引).

Needs pypinyin (listed in requirements.txt; the PDF build itself does not need it):
  pip install pypinyin && python3 tools/make_index_keys.py   # or: make index-keys
Re-run after adding or renaming entries; build_pdf.py falls back to code-point order for ids missing here.
"""
import json, re
from pathlib import Path
from pypinyin import lazy_pinyin, Style, load_phrases_dict

# polyphone fixes found in review
load_phrases_dict({"公差": [["gōng"], ["chā"]]})

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "data" / "entries.json").read_text(encoding="utf-8"))
out = {}
for e in data["entries"]:
    zh = e["zh"]
    syl = [s for s in lazy_pinyin(zh, style=Style.NORMAL, errors=lambda x: list(x)) if s.strip()]
    key = " ".join(s.lower() for s in syl)
    first = zh[0]
    if first.isdigit():
        letter = "#"
    elif re.match(r"[A-Za-z]", first):
        letter = first.upper()
    else:
        letter = (syl[0][:1] if syl else "#").upper()
    out[e["id"]] = {"key": key, "letter": letter}
(ROOT / "data" / "index_keys.json").write_text(json.dumps(out, ensure_ascii=False, indent=0), encoding="utf-8")
print(len(out), "keys")
