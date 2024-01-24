import yaml
import json
import requests
from fluent.syntax import parse, ast

yaml.SafeLoader.add_multi_constructor("", lambda loader, tag_suffix, node: None)

# медицинские реагентов
REAGENTS_URL = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Prototypes/Reagents/medicine.yml"
MEDICINE_LOCALISATION_URL = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Locale/ru-RU/reagents/meta/medicine.ftl"
RECIPES_URL = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Prototypes/Recipes/Reactions/medicine.yml"

# элементы раздатчика химикатов
ELEMENTS_URL = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Prototypes/Reagents/elements.yml"
ELEMENTS_LOCALISATION_URL = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Locale/ru-RU/reagents/meta/elements.ftl"

# токсины
TOXINS_URL = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Prototypes/Reagents/toxins.yml"
TOXINS_LOCALISATION_URL = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Locale/ru-RU/reagents/meta/toxins.ftl"

# локализация наркотиков/наркотических препаратов
NARCOTICS_LOCALISATION_URL = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Locale/ru-RU/reagents/meta/narcotics.ftl"

# газы
GASES_URL = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Prototypes/Reagents/gases.yml"
GASES_LOCALISATION_URL = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Locale/ru-RU/reagents/meta/gases.ftl"

# все съедобное и питьевое
FOOD_URL = "https://github.com/SerbiaStrong-220/space-station-14/raw/dev/Resources/Prototypes/Reagents/Consumable/Food/food.yml"
DRINKS_URL = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Prototypes/Reagents/Consumable/Drink/drinks.yml"
DRINKS_LOCALISATION_URL = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Locale/ru-RU/reagents/meta/consumable/drink/drinks.ftl"
FOOD_LOCALISATION_URL = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Locale/ru-RU/reagents/meta/consumable/food/ingredients.ftl"

localisation_list = [MEDICINE_LOCALISATION_URL, ELEMENTS_LOCALISATION_URL, TOXINS_LOCALISATION_URL,
                     GASES_LOCALISATION_URL, DRINKS_LOCALISATION_URL, FOOD_LOCALISATION_URL, NARCOTICS_LOCALISATION_URL]


class Reagent:
    def __init__(self, init_data: dict):
        self.__name: str = init_data.get("name")
        self.__desc: str = init_data.get("desc")
        self.__recipe: dict = init_data.get("reactants")
        self.__product = init_data.get("products")
        # raw значения которые обработаны

        self.heat: bool = init_data.get("heat")

    @property
    def name(self):
        return localise(self.__name).capitalize()

    @property
    def description(self):
        return localise(self.__desc)

    @property
    def recipe(self):
        result = []
        for item in self.__recipe:
            # Приводим к НОРМАЛЬНОМУ виду
            # "Бикаридин": [ [0, "Углерод", 1], [1, "Инапровалин"] ]
            result.append([self.__recipe[item]["reagent"], localise(item).capitalize(), self.__recipe[item]["amount"]])
        return result


def load_localisation():
    data = {"elements": {}, "reagents": {}, "gases": {}, "food": {}, "drinks": {}, "total": {}}
    elements = yaml.load(requests.get(ELEMENTS_URL).content.decode("utf-8"), Loader=yaml.SafeLoader)
    for element in elements:
        data["elements"][element["id"]] = {"name": element["name"], "desc": element["desc"]}
    reagents = yaml.load(requests.get(REAGENTS_URL).content.decode("utf-8"), Loader=yaml.SafeLoader)
    for reagent in reagents:
        data["reagents"][reagent["id"]] = {"name": reagent["name"], "desc": reagent["desc"]}
    gases = yaml.load(requests.get(GASES_URL).content.decode("utf-8"), Loader=yaml.SafeLoader)
    for gase in gases:
        data["gases"][gase["id"]] = {"name": gase["name"], "desc": gase["desc"]}
    food = yaml.load(requests.get(FOOD_URL).content.decode("utf-8"), Loader=yaml.SafeLoader)
    for item in food:
        data["food"][item["id"]] = {"name": item["name"], "desc": item["desc"]}
    drinks = yaml.load(requests.get(DRINKS_URL).content.decode("utf-8"), Loader=yaml.SafeLoader)
    for drink in drinks:
        data["drinks"][drink["id"]] = {"name": drink["name"], "desc": drink["desc"]}

    for url in localisation_list:
        content = requests.get(url).content.decode("utf-8")
        for entry in parse(content).body:
            if isinstance(entry, ast.Message):
                data["total"][entry.id.name] = entry.value.elements[0].value

    with open("locale.json", mode="w", encoding="utf-8") as localisation_file:
        json.dump(data, localisation_file, ensure_ascii=False, indent=2)


def localise(key: str) -> str:
    # TODO: почистить это говно
    with open("locale.json", mode="r", encoding="utf-8") as file:
        data = json.load(file)
        if key in data["elements"]:
            return data["total"].get(data["elements"][key]["name"])
        elif key in data["reagents"]:
            return data["total"].get(data["reagents"][key]["name"])
        elif key in data["gases"]:
            return data["total"].get(data["gases"][key]["name"])
        elif key in data["food"]:
            return data["total"].get(data["food"][key]["name"])
        elif key in data["drinks"]:
            return data["total"].get(data["drinks"][key]["name"])
        elif key in data["total"]:
            return data["total"][key]
        else:
            return f"[!] {key}"


load_localisation()

content = {}

for item in yaml.load(requests.get(REAGENTS_URL).content.decode("utf-8"), Loader=yaml.SafeLoader):
    content[item["id"]] = {"name": item["name"], "desc": item["desc"]}
for item in yaml.load(requests.get(TOXINS_URL).content.decode("utf-8"), Loader=yaml.SafeLoader):
    content[item["id"]] = {"name": item["name"], "desc": item["desc"]}
for item in yaml.load(requests.get(RECIPES_URL).content.decode("utf-8"), Loader=yaml.SafeLoader):
    if item["id"] not in content:
        continue
    content[item["id"]]["heat"] = "minTemp" in item
    content[item["id"]]["reactants"] = {
        element: {"amount": item["reactants"][element]["amount"], "reagent": element in content} for element in
        item["reactants"]}
    content[item["id"]]["products"] = item["products"]

reagents = [Reagent(init_data=content[item]) for item in content if "reactants" in content[item]]
print(reagents[0].name)
print(reagents[0].recipe)

db = {x.name: x.recipe for x in reagents}
with open("db.json", mode="w", encoding="utf-8") as db_file:
    json.dump(db, db_file, ensure_ascii=False, indent=2)
