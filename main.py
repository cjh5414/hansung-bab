import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings()

URL = 'https://www.hansung.ac.kr/web/www/life_03_01_t2'

http = urllib3.PoolManager()
response = http.request('GET', URL)
soup = BeautifulSoup(response.data, 'html.parser')
table = soup.findAll('table')[0]
td_list = table.findAll('td')

lunch_menu_list = []
dinner_menu_list = []

for i in range(5):
    lunch_menu_list.append(td_list[i].get_text(' ').split())
    dinner_menu_list.append(td_list[i+7].get_text(' ').split())

for i in range(5):
    print(str(i))
    for menu in lunch_menu_list[i]:
        print(menu)

    print()

    for menu in  dinner_menu_list[i]:
        print(menu)
