from parse import *
from calc import calc
from db import *

'''
# Загружаем локализацию
locales_url = ['medicine', 'chemicals']
locales = load_locales(locales_url)

# Загружаем сырые рецепты
recipes_url = ['medicine']
raw_recipes = load_recipes(recipes_url)

# Локализируем
recipes = localize(raw_recipes, locales)
# Сохранаяем данные
save(recipes, 'raw_db.json')
'''

rec = load('raw_db.json')

# Делаем предрасчёты
#calculated = 
