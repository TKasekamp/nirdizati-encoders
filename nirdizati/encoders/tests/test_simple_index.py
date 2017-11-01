from unittest import TestCase

from nirdizati.encoders import simple_index
from nirdizati.encoders.tests.setup import prod_xes


class TestSimpleIndex(TestCase):
    def test_has_columns(self):
        df = simple_index.encode_trace(prod_xes())

        self.assertIn("case_id", df.columns.values)
        self.assertIn("event_nr", df.columns.values)
        self.assertIn("remaining_time", df.columns.values)
        self.assertIn("elapsed_time", df.columns.values)
        self.assertIn("prefix_1", df.columns.values)
        self.assertEqual(5, df.columns.size)

    def test_prefix_length(self):
        df = simple_index.encode_trace(prod_xes(), prefix_length=3)

        self.assertIn("prefix_1", df.columns.values)
        self.assertIn("prefix_2", df.columns.values)
        self.assertIn("prefix_3", df.columns.values)
        self.assertEqual((28, 7), df.shape)

    def test_shape(self):
        df = simple_index.encode_trace(prod_xes())

        self.assertEqual((29, 5), df.shape)
        # Checking one row
        row = df[(df.event_nr == 1) & (df.case_id == "Case10")].iloc[0]

        self.assertEqual(8, row.prefix_1)
        self.assertEqual(0.0, row.elapsed_time)
        self.assertEqual(1447140.0, row.remaining_time)

    def test_encodes_next_activity(self):
        """Encodes for next activity"""
        df = simple_index.encode_trace(prod_xes(), next_activity=True)

        self.assertEqual((29, 3), df.shape)
        self.assertNotIn("remaining_time", df.columns.values)
        self.assertNotIn("elapsed_time", df.columns.values)
        self.assertIn("label", df.columns.values)
        self.assertNotIn("prefix_1", df.columns.values)

        # Checking one row
        row = df[df.case_id == 'Case10'].iloc[0]
        self.assertEqual(8, row.label)
        self.assertEqual(1, row.event_nr)

    def test_encodes_next_activity_prefix(self):
        """Encodes for next activity with prefix length"""
        df = simple_index.encode_trace(prod_xes(), prefix_length=6, next_activity=True)

        self.assertEqual((29, 8), df.shape)
        self.assertNotIn("remaining_time", df.columns.values)
        self.assertNotIn("elapsed_time", df.columns.values)
        self.assertIn("label", df.columns.values)
        self.assertIn("prefix_1", df.columns.values)
        self.assertIn("prefix_2", df.columns.values)
        self.assertIn("prefix_3", df.columns.values)

        # Checking one row
        row = df[df.case_id == 'Case10'].iloc[0]
        self.assertEqual(8, row.prefix_1)
        self.assertEqual(9, row.prefix_2)
        self.assertEqual(8, row.prefix_3)
        self.assertEqual(8, row.label)
        self.assertEqual(6, row.event_nr)
