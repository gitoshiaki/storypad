import os
import csv
import json
import pickle


def load_file(filepath):
	root, ext = os.path.splitext(filepath)

	if ext == '.json':
		with open(filepath, 'r', encoding='utf-8') as fp:
			return json.load(fp)

	elif ext == '.pickle':
		with open(filepath, 'rb') as fp:
			return pickle.load(fp)

	elif ext == '.csv':
		obj = []
		with open(filepath, 'r', newline='', encoding='utf-8') as fp:
			reader = csv.reader(fp)
			header = next(reader)
			for row in reader:
				obj.append(row)
			return obj

	else:
		print('check the extension: {}'.format(ext))


def save_obj(obj, filepath):
	root, ext = os.path.splitext(filepath)

	if ext == '.json':
		with open(filepath, 'w', encoding='utf-8') as fp:
			json.dump(obj, fp, ensure_ascii=False, sort_keys=True)

	elif ext == '.pickle':
		with open(filepath, 'wb') as fp:
			pickle.dump(obj, fp)

	elif ext == '.csv':
		with open(filepath, 'w', encoding='utf-8') as fp:
			writer = csv.writer(fp, lineterminator='\n')
			writer.writerows(obj)

	else:
		print('check the extension: {}'.format(ext))
