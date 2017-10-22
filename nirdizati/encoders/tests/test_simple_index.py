from unittest import TestCase

from nirdizati.encoders.tests.helper import data_frame
from nirdizati.encoders import SimpleIndexEncoder


class TestSimpleIndex(TestCase):
    def setUp(self):
        self.frame = data_frame()

    def test_has_columns(self):
        encoder = SimpleIndexEncoder()
        df = encoder.encode_trace(self.frame)
        # Column check
        self.assertIn("case_id", df.columns.values)
        self.assertIn("event_nr", df.columns.values)
        self.assertIn("remaining_time", df.columns.values)
        self.assertIn("elapsed_time", df.columns.values)
        self.assertIn("prefix_1", df.columns.values)
        self.assertEqual(5, df.columns.size)

    def test_prefix_length(self):
        encoder = SimpleIndexEncoder()
        df = encoder.encode_trace(self.frame, 3)
        # Column check
        self.assertIn("prefix_1", df.columns.values)
        self.assertIn("prefix_2", df.columns.values)
        self.assertIn("prefix_3", df.columns.values)
        self.assertEqual(7, df.columns.size)
