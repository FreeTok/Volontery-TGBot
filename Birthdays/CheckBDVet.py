import GoogleSpreadSheets as gss
import time

while True:
    dr = gss.CheckDR('Дни Рождения Ветеранов')
    if dr:
        print(dr)

    time.sleep(86400)