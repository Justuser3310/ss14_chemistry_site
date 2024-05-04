global expanded
def expand_recipe(recipe, recipes, main = False):
	global expanded
	if main:
		expanded = {}

	ok = False
	part = 1 # Одна часть
	while not ok:
		ok = True
		min_vol = 0 # Объём мин. рецепта (вход)
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
					min_vol += expand_recipe(recipes[el].comps, recipes)
			else:
				if el in expanded:
					expanded[el] += recipe[el]*part
				else:
					expanded[el] = recipe[el]*part

				min_vol += recipe[el]*part

	if main:
		return expanded, min_vol, part
	else:
		return min_vol

def calc(element, amount, recipes):
	# Получаем характеристику элемента
	recipe, vol_out = recipes[element].comps, recipes[element].out
	# Расчитываем минимальный рецепт
	expanded, vol_in, part = expand_recipe(recipe, recipes, True)

	need = amount//vol_in
	for i in expanded:
		expanded[i] = expanded[i]*need
	vol_in *= need
	vol_out *= part*need

	return expanded, vol_in, vol_out

