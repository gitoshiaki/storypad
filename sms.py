from flask import Flask
from flask import request, render_template
from flask_cors import CORS

import re
import json
import itertools
import collections
import numpy as np
from const import NEW_THEME

app = Flask(__name__)
CORS(app)

FILE = 'new_comic_dict.json'
with open(FILE, 'r') as fp:
    data = json.load(fp)


# @app.route('/')
# def hello_world():
#     return render_template('index.html')


@app.route('/api/network_graph')
def network_graph():
    cvt1 = {t: i for i, t in enumerate(NEW_THEME)}
    cvt2 = {c: i for i, c in enumerate(itertools.combinations(NEW_THEME, 2))}

    node = np.zeros(len(cvt1))
    edge = np.zeros(len(cvt2))

    for title in data:
        for th in data[title]['new_theme']:
            node[cvt1[th]] += 1
        for thc in itertools.combinations(sorted(data[title]['new_theme']), 2):
            edge[cvt2[thc]] += 1

    n = []
    for i, th in enumerate(NEW_THEME):
        id = i + 1
        n.append({
            'theme_id': id,
            'theme_name': th,
            'count': node[i],
            'ratio': node[i] / node.sum()
        })

    e = []
    for i, thc in enumerate(itertools.combinations(NEW_THEME, 2)):
        id = i + 1
        thc = [cvt1[th] + 1 for th in thc]
        e.append({
            'id': id,
            'combination': thc,
            'count': edge[i],
            'ratio': edge[i] / edge.sum()
        })

    return json.dumps({'node': n, 'edge': e}, ensure_ascii=False) 



@app.route('/api/trend/genre/<genre>')
def trend_genre(genre):

    counter = collections.Counter([data[t]['year'] for t in data])
    weight = np.array([counter[str(i)] for i in range(2000, 2017)], dtype=float)
    weight /= weight.sum()

    mtx = np.zeros([17, 17])
    cvt = {th: i for i, th in enumerate(NEW_THEME)}

    for title in data:
        if data[title]['genre'] == genre:
            year = data[title]['year']
            if year is not None and int(year) >= 2000:
                r = int(year) - 2000
            else:
                r = np.random.choice(list(range(2000, 2017)), p=weight) - 2000
            for th in data[title]['new_theme']:
                c = cvt[th]
                mtx[c][r] += 1

    for i in range(17):
        mtx.T[i] /= mtx.T[i].sum()

    lst = []
    for th in cvt:
        l = [th]
        l += mtx[cvt[th]].tolist()
        lst.append(l)

    return json.dumps({'columns': lst}, ensure_ascii=False)


@app.route('/api/trend/magazine/<magazine>')
def trend_magazine(magazine):

    counter = collections.Counter([data[t]['year'] for t in data])
    weight = np.array([counter[str(i)] for i in range(2000, 2017)], dtype=float)
    weight /= weight.sum()

    mtx = np.zeros([17, 17])
    cvt = {th: i for i, th in enumerate(NEW_THEME)}

    for title in data:
        if data[title]['magazine'] == magazine:
            year = data[title]['year']
            if year is not None and int(year) >= 2000:
                r = int(year) - 2000
            else:
                r = np.random.choice(list(range(2000, 2017)), p=weight) - 2000
            for th in data[title]['new_theme']:
                c = cvt[th]
                mtx[c][r] += 1

    for i in range(17):
        mtx.T[i] /= mtx.T[i].sum()

    lst = []
    for th in cvt:
        l = [th]
        l += mtx[cvt[th]].tolist()
        lst.append(l)

    return json.dumps({'columns': lst}, ensure_ascii=False)


@app.route('/api/search')
def search():
    theme_s = request.args.getlist('theme', type=str)
    title = request.args.get('title')

    lst = []
    a = set(theme_s)
    if title or any(theme_s):

        for t in data:

            if title:
                if re.search(title, t):
                    lst.append(t)

            if any(theme_s):
                b = set(data[t]['new_theme'])
                if len(a & b) == len(a) and t not in lst:
                    lst.append(t)

    return json.dumps(lst, ensure_ascii=False)


@app.route('/comic/<title>')
def comic(title):

    info = data[title]
    similar_comic = []
    for t in data:
        a = set(info['theme'])
        b = set(data[t]['theme'])

        if len(a) >= 3:
            if len(a & b) >= 3 and title != t:
                similar_comic.append(t)
        else:
            if len(a & b) == len(a) and info['genre'] == data[t]['genre'] and title != t:
                similar_comic.append(t)

    info['similar_comic'] = similar_comic

    return json.dumps(info, ensure_ascii=False)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
