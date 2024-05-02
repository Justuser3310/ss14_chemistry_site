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

def localize(ftl = parse_ftl()):
    recipes = load_recipes()
    for k, v in list(recipes.items()):
        for word in ftl:
            if k.lower() == word:
                new_key = ftl[word].capitalize()
                recipes[new_key] = recipes.pop(k)
                for k1, v1 in list(recipes[new_key].comps.items()):
                    for word1 in ftl:
                        if k1.lower() == word1:
                            new_key1 = ftl[word1]
                            recipes[new_key].comps[new_key1] = recipes[new_key].comps.pop(k1)
            else:
                try:
                    for k1, v1 in list(recipes[k].comps.items()):
                        for word1 in ftl:
                            if k1.lower() == word1:
                                new_key1 = ftl[word1].capitalize()
                                recipes[k].comps[new_key1] = recipes[k].comps.pop(k1)
                except:
                    for k1, v1 in list(recipes[new_key].comps.items()):
                        for word1 in ftl:
                            if k1.lower() == word1:
                                new_key1 = ftl[word1].capitalize()
                                recipes[new_key].comps[new_key1] = recipes[new_key].comps.pop(k1)
    return recipes