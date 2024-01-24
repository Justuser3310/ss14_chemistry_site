import os
import json

if not os.path.exists('db.json'):
	db = {}
	js = json.dumps(db, indent=2)
	with open("db.json", "w") as outfile:
		outfile.write(js)
	print('Created new db.json')


def read_db():
	with open('db.json', 'r') as openfile:
		db = json.load(openfile)
	return db
def write_db(db):
	js = json.dumps(db, indent=2)
	with open("db.json", "w") as outfile:
		outfile.write(js)
