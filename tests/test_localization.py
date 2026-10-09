import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from translate_english import explicit_magnitudes, protect_references


class TranslationPreparationTests(unittest.TestCase):
    def test_chinese_numeric_ranges_apply_the_unit_to_both_endpoints(self):
        self.assertEqual(explicit_magnitudes('20–50 亿').strip(), '2–5 billion')
        self.assertEqual(explicit_magnitudes('2–5 亿').strip(), '200–500 million')
        self.assertEqual(explicit_magnitudes('10 亿').strip(), '1 billion')

    def test_compound_quantities_are_not_partially_replaced(self):
        self.assertEqual(explicit_magnitudes('成百上千').strip(), 'hundreds or thousands')
        self.assertEqual(explicit_magnitudes('成千上万').strip(), 'thousands or tens of thousands')
        self.assertEqual(explicit_magnitudes('数百亿').strip(), 'tens of billions')
        self.assertEqual(explicit_magnitudes('上千万').strip(), 'over ten million')
        self.assertIn('milliampere-hours', explicit_magnitudes('3000 毫安时'))

    def test_reference_tokens_keep_ids_and_use_contextual_labels(self):
        batch = ['靠 [[p:locality|局部性]] 加速，见 [[cache]]。']
        data, replacements, meanings = protect_references(
            batch, {'p:locality': 'Locality & caching', 'cache': 'Cache'}, {'局部性': 'locality'})
        self.assertEqual(meanings['REF_TOKEN_0_X'], 'locality')
        restored = data['0']
        for token, reference in replacements.items():
            restored = restored.replace(token, reference)
        self.assertEqual(restored, '靠 [[p:locality|locality]] 加速，见 [[cache]]。')


if __name__ == '__main__':
    unittest.main()
