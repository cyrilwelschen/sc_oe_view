'__author__' == 'cyril'

from flask import Flask
from flask import request
from flask import render_template
import re
import pickle
import random

app = Flask(__name__)

def parents(oe):
    arr = oe.split("-")
    nr = len(arr)
    pa = []
    for i,o in enumerate(arr):
        if len(arr[:i]) != 0:
            if len(arr[:i]) == 1:
                pa.append(arr[:i][0])
            else:
                s =""
                for j in arr[:i]:
                   s += j+"-"
                pa.append(s[:-1])
    return pa

def minus(num):
    return num-1

@app.route('/', methods=['POST', 'GET'])
def logic():
    if request.method == 'POST':
        file = open("./templates/oes.txt", "r")
        data = file.readlines()
        file.close()
        return render_template('main.html', data=data)

    if request.method == 'GET':
        file = open("./templates/oes.txt", "r")
        data = file.readlines()
        file.close()
        data_new = []
        pattern = re.compile("[A-Z]{3}[^ ].*")
        for d in data:
            if pattern.match(d):
                data_new.append(d.split(";;")[0])
        dumpp = []
        for d in data_new:
            dumpp.append({'name': d, 'show': "y", 'pos_x': 1500*random.random(), 'pos_y': 1000*random.random(), 'parents': parents(d), 'level': len(d.split("-"))})
        pickle.dump(dumpp, open("./all_oes.txt","wb"))
        return render_template('main.html', data=pickle.load(open("./all_oes.txt","rb")),
                               minus=minus)
