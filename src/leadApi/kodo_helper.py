import os
import sys
import math

# try importing the ``kodo`` module
try:
    import kodo
    print("Kodo imported successfully")
except ImportError:
    print("Unable to import kodo!")

# parameters
symbols = 4
symbol_size = 32
field = kodo.field.binary8


def encode(data, l):
    data_in = bytearray(data)
    symbols = int(math.ceil(len(data_in) / float(symbol_size)))
    # Create encoder
    factory = kodo.RLNCEncoderFactory(field, symbols, symbol_size)    
    encoder = factory.build()
    encoder.set_const_symbols(data_in)

    packages = []
    for _ in range(0, symbols + l):
        packages.append(encoder.write_payload())

    return packages
    

    

def decode(data):
    symbols = len(data) # maybe minus l?
    # Create decoder
    decoder_factory = kodo.RLNCDecoderFactory(field, symbols, symbol_size)
    decoder = decoder_factory.build()
    data_out = bytearray(decoder.block_size())
    decoder.set_mutable_symbols(data_out)

    for i in data:
        decoder.read_payload(i)

    return data_out


d = "The size of this data is exactly 128 bytes which means it will fit perfectly in a single generation. That is very lucky, indeed!"
d2 = decode(encode(d, 1))
print(len(d))
print(len(d2))