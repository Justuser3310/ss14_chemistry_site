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


def localize(recipes, locale):
	loc_recipes = {}
	# Итерируем элементы
	for element in recipes:
		# Итерируем составные
		el = recipes[element]
		# Локализованные составные
		loc_comps = {}
		for comp in el.comps:
			# Ищем перевод
			if comp.lower() in locale:
				loc = locale[comp.lower()].capitalize()
				loc_comps[loc] = el.comps[comp]
			else:
				loc_comps[comp] = el.comps[comp]
		# Заменяем на локализованное
		el.comps = loc_comps

		# Локализуем ключ
		if element.lower() in locale:
			loc = locale[element.lower()].capitalize()
			loc_recipes[loc] = recipes[element]
		else:
			loc_recipes[element] = recipes[element]

	return loc_recipes
