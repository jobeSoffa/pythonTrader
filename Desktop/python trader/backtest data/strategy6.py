import trade
import candleCompressor
import candle
import math
class strategy6(object):
    highestBalance = 1000
    highestDrawdown = 0


    prevHullVal = 0
    prevMAVal = 0
    totalTrades = 0
    winCounter = 0
    lossCount = 0
    com = 0
    pip = .0001
    otherPip = 1/pip
    maxTrades = 30
    tempArr = []
    candleArr = []
    hullArr = []
    balance = 1000
    tr = trade.Trader()
    #cmp = candleCompressor.candleCompressor()
    currentCandle = 0

    #strategy variables
    riskReward = 8
    stopLoss = 10
    lotSizePercent = .001
    movingAverage = 10
    wMovingAverage = 10
    candles = 16 #number of 15m candles, 16 = 4hr

    def __init__(self, rw, sl, percent, ma,cad,pip,wma):
        self.riskReward = rw
        self.stopLoss = sl
        self.lotSizePercent = percent
        self.movingAverage = ma
        self.wMovingAverage = wma
        self.candles = cad
        self.pip = pip
        self.otherPip = 1/self.pip
        self.tr = trade.Trader()
        self.candleArr = []
        self.tempArr = []
        self.balance = 1000
    def getNumTrades(self):
        return self.totalTrades
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
        for i in range(len(self.candleArr)-self.movingAverage, len(self.candleArr)):
            value = (self.candleArr[i].getHigh() + self.candleArr[i].getLow())/2
            total += value

        return total / self.movingAverage
    def HMA(self,period):
        total = 0
        divide = 0
        inc = 1
        for i in range(len(self.hullArr) - period, len(self.hullArr)):
            value = (self.hullArr[i]) * inc
            total += value
            divide += inc
            inc += 1

        return total / divide
    def WMA(self,period):
        total = 0
        divide = 0
        inc = 1
        for i in range(len(self.candleArr)-period, len(self.candleArr)):


            value = ((self.candleArr[i].getHigh() + self.candleArr[i].getLow())/2)*inc
            total += value
            divide +=inc
            inc +=1


        return total / divide



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
            if (len(self.candleArr) > self.movingAverage+self.wMovingAverage):

                self.candleArr.pop(0)



                currentHigh = self.candleArr[self.len()-1].getHigh()
                currentLow = self.candleArr[self.len()-1].getLow()
                currentOpen = self.candleArr[self.len()-1].getOpen()
                currentClose = self.candleArr[self.len()-1].getClose()
                prevOpen = self.candleArr[self.len()-2].getOpen()
                wmaVal = self.WMA(self.wMovingAverage)
                maVal = self.MA()
                hullMA = (2*self.WMA(int(self.wMovingAverage/2)) - self.WMA(self.wMovingAverage))
                self.hullArr.append(hullMA)
                if(len(self.hullArr)>self.wMovingAverage):
                    crossUp = False
                    crossDown = False
                    hVal = self.HMA(int(math.sqrt(self.wMovingAverage)))
                    if(not self.prevHullVal == 0 and self.prevHullVal < self.prevMAVal and hVal > maVal):
                        crossUp = True
                    if (not self.prevHullVal == 0 and self.prevHullVal > self.prevMAVal and hVal < maVal):
                        crossDown = True


                    self.prevHullVal = hVal
                    self.prevMAVal = maVal



                #print('open',str(currentOpen),'close: ',str(currentClose),'high',str(currentHigh),'low: ',str(currentLow))

                    if (crossUp):
                        self.balance += self.tr.crossClose(currentClose)
                        self.tr.crossOpen(currentClose,.0000,True,self.balance,self.lotSizePercent)
                        self.totalTrades += 1


                    if (crossDown):
                        self.balance += self.tr.crossClose(currentClose)
                        self.tr.crossOpen(currentClose, .0000, False, self.balance,self.lotSizePercent)
                        self.totalTrades += 1




