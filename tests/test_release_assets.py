import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from build_web import version_assets


class ReleaseAssetTests(unittest.TestCase):
    def make_release(self, root, translation='English'):
        root.mkdir()
        files = {
            'index.html': '<script src="./app.js"></script><link href="./i18n.css">',
            'app.js': "import './i18n.js'; fetch('./book.json'); fetch('./en.json'); fetch('./runtime-config.json', {cache:'no-store'});",
            'i18n.js': 'export const ready=true;',
            'i18n.css': 'body {color: green}',
            'book.json': '{}',
            'en.json': '{"title":"' + translation + '"}',
            'runtime-config.json': '{"progressMode":"browser"}',
        }
        for name, text in files.items():
            (root / name).write_text(text)
        version_assets(root)
        return (root / 'index.html').read_text(), (root / 'app.js').read_text()

    def test_entrypoint_modules_styles_and_text_share_one_version(self):
        with tempfile.TemporaryDirectory() as directory:
            html, js = self.make_release(Path(directory) / 'release')
        versions = re.findall(r'\?v=([a-f0-9]{16})', html + js)
        self.assertEqual(len(versions), 5)
        self.assertEqual(len(set(versions)), 1)
        self.assertIn("'./runtime-config.json'", js)
        self.assertIn("'./i18n.js?v=", js)

    def test_translation_edits_invalidate_cached_modules_deterministically(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = self.make_release(root / 'first')
            same = self.make_release(root / 'same')
            changed = self.make_release(root / 'changed', 'Revised English')
        self.assertEqual(first, same)
        self.assertNotEqual(first, changed)


if __name__ == '__main__':
    unittest.main()
