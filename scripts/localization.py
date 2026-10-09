"""Deterministic translation inventory and strict build-time coverage checks.

English editorial data lives in translations/en.json. No model or network is
required to build the website. IDs, paths, formulas, and personal data stay out
of translation. Chinese remains the authoritative book manuscript.
"""
import re
import json
import hashlib
import xml.etree.ElementTree as ET
from pathlib import Path

HAN = re.compile(r'[\u3400-\u9fff]')
SKIP = {'id', 'file', 'source', 'src', 'related', 'cited_by', 'examples', 'readingOrder', 'coverage', 'index'}


def strings_in(value):
    if isinstance(value, str):
        for part in value.split('\n'):
            if HAN.search(part):
                yield part
    elif isinstance(value, list):
        for item in value:
            yield from strings_in(item)
    elif isinstance(value, dict):
        for key, item in value.items():
            if key not in SKIP:
                yield from strings_in(item)


def figure_strings(root):
    files = sorted((root / 'assets/figs').rglob('*.svg')) + [root / 'front/cover.svg']
    for path in files:
        tree = ET.parse(path)
        for node in tree.iter():
            if node.tag.rsplit('}', 1)[-1] in ('text', 'tspan', 'title', 'desc') and node.text and HAN.search(node.text):
                yield node.text


def translate_text(text, catalog):
    return '\n'.join(catalog.get(line, line) for line in text.split('\n'))


