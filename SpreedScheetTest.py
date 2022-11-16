import gspread
import datetime
import time

sa = gspread.service_account(filename='service_account.json')
sh = sa.open('Дни Рождения Ветеранов')

wks = sh.worksheet('Лист1')

while True:
    for i in range(2, wks.row_count):
        if wks.cell(i, 1).value is None:
            break

        newDay = wks.cell(i, 2).value.split('.')
        today = [str(datetime.date.today().day), str(datetime.date.today().month), str(datetime.date.today().year)]

        if newDay == today:
            print(f'Сегодня день рождения у - {wks.cell(i, 1).value}')

    time.sleep(24 * 60 * 60)
