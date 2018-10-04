import storage_simulation as ss

data = ss.read_file('pikachu.jpg')
ss.write_bytearray_to_file('pika2.jpg', data)

ss.simulation(data, 160, 1000, 5, 20, .4)
ss.simulation(data, 160, 1000, 5, 20)
