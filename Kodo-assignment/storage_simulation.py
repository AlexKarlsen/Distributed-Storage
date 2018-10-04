import random

import kodo

def _select_cloud(clouds, number_of_clouds=None):
    r = random.randint(0, clouds - 1)
    if number_of_clouds is not None:
        if not r < number_of_clouds:
            r = _select_cloud(clouds, number_of_clouds)
    return r

def _make_clouds(clouds):
    res = list()
    for i in range(0, clouds):
        res.append(list())
    return res


def read_file(file_path):
    file = open(file_path, 'rb')
    bytes = bytearray(file.read())
    return bytes

def write_bytearray_to_file(file_path, data):
    file = open(file_path, 'wb')
    file.write(data)

def is_complete(data_in, data_out):
    for i, j in zip(data_in, data_out):
        if not i == j:
            return False
    return True

"""
   simulation: Is a function which simulates the loss of X percentage of clouds
"""
def simulation(data, symbols, symbol_size, redundancy, clouds, lost=0.0):

    if clouds <= lost:
        print('The amount of clouds lost must be less than the number of clouds')
        return

    cloud_locations = _make_clouds(clouds)

    field = kodo.field.binary8

    factory = kodo.RLNCEncoderFactory(field, symbols, symbol_size)
    encoder = factory.build()
    encoder.set_const_symbols(data)
    encoder.set_systematic_off()

    remainder = (symbols + redundancy) % clouds
    payloads_per_cloud = ((symbols + redundancy) - remainder) / clouds

    cloud = 0
    current_payload = 0
    for i in range(0, payloads_per_cloud * clouds):
        # print(cloud)
        payload = encoder.write_payload()
        cloud_locations[cloud].append(payload)
        current_payload += 1
        if current_payload == payloads_per_cloud:
            cloud += 1
            current_payload = 0

    cloud -= 1 # Adjust for last iterations
    if not remainder == 0:
        for i in range(0, remainder):
            payload = encoder.write_payload()
            cloud_locations[cloud].append(payload)

    lost = int(clouds * lost)
    for i in range(0, lost):
        cloud = _select_cloud(clouds, len(cloud_locations))
        del cloud_locations[cloud]

    factory = kodo.RLNCDecoderFactory(field, symbols, symbol_size)
    decoder = factory.build()

    data_out = bytearray(decoder.block_size())
    decoder.set_mutable_symbols(data_out)

    clouds_accessed = 0
    number_of_payloads = 0
    for cloud in cloud_locations:
        clouds_accessed += 1
        for payload in cloud:
            number_of_payloads += 1
            decoder.read_payload(payload)
            if decoder.is_complete():
                break
        else:
            continue
        break

    if decoder.is_complete():
        print('Decoding completed by accessing {!s} clouds and getting {!s} payloads'.format(clouds_accessed, number_of_payloads))
    else:
        print('Decoding failed after accessing {!s} clouds and getting {!s} payloads'.format(clouds_accessed, number_of_payloads))

    if is_complete(data, data_out):
        print('Decoding completed by accessing {!s} clouds and getting {!s} payloads'.format(clouds_accessed, number_of_payloads))
    else:
        print('Decoding failed after accessing {!s} clouds and getting {!s} payloads'.format(clouds_accessed, number_of_payloads))
    write_bytearray_to_file('pika3.jpg', data_out)
