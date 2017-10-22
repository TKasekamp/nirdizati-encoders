from unittest import TestCase

from nirdizati.encoders import simple_index
from nirdizati.encoders.tests.setup import data_frame, sample_trace


class TestSimpleIndex(TestCase):
    def setUp(self):
        self.frame = data_frame()

    def test_has_columns(self):
        df = simple_index.encode_trace(self.frame)
        # Column check
        self.assertIn("case_id", df.columns.values)
        self.assertIn("event_nr", df.columns.values)
        self.assertIn("remaining_time", df.columns.values)
        self.assertIn("elapsed_time", df.columns.values)
        self.assertIn("prefix_1", df.columns.values)
        self.assertEqual(5, df.columns.size)

    def test_prefix_length(self):
        df = simple_index.encode_trace(self.frame, 3)
        # Column check
        self.assertIn("prefix_1", df.columns.values)
        self.assertIn("prefix_2", df.columns.values)
        self.assertIn("prefix_3", df.columns.values)
        self.assertEqual(7, df.columns.size)

    def test_shape(self):
        df = simple_index.encode_trace(self.frame)

        self.assertEqual((3, 5), df.shape)
        # Checking one row
        row = df[(df.event_nr == 1) & (df.case_id == "Case10")].iloc[0]

        self.assertEqual(8, row.prefix_1)
        self.assertEqual(0.0, row.elapsed_time)
        self.assertEqual(1447140.0, row.remaining_time)

    def test_encodes_next_activity(self):
        """Encodes for next activity"""
        df = simple_index.encode_trace(sample_trace(), next_activity=True)

        # Column check
        self.assertNotIn("remaining_time", df.columns.values)
        self.assertNotIn("elapsed_time", df.columns.values)
        self.assertIn("label", df.columns.values)
        self.assertIn("prefix_1", df.columns.values)
        self.assertIn("prefix_2", df.columns.values)
        self.assertIn("prefix_3", df.columns.values)
        self.assertEqual((8, 6), df.shape)

        # Checking one row
        row = df[(df.event_nr == 1) & (df.case_id == 1)].iloc[0]
        self.assertEqual(0, row.prefix_1)
        self.assertEqual(0, row.prefix_2)
        self.assertEqual(0, row.prefix_3)
        self.assertEqual(1, row.label)
        self.assertEqual(1, row.case_id)
        self.assertEqual(1, row.event_nr)
