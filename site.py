from db import *
# Загружаем элементы БД
db = read_db()
els = list(db.keys())


###### ОФОРМЛЕНИЕ #######

from dash import Dash, dcc, html, Input, Output,callback
app = Dash(__name__)


# Форматируем список для красоты
def list_form(ll):
	global db

	formatted = []
	imgs = {'medicine': '💊',
					'chemicals': '🧪'}

	for i in ll:
		print(db[i][1])
		if db[i][1] in imgs:
			formatted.append(imgs[db[i][1]] + ' ' + i)
		else:
			formatted.append(i)

	return formatted


app.layout = html.Div([

# Название + объём
html.Div([
	# Реакция
	html.Div([
		dcc.Dropdown(list_form(els), id='reaction', placeholder="Реакция", maxHeight=500, style={'font-size': '120%'})
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

from calc import *

@callback(
	Output('output', 'children'),
	Input('reaction', 'value'),
	Input('amount', 'value')
)
def update_output(reaction, amount):
	if reaction:
		reaction = reaction[2:]
		comps, res = calc(reaction, amount, main = True)

		# Форматирование для HTML
		result = []
		for i in comps:
			result.append( html.Div(i + ': ' + str(comps[i])
, style={'background-color': '#3f3b17', 'margin-top': 10, 'border-radius': 10, 'padding': 15, 'font-family': '"Source Sans Pro", sans-serif', 'font-size': '120%'}) )

		# Выходное вещество
		result.append( html.Div(f'{reaction}: {res}'
, style={'background-color': '#183929', 'margin-top': 10, 'border-radius': 10, 'padding': 15, 'font-family': '"Source Sans Pro", sans-serif', 'font-size': '120%'}) )


		return result


#########################



if __name__ == '__main__':
	app.run(debug=True)
#	app.run(debug=False)
