import datetime
import time
import pandas as pd

df = pd.read_csv("https://docs.google.com/spreadsheets/d/15-BAQYs4GgxRauziRTzdycb0OIOvinpd4Da4M7G78fg/gviz/tq?tqx=out:csv&sheet=%D0%94%D0%BD%D0%B8%20%D0%A0%D0%BE%D0%B6%D0%B4%D0%B5%D0%BD%D0%B8%D1%8F%20%D0%92%D0%B5%D1%82%D0%B5%D1%80%D0%B0%D0%BD%D0%BE%D0%B2")

while True:
    for i in range(len(df.index)):
        today = f'{datetime.date.today().day}.{datetime.date.today().month}.{datetime.date.today().year}'
        if today == df.iloc[i][1]:
            print(f'У {df.iloc[i][0]} день рождения')

    time.sleep(86400)