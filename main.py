import csv

from plotly import graph_objs as go
import plotly.subplots as sp

FILENAME = 'DATA.CSV'

y_data = []
for i in range(10):
    y_data.append([])

for row in csv.reader(open(FILENAME, encoding='utf-8'), delimiter=";"):
    if row[0] == 'timestamp':
        continue
    del row[0]
    del row[-1]
    for k, i in enumerate(row):
        y_data[k].append(float(i))

# Данные для построения 3D графика
x_data = [i for i in range(4516)]
# Массив имен графиков
line_names = ['Аммиак', 'Угарный газ', 'Оксид азота', 'Пыль', 'Ультрафиолет',
              'Температура', 'Давление', 'Влажность',
              'Скорость ветра',
              'Направление ветра от времени']  # Названия линий

fig = sp.make_subplots(rows=4, cols=3, subplot_titles=line_names,
                       shared_xaxes=True, horizontal_spacing=0.05,
                       vertical_spacing=0.05)
row_idx = 1
col_idx = 1
# Цикл для отображения графиков
for i, name in enumerate(line_names):
    if name != 'Направление ветра от времени':
        fig.add_trace(go.Scatter(x=x_data, y=y_data[i], name=name),
                      row=row_idx, col=col_idx)
    else:
        # Отображение графика "Направление ветра от времени"
        wind_speeds = x_data
        direction = y_data[9]
        fig.add_trace(go.Scatter(x=wind_speeds, y=direction, mode='markers',
                                 marker=dict(size=10, color=wind_speeds,
                                             showscale=False),
                                 text=wind_speeds,
                                 hovertemplate='Скорость ветра: %{x}<br>Направление: %{y}<extra></extra>'),
                      row=row_idx, col=col_idx)
    col_idx += 1
    if col_idx > 3:
        col_idx = 1
        row_idx += 1
# Вывод графиков на экран
fig.update_layout(height=1200, width=1900, showlegend=False)
fig.show(config={'displayModeBar': False})
# Отображение графика "Направление ветра от времени" в виде Розы ветров
wind_speeds = x_data
direction = y_data[9]
fog = go.Figure(data=go.Scatterpolar(
    r=wind_speeds,
    theta=direction,
    mode='markers',
    marker=dict(
        size=10,
        color=wind_speeds,
        colorscale='Blues',
        showscale=True
    ),
    cliponaxis=False
))
# Настройка внешнего вида диаграммы
fog.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, max(wind_speeds)]
        )
    ),
    showlegend=False
)
# Вывод графика на экран
fog.update_layout(height=1200, width=1900, showlegend=False)
fog.show(config={'displayModeBar': False})
