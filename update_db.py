import yaml
import json
import requests
from fluent.syntax import parse, ast

yaml.SafeLoader.add_multi_constructor("", lambda loader, tag_suffix, node: None)

# медицинские реагентов
MEDICINE_R = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Prototypes/Reagents/medicine.yml"
MEDICINE = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Prototypes/Recipes/Reactions/medicine.yml"
MEDICINE_LOCALISATION = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Locale/ru-RU/reagents/meta/medicine.ftl"


CHEMICALS_R = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Prototypes/Reagents/chemicals.yml"
CHEMICALS = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Prototypes/Recipes/Reactions/chemicals.yml"
CHEMICALS_LOCALISATION= "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Locale/ru-RU/reagents/meta/chemicals.ftl"

# элементы раздатчика химикатов
ELEMENTS_URL = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Prototypes/Reagents/elements.yml"
ELEMENTS_LOCALISATION_URL = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Locale/ru-RU/reagents/meta/elements.ftl"

# токсины
TOXINS = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Prototypes/Reagents/toxins.yml"
TOXINS_LOCALISATION_URL = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Locale/ru-RU/reagents/meta/toxins.ftl"

# локализация наркотиков/наркотических препаратов
NARCOTICS_LOCALISATION_URL = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Locale/ru-RU/reagents/meta/narcotics.ftl"

# газы
GASES_URL = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Prototypes/Reagents/gases.yml"
GASES_LOCALISATION_URL = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Locale/ru-RU/reagents/meta/gases.ftl"

# биология
BIOLOGY_URL = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Prototypes/Reagents/biological.yml"
BIOLOGY_LOCALISATION_URL = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Locale/ru-RU/reagents/meta/biological.ftl"

# ботаника
BOTANY = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Prototypes/Reagents/botany.yml"
BOTANY_LOCALISATION_URL = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Locale/ru-RU/reagents/meta/botany.ftl"

# все съедобное и питьевое
FOOD = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Prototypes/Reagents/Consumable/Food/condiments.yml"
FOOD_R = "https://raw.githubusercontent.com/SerbiaStrong-220/space-station-14/master/Resources/Prototypes/Reagents/Consumable/Food/condiments.yml"

INGREDIENTS_URL = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Prototypes/Reagents/Consumable/Food/ingredients.yml"
DRINKS_URL = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Prototypes/Reagents/Consumable/Drink/drinks.yml"
ALCOHOL_URL = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Prototypes/Reagents/Consumable/Drink/alcohol.yml"
INGREDIENTS_LOCALISATION_URL = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Locale/ru-RU/reagents/meta/consumable/food/ingredients.ftl"
ALCOHOL_LOCALISATION_URL = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Locale/ru-RU/reagents/meta/consumable/drink/alcohol.ftl"
CONDIMENTS_LOCALISATION_URL = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Locale/ru-RU/reagents/meta/consumable/food/condiments.ftl"
DRINKS_LOCALISATION_URL = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Locale/ru-RU/reagents/meta/consumable/drink/drinks.ftl"
FOOD_LOCALISATION_URL = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Locale/ru-RU/reagents/meta/consumable/food/ingredients.ftl"


class Reagent:
	def __init__(self, init_data: dict):
		self.__name: str = init_data.get("name")
#		self.__desc: str = init_data.get("desc")
		self.__recipe: dict = init_data.get("reactants")
		self.__product = init_data.get("products")
		self.__category = init_data.get("category")
		# raw значения которые обработаны

		self.heat: bool = init_data.get("heat")

	@property
	def name(self):
		return localise(self.__name).capitalize()

#		@property
#		def description(self):
#			return localise(self.__desc)

	@property
	def recipe(self):
		result = []

		# Добавляем количество в итоге
		react_res = self.__product
		for i in react_res:
			if i.lower() == self.__name.replace('reagent-name-','',1).replace('-','',1):
				result.append(react_res[i])

		# Добавляем категорию
		print(self.__category)
		result.append(self.__category)

		if not self.__recipe:
			return None
		for item in self.__recipe:
				# "Бикаридин": [ 2, ["Углерод", 1], ["Инапровалин", 1] ]
				result.append([localise(item).capitalize(), self.__recipe[item]['amount']])
		#print(result)
		return result


