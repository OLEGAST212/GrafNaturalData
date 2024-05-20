import csv
import random
from pprint import pprint

from plotly import graph_objs as go
import plotly.subplots as sp

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
    axt_ver_1 = extrapolation(avg_data[0][0], avg_data[1][0], 5)
    axt_ver_2 = extrapolation(avg_data[2][0], avg_data[3][0], 5)

    for t1, t2 in zip(axt_ver_1, axt_ver_2):
        data.append(extrapolation(t1, t2, 16))
    return data


def main() -> None:
    """
    Запуск программы.
    """
    print(extrapolate_weather_data())


if __name__ == '__main__':
    main()
