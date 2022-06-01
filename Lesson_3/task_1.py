import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke


client = MongoClient('127.0.0.1', 27017)
db = client.vacancies_db
vac_collection = db.vac_collection

# https://hh.ru/search/vacancy?text=data+science&from=suggest_post&salary=&clusters=true&ored_clusters=true&search_field=name&enable_snippets=true&page=0&items_on_page=20&hhtmFrom=vacancy_search_list

main_url = "https://hh.ru"
# vacancy = input('Input your vacancy name: ')
vacancy = 'data science'
page = 0
all_vacancies = []
params = {'text': vacancy,
          'from': 'suggest_post',
          'clusters': 'true',
          'ored_clusters': 'true',
          'enable_snippets': 'true',
          'search_field': 'name',
          'page': page,
          'hhtmFrom': 'vacancy_search_list',
          'items_on_page': 20,
          }
url = 'https://hh.ru/search/vacancy'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) /'
                         'Chrome/101.0.4951.67 Safari/537.36'}
response = requests.get(url=url, params=params, headers=headers)
soup = bs(response.content, 'html.parser')

try:
    last_page = int(soup.find_all('a', {'data-qa': 'pager-page'})[-1].text)
except:
    last_page = 1

for i in range(last_page):
    soup = bs(response.content, 'html.parser')
    vacancies = soup.find_all('div', {'class': 'vacancy-serp-item__layout'})

    for vacancy in vacancies:

        vac_name_anchor = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
        vac_name = vac_name_anchor.text.strip()

        vac_link = vac_name_anchor['href']

        vac_salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        if vac_salary is None:
            min_salary = None
            max_salary = None
            currency = None
        else:
            vac_salary = vac_salary.text
            if vac_salary.startswith('от'):
                min_salary = int(''.join([s for s in vac_salary.split() if s.isdigit()]))
                max_salary = None
                currency = vac_salary.split(' ')[-1]
            elif vac_salary.startswith('до'):
                min_salary = None
                max_salary = int(''.join([s for s in vac_salary.split() if s.isdigit()]))
                currency = vac_salary.split(' ')[-1]
            else:
                min_salary = int("".join([s for s in vac_salary.split('–')[0] if s.isdigit()]))
                max_salary = int("".join([s for s in vac_salary.split('–')[1] if s.isdigit()]))
                currency = vac_salary.split()[-1]
        vacancies_dict = {
            '_id': vac_link,
            'Site': main_url,
            'MaxSalary': max_salary,
            'MinSalary': min_salary,
            'Currency': currency,
            'Name': vac_name,
            'Link': vac_link
        }
        all_vacancies.append(vacancies_dict)
        try:
            vac_collection.insert_one(vacancies_dict)
        except dke:
            print(f'Документ с ссылкой = {vacancies_dict["_id"]} уже существует в базе')
    # print(len(all_vacancies))
    params['page'] += 1
    response = requests.get(url=url, params=params, headers=headers)

# pprint(all_vacancies[0])
# print(client.list_database_names())
# print(db.list_collection_names())

# print(f'Всего собрано вакансий {len(all_vacancies)}')
# print(f'Вакансий уникальных в БД {len(list(vac_collection.find()))}')


def vac_salary(wish_salary):
    temp = vac_collection.find({'$or': [
        {'MinSalary': {'$gte': wish_salary}},
        {'MaxSalary': {'$gte': wish_salary}},
    ]})
    for t in temp:
        print(t['MinSalary'], t['MaxSalary'])


vac_salary(170000)


# for vac in vac_collection.find():
#     print(vac['MinSalary'], vac['MaxSalary'])
