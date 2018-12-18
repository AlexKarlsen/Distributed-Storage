##################################################
# File name: routes.py (lead)                    #
# Author: Alex Karlsen & Kasper Klausen          #
# Submission: Distributed Storage, Mini-project  #
# Instructor: Daniel Lucani                      #
##################################################


## Imports
import os
from app import app
from flask import request, Response
import requests as req
import time
from random import randint
import kodo_helper
import json

## REST Endpoints
store = ['http://raspberrypi2.local:5000/api/e2/store','http://raspberrypi3.local:5000/api/e2/store', 'http://raspberrypi4.local:5000/api/e2/store']
replica = ['http://raspberrypi2.local:5000/api/e2/replicate','http://raspberrypi3.local:5000/api/e2/replicate', 'http://raspberrypi4.local:5000/api/e2/replicate']
store3 = ['http://raspberrypi2.local:5000/api/e3/store','http://raspberrypi3.local:5000/api/e3/store', 'http://raspberrypi4.local:5000/api/e3/store']
replica3 = ['http://raspberrypi2.local:5000/api/e3/replicate','http://raspberrypi3.local:5000/api/e3/replicate', 'http://raspberrypi4.local:5000/api/e3/replicate']

################## Exercise 2 ##################

########       Case A     ########
@app.route('/e2/store/upload/<k>', methods=['GET', 'POST'])
def uploadStore(k):
    if (request.method == 'POST'):
        start = time.time()
        fp = request.files['file']
        k = int(k)
        for i in range(k):
            # Resetting file stream pointer
            fp.stream.seek(0)
            req.post(store[i], files={'file':
                (fp.filename, fp.stream,
                fp.content_type, fp.headers)})
        end = time.time()
        return 'Success, time elapsed: ' + str(end - start) + 's'  
    else:
        return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
        <p><input type=file name=file>
        <input type=submit value=Upload>
        </form>
        '''

########       Case B     ########
@app.route('/e2/replicate/upload/<k>', methods=['GET', 'POST'])
def uploadReplicate(k):
    if (request.method == 'POST'):
        start = time.time()
        fp = request.files['file']
        # Random selection of replica nodes
        rand = randint(0,2)
        req.post(replica[rand] + '/' + k, files={
            'data': ('data', json.dumps({'hist': [rand]}), 'application/json'),
            'file': (fp.filename, fp.stream, fp.content_type, fp.headers) 
            }
        )
        end = time.time()
        return 'Success, time elapsed: ' + str(end - start)+ 's' 
    else:
        return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
        <p><input type=file name=file>
        <input type=submit value=Upload>
        </form>
        '''

########     Download    ########
@app.route('/download/<directory>/<filename>', methods=['GET'])
def downloadFile(directory, filename):
    start = time.time()
    # Hardcoded download of replica from node 2
    r = req.get('http://raspberrypi2.local:5000/api/e2/download/' + directory + '/' + filename)
    end = time.time()
    print(str(end - start) + 's')
    return Response(r.content, mimetype='application/octet-stream')

################## Exercise 3 ##################

########       Case A     ########
@app.route('/e3/local/upload/<l>', methods=['GET', 'POST'])
def uploadReplicateCodedLocal(l):
    if (request.method == 'POST'):
        start = time.time()
        fp = request.files['file']
        l = int(l)
        l = (l*l)*2
        ned = fp.read()
        ## Encoding
        time_enc_start = time.time()
        data = kodo_helper.encode(ned, l)
        time_enc_end = time.time()
        for i in range(0,len(data),3):
            req.post(store[0], files={
                 'file': (fp.filename + str(i), data[i], 'application/octet-stream')})
            req.post(store[1], files={
                 'file': (fp.filename + str(i+1), data[i+1], 'application/octet-stream')})
            req.post(store[2], files={
                 'file': (fp.filename + str(i+2), data[i+2], 'application/octet-stream')})
        end = time.time()
        return 'Success, time elapsed: ' + str(end - start) + 's' + 'Encoding time: ' + str(time_enc_end - time_enc_start) + 's'  
    else:
        return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
        <p><input type=file name=file>
        <input type=submit value=Upload>
        </form>
        '''

@app.route('/local/download/<directory>/<filename>/<l>', methods=['GET'])
def downloadFile2(directory, filename, l):
    start = time.time()
    # Multiple request workaround (Hardcoded)
    if int(l) == 1:
        r1 = req.get('http://raspberrypi2.local:5000/api/e2/download/' + directory + '/' + filename + '0')
        r2 = req.get('http://raspberrypi2.local:5000/api/e2/download/' + directory + '/' + filename + '3')
        r3 = req.get('http://raspberrypi3.local:5000/api/e2/download/' + directory + '/' + filename + '1')
        r4 = req.get('http://raspberrypi3.local:5000/api/e2/download/' + directory + '/' + filename + '4')
    elif int(l) == 2:
        r1 = req.get('http://raspberrypi2.local:5000/api/e2/download/' + directory + '/' + filename + '0')
        r2 = req.get('http://raspberrypi2.local:5000/api/e2/download/' + directory + '/' + filename + '3')
        r3 = req.get('http://raspberrypi2.local:5000/api/e2/download/' + directory + '/' + filename + '6')
        r4 = req.get('http://raspberrypi2.local:5000/api/e2/download/' + directory + '/' + filename + '9')
    ## Decoding
    decode_time_start = time.time()
    data = kodo_helper.decode([bytearray(r1.content), bytearray(r2.content), bytearray(r3.content), bytearray(r4.content)], len(r1.content) + len(r2.content) + len(r3.content) + len(r4.content))
    decode_time_end = time.time()
    print('Decoding time: {}'.format(decode_time_end - decode_time_start))
    end = time.time()
    print('Download time: ' + str(end - start) + 's')
    return Response(data , mimetype="application/octet-stream")

########       Case B     ########
@app.route('/e3/dist/upload/<l>', methods=['GET', 'POST'])
def uploadReplicateCodedDist(l):
    if (request.method == 'POST'):
        start = time.time()
        fp = request.files['file']
        req.post(replica3[0] + '/' + l, files={
            'file': (fp.filename, fp.stream, fp.content_type, fp.headers) 
            }
        )
        end = time.time()
        return 'Success, time elapsed: ' + str(end - start)+ 's' 
    else:
        return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
        <p><input type=file name=file>
        <input type=submit value=Upload>
        </form>
        '''
### Download for distributed is omitted...