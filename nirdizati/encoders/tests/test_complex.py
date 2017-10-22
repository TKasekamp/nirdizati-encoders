from unittest import TestCase

from nirdizati.encoders import ComplexEncoder
from nirdizati.encoders import Encoder
from nirdizati.encoders.tests.helper import data_frame, get_encoder


class TestComplex(TestCase):
    def setUp(self):
        self.frame = data_frame()
        self.attributes = get_encoder().event_attributes

    def test_has_columns(self):
        encoder = ComplexEncoder()
        df = encoder.encode_trace(self.frame, additional_columns=self.attributes)

        self.assertIn("case_id", df.columns.values)
        self.assertIn("event_nr", df.columns.values)
        self.assertIn("remaining_time", df.columns.values)
        self.assertIn("elapsed_time", df.columns.values)
        self.assertIn("prefix_1", df.columns.values)
        self.assertEqual(16, df.columns.size)

    def test_prefix_length(self):
        encoder = ComplexEncoder()
        df = encoder.encode_trace(self.frame, additional_columns=self.attributes, prefix_length=3)

        self.assertIn("prefix_1", df.columns.values)
        self.assertIn("prefix_2", df.columns.values)
        self.assertIn("prefix_3", df.columns.values)
        self.assertEqual(40, df.columns.size)

    def test_shape(self):
        encoder = ComplexEncoder()
        df = encoder.encode_trace(self.frame, additional_columns=self.attributes)

        self.assertEqual((3, 16), df.shape)
        # Checking one row
        row = df[(df.event_nr == 1) & (df.case_id == "Case10")].iloc[0]

        self.assertEqual('Turning & Milling - Machine 9', row.prefix_1)
        self.assertEqual('1', row.Qty_Completed_1)
        self.assertEqual(0.0, row.elapsed_time)
        self.assertEqual(1447140.0, row.remaining_time)
