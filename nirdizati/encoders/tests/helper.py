from nirdizati.encoders import Encoder

dataframe = None
encoder = None


def data_frame():
    global encoder
    if encoder is None:
        get_encoder()
    return encoder.df


def get_encoder():
    global encoder
    if encoder is not None:
        return encoder
    else:
        encoder = Encoder()
        encoder.set_path('./log')
        filename = 'Productiontrim.xes'
        encoder.xes_to_csv(filename)
        return encoder
