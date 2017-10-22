from unittest import TestCase

from nirdizati.encoders import FrequencyEncoder
from nirdizati.encoders.tests.helper import data_frame


class TestFrequency(TestCase):
    def setUp(self):
        self.frame = data_frame()

    def test_has_columns(self):
        encoder = FrequencyEncoder()
        df = encoder.encode_trace(self.frame)
        # Column check
        self.assertIn("case_id", df.columns.values)
        self.assertIn("event_nr", df.columns.values)
        self.assertIn("remaining_time", df.columns.values)
        self.assertIn("elapsed_time", df.columns.values)
        self.assertEqual(16, df.columns.size)

    def test_shape(self):
        encoder = FrequencyEncoder()
        df = encoder.encode_trace(self.frame)

        self.assertEqual((108, 16), df.shape)
        # Checking one row
        row = df[(df.event_nr == 1) & (df.case_id == "Case10")].iloc[0]

        self.assertEqual(1, row['Turning & Milling - Machine 9'])
        self.assertEqual(0.0, row.elapsed_time)
        self.assertEqual(1447140.0, row.remaining_time)
