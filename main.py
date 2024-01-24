import yaml
import json
import requests
from fluent.syntax import parse, ast
from db import write_db

yaml.SafeLoader.add_multi_constructor("", lambda loader, tag_suffix, node: None)

# список реагентов
REAGENTS_URL = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Prototypes/Reagents/medicine.yml"

# список токсинов
TOXINS_URL = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Prototypes/Reagents/toxins.yml"

# рецепты медицинских реагентов
RECIPES_URL = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Prototypes/Recipes/Reactions/medicine.yml"

# локализация медицинских реагентов
MEDICINE_LOCALISATION_URL = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Locale/ru-RU/reagents/meta/medicine.ftl"

# локализация элементов из раздатчика химикатов
ELEMENTS_LOCALISATION_URL = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Locale/ru-RU/reagents/meta/elements.ftl"

# локализация токсинов/"токсичных реагентов" типа пакса и т.п
TOXINS_LOCALISATION_URL = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Locale/ru-RU/reagents/meta/toxins.ftl"

# локализация наркотиков/наркотических препаратов
NARCOTICS_LOCALISATION_URL = "https://github.com/SerbiaStrong-220/space-station-14/raw/master/Resources/Locale/ru-RU/reagents/meta/narcotics.ftl"

localisation_list = [MEDICINE_LOCALISATION_URL, ELEMENTS_LOCALISATION_URL, TOXINS_LOCALISATION_URL,
                     NARCOTICS_LOCALISATION_URL]


class Reagent:
    def __init__(self, init_data: dict):
        self.__name: str = init_data.get("name")
        self.__desc: str = init_data.get("desc")
        self.__recipe: dict = init_data.get("reactants")
        self.__product = init_data.get("products")
        # raw значения которые не нужны

        self.heat: bool = init_data.get("heat")

    @property
    def name(self):
        return localise(self.__name)

    @property
    def description(self):
        return localise(self.__desc)

    @property
    def recipe(self):
        result = [self.heat]
        for item in self.__recipe:
            result.append([item, self.__recipe[item]["amount"], self.__recipe[item]["reagent"]])
        return result

    def dict(self):
        return {"name": self.name, "desc": self.description, "recipe": self.recipe}


def load_localisation():
    data = {}
    for url in localisation_list:
        content = requests.get(url).content.decode("utf-8")
        for entry in parse(content).body:
            if isinstance(entry, ast.Message):
                data[entry.id.name] = entry.value.elements[0].value
    with open("locale.json", mode="w", encoding="utf-8") as localisation_file:
        json.dump(data, localisation_file, ensure_ascii=False, indent=2)


def localise(key: str) -> str:
    with open("locale.json", mode="r", encoding="utf-8") as file:
        data = json.load(file)
        return data.get(key, f"[!] {key}")


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

write_db({x.name: x.dict() for x in reagents})
