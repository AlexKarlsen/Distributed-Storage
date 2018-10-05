import exercise2
import numpy as np
import matplotlib.pyplot as plt

# A function for multiplying each element in array by a factor
# def multiplyArray(array, multi):
#     tmp = []
#     for val in array:
#         tmp.append(val*multi)
#     #print(tmp)
#     return tmp

# The symbols
g = [8,16,32,64,128]

# The Symbol sizes of g1
k = [8,16,32,64,128,256,512,1024,2048,4096,8192,16384,32768,65536,131072]

# Create encode decode m x n matrices as a 5x9 matrices
encode = np.zeros(shape=(5,15))
decode = np.zeros(shape=(5,15))

# For every g and for all k do the simulation and store the timing
for i, g_val in enumerate(g):
    print('G = %s' %g_val)
    for j, k_val in enumerate(k):
        print('K = %s' %(k_val))
        timing = exercise2.simulation(g_val,k_val)
        print('Encode time = %s ms' %timing[0])
        print('Decode time = %s ms' %timing[1])
        # set the timing on the correct position in the matrix
        encode[i][j], decode[i][j] = timing
#print(k)

# Create the plot
plt.plot(k,encode[0],color='r')
#k = multiplyArray(k,2)
plt.plot(k,encode[1],color='b')
#k = multiplyArray(k,2)
plt.plot(k,encode[2],color='g')
#k = multiplyArray(k,2)
plt.plot(k,encode[3],color='y')
#k = multiplyArray(k,2)
plt.plot(k,encode[4],color='m')
plt.xlabel('Symbol Size')
plt.ylabel('Time (ms)')
plt.xlim(xmin=0)
plt.ylim(ymin=0)
plt.legend(g, title="Symbols", loc=2)
plt.title('Encode Timings')
plt.show()

# Create the plot
plt.plot(k,decode[0],color='r')
#k = multiplyArray(k,2)
plt.plot(k,decode[1],color='b')
#k = multiplyArray(k,2)
plt.plot(k,decode[2],color='g')
#k = multiplyArray(k,2)
plt.plot(k,decode[3],color='y')
#k = multiplyArray(k,2)
plt.plot(k,decode[4],color='m')
plt.xlabel('Symbol Size')
plt.ylabel('Time (ms)')
plt.xlim(xmin=0)
plt.ylim(ymin=0)
plt.legend(g, title="Symbols", loc=2)
plt.title('Decode Timings')
plt.show()

