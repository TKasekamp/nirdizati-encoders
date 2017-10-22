from unittest import TestCase

from nirdizati.encoders import ComplexEncoder
from nirdizati.encoders import Encoder


class TestComplex(TestCase):
    def setUp(self):
        encoder = Encoder()
        encoder.set_path('./log')
        filename = 'Productiontrim.xes'
        encoder.xes_to_csv(filename)
        self.frame = encoder.df
        self.attributes = encoder.event_attributes

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
