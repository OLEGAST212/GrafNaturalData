import csv

from plotly import graph_objs as go
import plotly.subplots as sp

FILENAMES = ['DATA.CSV','DATA.CSV','DATA.CSV','DATA.CSV']

# Проблемы:
# 1) Нет подходящих библиотек на Python
# 2) Обработать столь большой объём данных очень затратно
# 3) Практически полное отсутствие информации и примеров с подобными технологиями

# Решение:
# 1) Вернуться к предыдущему отображению графиков
# 2) Добавить поддержку большого кол-ва файлов
# 3) Исправить ошибки и неточности в отображении данных
# 4) Улучшить отображение графиков
# 5) Оптимизировать код (скорость обработки и отображения графиков)
# 6) Повысить читаемость и поддерживаемость кода

def get_datas(filename: str) -> tuple:
    """
    Получение список данных.

    Возвращает данные с файла, предварительно очистив их.

    Args:
        filename: str (название файла)

    Returns:
        tuple: кортеж с двумя списками данных
    """
    y_data = []
    for i in range(10):
        y_data.append([])

    for row in csv.reader(open(filename, encoding='utf-8'), delimiter=";"):
        if row[0] == 'timestamp':
            continue
        del row[0]
        del row[-1]
        for k, i in enumerate(row):
            y_data[k].append(float(i))

    x_data = [i for i in range(len(y_data[0]))]
    return x_data, y_data


def time_conversion(x_data: list, y_data: list) -> None:
    """
    Преобразование во время.

    Преобразует числа во время (период 5 секунд) в формате HH:MM:SS

    Args:
        x_data: list (список чисел)
        y_data: list (список с данными измерений)
    """
    hour = 0
    minute = 0
    second = 0
    for i in range(len(y_data[0])):
        x_data[i] = f'{hour}:{minute}:{second}'
        second += 5
        if second == 60:
            minute += 1
            second = 0
        if minute == 60:
            hour += 1
            minute = 0

def degrees_to_directions(degrees: list) -> list:
    """
    Преобразование градусов в направление.

    Распределяет градусы (числа) в направления сторон света.

    Args:
        degrees: list (градусы)

    Returns:
        list: распределённые данные
    """
    directions_map = {
        0: 'Север, 0/360', 22.5: 'Северо-северо-восток, 22.5', 45: 'Северо-восток, 45',
        67.5: 'Востоко-северо-восток, 67.5',
        90: 'Восток, 90', 112.5: 'Востоко-юго-восток, 112.5', 135: 'Юго-восток, 135', 157.5: 'Юго-юго-восток, 157.5',
        180: 'Юг, 180', 202.5: 'Юго-юго-запад, 202.5', 225: 'Юго-запад, 225', 247.5: 'Западо-юго-запад, 247.5',
        270: 'Запад, 270', 292.5: 'Западо-северо-запад, 292.5', 315: 'Северо-запад, 315',
        337.5: 'Северо-северо-запад, 337.5',
    }

    directions_output = []
    for degree in degrees:
        normalized_degree = degree % 360
        closest_direction = min(directions_map.keys(), key=lambda x: abs(normalized_degree - x))
        directions_output.append(directions_map[closest_direction])

    return directions_output


def first_page(filename: str, x_data: list, y_data: list):
    """
    Отрисовка графиков по указанным данным.

    Отрисовка графиков по параметрам: аммиак, угарный газ, оксид азота, пыль,
    ультрафиолет, температура, давление, влажность, скорость ветра,
    направление ветра от времени.

    Args:
        filename: str (название файла откуда берутся данные)
        x_data: list (список с данными времени)
        y_data: list (список с данными направления ветра)
    """
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
            time = x_data
            direction = y_data[9]
            sorted_indices = sorted(range(len(direction)), key=lambda i: direction[i])

            # Применение индексов сортировки к обоим массивам
            time = [time[i] for i in sorted_indices]
            direction = [direction[i] for i in sorted_indices]
            directions_output = degrees_to_directions(direction)
            fig.add_trace(go.Scatter(x=time, y=directions_output, mode='markers',
                                     marker=dict(size=10, showscale=False),
                                     text=time,  # Отображение временных меток при наведении
                                     hovertemplate='Время: %{text}<br>Направление: %{y}<extra></extra>'),
                          row=row_idx, col=col_idx)
        col_idx += 1
        if col_idx > 3:
            col_idx = 1
            row_idx += 1
    # Вывод графиков на экран
    fig.update_xaxes(visible=False)
    fig.update_layout(height=1200, width=1900, showlegend=False, title=f'Графики измерения ({filename})')
    fig.show(config={'displayModeBar': False})


