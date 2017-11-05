from unittest import TestCase

from nirdizati.encoders import boolean
from nirdizati.encoders.tests.setup import sample_trace


class TestBoolean(TestCase):
    def test_shape(self):
        df = boolean.encode_trace(sample_trace())

        self.assertIn("case_id", df.columns.values)
        self.assertIn("event_nr", df.columns.values)
        self.assertIn("remaining_time", df.columns.values)
        self.assertIn("elapsed_time", df.columns.values)
        for name in ['A', 'B', 'C', 'D']:
            self.assertIn(name, df.columns.values)
        self.assertEqual((12, 8), df.shape)

    def test_row(self):
        df = boolean.encode_trace(sample_trace())
        row = df[(df.event_nr == 2) & (df.case_id == 2)].iloc[0]

        self.assertTrue(row['A'])
        self.assertTrue(row['C'])
        self.assertFalse(row['B'])
        self.assertFalse(row['D'])
        self.assertEqual(1.0, row.elapsed_time)
        self.assertEqual(1.0, row.remaining_time)
