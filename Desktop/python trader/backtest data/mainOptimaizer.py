import fileReader
import strategy1
import candle
import backtest
pair = 'usdjpy'
print(pair)
highestBalance = 0

highestWR = 0
lowestWR = 1
#ma 141, rw 3, sl 101, cand 29 strat 1
#ma 141, rw 7, sl 181, cand 33 strat 2
#ma 101, rw 2, sl 141, cand 5  strat 2

for length in range (100,1,-1):



            for cad in range (1,16,1):

#                                           rw,sl, percent,  ma,   cad,  pip
                thisResult = backtest.testYear(pair, False,999,999, cad/2, 999,     cad, .01,9,  length, 999)

                if (not thisResult.numTrades == 0):
                    rate = (1 - (1 / (1 + 1)))
                    # if(thisResult.winrate - rate > highestWR):
                    #     highestWR = thisResult.winrate - rate
                    #
                    #     print('balance: ', thisResult.balance, 'length: ', length,
                    #           'candles: ', cad, 'win rate: ', thisResult.winrate, 'amnt higher: ',
                    #           thisResult.winrate - rate, thisResult.increaseArr)
                    #    print('num trades: ',thisResult.numTrades)


                    # if (thisResult.winrate - rate < lowestWR and not thisResult.winrate == 0):
                    #     lowestWR = thisResult.winrate - rate
                    #
                    #     #print(thisResult.winrate , '-', rate,' =', lowestWR)
                    #
                    #
                    #
                    #
                    #     print('balance: ', thisResult.balance, 'length: ', length,
                    #           'candles: ', cad, 'win rate: ', thisResult.winrate, 'amnt lower: ',
                    #           lowestWR, thisResult.increaseArr)
                    #     print('num trades: ', thisResult.numTrades)


                    if (thisResult.balance > highestBalance):
                        highestBalance = thisResult.balance
                        print('balance: ', thisResult.balance, 'length: ', length,
                              'candles: ', cad, thisResult.increaseArr)
                        print('drawdown: ' + str(thisResult.drawdown))
                        print('num trades: ', thisResult.numTrades)

