import requests
from bs4 import BeautifulSoup
import sqlite3
from fake_useragent import UserAgent
import functools



all_list = []  # под список словарей с проксями
        
def decoratar_open_close(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        connection = sqlite3.connect('proxy_base.db')
        cursor = connection.cursor()

        func(cursor)

        connection.commit()
        connection.close()
    return wrapper


@decoratar_open_close
def db_creater(cursor) -> None:  # создание базы и таблицы
    cursor.execute('''CREATE TABLE IF NOT EXISTS Proxys (
                   id INTEGER PRIMARY KEY,
                   IP TEXT,
                   country TEXT,            
                   type TEXT
    )''')


@decoratar_open_close
def db_writer(cursor) -> None:  # записывает прокси в базу
    global all_list
    for i in all_list:
        tup = (i['ip'], i['country'], i['type'])
        cursor.execute('INSERT INTO Proxys (IP, country, type) VALUES (?, ?, ?)', tup)

    



def pars(n: int) -> list:  # подается номер текущей страницы
    global all_list
    url = f'https://free.proxy-sale.com/ru/?page={n}'
    ua = UserAgent()
 

    response = requests.get(url, headers={'user-agent': ua.random})
    response.encoding = 'utf-8'

    soup = BeautifulSoup(response.text, 'html.parser')
    tags = soup.find_all('div', class_='css-ckmntm')
    
    for tag in tags:
        dct = {}
        dct['ip'] = tag.find('p', class_='css-c524v5').text
        dct['country'] = tag.find('p', class_='css-11hq6zf').text
        dct['type'] = tag.find('a', class_='css-qdp10g').text

        all_list.append(dct)
    
    return all_list


db_creater()

for i in range(1, 19):
    pars(i)

db_writer()






