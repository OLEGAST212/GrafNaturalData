import csv
import random
from pprint import pprint
import matplotlib.pyplot as plt
FILENAMES = ['DATA.CSV', 'DATA.CSV', 'DATA.CSV', 'DATA.CSV']



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
                  'Влажности', 'Скорости ветра', 'Направление ветра от времени']

    data = extrapolate_weather_data()

    # Размер фигуры в дюймах
    fig_width = 2000 / 100  # 2000 пикселей / 100 dpi = 20 дюймов
    fig_height = 1500 / 100  # 1500 пикселей / 100 dpi = 15 дюймов

    fig, axs = plt.subplots(3, 3, figsize=(fig_width, fig_height))

    counter = 0
    for i in range(3):
        for j in range(3):
            if counter < 9:
                im = axs[i, j].imshow(data[counter], cmap='viridis')
                axs[i, j].set_title(f"График {line_names[counter]}")
                fig.colorbar(im, ax=axs[i, j])
                counter += 1

    plt.tight_layout()
    plt.show()
def main() -> None:
    """
    Запуск программы.
    """
    drawing_graphs()


if __name__ == '__main__':
    main()
