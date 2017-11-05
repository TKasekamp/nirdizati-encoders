from unittest import TestCase

from nirdizati.encoders import boolean
from nirdizati.encoders.tests.setup import sample_trace, general_example


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


class TestBooleanGeneral(TestCase):
    def test_shape(self):
        df = boolean.encode_trace(general_example())

        names = ['register request', 'examine casually', 'check ticket', 'decide',
                 'reinitiate request', 'examine thoroughly', 'pay compensation',
                 'reject request', 'case_id', 'event_nr', 'remaining_time',
                 'elapsed_time']
        self.assertListEqual(names, df.columns.values.tolist())
        self.assertEqual((42, 12), df.shape)

    def test_row(self):
        df = boolean.encode_trace(general_example())
        row = df[(df.event_nr == 2) & (df.case_id == 2)].iloc[0]

        self.assertTrue(row['register request'])
        self.assertFalse(row['examine casually'])
        self.assertTrue(row['check ticket'])
        self.assertFalse(row['decide'])
        self.assertEqual(2400.0, row.elapsed_time)
        self.assertEqual(777180.0, row.remaining_time)
