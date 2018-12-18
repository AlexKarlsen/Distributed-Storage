##################################################
# File name: kodo_helper.py                      #
# Author: Alex Karlsen & Kasper Klausen          #
# Submission: Distributed Storage, Mini-project  #
# Instructor: Daniel Lucani                      #
##################################################

## Imports
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
symbol_size = 1024
field = kodo.field.binary8

def encode(data, overhead):
    data_in = bytearray(data)
    symbol_size = int(math.ceil(len(data_in) / float(symbols)))
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
    # Create decoder
    decoder_factory = kodo.RLNCDecoderFactory(field, symbols, symbol_size)
    decoder = decoder_factory.build()
    data_out = bytearray(decoder.block_size())
    decoder.set_mutable_symbols(data_out)

    for i in data:
        decoder.read_payload(i)

    return data_out
