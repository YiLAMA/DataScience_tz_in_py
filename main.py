import numpy as np
import pandas as pd
import csv
import time


# from memory_profiler import profile  # @profile  # Для теста объёма памяти

# file_read = "incidents"
# file_save = "counts"
# M = "100"

# @profile  # Для теста объема потребляемой программой памяти в процессе работы
def get_counts(file_read, M, dT):
    """
    Функция, которая получает на вход M, dT и файл с инцидентами.
    Вычисляет для каждого из N инцидентов количество инцидентов из того же файла, которые удовлетворяют условиям:
    1) предшествуют данному инциденту по времени, при этом разница по времени не превосходит dT;
    2) имеют значения feature1 и feature2, совпадающие с соответствующими значениями данного инцидента;
    3) категориальные признаки feature1 и feature1 не превосходит наш указанный M.
    """
    dict_counts = {}  # Cловарь, куда записываем id и counts (количество инцидентов удовл-щие условия задачи)
    df = pd.read_csv(f'incidents/' + file_read + ".csv")  # Читаем файл
    # Удаляем инциденты, которые не соответствуют нашим условиям М из арументов функции
    df = df.drop(df[(df.feature1 >= M) | (df.feature2 >= M)].index)
    array = df.sort_values('time').values  # Отсортируем по времени все инциденты
    """
    Если нам нужно инициализировать массив numpy с идентичными значениями, то используем fill().
    Нам не нужно будет использовать циклы для инициализации массива, если мы используем fill().
    Это ускорит процесс работы нашей функции.
    """
    box = np.empty((M, M), dtype=object)  # Матрица записей времени срабатывания инцидентов с одинаковыми feature1 и 2
    box.fill([])

    for i, a in enumerate(array):
        feature1 = int(array[i][1])
        feature2 = int(array[i][2])
        time_ = array[i][3] - dT  # Диапазон времени с учётом dT
        counts = ((box[feature1, feature2] - time_) > 0).sum()  # Считаем инциденты, попавшие в диапазон времени
        box[feature1, feature2] = np.append(box[feature1, feature2],
                                            (array[i][3]))  # Передаём время текущего инцидента в box
        dict_counts[int(array[i][0])] = counts  # Добавляем id и counts в наш словарь

    with open(f'counts/' + file_save + ".csv", 'w') as f:  # Записываем в файл
        writer = csv.writer(f)
        writer.writerow(['id', 'counts'])  # Первой строчкой записываем заголовки для наших данных
        for key, value in sorted(dict_counts.items()):  # Записываем словарь в файл и сортируем по id
            writer.writerow([key, value])


def main():
    str_time = time.time()
    get_counts(file_read, M, dT)
    end_time = time.time() - str_time
    print(f'Наша функция закончила свою работу за {round(end_time, 2)} секунд')


if __name__ == '__main__':
    # Метод №1, с помощью argparse. Вызов из командной строки:
    # Пример вызова из командной строки:
    # python3 main.py -fr incidents -M 100 -dT 0.3 -fs countsTest
    import argparse

    parser = argparse.ArgumentParser(description='Тестовое задание. Описание именных аргументов')
    parser.add_argument('-fr', dest="file_read", default='incidents', type=str,
                        help="Название файла для чтения данных (без указания формата), например: incidents")
    parser.add_argument('-M', dest="M", default=100, type=int,
                        help="Аргумент M. Ограничение для катериальных признаков инцидента при чтении")
    parser.add_argument('-dT', dest="dT", default=0.3, type=float,
                        help="Аргумент dT. Диапазон времени при подсчете результатов совпадающих инцидентов")
    parser.add_argument('-fs', dest="file_save", default='countsTest', type=str,
                        help="Название файла, куда сохраняем данные (без указания формата), например: counts")

    # globals().update(...) - чтобы поместить эти переменные в глобальное пространство имен.
    globals().update(vars(parser.parse_args()))
    args = parser.parse_args()
    print(args)

    # Метод №2, с помощью sys.argv. РАБОЧИЙ. Вызов из командной строки:
    # Пример вызова из командной строки:
    # python3 main.py get_counts incidents 100 0.3 counts
    # import sys
    # func_name = sys.argv[1]
    # file_read = sys.argv[2]
    # M = int(sys.argv[3])
    # dT = float(sys.argv[4])
    # file_save = sys.argv[5]
    # getattr(sys.modules[__name__], func_name)(file_read, M, dT), (file_save)

    main()
