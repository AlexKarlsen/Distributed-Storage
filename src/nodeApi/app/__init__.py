from flask import Flask, Request, redirect, url_for

app = Flask(__name__)

from app import routes