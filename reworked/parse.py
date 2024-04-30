from requests import get
from yaml import load, SafeLoader
from reag__ import reag__

def parse_yml(url = 'https://raw.githubusercontent.com/SerbiaStrong-220/space-station-14/master/Resources/Prototypes/Recipes/Reactions/medicine.yml'):
	yml = load(get(url).content.decode('utf-8'), Loader=SafeLoader)
	return yml

def parse_ftl(url = 'https://raw.githubusercontent.com/SerbiaStrong-220/space-station-14/master/Resources/Locale/ru-RU/reagents/meta/medicine.ftl'):
	raw = get(url).content.decode('utf-8')
	locales = {}
	for i in raw.splitlines():
		if 'name' in i:
			splitted = i.split()
			name = splitted[0][13:]
			locale = splitted[2]
			locales[name] = locale
	return locales

def load_recipes(url = 'https://raw.githubusercontent.com/SerbiaStrong-220/space-station-14/master/Resources/Prototypes/Recipes/Reactions/medicine.yml', category = '-'):
	yml = parse_yml(url)
	recipes = {}
	for element in yml:
		product = element["id"]
		comps = {}
		for elem in element["reactants"]:
			comps[elem] = element["reactants"][elem]["amount"]
		for id, value in element["products"].items():
			out =  value
			recipes[product] = reag__(category=category, comps=comps, out=out)
	return recipes
