from dash import Dash, dcc, html, Input, Output,callback

app = Dash(__name__)

app.layout = html.Div([
	dcc.Dropdown(['NYC', 'MTL', 'SF'], 'NYC', id='demo-dropdown'),
	html.Div(id='dd-output-container')
])


@callback(
	Output('dd-output-container', 'children'),
	Input('demo-dropdown', 'value')
)
def update_output(value):
	return f'You have selected {value}'


if __name__ == '__main__':
	#app.run(debug=True)
	app.run(debug=False)
