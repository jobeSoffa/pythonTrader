import zipfile
import os
def extract(pair, num, year, week):
    string = pair + '_years/' + str(year) +'/week' + str(num) + '.zip'
    zip = zipfile.ZipFile(string)
    zip.extract('XAU_USD_Week'+str(week) + '.csv', pair + '_years/' + str(year))
    os.rename(pair + '_years/' + str(year) +'/' +'XAU_USD_Week'+str(week) + '.csv', pair + '_years/' + str(year) +'/' +str(num)+'.csv')


idk = 0
for yr in range(2010, 2019):
    for num in range (1,54):
        for week in range (1,6):
            try:
                extract('xauusd',num,yr,week)

            except Exception as e:
                idk +=1
