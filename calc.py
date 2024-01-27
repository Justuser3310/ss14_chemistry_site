from db import *
from math import floor

db = read_db()

# Составные
recipe = {}

# Функция для спец. округления
# 16.666...8 => 15
def sround(num):
	num = floor(num)

	# Подмены
	rep = [[16,15], [33,30], [21,20], [12,10], [8,5]]

	for i in rep:
		if num == i[0]:
			num = i[1]

	return num

def calc(el, amount, main = False):
	global db, recipe
	if main:
		recipe = {}

	comps = db[el][1:] # Получаем составные
	out = db[el][0] #Количество на выходе

	# Считаем количество частей
	parts = 0
	for i in comps:
		parts += i[1]

	# Делаем поправку на выход
	if out < parts:
		print(el, ': ',out,' < ', parts)
		parts = out

	# Считаем 1 часть
	part = sround(amount/parts)

	# Перебираем составные и делаем рекурсию
	for i in comps:
		if i[0] in db:
			lpart = calc(i[0], part*i[1])
	# lpart - количество составного в итоге
	# 50/3, часть = 16, ИТОГ: 16*3=48 <
	try:
		if lpart < part:
			part = lpart
	except:
		pass

	# Перебираем элементарные вещества
	for i in comps:
		if i[0] not in db:
			if i[0] == 'Плазма':
				recipe[i[0]] = 1
			else:
				if i[0] not in recipe:
					recipe[i[0]] = part*i[1]
				else:
					recipe[i[0]] += part*i[1]

	if main:
		print('PART: ', part)
		return [recipe, parts*part]
	else:
		print('PART: ', part)
		return part*parts

#print( calc("Лексорин", 100, True))
