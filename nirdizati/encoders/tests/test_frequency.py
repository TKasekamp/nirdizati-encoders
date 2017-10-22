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
