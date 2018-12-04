import urllib.request
import re
import time
import candle
import candleCompressor
import datetime
import strat2live
import strat3Live

priceArr = []
candleArr15m = []
candleArr3h = []
wmaArr = []
maArr = []
hullArr = []
canLen = 15*60 #15min cand
otherCand = 60*60 *3#15*60* 3 = 3hr minute candle
otherCount = 0
headers = {"User-Agent": "Mozilla/4.0"}


totalCount = 0
tickTime = 10
marketOpen = True


print('date: '+ str(datetime.datetime.time(datetime.datetime.now())))


def HMA(period, arr):
    total = 0
    divide = 0
    inc = 1
    for i in range(len(arr) - period, len(arr)):
        value = (arr[i]) * inc
        total += value
        divide += inc
        inc += 1

    return total / divide
def MA(period,arr):
    total = 0
    for i in range(len(arr) - period, len(arr)):
        value = arr[i]
        total += value

    return total / period
def WMA(period,arr):
    total = 0
    divide = 0
    inc = 1
    for i in range(len(arr)-period, len(arr)):


        value = (arr[i])*inc
        total += value
        divide +=inc
        inc +=1
        #print('close: ', arr[i])
    return total / divide
while True:
    start = time.time()

    for p in range (0,1):
        try:


            url ='https://forex.1forge.com/1.0.2/convert?from=BTC&to=USD&quantity=1&api_key=cqVwByGarSxvD1wZt9jDS51iJEyf8UbU'

            resp = urllib.request.urlopen(url,data=None, timeout=2)
            urlStr = resp.read()
            currentBid = re.findall(r'"value":(.*?),"text', str(urlStr))

            thisBid = float(currentBid[0])

            #print(pairArr[p][0],':',priceArr[p])
        except Exception as e:
            print('exception: ',e)
            # every 15 minutes
        if (marketOpen):
            cand = candle.Candle(thisBid, thisBid, thisBid, thisBid)
            priceArr.append(cand)



        if (totalCount > canLen and marketOpen):
            #print('pair:',pairArr[p][0],'arr:',priceArr[p])
            thisCandle = candleCompressor.candleCompressor().compress(priceArr)
            candleArr15m.append(thisCandle)
            priceArr = []
            thisFile = open('BTCUSD15m.csv', 'a')
            toWrite = str(thisCandle.getOpen()) + ',' + str(thisCandle.getClose()) + ',' + str(thisCandle.getLow()) + ',' + str(thisCandle.getHigh()) + '\n'
            thisFile.write(toWrite)
            thisFile.close()
            otherCount +=1



            totalCount = 0
            #print('date: ' + str(datetime.datetime.time(datetime.datetime.now())))
        if(otherCount >11): #every 3 hours
            otherCount = 0
            thisCandle = candleCompressor.candleCompressor().compress(candleArr15m[len(candleArr15m)-12:len(candleArr15m)])
            candleArr3h.append(thisCandle)
            thisFile = open('BTCUSD3h.csv', 'a')
            toWrite = str(thisCandle.getOpen()) + ',' + str(thisCandle.getClose()) + ',' + str(
                thisCandle.getLow()) + ',' + str(thisCandle.getHigh()) + '\n'
            thisFile.write(toWrite)
            thisFile.close()
            if(len(candleArr3h)>9):
                thisWMA = WMA(9,candleArr3h)
                thisMA = MA(9,candleArr3h)
                print("9 WMA: " + str(thisWMA))
                print("9 MA: " + str(thisMA))
                hullMA = (2 * WMA(int(9 / 2)) - WMA(9))
                hullArr.append(hullMA)
                if(len(hullArr)>3):
                    hullMov = HMA(3,hullArr)
                    print("9 HMA: " + str(hullMov))






    if((time.time() - start)>tickTime):
        wait = 0
    else:
        wait = tickTime - ((time.time() - start) % tickTime)
    if(marketOpen):
        totalCount +=tickTime
    time.sleep(wait)





