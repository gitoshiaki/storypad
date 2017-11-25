import os
import json
import pickle


def file2object(filepath):
	root, ext = os.path.splitext(filepath)

	isPickle = ext == '.pickle'
	if isPickle:
		mode = 'rb'
		encoding = None
	else:
		mode = 'r'
		encoding = 'utf-8'

	with open(filepath, mode=mode, encoding=encoding) as fp:
		if isPickle:
			return pickle.load(fp)
		else:
			return json.load(fp)
