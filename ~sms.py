from flask import Flask
from flask import request, render_template

import json
import itertools
import collections
import numpy as np
from const import NEW_THEME

app = Flask(__name__)

FILE = 'new_comic_dict.json'
with open(FILE, 'r') as fp:
    data = json.load(fp)


@app.route('/')
def hello_world():
    return render_template('index.html')


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
        thc = [cvt1[th] + 1 for th in thc]  # 切り替え可能
        e.append({
            'id': id,
            'combination': thc,
            'count': edge[i],
            'ratio': edge[i] / edge.sum()
        })

    return json.dumps({'node': n, 'edge': e}, ensure_ascii=False)


'''
@app.route('/api/network_graph')
def network_graph():

    theme_dic = {}
    theme_combination_dic = {}
    for title in data:
        for theme in data[title]['new_theme']:
            if theme in theme_dic:
                theme_dic[theme] += 1
            else:
                theme_dic[theme] = 1
        for theme_combination in itertools.combinations(data[title]['new_theme'], 2):
            if theme_combination in theme_combination_dic:
                theme_combination_dic[theme_combination] += 1
            else:
                theme_combination_dic[theme_combination] = 1

    node = []
    for i, theme in enumerate(NEW_THEME):
        id = i + 1
        if theme in theme_dic:
            count = theme_dic[theme]
        else:
            count = 0
        ratio = count / max(list(theme_dic.values()))
        node.append({
            'theme_id': id,
            'theme_name': theme,
            'count': count,
            'ratio': ratio
        })

    edge = []
    for i, theme_combination in enumerate(itertools.combinations(NEW_THEME, 2)):
        id = i + 1
        if theme_combination in theme_combination_dic:
            count = theme_combination_dic[theme_combination]
        else:
            count = 0
        ratio = count / max(list(theme_combination_dic.values()))
        edge.append({
            'id': id,
            'combinaiton': theme_combination,
            'count': count,
            'ratio': ratio
        })

    network = {
        'node': node,
        'edge': edge
    }

    return json.dumps(network, ensure_ascii=False)
'''


@app.route('/search')
def comic_info():

    title = request.args.get('title')

    theme1 = request.args.get('theme1')
    theme2 = request.args.get('theme2')
    theme3 = request.args.get('theme3')
    theme_s = [theme1, theme2, theme3]

    if title:

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

    if any(theme_s):

        a = set()
        for th in theme_s:
            if th:
                a.add(th)

        lst = []
        for t in data:
            b = set(data[t]['new_theme'])
            if len(a & b) == len(a):
               lst.append(t)

        return json.dumps(lst, ensure_ascii=False)


@app.route('/trend')
def trend():

    genre = '青年漫画'

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

    lst =[]
    for th in cvt:
        l = [th]
        l += mtx[cvt[th]].tolist()
        lst.append(l)

    dic = {
        'columns': lst
    }

    return json.dumps(dic, ensure_ascii=False)


'''
@app.route('/trend')
def trend():

    counter = collections.Counter([data[t]['year'] for t in data])
    weight = np.array([counter[str(i)] for i in range(2000, 2017)], dtype=float)
    weight /= weight.sum()

    mtx = np.zeros([17, 17])
    cvt = {th: i for i, th in enumerate(NEW_THEME)}

    for title in data:
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

    dic = {}
    for th in cvt:
        dic[th] = mtx[cvt[th]].tolist()

    return json.dumps(dic, ensure_ascii=False)
'''


if __name__ == '__main__':
    app.run()
