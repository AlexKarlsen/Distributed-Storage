import os
from app import app
from flask import request, Response
import requests as req

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = './uploads'

store = ['http://raspberry2.local:5001/api/e2/store','http://raspberry3.local:5001/api/e2/store', 'http://raspberry2.local:5001/api/e2/store']
replica = ['http://raspberry2.local:5001/api/e2/replicate']

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

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if (request.method == 'POST'):
        fp = request.files['file']
        
        
        #print(request.headers)
        # Should not be stored on lead
        #file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        #fileToSend = open(os.path.join(UPLOAD_FOLDER, file.filename), 'rb')
        
        process('replicas', fp)
        return 'Success'
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