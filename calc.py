from db import *
from math import floor

db = read_db()

# Составные
recipe = {}

'''
def sround(num, parts):
	acc = [1,2,3,4,5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
	amount = num*parts

	# Ловим частые повторения
	tries = 0

	# Пока не вывели хорошее число
	good = False
	while not good:
		num = floor(num)
		print(good, ' ', num)
		st = 1 ; good = True
		# Перебираем различное количество частей
		while st < parts:
			# Если в допустимых значениях
			if num*st in acc:
				st += 1
				continue

			good = False
			# Перебираем допустимые значения
			for i in acc:
				if abs(i - num*st) <= 2:
					num = i
					break
			st += 1

		# Ловим частые повторения
		tries += 1
		if tries > 500:
			return sround1(num, parts)

	if num*parts > amount:
		return sround1(num, parts)

	return num
'''


def sround(num, parts):
	acc = [1,2,3,4,5]
	num = floor(num)

	if num == 0:
		return 1
	if num in acc:
		return num
	elif num%5 == 0:
		return num

	while num%5 != 0:
		num -= 1
	return num

def calc(el, amount, main = False):
	global db, recipe
	if main:
		recipe = {}

	comps = db[el][2:] # Получаем составные
	out = db[el][0] #Количество на выходе

	# Считаем количество частей
	parts = 0
	for i in comps:
		parts += i[1]

	# Делаем поправку на выход
	while out < parts:
		# Предварительная часть
		part = sround(amount/parts, parts)
		#print(el, ': ',out,' < ', parts)
		# Если итоговый объём <= входного объёма
		if (parts+1)*part <= amount:
			parts += 1
		else:
			break

#		parts = out

	# Считаем 1 часть
	part = sround(amount/parts, parts)

	# Перебираем составные и делаем рекурсию
	for i in comps:
		if i[0] in db:
			lpart = calc(i[0], part*i[1])
	# lpart - количество составного в итоге
	# 50/3, часть = 16, ИТОГ: 16*3=48 <
	try:
		if lpart < part:
			print("LPART: ",lpart)
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
		return [recipe, out*part]
	else:
		print('PART: ', part)
		return part*parts

#print( calc("Лексорин", 100, True))
#print( calc("Бикаридин", 100, True))
#print( calc("Диловен", 100, True))
#print( calc("Эфедрин", 100, True))
