from db import *
from math import floor

db = read_db()

# Составные
recipe = {}

'''
# Функция для спец. округления
# 16.666...8 => 15
def sround(num):
	num = floor(num)
#	num = round(num)

	# Подмены
	rep = [[16,15], [33,30], [21,20], [12,10], [8,5], [6,5]]

	if num == 0:
		return 1

	for i in rep:
		if num == i[0]:
			print('ПОДМЕНА: ', num)
			num = i[1]

	return num
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

#		if num*parts > amount:
#			num = num - 3
#			good = False

		# Ловим частые повторения
		tries += 1
		if tries > 500:
			return 0

	print(num)
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
print( calc("Эфедрин", 100, True))
