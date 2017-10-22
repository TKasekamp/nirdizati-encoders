from nirdizati.encoders import *


def boolean_encode(data):
    encoded_trace = boolean.encode_trace(data)
    return encoded_trace


def frequency_encode(data):
    encoded_trace = frequency.encode_trace(data)
    return encoded_trace


def simple_index_encode(data, prefix):
    encoded_trace = simple_index.encode_trace(data, prefix)
    return encoded_trace


def index_latest_payload_encode(data, attributes, prefix):
    encoded_trace = index_latest_payload.encode_trace(data, attributes, prefix)
    return encoded_trace


def complex_encode(data, attributes, prefix):
    encoded_trace = complex.encode_trace(data, attributes, prefix)
    return encoded_trace


encoder = Encoder()
encoder.set_path("./log")
filename = "Productiontrim.xes"
encoder.xes_to_csv(filename)
encoder.write_df_to_csv(encoder.df, "xes_to_csv_" + filename + ".csv")

encoded_trace = boolean_encode(encoder.df)
encoder.write_df_to_csv(encoded_trace, "boolean_encode_" + filename + ".csv")

encoded_trace = frequency_encode(encoder.df)
encoder.write_df_to_csv(encoded_trace, "frequency_encode_" + filename + ".csv")

encoded_trace = simple_index_encode(encoder.df, 2)
encoder.write_df_to_csv(encoded_trace, "simple_index_encode_" + filename + ".csv")

encoded_trace = index_latest_payload_encode(encoder.df, encoder.event_attributes, 2)
encoder.write_df_to_csv(encoded_trace, "index_latest_payload_encode_" + filename + ".csv")

encoded_trace = complex_encode(encoder.df, encoder.event_attributes, 2)
encoder.write_df_to_csv(encoded_trace, "complex_encode_" + filename + ".csv")