def second_page(filename: str, x_data: list, y_data: list) -> None:
    """
    Отрисовка графика Роза ветров.

    График направления ветра от времени.

    Args:
        filename: str (название файла откуда берутся данные)
        x_data: list (список с данными времени)
        y_data: list (список с данными направления ветра)
    """
    time = x_data
    direction = y_data[9]

    wind_directions = {
        0: 'Север, 0/360', 22.5: 'Северо-северо-восток, 22.5',
        45: 'Северо-восток, 45', 67.5: 'Востоко-северо-восток, 67.5',
        90: 'Восток, 90', 112.5: 'Востоко-юго-восток, 112.5',
        135: 'Юго-восток, 135', 157.5: 'Юго-юго-восток, 157.5',
        180: 'Юг, 180', 202.5: 'Юго-юго-запад, 202.5', 225: 'Юго-запад, 225',
        247.5: 'Западо-юго-запад, 247.5',
        270: 'Запад, 270', 292.5: 'Западо-северо-запад, 292.5',
        315: 'Северо-запад, 315',
        337.5: 'Северо-северо-запад, 337.5',
    }

    hover_text = [f"Время: {t}, Направление: {wind_directions[a]}" for t, a in
                  zip(x_data, direction)]
    fog = go.Figure(data=go.Scatterpolar(
        r=x_data,
        theta=direction,
        mode='markers',
        text=hover_text,
        hoverinfo='text',
        marker=dict(
            size=10,
            colorscale='Blues',
            showscale=False

        ),
    ))
    # Настройка внешнего вида диаграммы
    fog.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=False,
                range=[0, max(time)]

            ),

        ),
        showlegend=False,
        title=f'Направление ветра от времени в виде Розы ветров ({filename})',
        title_x=0.5,
    )

    # Вывод графика на экран
    fog.update_layout(height=1200, width=1900, showlegend=False,
                      font_size=16, )
    fog.show(config={'displayModeBar': False})


def third_page(filename: str, y_data: list) -> None:
    """
    Отрисовка графика Роза ветров.

    График направления ветра от скорости ветра.

    Args:
        filename: str (название файла откуда берутся данные)
        y_data: list (список с данными направления/скорости ветра)
    """
    time = y_data[8]
    direction = y_data[9]
    color_scale = [
        [1, 'white'],
        [0, 'red']
    ]

    wind_directions = {
        0: 'Север, 0/360', 22.5: 'Северо-северо-восток, 22.5', 45: 'Северо-восток, 45', 67.5: 'Востоко-северо-восток, 67.5',
        90: 'Восток, 90', 112.5: 'Востоко-юго-восток, 112.5', 135: 'Юго-восток, 135', 157.5: 'Юго-юго-восток, 157.5',
        180: 'Юг, 180', 202.5: 'Юго-юго-запад, 202.5', 225: 'Юго-запад, 225', 247.5: 'Западо-юго-запад, 247.5',
        270: 'Запад, 270', 292.5: 'Западо-северо-запад, 292.5', 315: 'Северо-запад, 315',
        337.5: 'Северо-северо-запад, 337.5',
    }

    hover_text = [f"Скорость ветра: {t}, Направление: {wind_directions[a]}" for t, a in zip(time, direction)]

    fyg = go.Figure(data=go.Scatterpolar(
        r=time,
        theta=direction,
        mode='markers',
        text=hover_text,
        hoverinfo='text',
        marker=dict(
            size=10,
            color=time,  # Устанавливаем цвет в зависимости от y_data[8]
            colorscale=color_scale,
            reversescale=True,  # Разворачиваем цветовую шкалу
            showscale=False
        ),
    ))

    # Настройка внешнего вида диаграммы
    fyg.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=False,
                range=[0, max(time)]
            ),
        ),
        showlegend=False,
        title=f'Направление ветра от скорости ветра в виде Розы ветров ({filename})',
        title_x=0.5,
    )

    # Вывод графика на экран
    fyg.update_layout(height=1200, width=1900, showlegend=False, font_size=16, )
    fyg.show(config={'displayModeBar': False})



def main() -> None:
    """
    Запуск программы.
    """
    for filename in FILENAMES:
        x_data, y_data = get_datas(filename)
        time_conversion(x_data, y_data)

        first_page(filename, x_data, y_data)

        second_page(filename, x_data, y_data)

        third_page(filename, y_data)


if __name__ == '__main__':
    main()
