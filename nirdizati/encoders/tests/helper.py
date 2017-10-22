from nirdizati.encoders import Encoder


def data_frame():
    encoder = Encoder()
    encoder.set_path('./log')
    filename = 'Productiontrim.xes'
    encoder.xes_to_csv(filename)
    return encoder.df
