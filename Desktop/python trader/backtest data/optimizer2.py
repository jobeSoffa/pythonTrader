import fileReader
import strategy1
import candle
import backtest
pair = 'audusd'
print(pair)
highestBalance = 0
highestWR = 0
lowestWR = 1
#ma 141, rw 3, sl 101, cand 29 strat 1
#ma 141, rw 7, sl 181, cand 33 strat 2
#ma 101, rw 2, sl 141, cand 5  strat 2

for riskReward in range(1,5,1):
    rw = riskReward / 2
    print(rw)
    for sl in range (1,101,10):
        for ma in range(1,201,20):
            for cad in range (4,10,3):
                for maMa in range(ma+10,ma+30,10):
                    for pipDif in range (40,100,10):


        #                                                      rw,sl, percent,ma,   cad,  pip
                        thisResult = backtest.testYear(pair,False,rw,sl,.001,ma,cad,.0001,3,maMa,pipDif)

                        if (not thisResult.numTrades == 0):
                            rate = ((1 / (1 + rw)))
                            if(thisResult.winrate - rate > highestWR and thisResult.numTrades>1000):
                                highestWR = thisResult.winrate - rate
                                print('testYear(',pair,', True,',rw,',',sl,',', '.001,', ma,',',  cad,',',   '.0001,',  '3,',  maMa,',',  pipDif,')','win rate: ', thisResult.winrate, 'amnt higher: ',
                                      highestWR, thisResult.increaseArr)
                                print('num trades: ',thisResult.numTrades,'maMa: ',maMa, 'pipDif', pipDif)


                            if (thisResult.winrate - rate < lowestWR and not thisResult.winrate == 0 and thisResult.numTrades>1000):
                                lowestWR = thisResult.winrate - rate

                                #print(thisResult.winrate , '-', rate,' =', lowestWR)
                                print('testYear(', pair, ', True,', rw, ',', sl, ',', '.001,', ma, ',', cad, ',',
                                      '.0001,', '3,', maMa, ',', pipDif, ')', 'win rate: ', thisResult.winrate,
                                      'amnt lower: ',
                                      lowestWR, thisResult.increaseArr)
                                print('num trades: ', thisResult.numTrades, 'maMa: ', maMa, 'pipDif', pipDif)




