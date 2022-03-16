import pandas as pd
import httplib2
import numpy as np
from bs4 import BeautifulSoup


columns = ['Состояние', 'Бренд', 'Модель', 'Процессор',
           'Оперативная память (ГБ)', 'Частота процессора',
           'Количество ядер', 'Диагональ (дюйм)',
           'Разрешение экрана', 'Тип матрицы',
           'Видеокарта', 'Тип', 'Назначение',
           'Накопитель', 'Объем накопителя',
           'ОС', 'Цвет',  'Емкость батареи', 'Доставка', 'Title', 'Link', 'Price']


def return_index(feature):
    return columns.index(feature)


def single_url(link):
    df = pd.DataFrame(columns = columns)
    arr = np.empty(len(columns), dtype='object')
    http = httplib2.Http()
    status, response = http.request(link)
    bs = BeautifulSoup(response, 'lxml')

    for item in bs.findAll('ul')[1]:
        feature = item.contents[0].contents[0].strip(':')
        value = item.contents[1].contents[0]
        arr[return_index(feature)] = value

    arr[return_index('Link')] = link
    arr[return_index('Title')] = bs.find('h1', class_ = 'Heading secondary-small').contents[0]
    arr[return_index('Price')] = 'Договорная'

    idx = len(df)
    df.loc[0] = arr

    d = dict()
    for i in range(len(columns)):
        d[columns[i]] = df[columns[i]][0]

    return d
