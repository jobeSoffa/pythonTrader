import trade
import candleCompressor
import candle
import fileReader
import liveTrade
class strategy2(object):

    fileArr = ['eurusd2017.csv', 'gbpusd2017.csv', 'audusd2017.csv', 'usdjpy2017.csv']

    totalTrades = 0
    com = .3
    pip = .0001
    otherPip = 1/pip
    maxTrades = 30
    tempArr = [[],[],[],[]]
    candleArr = [[],[],[],[]]
    balance = [1000,1000,1000,1000]
    tr = [liveTrade.Trader(0),liveTrade.Trader(1),liveTrade.Trader(2),liveTrade.Trader(3)]
    #cmp = candleCompressor.candleCompressor()
    currentCandle = [0,0,0,0]

    #strategy variables
    riskReward = 1/3
    stopLoss = 1
    lotSizePercent = .03
    movingAverage = 21
    candles = 3 #number of 15m candles, 16 = 4hr

    def __init__(self, rw, sl, percent, ma,cad,pip):
        self.riskReward = rw
        self.stopLoss = sl
        self.lotSizePercent = percent
        self.movingAverage = ma
        self.candles = cad
        self.pip = pip
        self.otherPip = 1/self.pip
        self.tr =[liveTrade.Trader(0),liveTrade.Trader(1),liveTrade.Trader(2),liveTrade.Trader(3)]
        self.candleArr = [[],[],[],[]]
        self.tempArr = [[],[],[],[]]
        self.balance = [1000,1000,1000,1000]
    def getNumTrades(self):
        return self.tr.getNumTrades()
    def getWinRate(self):
        totalWins = self.tr[0].winCount + self.tr[1].winCount + self.tr[2].winCount + self.tr[3].winCount
        totalLosses = self.tr[0].lossCount + self.tr[1].lossCount + self.tr[2].lossCount + self.tr[3].lossCount
        if(totalWins == 0):
            return 0
        else:
            return totalWins/(totalWins+totalLosses)



    def MA(self,p):
        total = 0
        for i in range(0, self.movingAverage):
            value = (self.candleArr[p][i].getHigh() + self.candleArr[p][i].getLow())/2
            total += value

        return total / self.movingAverage

    def update(self, h, l, print,c,p):
        self.balance[p] += self.tr[p].update(h, l, self.balance[p], print,c)
    def len(self):
        return len(self.candleArr[0])


    def createArr(self,pair,p):
        arr = []
        try:

            reader = fileReader.Reader(self.fileArr[p])
            for i in range(0,self.movingAverage):
                for j in range (0,self.candles):
                    incr = (j+1) + (i*self.candles)
                    newCand = candle.Candle(reader.getHigh(incr),reader.getLow(incr),reader.getOpen(incr),reader.getClose(incr))
                    arr.append(newCand)
        except Exception as e:
            print('error in createArr():',e)

        return arr
    def nextCandle(self,cand, p):
        if(p==3):
            self.pip=.01
            self.otherPip = 1/self.pip
        else:
            self.pip = .0001
            self.otherPip = 1 / self.pip

        self.tempArr[p].append(cand)
        self.currentCandle[p] +=1



        if(self.currentCandle[p] == self.candles):
            self.candleArr[p].append(candleCompressor.candleCompressor().compress(self.tempArr[p]))
            self.currentCandle[p] = 0
            self.tempArr[p] = []
            if (len(self.candleArr[p]) > self.movingAverage):

                self.candleArr[p].pop(0)



                currentHigh = self.candleArr[p][self.len()-1].getHigh()
                currentLow = self.candleArr[p][self.len()-1].getLow()
                currentOpen = self.candleArr[p][self.len()-1].getOpen()
                currentClose = self.candleArr[p][self.len()-1].getClose()
                prevOpen = self.candleArr[p][self.len()-2].getOpen()
                maVal = self.MA(p)

                #print('open',str(currentOpen),'close: ',str(currentClose),'high',str(currentHigh),'low: ',str(currentLow))

                if (currentClose > currentOpen and currentClose < maVal and currentOpen > prevOpen):

                    totalPips = (self.stopLoss * self.pip) + (currentClose - currentLow)


                    # print(totalPips*otherPip)

                    thisTake = currentClose - totalPips
                    thisStop = currentClose + (totalPips * self.riskReward)

                    winLossGain = (self.balance * self.lotSizePercent)

                    comWinLoss = (self.com / (totalPips * self.otherPip)) * winLossGain
                    print(comWinLoss)
                    comLossLoss = (self.com / ((totalPips * self.riskReward) * self.otherPip)) * winLossGain
                    # print('lossloss: ',comWinLoss,  'money lost per trade: ', (winLossGain*riskReward)+comWinLoss)
                    # def addTrade(self, entry, stop, take, win, loss):
                    self.totalTrades += 1

                    self.tr[p].addTrade(currentClose, thisTake, thisStop, (winLossGain * self.riskReward) - comWinLoss,(winLossGain) + comWinLoss)
                    print('entry, top, take, win , loss', [currentClose, thisTake, thisStop, (winLossGain * self.riskReward) - comWinLoss,(winLossGain) + comWinLoss])




