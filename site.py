import streamlit as st

## LOAD DB ##

#{
#	"Бикаридин": [ [0, "Углерод", 1], [1, "Инапровалин"] ],
# "Инапровалин": [ [0, "Кислород", 1], [0, "Сахар", 1], [0, "Углерод", 1] ]
#}
#                  Тип  Название  Часть (1 к 1)
#
#               0 - без нагрева и т.п., 1 - зависит от того-то
#
#   100 = 50 углерод + 50 инапровалин =
#   = 50 углерод + round(50/3) * составные
#   = 50 углерод + 16 кислород + 16 сахар + 16 углерод
#            !!!   50 != 48    =>  делаем 48   !!!
#   = 48 углерод + 16 кислород + 16 сахар + 16 углерод
#   = 96 бикаридин
#
# Список составных: ["Кислород", "Сахар", "Углерод"]

from db import *

db = read_db()
els = list(db.keys())

#############


#### UI ####

# Set columns
react, star, amount = st.columns([73, 7, 20])

with react:
	option_react = st.selectbox(
		label = '0',
		options = els,
		index = None,
		placeholder = 'Реакция',
		label_visibility = 'collapsed',
	)

with star:
	st.button(':orange[:star:]')

with amount:
	option_amount = st.selectbox(
		label = '0',
		options = [30, 50, 100, 300, 1000],
		index = 2,
		placeholder = 'Объём',
		label_visibility = 'collapsed'
	)


#### CALCULATE RECIPE ####

if option_react:
	parts = 0
	part = 0
	vol = option_amount

	# Определяем 1 часть
	for i in db[option_react]:
		parts += i[2]
	part = vol // parts

	# Делаем около-кратным 10
	# !!ЭКСПЕРЕМЕНТАЛЬНОЕ!!
	part = round(part/10)*10
	part = round(part/15)*15

	# Название: количество (локальные части)
	parted = {}
	# Проверяем конфликты с сложными частями: 48 != 50
	lparts = 0 ; lpart = 0
	for i in db[option_react]:
		if i[0] == True:
			# Перебираем составные
			for el in db[i[1]]:
				lparts += el[2]
			# 50//3 ~ 16    16 * 3 = 48
			lpart = (part//lparts) * lparts
			if lpart < part:
				part = lpart

			parted[i[1]] = part//lparts
	# part = 48
	# parted["Инапровалин"] = 16


	comps = {}
	# Распределяем (пока не учитывает большую глубину)
	for i in db[option_react]:
		if i[0] == False:
			comps[i[1]] = part * i[2]
		elif i[0] == True:
			# Перебираем составные
			for el in db[i[1]]:
				if el[1] not in comps:
					comps[el[1]] = parted[i[1]] * i[2]
				else:
					comps[el[1]] += parted[i[1]] * i[2]

	# Выводим результат
	for i in comps:
		st.warning(f'{i}: {comps[i]}')

	st.success(f'{option_react}: {part*parts}')
