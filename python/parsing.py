
from selenium.webdriver.common.by import By
#from bs4 import BeautifulSoup
from dataclasses import dataclass
from urllib.parse import urljoin
from typing import List

import numpy as np

import simplejson
import json

from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests

import requests
from bs4 import BeautifulSoup


def replace_str(str):
    # for string in parent.stripped_strings:
    # 	print(repr(string))
    return ((((str).replace("xa;", '').replace('₽', '')).replace('№', '')).replace('\n', '')).replace(' ', '')



def parse_zakupki(search_string):
    url = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html'

    response = requests.get(url)  # get запрос по сформированной ссылке

    if response.status_code == 404:  # если сайт еис недоступен
        for i in range(20):
            # print(response.status_code)
            response = requests.get(url)
            time.sleep(2)
            print(response.status_code, 'Ошибка подключения')
            if response.status_code == 200:
                break
        return (0)

    soup = BeautifulSoup(response.text, 'html.parser')

    soup = BeautifulSoup(response.content, 'html.parser')
    tenders = []
    nameTender = soup.findAll('div', class_='registry-entry__body-value')
    numbersTender = soup.find('div', class_='registry-entry__header-mid__number')
    costsTender = soup.find('div', class_='price-block__value')

    # Example of how you might extract multiple tenders
    for tender in nameTender:
        tender_id = numbersTender.text
        tender_link = "https://zakupki.gov.ru"
        tender_title = (soup.find('div', class_ ='registry-entry__body-value')).text
        tender_price = costsTender.text
        tender_customer = "заказчик"

        tenders.append([tender_id, tender_title, tender_price, tender_customer, tender_link])
    print(tenders)
    return

# Example usage
result = parse_zakupki("mobi")
print(result,"готово")
# Пример использования
result = parse_zakupki("привет")
print(result)
def parseEis(msg):
    clearList = [[0] * 3 for i in range(10)]
    print("УУУУУУУУУУУУУУУУУСССССССПППППППППППЕЕЕЕЕЕЕЕЕЕЕЕХХХХХХХ")
    listTender = [{'name':'Название закупки','href' : 'ссылка','cost': 21,'number': '03902934'}]
    url = "https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString="+ msg
    url = "https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString=mobi"


    print('msg=',msg)
    #url = "https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString=%D0%BC%D0%B0%D1%80%D0%BA%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%BD%D1%8B%D0%B9+%D0%BA%D0%BE%D0%BD%D0%B2%D0%B5%D1%80%D1%82&morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&pageNumber=1&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&sortBy=UPDATE_DATE&fz44=on&af=on&currencyIdGeneral=-1"

    data = {
        "searchString":msg
    }
    #print(url)
    # browser = webdriver.Chrome()
    # browser.get(url)
    response = requests.get(url) #get запрос по сформированной ссылке
    #print(type(response))
    if response.status_code == 404: #если сайт еис недоступен
        for i in range(20):
            #print(response.status_code)
            response = requests.get(url,data=data)
            time.sleep(2)
            print(response.status_code, 'Ошибка подключения')
            if response.status_code == 200:
                break
        return(0)

    soup = BeautifulSoup(response.text, 'html.parser')
    #print(soup)

    def replace_str(str):
        # for string in parent.stripped_strings:
        # 	print(repr(string))
        return ((((str).replace("xa;", '').replace('₽', '')).replace('№', '')).replace('\n', '')).replace(' ', '')


    nameTender = soup.findAll('div', class_='registry-entry__body-value')
    numbersTender = soup.find('div', class_='registry-entry__header-mid__number')
    costsTender = soup.find('div', class_='price-block__value')
    #print(numbersTender, "  ", type(numbersTender))



    #hrefTenders = numbersTender.find_all('a')
    #print(hrefTenders)
    #or href in hrefTenders:
        #direct_a_children = href.findChildren('a', recursive=False)
    #	print(href)
    #	'href': direct_a_children

    index=0
    for object in nameTender:

        clearList[index][0]= replace_str(numbersTender.text)
        clearList[index][1]=object.text
        clearList[index][2]=replace_str(costsTender.text)
        index=index+1

        # listTender.append({'name':object.text, 'numbers': replace_str(numbersTender.text),'cost':replace_str(costsTender.text)#, 'href' : browser.find_element("link", replace_str(costsTender))
        # #				   (numbersTender.find_all('a')).get('href')
        # 				   })
    #работает)
    # for object in nameTender:
    # 	listTender.append({'name':object.text, 'numbers': replace_str(numbersTender.text),'cost':replace_str(costsTender.text)#, 'href' : browser.find_element("link", replace_str(costsTender))
    #
    #  					   })

    print(clearList)
    return(clearList)



