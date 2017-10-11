'__author__' == 'cyril'

from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route('/')
def logic():
    return "Hello from the other side"
