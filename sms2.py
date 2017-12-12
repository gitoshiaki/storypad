from flask import Flask, request, render_template, send_file
from flask_cors import CORS

from db_setup import engine, Comics, ComicReviewNouns, \
	ComicStoryNouns, ReviewNouns, StoryNouns, ComicArtists, Artists
from sqlalchemy.orm import sessionmaker

from wordcloud import WordCloud

import io
import os
import json
import itertools
import collections
import numpy as np

from const import *

# wordcloud settings
font_path = './misc/ヒラギノ丸ゴ ProN W4.ttc'
kwargs = {
	'background_color': 'white',
	'font_path': font_path,
	'width': 1500,
	'height': 1000
}

Session = sessionmaker(engine)
session = Session()

app = Flask(__name__)
CORS(app)


def calculate_distance(title_id, array):
	"""対象の漫画と他の漫画とのユークリッド距離を求めて、距離の近い３０作品のtitle_idと距離の値のリストを作る"""
	distance_list = []
	vec0 = array[title_id]
	for i, vec1 in enumerate(array):
		distance = np.linalg.norm(vec1 - vec0)
		if i == title_id:
			continue
		else:
			distance_list.append((i, distance))
	distance_list = sorted(distance_list, key=lambda x: x[1])[:30]

	return distance_list


def fit_to_c3(array, isCombination=False):
	for m, r in enumerate(array):
		if r.sum() != 0:
			r = np.round(r / r.sum() * 100, 2)
		array[m] = r

	columns = []
	if isCombination:
		for m, r in enumerate(array.T):
			lst = r.tolist()
			combination = '&'.join(num2combination[m])
			lst.insert(0, combination)
			columns.append(lst)

	else:
		for m, r in enumerate(array.T):
			lst = r.tolist()
			theme = num2theme[m]
			lst.insert(0, theme)
			columns.append(lst)

	return {'columns': columns}


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def dashboard(path):
	return render_template('index.html')


@app.route('/api/network_graph')
def network_graph():
	return json.dumps(NETWORK_GRAPH, ensure_ascii=False)


@app.route('/api/themes')
def theme17():
	return json.dumps(THEME17, ensure_ascii=False)


# TODO: 正しいトレンドグラフを作る
@app.route('/api/trend/genre/<genre>')
def trend_genre(genre):
	genre_id = genre2num[genre]
	array = np.zeros([17, 17])

	for r in session.query(Comics.theme17).filter_by(genre_id=genre_id).all():
		i = np.random.choice(range(0, 17))
		for theme in r[0]:
			j = theme2num[theme]
			array[i][j] += 1

	data = fit_to_c3(array)
	return json.dumps(data, ensure_ascii=False)


# TODO: 正しいトレンドグラフを作る
@app.route('/api/trend/magazine/<magazine>')
def trend_magazine(magazine):
	magazine_id = magazine2num[magazine]
	array = np.zeros([17, 17])

	for r in session.query(Comics.theme17).filter_by(magazine_id=magazine_id).all():
		i = np.random.choice(range(0, 17))
		for theme in r[0]:
			j = theme2num[theme]
			array[i][j] += 1

	data = fit_to_c3(array)
	return json.dumps(data, ensure_ascii=False)


# TODO: 正しいトレンドグラフを作る
@app.route('/api/trend/theme')
def trend_theme():
	array = np.zeros([17, 17])

	for r in session.query(Comics.theme17).all():
		i = np.random.choice(range(0, 17))
		for theme in r[0]:
			j = theme2num[theme]
			array[i][j] += 1

	data = fit_to_c3(array)
	return json.dumps(data, ensure_ascii=False)


# TODO: 正しいトレンドグラフを作る
@app.route('/api/trend/theme_combination')
def trend_theme_combination():
	array = np.zeros([17, 136])

	for r in session.query(Comics.theme17).all():
		i = np.random.choice(range(0, 17))
		for cmb in itertools.combinations(r[0], 2):
			j = combination2num[cmb]
			array[i][j] += 1

	data = fit_to_c3(array, isCombination=True)
	return json.dumps(data, ensure_ascii=False)


