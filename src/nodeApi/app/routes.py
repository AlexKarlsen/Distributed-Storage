from app import app
from flask import Flask, request, Response
import os

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/store', methods=["POST"])
def store():
    file = request.files['file']
    directory = './replicas/'
    file.save(os.path.join(directory, file.filename))
    return 'Success'

@app.route('/replicate', methods=["POST"])
def replicate():
    return "replicate"