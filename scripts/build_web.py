#!/usr/bin/env python3
"""Build the learning site using only Python's standard library. Book files remain canonical."""
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'build' / 'web'
FIELDS = ['是什么', '原理', '怎么工作', '年份人物', '改变了', '注意', '图注']


def parse_body(body):
    figures = re.findall(r'^```svg[^\n]*\n(.*?)^```', body, re.M | re.S)
    body = re.sub(r'^```svg[^\n]*\n.*?^```', '', body, flags=re.M | re.S)
    fields, current = {}, None
    for line in body.splitlines():
        match = re.match(r'^(' + '|'.join(FIELDS) + r')[：:]\s*(.*)', line)
        if match:
            current = match[1]
            fields[current] = match[2]
        elif current and line.strip():
            fields[current] += '\n' + line
    refs = [f.strip() for f in figures]
    for ref in refs:
        if not ref.startswith('figs/') or not ref.endswith('.svg') or '..' in ref or not (ROOT / 'assets' / ref).is_file():
            raise ValueError(f'Invalid figure reference: {ref}')
    return {'fields': fields, 'figures': refs}


def compile_site():
    data = json.loads((ROOT / 'data/entries.json').read_text())
    bodies = {}
    for domain in data['domains']:
        path = ROOT / 'domains' / Path(domain['file']).with_suffix('.md')
        text = path.read_text()
        parts = re.split(r'^@entry ([a-z0-9-]+)\s*$', text, flags=re.M)
        for entry_id, body in zip(parts[1::2], parts[2::2]):
            if entry_id in bodies:
                raise ValueError(f'Duplicate body: {entry_id}')
            bodies[entry_id] = parse_body(body.split('@outro')[0])
        domain['source'] = f'domains/{path.name}'
    entry_ids = {e['id'] for e in data['entries']}
    principle_ids = {p['id'] for p in data['principles']}
    assert len(entry_ids) == len(data['entries']), 'Duplicate entry IDs'
    assert set(bodies) == entry_ids, 'Book body and index IDs differ'
    for entry in data['entries']:
        entry.update(bodies[entry['id']])
        assert entry['fields'].get('原理'), f"Missing principle explanation: {entry['id']}"
        assert set(entry['related']) <= entry_ids, f"Unknown related entry: {entry['id']}"
        assert set(entry['principles']) <= principle_ids, f"Unknown principle: {entry['id']}"
        for ref in re.findall(r'\[\[([^\]|]+)', '\n'.join(entry['fields'].values())):
            assert (ref[2:] in principle_ids if ref.startswith('p:') else ref in entry_ids), f'Unknown cross reference: {ref}'
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT / 'web', OUT)
    shutil.copytree(ROOT / 'assets/figs', OUT / 'figs')
    (OUT / 'book.json').write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    (OUT / '.nojekyll').touch()
    print(f"Built {len(data['entries'])} entries, {len(data['principles'])} principles → build/web")
    return data


if __name__ == '__main__':
    compile_site()
