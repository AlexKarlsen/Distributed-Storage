from app import app
from flask import Flask, request, Response
import os
import requests as req
from random import randint

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

#store = ['http://raspberry2.local:5001/api/e2/store','http://raspberry3.local:5001/api/e2/store', 'http://raspberry2.local:5001/api/e2/store']

replica = ['http://127.0.0.1:5002/api/e2/replicate']

@app.route('/api/e2/store', methods=["POST"])
def store():
    fp = request.files['file']
    directory = './store/'
    fp.save(os.path.join(directory, fp.filename))
    return 'Success'

@app.route('/api/e2/replicate/<replicaNo>', methods=["POST"])
def replicate(replicaNo):
    fp = request.files['file']
    json = request.data
    print(json)
    hist = json['hist']
    directory = './replicas/'
    fp.save(os.path.join(directory, fp.filename))
    replicaNo = int(replicaNo)
    if (replicaNo > 1):
        rand = randint(0, 2)
        while rand in hist:
            rand = randint(0, 2)
        hist.append(rand)
        req.post(replica[rand] + '/' + str(replicaNo - 1), files={'file':
            (fp.filename, fp.stream,
            fp.content_type, fp.headers)}, json={'hist': hist})
    return "Success"

@app.route('/api/e3/store', methods=["POST"])
def store_rlnc():
    return 'Success'

@app.route('/api/e3/replicate', methods=["POST"])
def replicate_rlnc():
    return "Success"