def load_localisation():
    data = {"elements": {}, "placeholders": {}}
    elements_urls = [ELEMENTS_URL, REAGENTS_URL, TOXINS_URL, GASES_URL, FOOD_URL, DRINKS_URL, BIOLOGY_URL,
                     CONDIMENTS_URL, BOTANY_URL, ALCOHOL_URL, CHEMICALS_URL, INGREDIENTS_URL]
    for url in elements_urls:
        response = yaml.load(requests.get(url).content.decode("utf-8"), Loader=yaml.SafeLoader)
        for i in response:
            data["elements"][i["id"]] = {"name": i["name"], "desc": i["desc"]}

    localisation_urls = [MEDICINE_LOCALISATION, ELEMENTS_LOCALISATION_URL, TOXINS_LOCALISATION_URL,
                         GASES_LOCALISATION_URL, DRINKS_LOCALISATION_URL, FOOD_LOCALISATION_URL,
                         CONDIMENTS_LOCALISATION_URL, BIOLOGY_LOCALISATION_URL, NARCOTICS_LOCALISATION_URL,
                         BOTANY_LOCALISATION_URL, ALCOHOL_LOCALISATION_URL, CHEMICALS_LOCALISATION,
                         INGREDIENTS_LOCALISATION_URL]

    for url in localisation_urls:
        response = requests.get(url).content.decode("utf-8")
        for entry in parse(response).body:
            if isinstance(entry, ast.Message):
                data["placeholders"][entry.id.name] = entry.value.elements[0].value

    with open("locale.json", mode="w", encoding="utf-8") as localisation_file:
        json.dump(data, localisation_file, ensure_ascii=False, indent=2)


def localise(key: str) -> str:
	with open("locale.json", mode="r", encoding="utf-8") as file:
		data = json.load(file)
		if "-" in key:  # если это placeholder
			return data["placeholders"].get(key, f"[p] {key}")
		elif key in data["elements"]:
			return localise(data["elements"][key]["name"])
		else:
			print('No localisation: ', key)
			return f"[!] {key}"

# Показатель прогресса
from tqdm import tqdm

# Загрузить локализацию если нету файла
import os
if not os.path.exists('locale.json'):
	load_localisation()

content = {}

def yml_load(url):
	return yaml.load(requests.get(url).content.decode("utf-8"), Loader=yaml.SafeLoader)


def load_reagents(url,name):
	for item in tqdm(yml_load(url), desc=name+'_reagents'):
		content[item["id"]] = {"name": item["name"], "desc": item["desc"]}

def load_recipes(url,name):
	global content
	for item in tqdm(yml_load(url), desc=name+'_recipes'):
#		print(item["id"])
		if item["id"] not in content:
			continue
		content[item["id"]]["heat"] = "minTemp" in item
		content[item["id"]]["reactants"] = {
			element: {"amount": item["reactants"][element]["amount"], "reagent": element in content} for element in
			item["reactants"]}
		content[item["id"]]["products"] = item["products"]
		content[item["id"]]["category"] = name

load_reagents(BOTANY, 'botany')
load_reagents(TOXINS, 'toxins')
load_reagents(MEDICINE_R, 'medicine')
# Не загружается?
load_reagents(CHEMICALS_R, 'chemicals')
#load_reagents(FOOD_R, 'food')
load_reagents(FOOD_R, 'food')


load_recipes(MEDICINE, 'medicine')
load_recipes(CHEMICALS, 'chemicals')
load_recipes(CHEMICALS, 'chemicals')

#                                                                TODO: Включать ли токсины без крафта? (некоторые имеют крафт)
reagents = [Reagent(init_data=content[item]) for item in content if "reactants" in content[item]]

db = {x.name: x.recipe for x in reagents}

from db import *
write_db(db)
