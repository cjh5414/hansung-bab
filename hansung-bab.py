import sys
from datetime import datetime

import urllib3
from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler


urllib3.disable_warnings()
sched = BlockingScheduler()

HANSUNG_MENU_URL = 'https://www.hansung.ac.kr/web/www/life_03_01_t2'
LINE_NOTIFY_URL = 'https://notify-api.line.me/api/notify'
LINE_HEADERS = {
    'Authorization' : 'Bearer ' + 'Bowy7xq0o6YCz3duv76a6dmlICDQwv728MrmMnUMKsK'
}

lunch_menu_list = []
dinner_menu_list = []


def get_menu_divided_by_days_of_the_week():
    http = urllib3.PoolManager()
    response = http.request('GET', HANSUNG_MENU_URL)
    soup = BeautifulSoup(response.data, 'html.parser')
    table = soup.findAll('table')[0]
    td_list = table.findAll('td')

    for i in range(5):
        lunch_menu_list.append(td_list[i].get_text(' ').split())
        dinner_menu_list.append(td_list[i+7].get_text(' ').split())


def get_today_menu():
    today_menu = ''
    today_index = datetime.today().weekday()
    try:
        today_menu += '\n-----중식-----\n'
        for menu in lunch_menu_list[today_index]:
            today_menu += menu + '\n'
        if len(dinner_menu_list[today_index]) < 1:
            return today_menu

        today_menu += '\n-----석식-----\n'
        for menu in dinner_menu_list[today_index]:
            today_menu += menu + '\n'
        return today_menu
    except IndexError:
        print('Today is the weekend. There is no menu.')
        sys.exit()

def notify_to_line(today_menu):
    try:
        http = urllib3.PoolManager()
        response = http.request(
            'POST',
            LINE_NOTIFY_URL,
            headers=LINE_HEADERS,
            fields={'message': today_menu}
        )
        print('Response HTTP Status Code: {status_code}'.format(
        status_code=response.status))
    except urllib3.exceptions.NewConnectionError:
        print('Connection failed.')

# @sched.scheduled_job('cron', day_of_week='mon-fri', hour=16)
@sched.scheduled_job('interval', minutes=3)
def main():
    get_menu_divided_by_days_of_the_week()
    today_menu = get_today_menu()
    notify_to_line(today_menu)

sched.start()

# if __name__ == '__main__':
#    main()
