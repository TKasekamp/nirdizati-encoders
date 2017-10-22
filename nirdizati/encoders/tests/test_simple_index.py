from unittest import TestCase

from nirdizati.encoders.tests.helper import data_frame
from nirdizati.encoders import SimpleIndexEncoder


class TestSimpleIndex(TestCase):
    def test_has_columns(self):
        encoder = SimpleIndexEncoder()
        df = encoder.encode_trace(data_frame())
        # Column check
        self.assertTrue("case_id" in df.columns.values)
        self.assertTrue("event_nr" in df.columns.values)
        self.assertTrue("remaining_time" in df.columns.values)
        self.assertTrue("elapsed_time" in df.columns.values)
        self.assertTrue("prefix_1" in df.columns.values)
        self.assertEqual(5, df.columns.size)

    def test_prefix_length(self):
        encoder = SimpleIndexEncoder()
        df = encoder.encode_trace(data_frame(), 3)
        # Column check
        self.assertTrue("prefix_1" in df.columns.values)
        self.assertTrue("prefix_2" in df.columns.values)
        self.assertTrue("prefix_3" in df.columns.values)
        self.assertEqual(7, df.columns.size)
