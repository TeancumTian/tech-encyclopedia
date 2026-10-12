"""Plain HTML pages for every entry and principle, in Chinese and English.

The interactive reader is a single page that needs JavaScript and keeps its
address after "#", so search engines, link previews and readers without
JavaScript cannot reach an individual entry. These pages give each entry a
real address with the same manuscript text, and link back to the interactive
reader. They carry no scripts and store nothing.
"""
import html
import json
import re
from pathlib import Path

FIELDS = [('原理', 'why'), ('怎么工作', 'how'), ('年份人物', 'history'), ('改变了', 'impact'), ('注意', 'caution')]
LABELS = {
    'zh': {
        'lang': 'zh-CN', 'locale': 'zh_CN', 'site': '原来如此 · 互动科技百科', 'brand': '原来如此', 'book': '近现代科技百科全书',
        'why': '为什么行得通', 'how': '它是怎么工作的', 'history': '关键年份与人物', 'impact': '改变了什么', 'caution': '常见误解',
        'related': '相关词条', 'principles': '用到的底层原理', 'open': '打开互动学习版', 'all': '全部词条', 'other': 'English',
        'cta': '在互动学习版里继续：做笔记、翻卡复习、动手实验', 'figure': '图解', 'year': '关键年份', 'core': '核心词条',
        'index_title': '全部词条目录', 'index_intro': '{entries} 个词条和 {principles} 条底层原理的纯文本目录。每个词条都有独立网页，也可以进入互动学习版阅读、做笔记和复习。',
        'principle_kicker': '底层原理', 'principle_entries': '用到这条原理的 {count} 个词条', 'principle_list': '底层原理',
        'footer': '© 2026 Teancum Tian · 基于《近现代科技百科全书》· 保留所有权利。历史与数字沿用书稿核实时间。',
    },
    'en': {
        'lang': 'en', 'locale': 'en_US', 'site': 'Now I See — The Technology Atlas', 'brand': 'Now I See', 'book': 'An Illustrated Encyclopedia of Modern Technology',
        'why': 'Why it works', 'how': 'How it works', 'history': 'Key dates and people', 'impact': 'What it changed', 'caution': 'A common misconception',
        'related': 'Related entries', 'principles': 'Underlying principles', 'open': 'Open the interactive version', 'all': 'All entries', 'other': '中文',
        'cta': 'Continue in the interactive version: take notes, review with cards and run experiments', 'figure': 'Diagram', 'year': 'Key year', 'core': 'Core entry',
        'index_title': 'All entries', 'index_intro': 'A plain-text directory of {entries} entries and {principles} underlying principles. Every entry has its own page, and you can also read, take notes and review in the interactive version.',
        'principle_kicker': 'Underlying principle', 'principle_entries': '{count} entries that use this principle', 'principle_list': 'Underlying principles',
        'footer': '© 2026 Teancum Tian · Based on the Chinese manuscript; all rights reserved. English is a machine-assisted, edited translation. Dates and figures follow the manuscript’s verification dates.',
    },
}
INLINE = re.compile(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]|\*\*(.+?)\*\*|`([^`]+)`|(https?://[^\s<>；，。)]+)|(^|[^*\w])\*([^*\s][^*]*?)\*(?![*\w])')
esc = lambda value: html.escape(str(value), quote=True)


def inline(text, names, entry_href, principle_href):
    """Escape everything, then format the manuscript's small inline syntax."""
    out, position = [], 0
    for match in INLINE.finditer(text):
        out.append(esc(text[position:match.start()]))
        if match[1]:
            ref = match[1]
            label = esc(match[2] or names.get(ref, ref))
            if ref not in names:
                out.append(label)
            else:
                href = principle_href(ref[2:]) if ref.startswith('p:') else entry_href(ref)
                out.append(f'<a href="{esc(href)}">{label}</a>')
        elif match[3]:
            out.append('<strong>' + inline(match[3], names, entry_href, principle_href) + '</strong>')
        elif match[4]:
            out.append('<code>' + esc(match[4]) + '</code>')
        elif match[5]:
            out.append(f'<a href="{esc(match[5])}" rel="noopener">{esc(match[5])}</a>')
        else:
            out.append(esc(match[6]) + '<em>' + inline(match[7], names, entry_href, principle_href) + '</em>')
        position = match.end()
    return ''.join(out) + esc(text[position:])


def json_ld(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')


def page(lang, title, description, path, other_path, site_url, root, index_href, body, structured):
    t, o = LABELS[lang], LABELS['en' if lang == 'zh' else 'zh']
    url, other = site_url + path, site_url + other_path
    zh_url, en_url = (url, other) if lang == 'zh' else (other, url)
    description = ' '.join(description.split())
    if len(description) > 160:
        description = description[:157].rstrip() + '…'
    return f'''<!doctype html>
<html lang="{t['lang']}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{esc(url)}">
<link rel="alternate" hreflang="zh-CN" href="{esc(zh_url)}">
<link rel="alternate" hreflang="en" href="{esc(en_url)}">
<link rel="alternate" hreflang="x-default" href="{esc(zh_url)}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="{esc(t['site'])}">
<meta property="og:locale" content="{t['locale']}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{esc(url)}">
<meta name="twitter:card" content="summary">
<link rel="stylesheet" href="{root}static.css">
<script type="application/ld+json">{json_ld(structured)}</script>
</head>
<body>
<header class="top"><a class="brand" href="{root}"><span aria-hidden="true">✳</span> {esc(t['brand'])}</a><nav><a href="{index_href}">{esc(t['all'])}</a><a href="{esc(root + other_path)}" lang="{o['lang']}" hreflang="{o['lang']}">{esc(t['other'])}</a></nav></header>
<main>
{body}
</main>
<footer>{esc(t['footer'])}</footer>
</body>
</html>
'''


def write_static_pages(out, data, catalog, site_url):
    """Write e/<id>.html, p/<id>.html and their English twins under en/. Returns sitemap rows."""
    site_url = site_url.rstrip('/') + '/'
    entries = {e['id']: e for e in data['entries']}
    principles = {p['id']: p for p in data['principles']}
    domains = {d['id']: d for d in data['domains']}
    english = lambda text: '\n'.join(catalog.get(line, line) for line in str(text).split('\n'))
    rows, count = [], 0
    for lang in ('zh', 'en'):
        t = LABELS[lang]
        base = '' if lang == 'zh' else 'en/'
        root = '../' if lang == 'zh' else '../../'
        other_base = 'en/' if lang == 'zh' else ''
        tr = (lambda text: text) if lang == 'zh' else english
        entry_name = (lambda e: e['zh']) if lang == 'zh' else (lambda e: e['en'])
        second_name = (lambda e: e['en']) if lang == 'zh' else (lambda e: e['zh'])
        second_lang = 'en' if lang == 'zh' else 'zh-CN'
        names = {**{i: entry_name(e) for i, e in entries.items()}, **{'p:' + i: (p['zh'] if lang == 'zh' else p['en']) for i, p in principles.items()}}
        domain_name = lambda d: d['zh'] if lang == 'zh' else d['en']
        term_set = {'@type': 'DefinedTermSet', 'name': t['book'], 'url': site_url}
        for kind in ('e', 'p'):
            (out / base / kind).mkdir(parents=True, exist_ok=True)

        # Entries
        fmt = lambda text: inline(text, names, lambda i: f'./{i}.html', lambda i: f'../p/{i}.html')
        for e in data['entries']:
            domain = domains[e['domain']]
            name, definition = entry_name(e), tr(e['definition'])
            parts = [f'<p class="crumb"><a href="./index.html">{esc(t["all"])}</a> / {esc(domain_name(domain))} / {esc(tr(e["subcategory"]))}</p>',
                     f'<h1>{esc(name)}</h1>', f'<p class="secondary" lang="{second_lang}">{esc(second_name(e))}</p>',
                     f'<p class="definition">{fmt(definition)}</p>']
            facts = []
            if e.get('year') is not None:
                facts.append(f'{esc(t["year"])} {esc(e["year"])}')
            if e['tier'] == 'A':
                facts.append('★ ' + esc(t['core']))
            if facts:
                parts.append(f'<p class="facts">{" · ".join(facts)}</p>')
            caption = e['fields'].get('图注')
            for field, key in FIELDS:
                text = e['fields'].get(field)
                if not text:
                    continue
                paragraphs = ''.join(f'<p>{fmt(re.sub(r"^[-*] ", "", line))}</p>' for line in tr(text).split('\n') if line.strip())
                parts.append(f'<section class="{key}"><h2>{esc(t[key])}</h2>{paragraphs}</section>')
                if key == 'how':
                    for src in e['figures']:
                        label = fmt(tr(caption)) if caption else f'{esc(name)} · {esc(t["figure"])}'
                        parts.append(f'<figure><a href="../{esc(src)}"><img src="../{esc(src)}" alt="{esc(name)} · {esc(t["figure"])}" loading="lazy"></a><figcaption>{label}</figcaption></figure>')
            if e['related']:
                links = ''.join(f'<li><a href="./{esc(i)}.html">{esc(names[i])}</a></li>' for i in e['related'])
                parts.append(f'<section class="links"><h2>{esc(t["related"])}</h2><ul>{links}</ul></section>')
            links = ''.join(f'<li><a href="../p/{esc(i)}.html">{esc(names["p:" + i])}</a></li>' for i in e['principles'])
            parts.append(f'<section class="links"><h2>{esc(t["principles"])}</h2><ul>{links}</ul></section>')
            parts.append(f'<p class="cta"><a class="button" href="{root}#/entry/{esc(e["id"])}">{esc(t["cta"])} →</a></p>')
            path, other = f'{base}e/{e["id"]}.html', f'{other_base}e/{e["id"]}.html'
            structured = {'@context': 'https://schema.org', '@type': 'DefinedTerm', 'name': name, 'alternateName': second_name(e),
                          'description': definition, 'inLanguage': t['lang'], 'url': site_url + path, 'inDefinedTermSet': term_set}
            title = f'{name} · {second_name(e)} | {t["brand"]}'
            (out / path).write_text(page(lang, title, definition, path, other, site_url, root, './index.html', '\n'.join(parts), structured), encoding='utf-8')
            rows.append((path, other)); count += 1

        # Principles
        fmt = lambda text: inline(text, names, lambda i: f'../e/{i}.html', lambda i: f'./{i}.html')
        for p in data['principles']:
            name = names['p:' + p['id']]
            second = p['en'] if lang == 'zh' else p['zh']
            statement = tr(p['statement'])
            users = [e for e in data['entries'] if p['id'] in e['principles']]
            links = ''.join(f'<li><a href="../e/{esc(e["id"])}.html">{esc(entry_name(e))}</a></li>' for e in users)
            body = '\n'.join([
                f'<p class="crumb"><a href="../e/index.html">{esc(t["all"])}</a> / {esc(t["principle_kicker"])} / {esc(tr(p["group"]))}</p>',
                f'<h1>{esc(name)}</h1>', f'<p class="secondary" lang="{second_lang}">{esc(second)}</p>',
                f'<p class="definition">{fmt(statement)}</p>',
                f'<section class="links"><h2>{esc(t["principle_entries"].format(count=len(users)))}</h2><ul>{links}</ul></section>',
                f'<p class="cta"><a class="button" href="{root}#/principle/{esc(p["id"])}">{esc(t["open"])} →</a></p>'])
            path, other = f'{base}p/{p["id"]}.html', f'{other_base}p/{p["id"]}.html'
            structured = {'@context': 'https://schema.org', '@type': 'DefinedTerm', 'name': name, 'alternateName': second,
                          'description': statement, 'inLanguage': t['lang'], 'url': site_url + path, 'inDefinedTermSet': term_set}
            (out / path).write_text(page(lang, f'{name} · {second} | {t["brand"]}', statement, path, other, site_url, root, '../e/index.html', body, structured), encoding='utf-8')
            rows.append((path, other)); count += 1

        # Directory of every page
        sections = []
        for d in data['domains']:
            groups = []
            for sub in d['subcategories']:
                links = ''.join(f'<li><a href="./{esc(e["id"])}.html">{esc(entry_name(e))}</a>{" ★" if e["tier"] == "A" else ""}</li>'
                                for e in data['entries'] if e['domain'] == d['id'] and e['subcategory'] == sub)
                groups.append(f'<h3>{esc(tr(sub))}</h3><ul>{links}</ul>')
            sections.append(f'<section class="links" id="{esc(d["id"])}"><h2>{d["num"]:02d} · {esc(domain_name(d))}</h2><p>{esc(tr(d["tagline"]))}</p>{"".join(groups)}</section>')
        links = ''.join(f'<li><a href="../p/{esc(p["id"])}.html">{esc(names["p:" + p["id"]])}</a></li>' for p in data['principles'])
        sections.append(f'<section class="links"><h2>{esc(t["principle_list"])}</h2><ul>{links}</ul></section>')
        intro = t['index_intro'].format(entries=len(entries), principles=len(principles))
        body = '\n'.join([f'<h1>{esc(t["index_title"])}</h1>', f'<p class="definition">{esc(intro)}</p>',
                          f'<p class="cta"><a class="button" href="{root}">{esc(t["open"])} →</a></p>', *sections])
        path, other = f'{base}e/index.html', f'{other_base}e/index.html'
        structured = {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': t['index_title'], 'description': intro,
                      'inLanguage': t['lang'], 'url': site_url + path, 'isPartOf': {'@type': 'WebSite', 'name': t['site'], 'url': site_url}}
        (out / path).write_text(page(lang, f'{t["index_title"]} | {t["brand"]}', intro, path, other, site_url, root, './index.html', body, structured), encoding='utf-8')
        rows.append((path, other)); count += 1

    # Sitemap: every page once, each with both language versions.
    def url_node(path, zh, en):
        return (f'<url><loc>{esc(site_url + path)}</loc>'
                f'<xhtml:link rel="alternate" hreflang="zh-CN" href="{esc(site_url + zh)}"/>'
                f'<xhtml:link rel="alternate" hreflang="en" href="{esc(site_url + en)}"/></url>')
    nodes = [f'<url><loc>{esc(site_url)}</loc></url>']
    for path, other in rows:
        zh, en = (other, path) if path.startswith('en/') else (path, other)
        nodes.append(url_node(path, zh, en))
    (out / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
                                     + '\n'.join(nodes) + '\n</urlset>\n', encoding='utf-8')
    return count
