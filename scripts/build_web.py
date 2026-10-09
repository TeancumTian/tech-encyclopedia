#!/usr/bin/env python3
"""Compile every book section to an offline-capable, dependency-free web reader."""
import hashlib
import json
import re
import shutil
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'build' / 'web'
FIELDS = ['是什么', '原理', '怎么工作', '年份人物', '改变了', '注意', '图注']


def figure_ref(ref):
    ref = ref.strip()
    if not ref.startswith('figs/') or not ref.endswith('.svg') or '..' in ref or not (ROOT / 'assets' / ref).is_file():
        raise ValueError(f'Invalid figure reference: {ref}')
    return ref


def parse_blocks(text):
    """Small, lossless-for-this-book Markdown subset. No arbitrary HTML execution."""
    lines, blocks, i = text.splitlines(), [], 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line.startswith('```'):
            language, content = line[3:], []
            i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                content.append(lines[i]); i += 1
            if i == len(lines):
                raise ValueError('Unclosed code fence')
            body = '\n'.join(content)
            blocks.append({'type': 'figure', 'src': figure_ref(body)} if language.startswith('svg') else {'type': 'code', 'text': body})
        elif re.match(r'^#{1,6} ', line):
            level, title = line.split(' ', 1)
            blocks.append({'type': 'heading', 'level': len(level), 'text': title})
        elif line.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                row = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?', c.replace(' ', '')) for c in row):
                    rows.append(row)
                i += 1
            # Book table cells contain no wiki links with display-label pipes.
            if not rows or any(len(row) != len(rows[0]) for row in rows):
                raise ValueError(f'Malformed table: {rows}')
            blocks.append({'type': 'table', 'rows': rows}); continue
        elif re.match(r'^(?:[-*]|\d+\.) ', line):
            ordered = bool(re.match(r'^\d+\.', line))
            items = []
            pattern = r'^\d+\. ' if ordered else r'^[-*] '
            while i < len(lines) and re.match(pattern, lines[i].strip()):
                items.append(re.sub(pattern, '', lines[i].strip())); i += 1
            blocks.append({'type': 'list', 'ordered': ordered, 'items': items}); continue
        else:
            # Keep every paragraph line; unknown Markdown remains readable text.
            content = [line]
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(r'^(?:#|\||```|[-*] |\d+\. )', lines[i].strip()):
                content.append(lines[i].strip()); i += 1
            blocks.append({'type': 'paragraph', 'text': '\n'.join(content)}); continue
        i += 1
    return blocks


def parse_body(body):
    figures = re.findall(r'^```svg[^\n]*\n(.*?)^```', body, re.M | re.S)
    body = re.sub(r'^```svg[^\n]*\n.*?^```', '', body, flags=re.M | re.S)
    fields, current = {}, None
    for line in body.splitlines():
        match = re.match(r'^(' + '|'.join(FIELDS) + r')[：:]\s*(.*)', line)
        if match:
            current = match[1]; fields[current] = match[2]
        elif line.strip():
            if not current:
                raise ValueError(f'Unparsed entry content: {line}')
            fields[current] += '\n' + line
    return {'fields': fields, 'figures': [figure_ref(f) for f in figures]}


