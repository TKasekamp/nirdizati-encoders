from nirdizati.encoders.common import encode_complex_index_latest


def encode_trace(data, additional_columns, prefix_length=1):
    return encode_complex_index_latest(data, additional_columns, prefix_length, 'frequency')
