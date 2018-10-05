import storage_simulation as ss
import numpy as np

data = ss.read_file('pikachu.jpg')
ss.write_bytearray_to_file('pika2.jpg', data)
#def simulation(data, symbols, symbol_size, redundancy, clouds, lost=0.0):
# The symbols
g = [64,128]

# The Symbol sizes of g1
k = [1024,2048,4096,8192,16384,32768,65536,131072]

loss = np.linspace(0,1,11)

##for  i in loss:
#    print(ss.simulation(data,128,1024,10,20,i), i)

print(ss.simulation(data,64,1024,5,20,0.5))
for i in g:
    #print(i)
    for j in k:
        #print(j)
        res = ss.simulation(data,i,j,5,20,0.5)
        res1 = ss.simulation(data,i,j,5,20,0.6)
        print('G = %s'%i,'K = %s' %j,'0.5 %s' %res,'0.6 %s'  %res1)


#ss.simulation(data, 160, 1000, 5, 20, lost=0.9)
#ss.simulation(data, 160, 1000, 5, 20)
