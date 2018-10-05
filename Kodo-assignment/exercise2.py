import kodo
import os
import sys
import time

# g
symbols = 8
# k
symbol_size = 160
# finite field
field = kodo.field.binary8

def simulation(g, k, systematic=True, data=None):
    factory = kodo.RLNCEncoderFactory(field, g, k)
    encoder = factory.build()
    if data == None:
        data_in = bytearray(os.urandom(encoder.block_size()))
    else:
        data_in = bytearray(data)
    
    encoder.set_const_symbols(data_in)
    if systematic == True:
        encoder.set_systematic_off()
    else:
        encoder.set_systematic_on()

    #if encoder.is_systematic_on():
        #print("Systematic is on")
    #else:
        #print("Systematic is off")

    decoder_factory = kodo.RLNCDecoderFactory(field, g, k)
    decoder = decoder_factory.build()
    data_out = bytearray(decoder.block_size())
    decoder.set_mutable_symbols(data_out)

    #print('Measurering time of encode-decode')
    
    while not decoder.is_complete():
        # Encode a packet into the payload buffer
        start_encode = time.time() * 1000 # milliseconds
        packet = encoder.write_payload()
        end_encode = time.time() * 1000 # milliseconds
        # Pass that packet to the decoder
        start_decode = time.time() * 1000 # milliseconds
        decoder.read_payload(packet)
        end_decode = time.time() * 1000 # milliseconds


        #print("Rank of decoder {}".format(decoder.rank()))

        # Symbols that were received in the systematic phase correspond
        # to the original source symbols and are therefore marked as
        # decoded
        #print("Symbols decoded {}".format(decoder.symbols_uncoded()))

    #print("Coding finished")

    # The decoder is complete, the decoded symbols are now available in
    # the data_out buffer: check if it matches the data_in buffer
    timing_encode = end_encode-start_encode
    timing_decode = end_decode-start_decode
    #print('%s milliseconds' %(timing))
    #print("Checking results...")
    if data_out == data_in:
        print("Data decoded correctly")
    else:
        print("Unable to decode please file a bug report :)")
        sys.exit(1)
    return timing_encode, timing_decode
#simulation(symbols, symbol_size)
