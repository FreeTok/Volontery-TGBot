import GoogleSpreadSheets as gss
import time

while True:
    dr = gss.CheckDR('Дни Рождения Организаторов')
    if dr:
        print(dr)

    time.sleep(86400)