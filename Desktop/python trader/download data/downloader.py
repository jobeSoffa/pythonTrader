from urllib import request

ok = 'http://ratedata.gaincapital.com/2017/01%20January/EUR_GBP_Week1.zip'

arr = [ 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
arr2 = [ '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
arr3 = []



def downloadData(url,pair,week,month,year,index):
    urlN = str(url +str(year)+ '/' +str(arr2[month-1]) + '%20' + str(arr[month-1]) + '/' + str(pair) +'_Week' +str(week)+'.zip')
    #print(urlN)
    #print(ok)
    response = request.urlretrieve(urlN,'xauusd_years/' + str(year) +'/week'+ str(index) + '.zip')


id = 1



for yr in range(2010, 2019):
    id = 1
    for month in range (1,13):
        for week in range(1,6):
            try:
                downloadData('http://ratedata.gaincapital.com/','XAU_USD',week,month,yr,id)
                id+=1
            except Exception as e:
                print(e , 'deek')
