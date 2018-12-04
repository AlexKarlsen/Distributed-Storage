from app import app
from flask import Flask, request, Response
import os
import requests as req

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
    directory = './replicas/'
    fp.save(os.path.join(directory, fp.filename))

    if (replicaNo > 1):
        forward(fp, replicaNo-1)
    return "Success"

@app.route('/api/e3/store', methods=["POST"])
def store_rlnc():
    return 'Success'

@app.route('/api/e3/replicate', methods=["POST"])
def replicate_rlnc():
    return "Success"

def forward(fp, replicaNo):
    print(fp)
    response = req.post(replica[0], files={'file':
                            (fp.filename, fp.stream,
                            fp.content_type, fp.headers)})
    print(response)
