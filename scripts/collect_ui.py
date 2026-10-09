"""Finish an AST-extracted UI inventory without any HTML/runtime dependencies."""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

values=set()
class TextExtractor(HTMLParser):
    def handle_data(self,text):
        if re.search(r'[\u3400-\u9fff]',text):values.add(text.strip())
    def handle_starttag(self,tag,attributes):
        for key,value in attributes:
            if key in ('placeholder','aria-label','alt','title') and value and re.search(r'[\u3400-\u9fff]',value):values.add(value.strip())

data=json.load(sys.stdin)
for text in data['strings']:
    if '<' in text and '>' in text:TextExtractor().feed(text)
    else:values.add(text.strip())
output={'sources':data['sources'],'strings':sorted(values)}
Path('translations/ui.source.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
print(f'Extracted {len(values)} UI strings/templates; update translations before building.')
