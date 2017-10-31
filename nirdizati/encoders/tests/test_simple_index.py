from unittest import TestCase

from nirdizati.encoders import simple_index
from nirdizati.encoders.tests.setup import data_frame, sample_trace, prod_xes


class TestSimpleIndex(TestCase):
    def test_has_columns(self):
        df = simple_index.encode_trace(prod_xes())
        # Column check
        self.assertIn("case_id", df.columns.values)
        self.assertIn("event_nr", df.columns.values)
        self.assertIn("remaining_time", df.columns.values)
        self.assertIn("elapsed_time", df.columns.values)
        self.assertIn("prefix_1", df.columns.values)
        self.assertEqual(5, df.columns.size)

    def test_prefix_length(self):
        df = simple_index.encode_trace(prod_xes(), prefix_length=3)

       # print df
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

    def encodes_next_activity(self):
        """Encodes for next activity"""
        df = simple_index.encode_trace(prod_xes(), prefix_length=2,  next_activity=True)

       # print df
        self.assertEqual((4, 6), df.shape)
        # Column check
        self.assertNotIn("remaining_time", df.columns.values)
        self.assertNotIn("elapsed_time", df.columns.values)
        self.assertIn("label", df.columns.values)
        self.assertIn("prefix_1", df.columns.values)
        self.assertIn("prefix_2", df.columns.values)
        self.assertIn("prefix_3", df.columns.values)

        # Checking one row
        row = df[(df.event_nr == 1) & (df.case_id == 1)].iloc[0]
        self.assertEqual(0, row.prefix_1)
        self.assertEqual(0, row.prefix_2)
        self.assertEqual(0, row.prefix_3)
        self.assertEqual(1, row.label)
        self.assertEqual(1, row.case_id)
        self.assertEqual(1, row.event_nr)
