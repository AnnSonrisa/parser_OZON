import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver

URL = 'https://www.ozon.ru/highlight/ozon-global-155600/?from_global=true&text=xiaomi+redmi'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}



def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):

    driver = webdriver.Chrome()
    driver.get(URL)
    element = driver.find_element_by_classname("b6k2 b5y1")
    print(element)

def parse():
    html = get_html(URL)
    if html.status_code == 200:
        print(get_content(html.text))
    else:
        print('Error')


parse()
