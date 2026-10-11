#!/usr/bin/env python3
"""filler_check: keep writing-process padding out of the book.

Fails (exit 1) when it finds, in the chapter Markdown files:
  1. marker phrases left over from drafting (补强说明 N / 补强段 N / 补记N /
     密度补强 / 再写一层可操作对照 / 对本章再补可核对细节 / 第 N 轮补强 ...);
  2. the same paragraph (> 20 characters after stripping markup) twice inside
     one chapter, or in two different chapters;
  3. "template" paragraphs: identical once every number is replaced by '#'
     (catches 「……（补强段 3）」 style counters and number-swapped clones);
  4. the same section heading (>= 6 characters) twice in one chapter;
  5. the same sentence (> 20 characters) twice in one chapter, or in two
     chapters (catches a sentence pasted N times inside one paragraph).

Fenced blocks (```svg, code), tables and very short lines are ignored.
Paragraphs that are *meant* to repeat (a legal disclaimer, a fixed caption)
go into tools/filler_allow.txt, one regular expression per line; a paragraph
matching any of them is skipped.

Usage:
  python tools/filler_check.py [--dirs chapters ...] [--quiet] [--json out.json]
Defaults to the directories listed in tools/filler_dirs.txt, else chapters/.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MARKERS = [
    r"补强说明\s*\d*",
    r"（补强段\s*\d+）",
    r"补强段\s*\d+",
    r"（补记\s*\d+）",
    r"密度补强",
    r"第\s*\d+\s*轮补强",
    r"只服务达标与密度",
    r"再写一层可操作对照",
    r"对本章再补可核对细节",
    r"公开事实写到可检索为止",
    r"（本章适用。?）",
    r"（对照全书标准。?）",
    r"出版级密度要求",
    r"凑字数|注水段|扩写段\s*\d+|补充段\s*\d+|填充段",
    r"字数达标|达标字数|为达到字数|字数与结构均达标",
    # sentences that talk about the drafting standard instead of the subject
    r"出版级",
    r"信息槽",
    r"v1\s*病句",
    r"(?:本章|该章|章)(?:即)?(?:合格|达标)",
    r"收束达标|即达标|复述得出",
]
MARKER_RE = re.compile("|".join(f"(?:{m})" for m in MARKERS))
MIN_LEN = 20


def load_allow() -> list[re.Pattern]:
    f = ROOT / "tools" / "filler_allow.txt"
    if not f.exists():
        return []
    pats = []
    for line in f.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            pats.append(re.compile(line))
    return pats


def strip_fences(text: str) -> str:
    out, inside = [], False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            inside = not inside
            out.append("")
            continue
        out.append("" if inside else line)
    text = "\n".join(out)
    # raw HTML / svg blocks not fenced
    text = re.sub(r"<svg\b.*?</svg>", "", text, flags=re.S | re.I)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    return text


def norm(s: str) -> str:
    s = s.strip()
    s = re.sub(r"^(>\s*)+", "", s)
    s = re.sub(r"^([-*+]|\d+[.)])\s+", "", s)
    s = s.replace("**", "").replace("`", "").replace("*", "")
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def units_pipe(text: str):
    """pipe-separated data files (id | name | ... | definition): each long field is a unit."""
    for i, line in enumerate(text.split("\n"), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        for field in line.split("|"):
            if len(re.findall(r"[\u4e00-\u9fff]", field)) >= 10:  # skip id lists / names
                yield "p", i, norm(field)


def units(text: str):
    """yield (kind, line_no, normalized text). kind: 'h' heading, 'p' prose."""
    lines = strip_fences(text).split("\n")
    buf, start = [], 0
    def flush():
        if buf:
            yield "p", start, norm(" ".join(buf))
    for i, line in enumerate(lines, 1):
        s = line.strip()
        if not s:
            yield from flush(); buf = []
            continue
        if s.startswith("|"):
            yield from flush(); buf = []
            continue
        if s.startswith("#"):
            yield from flush(); buf = []
            yield "h", i, norm(re.sub(r"^#+\s*", "", s))
            continue
        if re.match(r"^([-*+]|\d+[.)])\s+", s) or s.startswith(">"):
            yield from flush(); buf = []
            yield "p", i, norm(s)
            continue
        if not buf:
            start = i
        buf.append(s)
    yield from flush()


REF_HEAD = re.compile(r"延伸阅读|参考|来源|资料|文献|出处|References|Sources|Further reading", re.I)
URL = re.compile(r"https?://|www\.|doi\.org|\bISBN\b")
MATHY = re.compile(r"\\\(|\\\[|\$|[=≈×÷→]")


def plen(s: str) -> int:
    return len(re.sub(r"[\s\W_]", "", s))


def key_exact(s: str) -> str:
    return re.sub(r"[\s\W_]", "", s)


def key_template(s: str) -> str:
    s = re.sub(r"[0-9０-９]+|[一二三四五六七八九十百千]+(?=[、）)])", "#", s)
    return re.sub(r"[\s\W_]", "", s)


def chapter_files(dirs: list[str]) -> list[Path]:
    files = []
    for d in dirs:
        p = ROOT / d
        if p.is_file():
            files.append(p)
        else:
            files += sorted(p.rglob("*.md")) + sorted(p.rglob("*.txt"))
    return files


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dirs", nargs="*")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--json")
    args = ap.parse_args()
    dirs = args.dirs
    if not dirs:
        cfg = ROOT / "tools" / "filler_dirs.txt"
        dirs = [l.strip() for l in cfg.read_text().splitlines() if l.strip() and not l.startswith("#")] if cfg.exists() else ["chapters"]
    allow = load_allow()
    files = chapter_files(dirs)

    problems: list[tuple[str, int, str]] = []
    sents = defaultdict(list)
    exact = defaultdict(list)
    templ = defaultdict(list)
    per_chars = defaultdict(int)
    for f in files:
        rel = str(f.relative_to(ROOT))
        text = f.read_text(encoding="utf-8")
        for i, line in enumerate((text if f.suffix == ".txt" else strip_fences(text)).split("\n"), 1):
            m = MARKER_RE.search(line)
            if m and not any(a.search(line) for a in allow):
                problems.append((rel, i, f"marker 「{m.group(0)}」: {line.strip()[:70]}"))
        heads = defaultdict(list)
        in_ref = rel.split("/")[-1].startswith(("sources", "appendix-d-sources", "references"))
        for kind, ln, s in (units_pipe(text) if f.suffix == ".txt" else units(text)):
            if any(a.search(s) for a in allow):
                continue
            if kind == "h":
                in_ref = bool(REF_HEAD.search(s)) or rel.split("/")[-1].startswith("sources")
                if plen(s) >= 6:
                    heads[key_exact(s)].append(ln)
                continue
            if plen(s) <= MIN_LEN:
                continue
            # citations and worked arithmetic may recur across chapters, never inside one
            ref = in_ref or bool(URL.search(s)) or bool(MATHY.search(s))
            exact[key_exact(s)].append((rel, ln, s, ref))
            if not ref:
                for sent in re.findall(r"[^。！？!?；]+[。！？!?；]?", s):
                    if plen(sent) > 20 and plen(sent) < plen(s) - 2 and not any(a.search(sent.strip()) for a in allow):
                        sents[key_exact(sent)].append((rel, ln, sent.strip()))
            digits = len(re.findall(r"[0-9]", s))
            if not ref and not MATHY.search(s) and digits < 0.25 * plen(s):
                templ[key_template(s)].append((rel, ln, s, ref))
        for k, lns in heads.items():
            if len(lns) > 1:
                problems.append((rel, lns[1], f"heading repeated {len(lns)}x in chapter (lines {lns})"))

    seen_exact_lines = set()
    for k, occ in exact.items():
        if len(occ) < 2:
            continue
        if all(o[3] for o in occ):
            # a citation may be cited by several chapters, but not twice in one
            seen_f = set()
            dups = []
            for o in occ:
                if o[0] in seen_f:
                    dups.append(o)
                seen_f.add(o[0])
            occ = [occ[0]] + dups if dups else [occ[0]]
            if len(occ) < 2:
                continue
        for rel, ln, s, _ in occ[1:]:
            seen_exact_lines.add((rel, ln))
            per_chars[rel] += len(s)
            others = sorted({f"{o[0]}:{o[1]}" for o in occ if (o[0], o[1]) != (rel, ln)})[:3]
            problems.append((rel, ln, f"duplicate paragraph (also {', '.join(others)}): {s[:60]}"))
    for k, occ in templ.items():
        if len(occ) < 2 or len({key_exact(o[2]) for o in occ}) < 2:
            continue
        for rel, ln, s, _ in occ[1:]:
            if (rel, ln) in seen_exact_lines:
                continue
            per_chars[rel] += len(s)
            problems.append((rel, ln, f"template paragraph (same text with numbers swapped as {occ[0][0]}:{occ[0][1]}): {s[:60]}"))

    para_keys = set(exact)
    for k, occ in sents.items():
        if len(occ) < 2 or k in para_keys:
            continue
        for rel, ln, sent in occ[1:]:
            if (rel, ln) in seen_exact_lines:
                continue
            per_chars[rel] += len(sent)
            problems.append((rel, ln, f"repeated sentence (also {occ[0][0]}:{occ[0][1]}): {sent[:60]}"))

    problems.sort()
    if not args.quiet or problems:
        for rel, ln, msg in problems:
            print(f"{rel}:{ln}: {msg}")
    by_file = defaultdict(int)
    for rel, _, _ in problems:
        by_file[rel] += 1
    if args.json:
        Path(args.json).write_text(json.dumps({"problems": len(problems), "by_file": by_file,
                                               "dup_chars": per_chars}, ensure_ascii=False, indent=1))
    print(f"# filler_check: files={len(files)} problems={len(problems)} files_with_problems={len(by_file)}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
