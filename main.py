import requests
from bs4 import BeautifulSoup
import sqlite3
from fake_useragent import UserAgent



all_list = []  # под список словарей с проксями

def db_writer():
    connection = sqlite3.connect('proxy_base.db')
    cursor = connection.cursor

    cursor.ex


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


for i in range(1, 19):
    pars(i)






