import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings()

URL = 'https://www.hansung.ac.kr/web/www/life_03_01_t2'

http = urllib3.PoolManager()
response = http.request('GET', URL)
soup = BeautifulSoup(response.data, 'html.parser')
table = soup.findAll('table')[0]
print(table)
