##################################################
# File name: routes.py (node)                    #
# Author: Alex Karlsen & Kasper Klausen          #
# Submission: Distributed Storage, Mini-project  #
# Instructor: Daniel Lucani                      #
##################################################

## Import
from app import app
from flask import Flask, request, Response, send_from_directory, stream_with_context
import os
import thread
import requests as req
from random import randint
import json
import kodo_helper

## REST endpoints
store = ['http://raspberrypi2.local:5000/api/e2/store','http://raspberrypi3.local:5000/api/e2/store', 'http://raspberrypi4.local:5000/api/e2/store']
replica = ['http://raspberrypi2.local:5000/api/e2/replicate','http://raspberrypi3.local:5000/api/e2/replicate', 'http://raspberrypi4.local:5000/api/e2/replicate']

################## Exercise 2 ##################

########       Case A     ########
@app.route('/api/e2/store', methods=["POST"])
def storeStrategy():
    fp = request.files['file']
    directory = './store/'
    fp.save(os.path.join(directory, fp.filename))
    return 'Success'

########       Case B     ########
@app.route('/api/e2/replicate/<replicaNo>', methods=["POST"])
def replicate(replicaNo):
    fp = request.files['file']
    directory = './replicas/'
    hist = json.load(request.files['data'])
    fp.save(os.path.join(directory, fp.filename))
    ## Starting a thread to free lead
    thread.start_new_thread(store_and_forward, (fp.filename, hist, replicaNo))
    return "Success"

def store_and_forward(filename, hist, replicaNo):
    directory = './replicas/'
    fp = open(os.path.join(directory, filename), 'rb')
    replicaNo = int(replicaNo)
    if (replicaNo > 1):
        rand = randint(0, 2)
        while rand in hist['hist']:
            rand = randint(0, 2)
        hist['hist'].append(rand)
        print('Next node: {}'.format(rand))
        req.post(replica[rand] + '/' + str(replicaNo - 1), files={
            'data': ('data', json.dumps(hist), 'application/json'),
            'file': (filename, open(os.path.join(directory, filename), 'rb'), 'application/octet-stream')
            }
        )

########     Download    ########
@app.route('/api/e2/download/<directory>/<filename>', methods=["GET"])
def download2(directory, filename):
    return Response(open(os.path.join(directory, filename)), mimetype='application/octet-stream')

################## Exercise 3 ##################

########       Case A     ########
### We reuse exercise 2 case A endpoint to store file blocks from lead

########       Case B     ########

### Endpoint only used on node 2, node 3 and 4 reuse exercise 2 store endpoint for file blocks
@app.route('/api/e3/replicate/<l>', methods=["POST"])
def replicateDistCoding(l):
    fp = request.files['file']
    directory = './tmp/'
    fp.save(os.path.join(directory, fp.filename))
    ## Starting a thread to free lead
    thread.start_new_thread(distributedCoding, (l, fp.filename))
    return "Success"

def distributedCoding(l, filename):
    directory = './tmp/'
    fp = open(os.path.join(directory, filename), 'rb')
    l = int(l)
    l = (l*l)*2
    ned = fp.read()
    data = kodo_helper.encode(ned, l)
    for i in range(0,len(data),3):
        # Saving file locally
        with open(os.path.join('./store/', filename + str(i)), 'w+') as f:
            f.write(data[i])
        # Distributing to other nodes
        req.post(store[1], files={
                'file': (filename + str(i+1), data[i+1], 'application/octet-stream')})
        req.post(store[2], files={
                'file': (filename + str(i+2), data[i+2], 'application/octet-stream')})
    return 'Success'  

########     Download    ########
@app.route('/api/e3/local/download/<directory>/<filename>/<l>', methods=["GET"])
def download3(directory, filename, l):
    files = [i for i in os.listdir(directory) if os.path.isfile(os.path.join(directory,i)) and filename in i]
    filesAsBytes = []
    if int(l) == 2:
        for i in files:
            filesAsBytes.append(open(os.path.join(directory, str(i)), 'rb').read())
    return Response(filesAsBytes, mimetype='application/octet-stream')

### Not finished
@app.route('/api/e3/dist/download/<directory>/<filename>/<l>', methods=["GET"])
def download4(directory, filename, l):
    files = [i for i in os.listdir(directory) if os.path.isfile(os.path.join(directory,i)) and filename in i]
    if int(l) == 2:
        fps = []
        for i in files:
            fps.append(bytearray(open(os.path.join(directory, i), 'rb').read()))
    return Response(kodo_helper.decode(fps, len(fps)), mimetype='application/octet-stream')