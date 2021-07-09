import csv
import os
import requests
import re
from selenium import webdriver


FILE = 'output.csv'
URL = 'https://www.ozon.ru/highlight/ozon-global-155600/?from_global=true&text=xiaomi+redmi'

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(URL):
    driver = webdriver.Chrome()
    driver.get(URL)
    items=driver.find_elements_by_class_name('a0c6')
    products=[]
    for item in items:
        price_without_sale=item.find_element_by_class_name('b5v4').text
        price_without_sale=re.sub(r'^.*?₽', ' ', price_without_sale)
        seller=item.find_element_by_class_name('d8e5').text
        seller_text=seller.split()
        seller_text=' '.join(seller_text[seller_text.index('продавец')+1:])
        products.append({
            'name': item.find_element_by_class_name('b3u9').text,
            'actual_price': item.find_element_by_class_name('b5v6').text,
            'price_without_sale': price_without_sale,
            'seller': seller_text
                    })
    return(products)

def save_file(items, path):
    with open(path, 'w',  encoding = 'utf-8-sig', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Наименование устройства','Цена со скидкой','Цена без скидки ("Вычеркнутая" цена)', 'Продавец'])
        for item in items:
            writer.writerow([item['name'], item['actual_price'], item['price_without_sale'], item['seller']])


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        products = []
        pages_count = 28
        products.extend(get_content(URL))
        for page in range(2, pages_count+1):
            print(f'Парсинг страницы {page} из {pages_count}...')
            URL2 = 'https://www.ozon.ru/highlight/ozon-global-155600/?from_global=true&page='+str(page)+'&text=xiaomi+redmi'
            products.extend(get_content(URL2))
        save_file(products, FILE)
        print(f'Получено {len(products)} товаров')
        os.startfile(FILE)
    else:
        print('Error')

parse()