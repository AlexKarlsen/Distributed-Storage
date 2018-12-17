from app import app
from flask import Flask, request, Response, send_from_directory, stream_with_context
import os
import thread
import requests as req
from random import randint
import json
import kodo_helper

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

@app.route('/api/e2/download/<directory>/<filename>', methods=["GET"])
def download2(directory, filename):
    return Response(open(os.path.join(directory, filename)), mimetype='application/octet-stream')

@app.route('/api/e3/local/download/<directory>/<filename>/<l>', methods=["GET"])
def download3(directory, filename, l):
    files = [i for i in os.listdir(directory) if os.path.isfile(os.path.join(directory,i)) and filename in i]
    filesAsBytes = []
    print(files)
    if int(l) == 2:
        # def generate():
        #     for i in files:
        #         yield open(os.path.join(directory, str(i)), 'rb').read()
        # myGenerator = generate()
        # print(myGenerator)
        # for i in myGenerator:
        #     print(i)
        
        for i in files:
            print(i)
            filesAsBytes.append(open(os.path.join(directory, str(i)), 'rb').read())
        #print(filesAsBytes[0])
        #print(json.dumps(filesAsBytes))
    return Response(filesAsBytes, mimetype='application/octet-stream')

@app.route('/api/e3/dist/download/<directory>/<filename>/<l>', methods=["GET"])
def download4(directory, filename, l):
    files = [i for i in os.listdir(directory) if os.path.isfile(os.path.join(directory,i)) and filename in i]
    print(files)
    if int(l) == 2:
        fps = []
        for i in files:
            fps.append(bytearray(open(os.path.join(directory, i), 'rb').read()))
        print(len(fps[0]))

    return Response(kodo_helper.decode(fps,10252), mimetype='application/octet-stream')