# TODO: レスポンスないのタイトル数制限の有無
@app.route('/api/search/genre')
def search_by_genre():
	genre = request.args.get('genre')
	genre_id = genre2num[genre]
	titles = []
	for title_id, title in session.query(Comics.title_id, Comics.title) \
		.filter_by(genre_id=genre_id).limit(30).all():
		titles.append({
			'title_id': title_id,
			'title': title
		})

	return json.dumps(titles, ensure_ascii=False)


@app.route('/api/search/theme')
def search_by_theme():
	theme_lst = request.args.getlist('theme')
	titles = []
	for title_id, title, themes in session.query(Comics.title_id, Comics.title, Comics.theme17).all():
		if set(themes) >= set(theme_lst):

			titles.append({
				'title_id': title_id,
				'title': title
			})

	return json.dumps(titles, ensure_ascii=False)


@app.route('/api/search')
def search_by_title():
	title = request.args.get('title')
	titles = []
	for r in session.query(Comics.title) \
		.filter(Comics.title.op('like')('%{}%'.format(title))).all():
		titles.append(r[0])
	return json.dumps(titles, ensure_ascii=False)


@app.route('/api/comic/<title>')
def comic(title):
	res = session.query(Comics).filter_by(title=title).first()
	similar_comic_list = similar_comics(title, returnJson=False)
	genre = num2genre[res.genre_id]
	magazine = num2magazine[res.magazine_id]
	data = {
		'title': res.title,
		'artist': res.artist,
		'genre': genre,
		'theme': res.theme17,
		'story': res.story,
		'magazine': magazine,
		'similar_comic': similar_comic_list
	}
	return json.dumps(data, ensure_ascii=False)


@app.route('/api/artist/<artist_name>')
def artist(artist_name):
	lst = []
	for title_id, title in session.query(Comics.title_id, Comics.title) \
		.filter(Comics.title_id==ComicArtists.title_id) \
		.filter(ComicArtists.artist_id==Artists.artist_id) \
		.filter(Artists.artist_name==artist_name).all():

		lst.append({
			'title_id': title_id,
			'title': title
		})

	return json.dumps(lst, ensure_ascii=False)


# TODO: サーバーサイドで文字クラウドを生成
@app.route('/api/word_cloud/<title>')
def word_cloud(title):
	similar_comic_ids = similar_comics(title, returnIDs=True)
	words = {}

	for w, v in session.query(ReviewNouns.noun_name, ComicReviewNouns.value) \
			.filter(ReviewNouns.noun_id == ComicReviewNouns.noun_id) \
			.filter(ComicReviewNouns.title_id.in_(similar_comic_ids)).all():
		if w in words:
			words[w] += v
		else:
			words[w] = v

	for w, v in session.query(StoryNouns.noun_name, ComicStoryNouns.value) \
			.filter(StoryNouns.noun_id == ComicStoryNouns.noun_id) \
			.filter(ComicStoryNouns.title_id.in_(similar_comic_ids)).all():
		if w in words:
			words[w] += v
		else:
			words[w] = v

	wc = WordCloud(**kwargs).generate_from_frequencies(words)
	return 'hello world'


# return send_file()


@app.route('/api/similar_comics/<title>')
def similar_comics(title, returnJson=True, returnIDs=False):
	title_id = session.query(Comics.title_id).filter_by(title=title).first()[0]
	distances = calculate_distance(title_id, COMICS_ARRAY)
	similar_comic_ids = [t_id for t_id, _ in distances]

	if returnIDs:
		return similar_comic_ids

	similar_comic_lst = []
	for r in session.query(Comics.title).filter(Comics.title_id.in_(similar_comic_ids)).all():
		similar_comic_lst.append(r[0])

	if returnJson:
		return json.dumps(similar_comic_lst, ensure_ascii=False)
	else:
		return similar_comic_lst


if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
	app.run(host="0.0.0.0", port=port, debug=True)
