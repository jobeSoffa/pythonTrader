import fileReader
import strategy1
import candle
import math
import strategy2
import strategy3
import strategy4
import strategy5
import strategy6
import strategy7
import strategy8
import strategy9
class result(object):
    increaseArr = []
    numTrades = 0
    winrate = 0
    balance = 0
    drawdown = 0
    def __init__(self,arr,num,rate,bal,drawdown):
        self.increaseArr = arr
        self.numTrades = num
        self.winrate = rate
        self.balance = bal
        self.drawdown = drawdown
def testYear(pair,printTrue,rw,sl,percent, ma,cad,pip,strat,maOfMa,pipsBetween):
    pair = pair
    if(strat == 1):
        strat = strategy1.strategy1(rw, sl, percent,ma, cad, pip)
    elif( strat == 2):
        strat = strategy2.strategy2(rw, sl, percent, ma, cad, pip)
    elif (strat == 3):
        strat = strategy3.strategy3(rw, sl, percent, ma, cad, pip,maOfMa,pipsBetween)
    elif(strat == 4):
        strat = strategy4.strategy4(rw, sl, percent, ma, cad, pip)

    elif(strat == 5):
        strat = strategy5.strategy5(rw, sl, percent, ma, cad, pip)
    elif(strat == 6):
        strat = strategy6.strategy6(rw, sl, percent, ma, cad, pip,maOfMa)
    elif(strat == 7):
        strat = strategy7.strategy7(percent,cad,pip,maOfMa,printTrue)
    elif (strat == 8):
        strat = strategy8.strategy8(percent, cad, pip, maOfMa, printTrue)
    elif (strat == 9):
        strat = strategy9.strategy9(percent, cad, pip, maOfMa, printTrue,sl,rw)


    else:

        strat = strategy2.strategy2(rw, sl, percent, ma, cad, pip)
    yearStart = 2010
    yearEnd = 2019
    increaseArr =[]
    price = 0
    for x in range(yearStart, yearEnd, 1):

        string = 'years/' + pair + str(x) + '.csv'
        string2 = 'years/' +pair + str(x) + '.csv'
        reader = fileReader.Reader(string)
        for i in range(0, reader.getSize()):

            nextCandle = candle.Candle(reader.getHigh(i), reader.getLow(i), reader.getOpen(i), reader.getClose(i))


            strat.update(nextCandle.getHigh(), nextCandle.getLow(), printTrue, nextCandle.getClose())
            strat.nextCandle(nextCandle)





            price = nextCandle.getClose()
        if(printTrue):
            print('year done: ', x)
        increaseArr.append(int(strat.balance+strat.closeAll(price)))
    if(printTrue):
        print(increaseArr)
        print('highest drawdown: ', strat.drawdown(price))
        print('trades:' ,strat.getNumTrades(), 'loss due to spread: ', strat.tr.totalPL,'total Volume: ', strat.tr.totalVolume, 'percentage: ', strat.tr.totalPL/strat.tr.totalVolume)
        print('avg increase: ', math.pow(((strat.balance+strat.closeAll(price))/1000),1/(yearEnd-yearStart)))
    thisResult = result(increaseArr,strat.getNumTrades(),strat.getWinRate(),strat.balance+strat.closeAll(price),strat.drawdown(price))
    return thisResult
    strat = 0




#strategy 1 testYear('gbpusd', True,7, 181, .01,    61,    33,   .0001)
# expected average increase : 35% pairs: audusd,gbpusd

#strategy 2 #            rw, sl,  percent, ma   cad    pip
#testYear('audusd', True,1, 181, .03,    41,    29,   .0001)
#testYear('usdjpy', True,   .5,   10, .005,   999,    1, .01,       2,       1, 999)




#3 amnt lower: ma:  161 risk reward:  0.2 stop loss:  1 candles:  5 aud
#3 amnt lower: ma:  121 risk reward:  0.2 stop loss:  1 candles:  5 aud

#3 amnt lower: ma:  21 risk reward:  0.3333333333333333 stop loss:  1 candles:  5 eur


#testYear('usdjpy', True,.5, 10, .007,    1,    1,   .01,  3,    20,      7)


#testYear('eurusd', True,.5, 60, .02,    10,    5,   .0001,  3,    24,      70)

#                       rw,sl,  percent,  ma,   cad,    pip,strat    maOfMa, pipDifference

#testYear('eurusd', True,1, 1,    10,     9,    3,   8,     6,    9,      1)



#testYear('eurusd', True,.5, 60, .02,    10,    5,   .0001,  3,    24,      70)


#channel strat: 60% increase on avg per year

#testYear('xauusd', True,999,999, 6, 999,     16, .01,8,  5, 999)

testYear('usdjpy', True,999,999, 6, 999, 13, .01,7,  3, 999)

#                 print    rw    sl  risk   ??    cad   pip   strat  length   ???
#testYear('usdjpy', True,   .5,   100, .0005,   999,    1, .01,       9,       1, 999)
