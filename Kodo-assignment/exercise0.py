import kodo
import os
import sys

symbols = 16
symbol_size = 100000

field = kodo.field.binary8

factory = kodo.RLNCEncoderFactory(field, symbols, symbol_size)
encoder = factory.build()

decoder_factory = kodo.RLNCDecoderFactory(field, symbols, symbol_size)
decoder = decoder_factory.build()

data_in = bytearray(os.urandom(encoder.block_size()))
encoder.set_const_symbols(data_in)

data_out = bytearray(decoder.block_size())
decoder.set_mutable_symbols(data_out)

packet_number = 0
while not decoder.is_complete():
    # Generate an encoded packet
    packet = encoder.write_payload()
    print("Packet {} encoded!".format(packet_number))

    # Pass that packet to the decoder
    decoder.read_payload(packet)
    print("Packet {} decoded!".format(packet_number))
    packet_number += 1
    print("rank: {}/{}".format(decoder.rank(), decoder.symbols()))

print("Coding finished")

# The decoder is complete, the decoded symbols are now available in
# the data_out buffer: check if it matches the data_in buffer
print("Checking results...")
if data_out == data_in:
    print("Data decoded correctly")
else:
    print("Unable to decode please file a bug report :)")
    sys.exit(1)
