import os
from app import app
from flask import request, Response
import requests as req
import time
from random import randint, shuffle
import kodo_helper
import json

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = './uploads'

store = ['http://raspberrypi2.local:5000/api/e2/store','http://raspberrypi3.local:5000/api/e2/store', 'http://raspberrypi4.local:5000/api/e2/store']
replica = ['http://raspberrypi2.local:5000/api/e2/replicate','http://raspberrypi3.local:5000/api/e2/replicate', 'http://raspberrypi4.local:5000/api/e2/replicate']
#download = ['http://raspberrypi2.local:5000/api/e2/download/', ]

def process(folder, fp):
    print(fp)
    response = req.post(store[0], files={'file':
                            (fp.filename, fp.stream,
                            fp.content_type, fp.headers)})
    print(response)

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/e2/store/upload/<k>', methods=['GET', 'POST'])
def uploadStore(k):
    if (request.method == 'POST'):
        start = time.time()
        fp = request.files['file']
        k = int(k)
        for i in range(k):
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

@app.route('/e2/replicate/upload/<k>', methods=['GET', 'POST'])
def uploadReplicate(k):
    if (request.method == 'POST'):
        start = time.time()
        fp = request.files['file']
        rand = randint(0,2)
        k = int(k)
        req.post(replica[rand] + '/' + str(k), files={
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

# Exercise 3: Erasure Code Storage, local
@app.route('/e3/local/upload/<l>', methods=['GET', 'POST'])
def uploadReplicateCodedLocal(l):
    if (request.method == 'POST'):
        start = time.time()
        fp = request.files['file']
        l = int(l)
        l = (l*l)*2
        print(l)
        ned = fp.read()
        time_enc_start = time.time()
        data = kodo_helper.encode(ned, l)
        time_enc_end = time.time()
        print(len(data))
        # print(ned in kodo_helper.decode([data[5],data[4],data[0],data[1]],len(ned)))
        shuffle(data)

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

@app.route('/download', defaults={'directory': None})
@app.route('/download/<directory>', methods=['GET'])
def download(directory):
    if directory == None:
        folder = os.path.join(UPLOAD_FOLDER)
    else:
        folder = os.path.join(UPLOAD_FOLDER, directory)
    filesList = os.listdir(folder)
    print(filesList)
    htmlTableString = ""
    for f in filesList:
        if os.path.isfile(os.path.join(folder, f)):
            htmlTableString = htmlTableString + '''<tr><td> ''' + f + ''' </td><td>
            <form action="/download/''' + folder + '''/''' + f + '''" method="get">
            <input type="submit" value="Submit"></form></td></tr> '''
    return '''
        <!doctype html>
        <title>Download</title>
        <h1>Download file</h1>
        <table style="border: 1px solid black"> ''' + htmlTableString + '''
        </table>
        '''

@app.route('/download/<directory>/<filename>', methods=['GET'])
def downloadFile(directory, filename):
    start = time.time()
    r = req.get('http://raspberrypi2.local:5000/api/e2/download/' + directory + '/' + filename)
    end = time.time()
    print(str(end - start) + 's')
    return Response(r.content, mimetype='application/octet-stream')

@app.route('/local/download/<directory>/<filename>/<l>', methods=['GET'])
def downloadFile2(directory, filename, l):
    start = time.time()
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
    
    decode_time_start = time.time()
    data = kodo_helper.decode([bytearray(r1.content), bytearray(r2.content), bytearray(r3.content), bytearray(r4.content)], len(r1.content) + len(r2.content) + len(r3.content) + len(r4.content))
    decode_time_end = time.time()

    print('Decoding time: {}'.format(decode_time_end - decode_time_start))
    end = time.time()
    print('Download time: ' + str(end - start) + 's')
    return Response(data , mimetype="application/octet-stream")

@app.route('/dist/download/<directory>/<filename>/<l>', methods=['GET'])
def downloadFile3(directory, filename, l):
    start = time.time()
    if int(l) == 1:
        r2 = req.get('http://raspberrypi2.local:5000/api/e3/dist/download/' + directory + '/' + filename + '/' + l)
        r3 = req.get('http://raspberrypi3.local:5000/api/e3/dist/download/' + directory + '/' + filename + '/' + l)
    elif int(l) == 2:
        r2 = req.get('http://raspberrypi2.local:5000/api/e3/dist/download/' + directory + '/' + filename + '/' + l)
        print(r2.content)
    end = time.time()
    print(str(end - start) + 's')
    return 'succes'
    #Response(r.content, mimetype='application/octet-stream')