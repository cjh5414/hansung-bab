from datetime import datetime

import urllib3
from bs4 import BeautifulSoup


urllib3.disable_warnings()

URL = 'https://www.hansung.ac.kr/web/www/life_03_01_t2'

lunch_menu_list = []
dinner_menu_list = []


def get_menu_divided_by_days_of_the_week():
    http = urllib3.PoolManager()
    response = http.request('GET', URL)
    soup = BeautifulSoup(response.data, 'html.parser')
    table = soup.findAll('table')[0]
    td_list = table.findAll('td')

    for i in range(5):
        lunch_menu_list.append(td_list[i].get_text(' ').split())
        dinner_menu_list.append(td_list[i+7].get_text(' ').split())


def get_todays_menu():
    today_index = datetime.today().weekday()
    for menu in lunch_menu[today_index]:
        print(menu)
    for menu in dinner_menu[today_index]:
        print(menu)

