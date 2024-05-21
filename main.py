import csv
import random
from pprint import pprint
import plotly.graph_objs as go
from plotly.subplots import make_subplots

FILENAMES = ['DATA.CSV', 'DATA.CSV', 'DATA.CSV', 'DATA.CSV']


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

    return y_data


def extrapolation(t1: int, t2: int, cell: int):
    distance = t2 - t1

    ext = []
    cell -= 1

    for i in range(1, cell + 1):
        ext.append(t1 + distance * (i / cell))
    ext.insert(0, t1)
    return ext


def extrapolate_weather_data():
    avg_data = []
    for filename in FILENAMES:
        y_data = get_datas(filename)
        del y_data[-1]
        avg_data.append([])
        for i in y_data:
            # avg_data.append(sum(i) / len(i))
            avg_data[-1].append(sum(i) / len(i) + random.randint(int(min(i)) - 1,
                                                                 int(max(i)) + 1))
    data = []
    for k, i in enumerate(avg_data[0]):
        data.append([])
        axt_ver_1 = extrapolation(avg_data[0][k], avg_data[1][k], 5)
        axt_ver_2 = extrapolation(avg_data[2][k], avg_data[3][k], 5)

        for t1, t2 in zip(axt_ver_1, axt_ver_2):
            data[-1].append(extrapolation(t1, t2, 16))
    pprint(data)
    return data
def drawing_graphs():
    line_names = ['Аммиака', 'Угарного газа', 'Оксида азота', 'Пыли', 'Ультрафиолета', 'Температуры', 'Давления',
                  'Влажности',
                  'Скорости ветра', 'Направление ветра от времени']

    data = extrapolate_weather_data()

    # Создаем субплот для размещения 10 графиков
    fig = make_subplots(rows=3, cols=3, subplot_titles=[f"График {line_names[i]}" for i in range(9)])

    # Добавляем тепловые графики на каждый субплот
    counter = 0
    for i, subplot_row in enumerate([1, 2, 3]):
        for j, subplot_col in enumerate([1, 2, 3]):
            subplot_index = i * 3 + j
            if subplot_index < 9:
                # Инвертируем порядок строк

                fig.add_trace(
                    go.Heatmap(
                        z=data[counter],
                        # text=[list(map(str, row)) for row in data],
                        # texttemplate="%{text}",
                        colorscale='Viridis',
                        hovertemplate="Значение в точке = %{z:.2f}<extra></extra>",

                    ),
                    row=subplot_row,
                    col=subplot_col
                )

                # Настройка осей и заголовка для каждого графика
                fig.update_xaxes(ticks='', tickvals=list(range(len(data[0]))), row=subplot_row,
                                 col=subplot_col)
                fig.update_yaxes(ticks='', tickvals=list(range(len(data))), autorange='reversed',
                                 row=subplot_row, col=subplot_col)
                counter += 1

    # Настройка общего размера и заголовка
    fig.update_layout(
        width=2000,  # Общая ширина
        height=1500,  # Общая высота

    )

    config = dict({'displayModeBar': False})

    # Отображение графика без верхней панели
    fig.show(config=config)


def main() -> None:
    """
    Запуск программы.
    """
    drawing_graphs()


if __name__ == '__main__':
    main()
