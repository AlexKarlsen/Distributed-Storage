import os
from app import app
from flask import request, Response
import requests as req
import time
from random import randint

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = './uploads'

store = ['http://raspberrypi2.local:5000/api/e2/store','http://raspberrypi3.local:5000/api/e2/store', 'http://raspberrypi4.local:5000/api/e2/store']
replica = ['http://raspberrypi2.local:5000/api/e2/replicate','http://raspberrypi3.local:5000/api/e2/replicate', 'http://raspberrypi4.local:5000/api/e2/replicate']

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
        req.post(replica[rand] + '/' + str(k-1), files={'file':
            (fp.filename, fp.stream,
            fp.content_type, fp.headers)}, data = {'hist': [rand]})
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
    f = open(os.path.join(directory, filename), 'rb')
    return Response(f, mimetype='application/octet-stream')