def compile_site():
    data = json.loads((ROOT / 'data/entries.json').read_text())
    bodies, sources = {}, []
    def source(path):
        raw = path.read_text(encoding='utf-8')
        sources.append({'path': str(path.relative_to(ROOT)), 'sha256': hashlib.sha256(raw.encode()).hexdigest()})
        return raw
    for domain in data['domains']:
        path = ROOT / 'domains' / Path(domain['file']).with_suffix('.md')
        text = source(path)
        sections = re.split(r'^@(intro|entry [a-z0-9-]+|outro)\s*$', text, flags=re.M)
        domain.update(intro=[], outro=[], source=str(path.relative_to(ROOT)))
        if sections[0].strip():
            raise ValueError(f'Content before section marker: {path}')
        for tag, body in zip(sections[1::2], sections[2::2]):
            if tag in ('intro', 'outro'):
                domain[tag] = parse_blocks(body)
            else:
                entry_id = tag.split()[1]
                if entry_id in bodies:
                    raise ValueError(f'Duplicate body: {entry_id}')
                bodies[entry_id] = parse_body(body)
    entry_ids = {e['id'] for e in data['entries']}
    principle_ids = {p['id'] for p in data['principles']}
    assert len(entry_ids) == len(data['entries']), 'Duplicate entry IDs'
    assert set(bodies) == entry_ids, 'Book body and index IDs differ'
    index_keys = json.loads((ROOT / 'data/index_keys.json').read_text())
    assert entry_ids <= set(index_keys), 'Missing pinyin index keys; run make index-keys'
    for entry in data['entries']:
        entry.update(bodies[entry['id']], index=index_keys[entry['id']])
        assert entry['fields'].get('原理'), f"Missing principle explanation: {entry['id']}"
        assert set(entry['related']) <= entry_ids, f"Unknown related entry: {entry['id']}"
        assert set(entry['principles']) <= principle_ids, f"Unknown principle: {entry['id']}"
    tiers = Counter(e['tier'] for e in data['entries'])
    stats = f"{len(data['domains'])} 个领域、{len(data['entries'])} 个词条（★ 核心 {tiers['A']} 条、标准 {tiers['B']} 条、短词条 {tiers['C']} 条）、{len(data['principles'])} 条第一性原理"
    rows = [f"| {d['num']:02d} | [{d['zh']}](#/chapter/{d['id']}) | {d['count']} | {d['tagline']} |" for d in data['domains']]
    rows.append(f"| | **合计** | **{len(data['entries'])}** | 另有 {len(data['principles'])} 条第一性原理 |")
    titles = {'howto': '怎么读这本书', 'map': '全书地图', 'principles-intro': '第一性原理导读'}
    data['documents'] = []
    for path in sorted((ROOT / 'front').glob('*.md')):
        raw = source(path)
        title = titles.get(path.stem, re.sub(r'^#\s*', '', raw.splitlines()[0]))
        if path.stem.startswith('sources-'):
            d = next(d for d in data['domains'] if d['id'] == path.stem[8:])
            title = d['zh'] + ' · 资料来源与核实记录'
        text = raw.replace('@@STATS@@', stats).replace('@@DOMAIN_TABLE@@', '\n'.join(rows))
        assert '@@' not in text, f'Unexpanded placeholder in {path}'
        data['documents'].append({'id': path.stem, 'title': title, 'source': str(path.relative_to(ROOT)), 'blocks': parse_blocks(text)})
    # Verify citations in every part, including front matter and chapter introductions.
    for record in sources:
        text = (ROOT / record['path']).read_text()
        for ref in re.findall(r'\[\[([^\]|]+)', text):
            assert (ref[2:] in principle_ids if ref.startswith('p:') else ref in entry_ids), f'Unknown cross reference: {ref}'
    data['readingOrder'] = ['document/howto', 'document/map', 'document/principles-intro']
    data['readingOrder'] += ['principle/' + p['id'] for p in data['principles']]
    for d in data['domains']:
        data['readingOrder'].append('chapter/' + d['id'])
        data['readingOrder'] += ['entry/' + e['id'] for e in data['entries'] if e['domain'] == d['id']]
    data['readingOrder'] += ['timeline', 'sources'] + ['document/sources-' + d['id'] for d in data['domains']] + ['index/zh', 'index/en', 'master']
    figures = {f for e in data['entries'] for f in e['figures']}
    for blocks in [d[k] for d in data['domains'] for k in ('intro', 'outro')] + [d['blocks'] for d in data['documents']]:
        figures.update(b['src'] for b in blocks if b['type'] == 'figure')
    all_figures = {str(p.relative_to(ROOT / 'assets')) for p in (ROOT / 'assets/figs').rglob('*.svg')}
    assert figures == all_figures, f'Unreachable figures: {all_figures - figures}'
    data['coverage'] = {'sources': sources, 'figures': sorted(figures), 'entries': len(entry_ids), 'principles': len(principle_ids)}
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT / 'web', OUT)
    shutil.copytree(ROOT / 'assets/figs', OUT / 'figs')
    shutil.copy(ROOT / 'front/cover.svg', OUT / 'cover.svg')
    (OUT / 'book.json').write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    (OUT / '.nojekyll').touch()
    print(f"Built complete book: {len(entry_ids)} entries, {len(data['documents'])} documents, {len(figures)} figures, {len(data['readingOrder'])} reading sections → build/web")
    return data


if __name__ == '__main__':
    compile_site()
