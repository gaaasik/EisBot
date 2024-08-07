import json
import time
import requests
from bs4 import BeautifulSoup
from bot.database.database import insert_data_in_db,select_true_false_db
import bot.data
from bot.start_bot import dp,bot
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
    with open(f"bot/data/{countTender}Dict_data.json", "w", encoding="utf-8") as file:
        json.dump(all_title_info_dict, file, indent=4, ensure_ascii=False)

    # открываем данные по тендеру которые лежат в файле
    with open(f"bot/data/{countTender}Dict_data.json", encoding='utf-8') as file:
        dict_data_tender = json.load(file)

    # открываем все ключи из файла всех ключей
    with open("myDict_keyTest.json", encoding='utf-8') as file:
        all_key = json.load(file)

    dict_data_tender = check_all_data_tender_error(dict_data_tender, all_key)
    insert_data_in_db("tenders", dict_data_tender, all_key)



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

        if select_true_false_db("tenders", "number", tender_number):
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

