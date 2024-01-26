from db import *
# Загружаем элементы БД
db = read_db()
els = list(db.keys())


###### ОФОРМЛЕНИЕ #######

from dash import Dash, dcc, html, Input, Output,callback

app = Dash(__name__)

app.layout = html.Div([

# Название + объём
html.Div([
	# Реакция
	html.Div([
		dcc.Dropdown(els, id='reaction', placeholder="Реакция", maxHeight=500, style={'font-size': '120%'})
	], style={'flex': 4}),

	# Объём
	html.Div([
		dcc.Dropdown([30, 50, 100, 300, 1000], 100, id='amount', clearable=False, searchable=False
			, style={'font-family': '"Source Sans Pro", sans-serif', 'font-size': '120%'})
	], style={'flex': 1, 'padding-left': 25})

], style={'display': 'flex', 'flexDirection': 'row'}),

	# Вывод
	html.Div(id='output', style={'text-align': 'center', 'padding-left': '15%', 'padding-right': '15%'})

], style={'padding': '5%', 'margin-left': '30%', 'margin-right': '30%'})

# padding - отступ
#    [#####]
# margin - сужение
#     [###]
#########################





####### ЛОГИКА ##########

@callback(
	Output('output', 'children'),
	Input('reaction', 'value'),
	Input('amount', 'value')
)
def update_output(reaction, amount):
	if reaction:
		print(reaction)
#		return f'You have selected {tt}'
		parts = 0
		part = 0
		vol = amount

		# Определяем 1 часть
		for i in db[reaction]:
			parts += i[2]
		part = vol // parts

		# Делаем около-кратным 10 и 15
		# !!ЭКСПЕРЕМЕНТАЛЬНОЕ!!
		part = round(part/10)*10
		if part%10 != 0:
			part = round(part/15)*15


		# Название: количество (локальные части)
		parted = {}
		# Проверяем конфликты с составными частями: 48 != 50
		lparts = 0 ; lpart = 0
		for i in db[reaction]:
			# TODO: только i[1] in db ?
			if i[0] == True and i[1] in db:
				# Перебираем составные
				for el in db[i[1]]:
					lparts += el[2]
				# 50//3 ~ 16    16 * 3 = 48
				lpart = (part//lparts) * lparts
				if lpart < part:
					part = lpart

				parted[i[1]] = [part, lparts]
		# part = 48
		# parted["Инапровалин"] = [48, 3]
		# 48 - 1 часть, 3 - кол. частей


		comps = {}
		# Распределяем (пока не учитывает большую глубину)
		for i in db[reaction]:
			if i[0] == False:
				if i[1] == "Плазма":
					comps[i[1]] = 1
				else:
					comps[i[1]] = part * i[2]
			elif i[0] == True and i[1] not in db:
				# Фикс Вестина и т.п. (нету крафта, но отмечено как есть)
				comps[i[1]] = part * i[2]
			elif i[0] == True and i[1] in db:
				# Перебираем составные
				for el in db[i[1]]:
					if el[1] == "Плазма":
						comps[el[1]] = 1
					else:
						if el[1] not in comps:
							comps[el[1]] = int( parted[i[1]][0]/parted[i[1]][1] * el[2] )
						else:
							comps[el[1]] += int( parted[i[1]][0]/parted[i[1]][1] * el[2] )


		print(comps)
		# Форматирование для HTML
		result = []
		for i in comps:
			result.append( html.Div(i + ': ' + str(comps[i])
, style={'background-color': '#3f3b17', 'margin-top': 10, 'border-radius': 10, 'padding': 15, 'font-family': '"Source Sans Pro", sans-serif', 'font-size': '120%'}) )

		# Выходное вещество
		result.append( html.Div(f'{reaction}: {part*parts}'
, style={'background-color': '#183929', 'margin-top': 10, 'border-radius': 10, 'padding': 15, 'font-family': '"Source Sans Pro", sans-serif', 'font-size': '120%'}) )

		print(result)
		return result

#########################



if __name__ == '__main__':
	app.run(debug=True)
#	app.run(debug=False)
