import trade
import candleCompressor
import fileReader
import candle
class strategy4(object):
    highestBalance = 1000
    highestDrawdown = 0

    totalTrades = 0
    winCounter = 0
    lossCount = 0
    com = 0
    pip = .0001
    otherPip = 1/pip
    maxTrades = 30
    tempArr = []
    candleArr = []
    balance = 1000
    tr = trade.Trader()
    #cmp = candleCompressor.candleCompressor()
    currentCandle = 0

    #strategy variables
    riskReward = 8
    stopLoss = 10
    lotSizePercent = .001
    movingAverage = 10
    candles = 16 #number of 15m candles, 16 = 4hr

    def __init__(self, rw, sl, percent, ma,cad,pip):
        self.riskReward = rw
        self.stopLoss = sl
        self.lotSizePercent = percent
        self.movingAverage = ma
        self.candles = cad
        self.pip = pip
        self.otherPip = 1/self.pip
        self.tr = trade.Trader()
        self.candleArr = []
        self.tempArr = []
        self.balance = 1000
    def getNumTrades(self):
        return self.tr.getNumTrades()
    def getWinRate(self):
        return self.tr.getWinRate()


    def drawdown(self,c):
        if (self.balance+self.closeAll(c) > self.highestBalance):
            self.highestBalance = self.balance+self.closeAll(c)



        if ((self.highestBalance - (self.balance+self.closeAll(c))) / self.highestBalance > self.highestDrawdown):
            self.highestDrawdown = (self.highestBalance - (self.balance+self.closeAll(c))) / self.highestBalance



        return self.highestDrawdown
    def MA(self):
        total = 0
        for i in range(0, self.movingAverage):
            value = (self.candleArr[i].getHigh() + self.candleArr[i].getLow())/2
            total += value

        return total / self.movingAverage
    def update(self, h, l, print,c):
        self.balance += self.tr.update(h, l, self.balance, print,c)
    def len(self):
        return len(self.candleArr)

    def closeAll(self,c):
        total = self.tr.closeAll(c)
        return total


    def nextCandle(self,cand):

        self.tempArr.append(cand)
        self.currentCandle +=1
        self.drawdown(cand.getClose())


        if(self.currentCandle == self.candles):
            self.candleArr.append(candleCompressor.candleCompressor().compress(self.tempArr))
            self.currentCandle = 0
            self.tempArr = []
            if (len(self.candleArr) > self.movingAverage):

                self.candleArr.pop(0)



                currentHigh = self.candleArr[self.len()-1].getHigh()
                currentLow = self.candleArr[self.len()-1].getLow()
                currentOpen = self.candleArr[self.len()-1].getOpen()
                currentClose = self.candleArr[self.len()-1].getClose()
                prevOpen = self.candleArr[self.len()-2].getOpen()
                maVal = self.MA()

                #print('open',str(currentOpen),'close: ',str(currentClose),'high',str(currentHigh),'low: ',str(currentLow))

                if (self.candleArr[self.len()-4].getClose() > maVal and self.candleArr[self.len()-3].getClose() > maVal and self.candleArr[self.len()-2].getClose() > maVal and currentClose < self.candleArr[self.len()-4].getOpen()):

                    totalPips = (self.stopLoss * self.pip)


                    # print(totalPips*otherPip)

                    thisTake = currentClose + totalPips
                    thisStop = currentClose - (totalPips * self.riskReward)

                    winLossGain = (self.balance * self.lotSizePercent)

                    comWinLoss = (self.com / (totalPips * self.otherPip)) * winLossGain
                    #print(comWinLoss)
                    comLossLoss = (self.com / ((totalPips * self.riskReward) * self.otherPip)) * winLossGain
                    # print('lossloss: ',comWinLoss,  'money lost per trade: ', (winLossGain*riskReward)+comWinLoss)
                    # def addTrade(self, entry, stop, take, win, loss):
                    self.totalTrades += 1

                    self.tr.addTrade(currentClose, thisTake, thisStop, (winLossGain * self.riskReward) - comWinLoss,(winLossGain) + comWinLoss)




