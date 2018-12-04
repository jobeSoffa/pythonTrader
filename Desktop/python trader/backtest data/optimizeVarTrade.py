import fileReader
import strategy1
import candle
import backtest
pair = 'eusd'
print(pair)
highestBalance = -23495240

highestWR = -5234520
lowestWR = 12345
#ma 141, rw 3, sl 101, cand 29 strat 1
#ma 141, rw 7, sl 181, cand 33 strat 2
#ma 101, rw 2, sl 141, cand 5  strat 2

for length in range (1,10,1):
    for sl in range(10,300,10):
        for rw in range(1,4,1):


            for cad in range (4,16,1):

#                                           rw,sl, percent,  ma,   cad,  pip
                thisResult = backtest.testYear(pair, False,rw/2,sl, .0005, 999,     cad, .01,9,  length, 999)

                if (not thisResult.numTrades == 0):
                    rate = ((rw/2) / (1 + (rw/2)))
                    #print(rate)
                    if(thisResult.winrate - rate > highestWR):
                        highestWR = thisResult.winrate - rate

                        print('balance: ', thisResult.balance,'sl: ', sl,'rw: ', rw/2, 'len: ', length,'cad: ', cad, 'wr: ', thisResult.winrate, 'amnt higher: ',thisResult.winrate - rate, thisResult.increaseArr)
                        print('num trades: ',thisResult.numTrades)


                    if (thisResult.winrate - rate < lowestWR and not thisResult.winrate == 0):
                        lowestWR = thisResult.winrate - rate

                        #print(thisResult.winrate , '-', rate,' =', lowestWR)




                        print('balance: ', thisResult.balance,'sl: ', sl,'rw: ', rw/2, 'len: ', length,'cad: ', cad, 'wr: ', thisResult.winrate, 'amnt lower: ',lowestWR, thisResult.increaseArr)
                        print('num trades: ', thisResult.numTrades)


                    if (thisResult.balance > highestBalance):
                        highestBalance = thisResult.balance
                        print('balance: ', thisResult.balance, 'length: ', length,
                              'candles: ', cad, thisResult.increaseArr)
                        print('drawdown: ' + str(thisResult.drawdown))
                        print('num trades: ', thisResult.numTrades)

