def expand_recipe(recipe, recipes):
	global expanded

	ok = False
	part = 1 # Одна часть
	while not ok:
		ok = True
		# Перебираем элементы
		for el in recipe:
			# Если составное
			if el in recipes:
				# Одна часть должна делиться без остатка!
				if part % recipes[el].out != 0:
					ok = False
					part += 1
					expanded = {}
					break
				else:
					expand_recipe(recipes[el].comps, recipes)
			else:
				if el in expanded:
					expanded[el] += recipe[el]*part
				else:
					expanded[el] = recipe[el]*part

def calc(element, amount, recipes):
	# TODO: Пока только выводит расширенную версию рецепта
	recipe, out = recipes[element].comps, recipes[element].out

	global expanded
	expanded = {}
	expand_recipe(recipe, recipes)

	return expanded


from parse import *
#print( load_recipes() )
print( calc('Dylovene', 100, load_recipes()) )
