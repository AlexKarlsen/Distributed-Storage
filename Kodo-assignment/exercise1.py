import kodo
import os
import sys

symbols = 3
symbol_size = 10

field = kodo.field.binary8

def setup_encoder(g, k, systematic=True):
    factory = kodo.RLNCEncoderFactory(field, g, k)
    encoder = factory.build()
    data_in = bytearray(os.urandom(encoder.block_size()))
    encoder.set_const_symbols(data_in)
    if systematic == True:
        encoder.set_systematic_off()
    else:
        encoder.set_systematic_on()

    if encoder.is_systematic_on():
        print("Systematic is on")
    else:
        print("Systematic is off")

    return encoder, data_in

def setup_decoder(g, k):
    decoder_factory = kodo.RLNCDecoderFactory(field, g, k)
    decoder = decoder_factory.build()
    data_out = bytearray(decoder.block_size())
    decoder.set_mutable_symbols(data_out)
    return decoder, data_out

encoder, data_in = setup_encoder(symbols, symbol_size, True)

decoder, data_out = setup_decoder(symbols, symbol_size)

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
