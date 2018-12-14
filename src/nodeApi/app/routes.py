from app import app
from flask import Flask, request, Response
import os
import thread
import requests as req
from random import randint
import json

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

#store = ['http://raspberry2.local:5001/api/e2/store','http://raspberry3.local:5001/api/e2/store', 'http://raspberry2.local:5001/api/e2/store']

replica = ['http://raspberrypi2.local:5000/api/e2/replicate','http://raspberrypi3.local:5000/api/e2/replicate', 'http://raspberrypi4.local:5000/api/e2/replicate']

@app.route('/api/e2/store', methods=["POST"])
def store():
    fp = request.files['file']
    directory = './store/'
    fp.save(os.path.join(directory, fp.filename))
    return 'Success'

@app.route('/api/e2/replicate/<replicaNo>', methods=["POST"])
def replicate(replicaNo):
    fp = request.files['file']
    directory = './replicas/'
    hist = json.load(request.files['data'])
    fp.save(os.path.join(directory, fp.filename))

    thread.start_new_thread(store_and_forward, (fp.filename, hist, replicaNo))
    #fp = request.files['file']
    #directory = './replicas/'
    #fp.save(os.path.join(directory, fp.filename))
    #fp.stream.seek(0)
    #hist = json.load(request.files['data'])
    #print('History: {}'.format(hist['hist']))
    #replicaNo = int(replicaNo)
    # if (replicaNo > 1):
    #     rand = randint(0, 2)
    #     while rand in hist['hist']:
    #         rand = randint(0, 2)
    #     hist['hist'].append(rand)
    #     print('Next node: {}'.format(rand))
    #     req.post(replica[rand] + '/' + str(replicaNo - 1), files={
    #         'data': ('data', json.dumps(hist), 'application/json'),
    #         'file': (fp.filename, fp.stream, fp.content_type, fp.headers)
    #         }
    #     )
    return "Success"

def store_and_forward(filename, hist, replicaNo):
    directory = './replicas/'
    fp = open(os.path.join(directory, filename), 'rb')
    #fp = request.files['file']
    #hist = json.load(request.files['data'])
    #fp.save(os.path.join(directory, fp.filename))
    #fp.stream.seek(0)
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

@app.route('/api/e3/store', methods=["POST"])
def store_rlnc():
    return 'Success'

@app.route('/api/e3/replicate', methods=["POST"])
def replicate_rlnc():
    return "Success"

@app.route('/api/e2/download/<directory>/<filename>', methods=["GET"])
def download2(directory, filename):
    return Response(open(os.path.join(directory, filename)), mimetype='application/octet-stream')