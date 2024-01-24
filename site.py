import streamlit as st

df = {
	'first column': [1, 2, 3, 4],
	'second column': [10, 20, 30, 40]
}

## LOAD DB ##

#{
#	"Бикаридин": [0, [0, "Углерод", 1], [1, "Инапровалин"] ],
# "Инапровалин": [0, [0, "Кислород", 1], [0, "Сахар", 1], [0, "Углерод", 1] ]
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

#############


# Set columns
react, star, amount = st.columns([73, 7, 20])

with react:
	option = st.selectbox(
		label = '0',
		options = df['first column'],
		index = None,
		placeholder = 'Реакция',
		label_visibility = 'collapsed'
	)

with star:
	st.button(':orange[:star:]')

with amount:
	option = st.selectbox(
		label = '0',
		options = [100],
		index = 0,
		placeholder = 'Объём',
		label_visibility = 'collapsed'
	)
