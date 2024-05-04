import os
import json
from reag__ import reag__
from precalc__ import precalc__

if not os.path.exists('precalc.json'):
	db = {}
	js = json.dumps(db, indent=2)
	with open('precalc.json', 'w') as outfile:
		outfile.write(js)
	print('Created new precalc.json')
if not os.path.exists('raw_db.json'):
  db = {}
  js = json.dumps(db, indent=2)
  with open('raw_db.json', 'w') as outfile:
    outfile.write(js)
  print('Created new raw_db.json')


def read_db(file):
	with open(file, 'r', encoding='utf-8') as openfile:
		db = json.load(openfile)
	return db

def write_db(db, file):
	js = json.dumps(db, indent=2, ensure_ascii=False)
	with open(file, 'w', encoding='utf-8') as outfile:
		outfile.write(js)



def save(db, file):
	raw = {}
	for el in db:
		class_data = db[el].get_all()
		raw[el] = class_data
	write_db(raw, file)

def load(file, type = 'raw'):
	raw = read_db(file)
	db = {}
	if type == 'raw':
		for el in raw:
			db[el] = reag__(raw[el][0], raw[el][1], raw[el][2])
	elif type == 'precalc':
		for el in raw:
			db[el] = precalc__(raw[el])
	return db
