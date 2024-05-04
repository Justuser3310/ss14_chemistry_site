import os
import json
from reag__ import reag__

if not os.path.exists('db.json'):
	db = {}
	js = json.dumps(db, indent=2)
	with open('db.json', 'w') as outfile:
		outfile.write(js)
	print('Created new db.json')
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

def load(file):
	raw = read_db(file)
	db = {}
	for el in raw:
		db[el] = reag__(raw[el][0], raw[el][1], raw[el][2])
	return db
