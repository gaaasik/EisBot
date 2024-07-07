import json
import time
import requests
from bs4 import BeautifulSoup
from main_bot import *
import database

#Парсинг


headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 YaBrowser/24.6.0.0 Safari/537.36'
}

def check_all_data_tender_error(dict_data_tender, all_key):
    for item in all_key:
        # print(dict_data_tender[item])
        try:
            if all_key[item] in dict_data_tender:
                pass
            else:
                dict_data_tender[all_key[item]] = "Нету значения"
        except KeyError:
            dict_data_tender[all_key[item]] = "Нету значения"
    return dict_data_tender


def add_tender(url, countTender):
    s = requests.Session()
    response = s.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    all_title_info_dict = {}
    all_blockInfo__section = soup.find_all(class_="blockInfo__section")


    count_all_blockInfo__section = 0
    for item in all_blockInfo__section:
        try:
            title = item.find(class_="section__title").text.strip().replace(" ", "")
            title.split()
            title = ' '.join(title.split())
        except AttributeError:
            title = f"TITLE{count_all_blockInfo__section}"
            count_all_blockInfo__section += 1
        try:
            info = item.find(class_="section__info").text.strip().replace(" ", "")
            info.split()
            info = ' '.join(info.split())
        except AttributeError:
            info = "INFO"
        all_title_info_dict[f"{title}"] = info
    all_title_info_dict["url"] = url
    all_title_info_dict["number"] = url[-19:]
    # записываем все данные по тендеру в файл
    with open(f"data/{countTender}Dict_data.json", "w", encoding="utf-8") as file:
        json.dump(all_title_info_dict, file, indent=4, ensure_ascii=False)

    # открываем данные по тендеру которые лежат в файле
    with open(f"data/{countTender}Dict_data.json", encoding='utf-8') as file:
        dict_data_tender = json.load(file)

    # открываем все ключи из файла всех ключей
    with open("myDict_keyTest.json", encoding='utf-8') as file:
        all_key = json.load(file)

    dict_data_tender = check_all_data_tender_error(dict_data_tender, all_key)
    database.insert_data_in_db("tenders", dict_data_tender, all_key)



def check_new_tenders(url):
    #заходим по url на 10шт или по файлу html
    s = requests.Session()
    response = s.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    # сохраним страницу чтоб просто посмотреть что там было
    # with open("index.html", "w", encoding="utf-8") as file:
    #     file.write(response.text)

    #создаем список классов registry-entry__header-mid__number
    all_tenders = soup.find_all(class_="registry-entry__header-mid__number")
    countTender = 0

    #пройдемся по каждому тендеру парсим номер тендера и если он есть в базе то ничего, если нет то добавляем
    for tender in all_tenders:
        tender_number = tender.text.strip().replace("№ ", "")

        if database.select_true_false_db("tenders", "number", tender_number):
            print("Уже есть")
        else:
            print("Новый тендер")
            # добавляем тендер в базу данных
            add_tender("https://zakupki.gov.ru"+tender.find("a").get("href"), countTender)
            # надо вывести его в телеграмм
        countTender += 1


def get_page(url):

    # здесь нужно будет пройтись по всем вкладкам и искать тендера пока только на первой странице
    for i in range(0, 1):
        check_new_tenders(url)




#############################################
############################################
#Старый код

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
    return tenders

# Example usage
# result = parse_zakupki("mobi")
# print(result,"готово")
# # Пример использования
# result = parse_zakupki("привет")
# print(result)
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

    # print(clearList)
    # return(clearList)



