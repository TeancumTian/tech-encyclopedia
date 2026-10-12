import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from static_pages import inline, page, json_ld

NAMES = {'cpu': '中央处理器', 'p:energy': '能量守恒'}
fmt = lambda text: inline(text, NAMES, lambda i: f'./{i}.html', lambda i: f'../p/{i}.html')


class StaticPageTests(unittest.TestCase):
    def test_manuscript_text_is_escaped_and_never_becomes_markup(self):
        html = fmt('<img src=x onerror=alert(1)> & "quoted" [[cpu|<b>芯片</b>]]')
        self.assertNotIn('<img', html)
        self.assertNotIn('<b>', html)
        self.assertIn('&lt;img', html)
        self.assertIn('&amp;', html)

    def test_references_emphasis_code_and_urls_are_formatted(self):
        self.assertEqual(fmt('见 [[cpu]] 与 [[p:energy|守恒]]'),
                         '见 <a href="./cpu.html">中央处理器</a> 与 <a href="../p/energy.html">守恒</a>')
        self.assertEqual(fmt('**重点** 和 `code` 和 *Nature*'), '<strong>重点</strong> 和 <code>code</code> 和 <em>Nature</em>')
        self.assertEqual(fmt('[[missing|标签]] 与 [[unknown]]'), '标签 与 unknown')
        self.assertEqual(fmt('2 * 3 * 4'), '2 * 3 * 4')
        self.assertIn('<a href="https://example.com/a?b=1" rel="noopener">', fmt('来源 https://example.com/a?b=1。'))

    def test_page_head_carries_canonical_language_links_and_a_short_description(self):
        text = page('zh', '标题 <x>', '长' * 400, 'e/cpu.html', 'en/e/cpu.html', 'https://example.org/book/', '../', './index.html', '<h1>x</h1>', {'name': '</script>'})
        self.assertIn('<link rel="canonical" href="https://example.org/book/e/cpu.html">', text)
        self.assertIn('hreflang="en" href="https://example.org/book/en/e/cpu.html"', text)
        self.assertIn('<title>标题 &lt;x&gt;</title>', text)
        self.assertIn('href="../en/e/cpu.html" lang="en"', text)
        description = text.split('<meta name="description" content="')[1].split('"')[0]
        self.assertLessEqual(len(description), 160)
        self.assertNotIn('</script>"', text)
        self.assertIn('\\u003c/script>', json_ld({'name': '</script>'}))
        self.assertNotIn('<script src', text)


if __name__ == '__main__':
    unittest.main()
