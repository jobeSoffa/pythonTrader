import urllib.request
import re
import time
import candle
import candleCompressor
import datetime
import strategy7live
fileArr = ['eurusd2017.csv','gbpusd2017.csv', 'audusd2017.csv', 'usdjpy2017.csv']
wrArr = ['eurusdWR2017.csv','gbpusdWR2017.csv', 'audusdWR2017.csv', 'usdjpyWR2017.csv']
pairArr = [['USD_JPY','USD','JPY'], ['GBP_USD','GBP','USD'], ['AUD_USD','AUD','USD'], ['EUR_USD','EUR','USD'] ]
priceArr = [[],[],[],[]]
canLen = 15*60 #15*60 = 15 minute candle
headers = {"User-Agent": "Mozilla/4.0"}


totalCount = 0
tickTime = 4
marketOpen = True
mkt = False
temp = mkt

print('date: '+ str(datetime.datetime.time(datetime.datetime.now())))
strat = strategy7live.strategy7(6,13,.01,4)
while True:
    start = time.time()

    for p in range (0,1):
        try:

            if (p==0):
                temp = mkt
                mkt = 'https://forex.1forge.com/1.0.2/market_status?api_key=[MY_API_KEY_GOES_HERE]'

                mktresp = urllib.request.urlopen(mkt,data=None, timeout=2)
                mktstr = mktresp.read()
                mktarr = re.findall(r'open":(.*?)}',str(mktstr))
                marketOpen = (mktarr[0] == 'true')
                if(temp != mkt):
                    print('market opened/closed')
                    print('date: ' + str(datetime.datetime.time(datetime.datetime.now())))


            url ='https://forex.1forge.com/1.0.2/convert?from='+pairArr[p][1]+'&to='+pairArr[p][2]+'&quantity=1&api_key=[MY_API_KEY_GOES_HERE]'

            resp = urllib.request.urlopen(url,data=None, timeout=2)
            urlStr = resp.read()
            currentBid = re.findall(r'"value":(.*?),"text', str(urlStr))

            thisBid = float(currentBid[0])

            # see if live strat buys, check every tick (every 4 seconds)
            if(marketOpen):
                strat.updateStrat(thisBid)

            cand = candle.Candle(thisBid,thisBid,thisBid,thisBid)
            priceArr[p].append(cand)
            #print(pairArr[p][0],':',priceArr[p])
        except Exception as e:
            print('exception: ',e)





        #if(totalCount > canlen - )
        #
        #every 15 mins
        if (totalCount > canLen and marketOpen):
            #print('pair:',pairArr[p][0],'arr:',priceArr[p])
            thisCandle = candleCompressor.candleCompressor().compress(priceArr[p])
            priceArr[p] = []
            thisFile = open(fileArr[p], 'a')
            toWrite = str(thisCandle.getOpen()) + ',' + str(thisCandle.getClose()) + ',' + str(thisCandle.getLow()) + ',' + str(thisCandle.getHigh()) + '\n'
            thisFile.write(toWrite)
            thisFile.close()
            print('pair', pairArr[p][0], 'candle', toWrite)
            #strat.nextCandle(thisCandle,p)

            strat.nextCandle(thisCandle)



            totalCount = 0
            #print('date: ' + str(datetime.datetime.time(datetime.datetime.now())))
            #print('total winrate:',strat.getWinRate())


    if((time.time() - start)>tickTime):
        wait = 0
    else:
        wait = tickTime - ((time.time() - start) % tickTime)
    totalCount +=tickTime
    time.sleep(wait)