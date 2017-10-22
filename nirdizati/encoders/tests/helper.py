from nirdizati.encoders import Encoder

ENCODER = None


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
