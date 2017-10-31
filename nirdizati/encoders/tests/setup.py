import pandas as pd

from nirdizati.encoders import Encoder

ENCODER = None
SAMPLE_TRACE = None
PROD_XES = None


def data_frame():
    global ENCODER
    if ENCODER is None:
        get_encoder()
    return ENCODER.df


def get_encoder():
    global ENCODER
    if ENCODER is not None:
        return ENCODER
    ENCODER = Encoder()
    ENCODER.set_path('./log')
    filename = 'Productiontrim.xes'
    ENCODER.xes_to_csv(filename)
    return ENCODER


def sample_trace():
    global SAMPLE_TRACE
    if SAMPLE_TRACE is None:
        SAMPLE_TRACE = pd.read_csv(filepath_or_buffer='./log/sample_trace.csv', header=0)
    return SAMPLE_TRACE


def prod_xes():
    global PROD_XES
    if PROD_XES is None:
        PROD_XES = pd.read_csv(filepath_or_buffer='./log/production.xes.csv', header=0)
    return PROD_XES
