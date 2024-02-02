from db import *
# Загружаем элементы БД
db = read_db()
els = list(db.keys())

## Сайт
from dash import Dash, dcc, html, Input, Output,callback
app = Dash(__name__, title="SS14 Tools", update_title=None)


#### ФОРМАТ СТРАНИЦЫ ####

app.index_string = '''
<!DOCTYPE html>
<html>
<head>
	{%metas%}
	<title>{%title%}</title>
	{%favicon%}
	{%css%}
</head>
<body>

<div class="panel">

<div class=img_text_panel>
	<img height="auto" src="assets/favicon.ico" class="logo">
	<div style="color: rgb(255, 255, 255); font-weight: bold; font-size: 2vh;">SS14 Tools</div>
</div>

<div class=soc_buttons>

<a href="https://discord.gg/VxHbM3cedQ" target="_blank" class="socials">
	<img src="assets/discord.svg" class="soc_logo">
	<p class="soc_text">Discord</p>
</a>
<a href="https://github.com/Justuser3310/ss14_chemistry_site" target="_blank">
	<img src="assets/github-mark-white.svg" class="git_logo">
</a>
<a href="https://t.me/ss14tools" target="_blank" class="socials">
	<img src="assets/telegram.svg" class="soc_logo">
	<p class="soc_text">Telegram</p>
</a>

</div>

<div class="empty_box"></div>

</div>

{%app_entry%}
<footer>
	{%config%}
	{%scripts%}
	{%renderer%}
</footer>
</body>
</html>
'''

###### ОФОРМЛЕНИЕ #######


# Форматируем список для красоты
def list_form(ll):
	global db

	formatted = []
	imgs = {'medicine': '💊',
					'chemicals': '🧪',
					'botany': '🪴',
					'drinks': '🍸'}

	for i in ll:
		if type(i) == int:
			formatted.append(i)
		elif db[i][1] in imgs:
			formatted.append(imgs[db[i][1]] + ' ' + i)
		else:
			formatted.append(i)

	return formatted

# Типо контейнер для всего
# [
# Div,
# Div
# ]
app.layout = html.Div([

# Название + объём + вывод
html.Div([
# Название + объём
html.Div([
	# Реакция
	html.Div([
		dcc.Dropdown(list_form(els), id='reaction', placeholder="Реакция", maxHeight=500,
		style={'font-size': '120%', 'font-family': 'NotaSans'})
	], style={'flex': 4, 'min-width': '200px'}),

	# Объём
	html.Div([
		dcc.Dropdown(list_form([30, 50, 100, 300, 1000]), 100, id='amount', clearable=False, searchable=False
			, style={'font-family': '"Mulish", sans-serif', 'font-size': '120%'})
	], className="vol")

], className="react_vol"),

	# Вывод
	html.Div(id='output', style={'text-align': 'center', 'padding-left': '15%', 'padding-right': '15%'})

], className="react_vol_out")
#], style={'padding': '5%', 'margin-left': '25vw', 'margin-right': '25vw'})

], style={'justify-content': 'center', 'display': 'flex'})
# vh - высота окна, vw - ширина окна
#
# 'background-color': '#242829',
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
, style={'background-color': 'rgb(213, 193, 86)', 'color': '#ffffff', 'margin-top': 10, 'border-radius': 10, 'padding': 15, 'font-family': '"Source Sans Pro", sans-serif', 'font-size': '120%'}) )

		# Выходное вещество
		result.append( html.Div(f'{reaction}: {res}'
, style={'background-color': 'rgb(61, 164, 113)', 'color': '#ffffff', 'margin-top': 10, 'border-radius': 10, 'padding': 15, 'font-family': '"Source Sans Pro", sans-serif', 'font-size': '120%'}) )


		return result


#########################



if __name__ == '__main__':
#	app.run(debug=True)
	app.run(debug=False)
