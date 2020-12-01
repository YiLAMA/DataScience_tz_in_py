# DataScience_tz_in_py  
  
## Комментарий к задаче: 

Желательна реализация на python3, при этом необходимо использовать последнюю анаконду (https://repo.continuum.io/archive/). Необходимо реализовать решение в виде функции, а также оформить вызов функции из командной строки. К вызову из командной строки необходимо, добавить именованные аргументы с названием входного файла с данными, выходного файла для записи, параметром dt. Программа должна работать не более минуты на все операции (включая чтение и запись данных), на одном ядре. Объем потребляемой программой памяти в процессе работы не должен превышать 2Гб.  
  
# ----------------- Задача -------------------- 
  
У нас есть набор "инцидентов", N штук. Каждый инцидент имеет id с последовательными значениями от 0 до N-1, два категориальных признака с какими-то целыми значениями от 0 до M-1, и признак времени с каким-то (нецелым) значением от 0 до 1.  
  
Например, следующий скрипт генерирует случайный набор таких инцидентов при N=10, M=2, и выписывает в csv-файл:  
  
```
import numpy as np
import pandas as pd
M = 2
N = 10
df = pd.DataFrame({'feature1':np.random.randint(M, size=(N,)),
                 'feature2':np.random.randint(M, size=(N,)),
                 'time':np.random.rand(N)
                 })

df.to_csv('incidents.csv', index_label='id')
```
  
Пример сгенерированного файла:  
```
id,feature1,feature2,time
0,1,0,0.206520219143
1,0,0,0.233725001118
2,0,1,0.760992754734
3,1,1,0.92776979943
4,1,0,0.569711498585
5,0,1,0.99224586863
6,0,0,0.593264390713
7,1,0,0.694181201747
8,1,1,0.823812651856
9,0,1,0.906011017725
```
  
Задача заключается в следующем: надо написать на Python функцию, которая получает на вход M, dT и файл с инцидентами, и вычисляет для каждого из N инцидентов количество инцидентов из того же файла, которые удовлетворяют следующим условиям:  
1. предшествуют данному инциденту по времени, при этом разница по времени не превосходит dT;  
2. имеют значения feature1 и feature2, совпадающие с соответствующими значениями данного инцидента.  
  
Например, в случае dT=0.3 для приведенного выше примера ответ должен выглядеть так:  
```
id,count
0,0
1,0
2,0
3,1
4,0
5,2
6,0
7,1
8,0
9,1
```
  
Функция должна считывать csv-файл с инцидентами, вычислять результаты для всех инцидентов и выписывать их в csv-файл указанного вида.  
Основной нюанс: функция должна работать достаточно быстро, а именно не дольше минуты при M=100, N=1000000, dT=0.3.  

# ----------------- Результаты --------------------  
  
- **Окружающей средой для проекта выбрана "Anaconda3-5.3.1-Linux-x86_64.sh".**
- **Созданные инциденты хранятся в папке "incidents", а результаты нашей функции хранятся в папке "counts".**  
- **Примерное время работы функции 38 секунд. (при M=100, N=1000000, dT=0.3).**  
- **Объем потребляемой программой памяти в процессе работы - находится в папке "memory_profiler".**  
Сам процесс вычисления объема памяти занимает большое время и сам по себе еще занимает конечно память, но меньше 2ГБ в итоге выходит спокойно.

## Вызов из командной строки  
  
Выполнен с помощью "argparse", а также в коде присутствует (откомментирован) вариант с "sys.argv".  
  
Для вызова помощи (описания именованных аргументов) напишите:  
```
$ python3 main.py -h
```

Собственно, само описание выглядит так:  
```
usage: main.py [-h] [-fr FILE_READ] [-M M] [-dT DT] [-fs FILE_SAVE]

  -h, --help     show this help message and exit
  -fr FILE_READ  Название файла для чтения данных (без указания формата),
                 например: incidents
  -M M           Аргумент M. Ограничение для катериальных признаков инцидента
                 при чтении
  -dT DT         Аргумент dT. Диапазон времени при подсчете результатов
                 совпадающих инцидентов
  -fs FILE_SAVE  Название файла, куда сохраняем данные (без указания формата),
                 например: counts
```
  ***ВАЖНО: Указывать формат файлов (.csv) не нужно, он автоопределён, как и папки, куда сохраняются файлы (для чтения и записи). Также не забываем, что по условию задачи у функции есть еще один аргумент М, который тоже должен присутствовать при вызове, по идее.
   
Пример вызова из командной строки:  
``` 
$ python3 main.py -fr incidents -M 100 -dT 0.3 -fs countsTest
```
Обычный вызов тоже сработает, в таком случае аргументы будут по умолчанию (default):  
default file_read='incidents', default M=100, default dT=0.3, default file_save='countsTest'  
```
$ python3 main.py
```
   
Результат выполнение вызова с указанными аргументами:  
```
$ python3 main.py -fr incidents -M 2 -dT 0.3 -fs countsTest
Namespace(M=2, dT=0.3, file_read='incidents', file_save='countsTest')
Наша функция закончила свою работу за 0.01 секунд
```
  
При вызове, необязательно указывать ВСЕ аргументы, пропущенные будут заполнены по умолчанию (default). 
Пример такого вызова:  
```
$ python3 main.py -fr incidents -fs countsTest
```
  
Метод №2, с помощью "sys.argv", для работы надо сперва его раскомментировать в файле main.py.  
Пример вызова из командной строки:  
```
$ python3 main.py get_counts incidents 100 0.3 counts
```
  
### Можно было "защиту от дураков" добавить. Например, чтобы dT параметр был строго от 0 до 1, иначе код будет реагировать. Однако, этого не требуется по условиям задачи. 

