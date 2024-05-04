from requests import get
from yaml import load, SafeLoader
from reag__ import reag__

#### Локализация ####

def parse_ftl(el, prefix = 'https://raw.githubusercontent.com/SerbiaStrong-220/space-station-14/master/Resources/Locale/ru-RU/reagents/meta'):
	url = f'{prefix}/{el}.ftl'
	raw = get(url).content.decode('utf-8')
	locales = {}
	for i in raw.splitlines():
		if 'name' in i:
			splitted = i.split()
			name = splitted[0][13:]
			locale = splitted[2]
			locales[name] = locale
	return locales

def load_locales(locales_url):
	locales = {}
	for el in locales_url:
		locales = locales | parse_ftl(el)
	return locales

#### Рецепты ####

def parse_yml(el, prefix = 'https://raw.githubusercontent.com/SerbiaStrong-220/space-station-14/master/Resources/Prototypes/Recipes/Reactions'):
	url = f'{prefix}/{el}.yml'
	yml = load(get(url).content.decode('utf-8'), Loader=SafeLoader)
	return yml

def load_recipes(recipes_url, prefix = 'https://raw.githubusercontent.com/SerbiaStrong-220/space-station-14/master/Resources/Prototypes/Recipes/Reactions'):
	for el in recipes_url:
		yml = parse_yml(el, prefix)
		recipes = {}
		for element in yml:
			product = element["id"]
			comps = {}
			for elem in element["reactants"]:
				comps[elem] = element["reactants"][elem]["amount"]
			for id, value in element["products"].items():
				out =  value
				recipes[product] = reag__(category=el, comps=comps, out=out)
	return recipes


#### Локализируем ####

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
