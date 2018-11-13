import os
from app import app
from flask import request, Response

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = './uploads'

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if (request.method == 'POST'):
        file = request.files['file']
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
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
@app.route('/download', methods=['GET'])
def download():
    folder = os.path.join(UPLOAD_FOLDER)
    filesList = os.listdir(folder)
    print(filesList)
    htmlTableString = ""
    for f in filesList:
        htmlTableString = htmlTableString + '''<tr><td> ''' + f + ''' </td><td>
        <form action="/download/''' + f + '''" method="get">
        <input type="submit" value="Submit"></form></td></tr> '''
    return '''
        <!doctype html>
        <title>Download</title>
        <h1>Download file</h1>
        <table style="border: 1px solid black"> ''' + htmlTableString + '''
        </table>
        '''

@app.route('/download/<filename>', methods=['GET'])
def downloadFile(filename):
    f = open(os.path.join(UPLOAD_FOLDER, filename))
    return Response(f, mimetype='application/octet-stream')