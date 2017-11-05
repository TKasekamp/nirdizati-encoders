from unittest import TestCase

from nirdizati.encoders import frequency
from nirdizati.encoders.tests.setup import data_frame, general_example


class TestFrequency(TestCase):
    def test_has_columns(self):
        df = frequency.encode_trace(data_frame())
        # Column check
        self.assertIn("case_id", df.columns.values)
        self.assertIn("event_nr", df.columns.values)
        self.assertIn("remaining_time", df.columns.values)
        self.assertIn("elapsed_time", df.columns.values)
        self.assertEqual(16, df.columns.size)

    def test_shape(self):
        df = frequency.encode_trace(data_frame())

        self.assertEqual((108, 16), df.shape)
        # Checking one row
        row = df[(df.event_nr == 1) & (df.case_id == "Case10")].iloc[0]

        self.assertEqual(1, row['Turning & Milling - Machine 9'])
        self.assertEqual(0.0, row.elapsed_time)
        self.assertEqual(1447140.0, row.remaining_time)


class TestFrequencyGeneral(TestCase):
    def test_shape(self):
        df = frequency.encode_trace(general_example())

        names = ['register request', 'examine casually', 'check ticket', 'decide',
                 'reinitiate request', 'examine thoroughly', 'pay compensation',
                 'reject request', 'case_id', 'event_nr', 'remaining_time',
                 'elapsed_time']
        self.assertListEqual(names, df.columns.values.tolist())
        self.assertEqual((42, 12), df.shape)

    def test_row(self):
        df = frequency.encode_trace(general_example())
        row = df[(df.event_nr == 2) & (df.case_id == 2)].iloc[0]

        self.assertEqual(1.0, row['register request'])
        self.assertEqual(0.0, row['examine casually'])
        self.assertEqual(1.0, row['check ticket'])
        self.assertEqual(0.0, row['decide'])
        self.assertEqual(2400.0, row.elapsed_time)
        self.assertEqual(777180.0, row.remaining_time)
