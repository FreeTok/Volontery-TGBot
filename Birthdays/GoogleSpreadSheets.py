import datetime
import gspread
import pandas as pd

sa = gspread.service_account(filename='service_account.json')
sh = sa.open('Волонтёры Победы')

def CheckDR(wksName):
    wks = sh.worksheet(wksName)

    df = pd.DataFrame(wks.get_all_records())

    for i in range(len(df.index)):
        today = f'{datetime.date.today().day}.{datetime.date.today().month}.{datetime.date.today().year}'
        if today == df.iloc[i][1]:
            return df.iloc[i][0]
    return None

CheckDR('Дни Рождения Ветеранов')
CheckDR('Дни Рождения Организаторов')