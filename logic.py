'__author__' == 'cyril'

from flask import Flask
from flask import request
from flask import render_template
import re
import pickle

app = Flask(__name__)


def parents(oe):
    arr = oe.split("-")
    pa = []
    for i, o in enumerate(arr):
        if len(arr[:i]) != 0:
            if len(arr[:i]) == 1:
                pa.append(arr[:i][0])
            else:
                s = ""
                for j in arr[:i]:
                    s += j + "-"
                pa.append(s[:-1])
    return pa


def minus(num):
    return num-1


def read_f():
    file = open("./templates/oes.txt", "r")
    data = file.readlines()
    file.close()
    return data


def match_reg(data):
    data_new = []
    pattern = re.compile("[A-Z]{3}[^ ].*")
    for d in data:
        if pattern.match(d):
            data_new.append(d.split(";;")[0])
    return data_new


def data_ini(data_new):
    dumpp = []
    top_level = {}
    nr_of_levels = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0}
    for i, d in enumerate(data_new):
        level = len(d.split("-"))
        if level < 8:
            show = "y"
            if level == 1:
                top_level[str(d)] = nr_of_levels.copy()
        else:
            show = "n"
        dumpp.append({'name': d, 'show': show, 'pos_x': 150*level,
                      'pos_y': 60*level, 'parents': parents(d),
                      'level': level})
    return dumpp, top_level


def max_per_toplevel(top_level):
    maxs_tl = {}
    for oe, levels in zip(top_level.keys(), top_level.values()):
        max_l = 0
        for v in levels.values():
            if v > max_l:
                max_l = v
        maxs_tl[oe] = max_l
    return maxs_tl


@app.route('/', methods=['POST', 'GET'])
def logic():
    if request.method == 'POST':
        data = read_f()
        return render_template('main.html', data=data)

    if request.method == 'GET':
        data_new = match_reg(read_f())
        data, top_level = data_ini(data_new)
        nr_of_levels = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0}
        for d in data:
            nr_of_levels[str(d['level'])] += 1
            if d['show'] == "y" and len(d['parents']) > 0:
                parent = d['parents'][0]
                tl_par = top_level[parent]
                tl_par[str(d['level'])] += 1

        current_x_max = 150
        for d in data:
            if d['show'] == "y" and len(d['parents']) > 0:
                parent = d['parents'][0]
                nr = top_level[parent][str(d['level'])]
                d['pos_x'] = current_x_max + nr*150
                top_level[parent][str(d['level'])] -= 1
        pickle.dump(data, open("./all_oes.txt", "wb"))
        return render_template('main.html',
                               data=pickle.load(open("./all_oes.txt", "rb")),
                               minus=minus)
