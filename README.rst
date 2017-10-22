Nirdizati encoders
--------

Requires pip to install dependencies.

Import and use SimpleIndexEncoder::

    >>> from nirdizati.encoders import SimpleIndexEncoder
    >>> simple_index_encoder = SimpleIndexEncoder()
    >>> encoded_trace = simple_index_encoder.encode_trace(data)

::
See example.py for more instructions.

Packaged with the help of http://python-packaging.readthedocs.io/

Run tests with::

python -m unittest discover

or

python setup.py test

::