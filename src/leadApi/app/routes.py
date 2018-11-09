import os
from app import app
from flask import request

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
