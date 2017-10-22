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

    def test_shape(self):
        encoder = SimpleIndexEncoder()
        df = encoder.encode_trace(self.frame)

        self.assertEqual((3, 5), df.shape)
        # Checking one row
        row = df[(df.event_nr == 1) & (df.case_id == "Case10")].iloc[0]

        self.assertEqual(8, row.prefix_1)
        self.assertEqual(0.0, row.elapsed_time)
        self.assertEqual(1447140.0, row.remaining_time)
