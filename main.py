import numpy as np
import pandas as pd
import csv
import time
# from memory_profiler import profile  # @profile  # Для теста объёма памяти


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
    df = pd.read_csv(file_read)  # Читаем файл
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
        box[feature1, feature2] = np.append(box[feature1, feature2], (array[i][3]))  # Передаём время текущего инцидента в box
        dict_counts[int(array[i][0])] = counts  # Добавляем id и counts в наш словарь

    with open(file_save, 'w') as f:  # Записываем в файл
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
    file_read = input(
        "Напишите название считываемого файла, без указания формата (.csv - это не надо),"
        "откуда берём данные для работы: (в условии задачи, был такой пример: incidents)\n")
    file_read = f'incidents/' + file_read + ".csv"

    file_save = input(
        "Напишите название сохраняемого файла, куда выписываем результаты работы, тоже без указания формата (.csv):\n")
    file_save = f'counts/' + file_save + ".csv"

    print("Укажите параметр dT для нашей функции, нецелое значение от 0 до 1: (Например 0.3)")
    dT = float(input())
    print("Укажите параметр M для нашей функции, целое значение от 0 до любое: (Например 100)")
    M = int(input())

    # Данные для теста объема потребляемой программой памяти в процессе работы или для теста скорости работы
    # file_read = 'incidents/incidents100KK.csv'
    # file_save = 'counts/counts100KK.csv'
    # dT = 0.3
    # M = 100
    # Примерное время работы функции 38 секунд.

    main()
