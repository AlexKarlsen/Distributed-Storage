import os
import sys
import math
import string
import random

# try importing the ``kodo`` module
try:
    import kodo
    print("Kodo imported successfully")
except ImportError:
    print("Unable to import kodo!")

# parameters
symbols = 4
symbol_size = 1024
field = kodo.field.binary8


# overhead should be 2 for l = 1 and 8 for l = 2
def encode(data, overhead):
    data_in = bytearray(data)
    symbol_size = int(math.ceil(len(data_in) / float(symbols)))
    print(symbol_size)
    # Create encoder
    factory = kodo.RLNCEncoderFactory(field, symbols, symbol_size)    
    encoder = factory.build()
    encoder.set_const_symbols(data_in)

    packages = []
    for _ in range(0, symbols + overhead):
        packages.append(encoder.write_payload())

    return packages
    

    

def decode(data, size):
    symbol_size = int(math.ceil(size / float(symbols)))
    print(symbol_size)
    # Create decoder
    decoder_factory = kodo.RLNCDecoderFactory(field, symbols, symbol_size)
    decoder = decoder_factory.build()
    data_out = bytearray(decoder.block_size())
    decoder.set_mutable_symbols(data_out)

    for i in data:
        decoder.read_payload(i)

    return data_out


d = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10000))
h = encode(d, 2)
d2 = decode([h[5], h[3], h[4], h[0]], len(d))
print(len(d))
#print(str(d))
print(len(d2))
#print(str(d2))
print(str(d) in str(d2))