def validate_catalog(book, root, catalog):
    expected = set(strings_in(book)) | set(figure_strings(root))
    missing = sorted(s for s in expected if not catalog.get(s))
    assert not missing, f'Missing English translations ({len(missing)}): {missing[:4]}'
    untranslated = [s for s in expected if HAN.search(catalog[s])]
    assert not untranslated, f'Chinese remains in English translations: {untranslated[:4]}'
    refs = lambda text: sorted(re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', text))
    changed_refs = [s for s in expected if refs(s) != refs(catalog[s])]
    assert not changed_refs, f'Translated cross-reference IDs changed: {changed_refs[:4]}'
    urls=lambda text: sorted(u.rstrip('.,;') for u in re.findall(r'https?://[^\s<>\[\]()\u3400-\u9fff；，。]+',text))
    changed_urls=[s for s in expected if urls(s)!=urls(catalog[s])]
    assert not changed_urls, f'Translated source URLs changed: {changed_urls[:4]}'
    inventory=json.loads((root/'translations/ui.source.json').read_text())
    for path,digest in inventory['sources'].items():
        assert hashlib.sha256((root/path).read_bytes()).hexdigest()==digest, f'UI inventory stale: {path}; run node scripts/extract_ui.cjs'
    signature=lambda text: re.sub(r'\{\d+\}','{}',text.strip())
    normalized={signature(key):value for key,value in catalog.items()}
    missing_ui=[text for text in inventory['strings'] if not normalized.get(signature(text))]
    assert not missing_ui, f'Missing UI translations ({len(missing_ui)}): {missing_ui[:5]}'
    incomplete_ui=[text for text in inventory['strings'] if HAN.search(normalized[signature(text)])]
    assert not incomplete_ui, f'Chinese remains in English UI: {incomplete_ui[:4]}'
    tokens=[s for s in expected if 'REF_TOKEN_' in catalog[s]]
    assert not tokens, f'Unexpanded translation references: {tokens[:4]}'
    placeholders = lambda text: sorted(re.findall(r'\{\d+\}', text))
    broken_templates = [key for key, value in catalog.items() if placeholders(key) and
                        (placeholders(key) != placeholders(value) or '{{' in value or '}}' in value)]
    assert not broken_templates, f'Changed UI placeholders: {broken_templates[:4]}'
    return len(expected)


def write_english_figures(root, out, catalog):
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    for path in sorted((root / 'assets/figs').rglob('*.svg')) + [root / 'front/cover.svg']:
        tree = ET.parse(path)
        viewbox=[float(n) for n in tree.getroot().get('viewBox','0 0 1000 1000').split()]
        canvas_area=viewbox[2]*viewbox[3]
        rectangles=[]
        text_boxes=[]
        for label in tree.iter():
            if label.tag.rsplit('}',1)[-1] not in ('text','tspan') or not label.text:continue
            try:
                x,y,size=(float(label.get(key,default)) for key,default in [('x','0'),('y','0'),('font-size','12')])
                width=sum(1 if HAN.match(c) else .55 for c in label.text)*size
                anchor=label.get('text-anchor','start')
                left=x-width/2 if anchor=='middle' else x-width if anchor=='end' else x
                text_boxes.append((label,left,left+width,y,size))
            except ValueError:pass
        for shape in tree.iter():
            if shape.tag.rsplit('}',1)[-1]=='rect':
                try:
                    rectangle=tuple(float(shape.get(key,'0')) for key in ('x','y','width','height'))
                    if rectangle[2]*rectangle[3]<canvas_area*.65:rectangles.append(rectangle)
                except ValueError:pass
        for node in tree.iter():
            tag = node.tag.rsplit('}', 1)[-1]
            if tag not in ('text', 'tspan', 'title', 'desc') or not node.text or not HAN.search(node.text):
                continue
            original=node.text
            node.text=catalog.get(original,original)
            if tag in ('text','tspan'):
                size=float(node.get('font-size','12'))
                original_width=sum(1 if HAN.match(c) else .55 for c in original)*size
                target_width=len(node.text)*size*.53
                available=max(original_width,64)
                try:
                    x,y=float(node.get('x','0')),float(node.get('y','0'))
                    anchor=node.get('text-anchor','start')
                    left_limit,right_limit=viewbox[0]+8,viewbox[0]+viewbox[2]-8
                    original_left=x-original_width/2 if anchor=='middle' else x-original_width if anchor=='end' else x
                    original_right=original_left+original_width
                    # Share horizontal whitespace with nearby labels, keeping their
                    # original bounding boxes clear rather than squeezing English
                    # into the exact number of Chinese glyphs.
                    for other,left,right,baseline,other_size in text_boxes:
                        if other is node or abs(y-baseline)>max(size,other_size):continue
                        if right<=original_left:left_limit=max(left_limit,(right+original_left)/2+3)
                        elif left>=original_right:right_limit=min(right_limit,(original_right+left)/2-3)
                    # Timeline labels must also stop before an adjacent panel,
                    # even when that panel has no text on the same baseline.
                    for left,top,width,height in rectangles:
                        if not top<y<top+height:continue
                        if left>=original_right:right_limit=min(right_limit,left-6)
                        elif left+width<=original_left:left_limit=max(left_limit,left+width+6)
                    room=2*min(x-left_limit,right_limit-x) if anchor=='middle' else x-left_limit if anchor=='end' else right_limit-x
                    available=max(original_width,min(room,max(original_width*2.4,128)))
                    containers=[r for r in rectangles if r[0]<x<r[0]+r[2] and r[1]<y<r[1]+r[3] and r[3]>size]
                    if containers:
                        left,top,width,height=min(containers,key=lambda r:r[2]*r[3])
                        anchor=node.get('text-anchor','start')
                        room=2*min(x-left,left+width-x) if anchor=='middle' else x-left if anchor=='end' else left+width-x
                        available=max(original_width,room-12)
                except ValueError:pass
                if target_width>available:
                    node.set('font-size',str(round(max(8,size*available/target_width),2)))
                    if len(node.text)*float(node.get('font-size'))*.53>available*1.05:
                        node.set('textLength',str(round(available,2)))
                        node.set('lengthAdjust','spacingAndGlyphs')
        relative=path.relative_to(root/'assets') if path.parent!=root/'front' else Path('cover.svg')
        target=out/'en'/relative
        target.parent.mkdir(parents=True,exist_ok=True)
        tree.write(target,encoding='unicode',xml_declaration=False)
