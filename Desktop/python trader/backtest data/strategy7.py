import trade
import candleCompressor
import candle
class strategy7(object):
    highestBalance = 1000
    highestDrawdown = 0
    shouldPrint = True

    inBuy = False
    totalTrades = 0
    winCounter = 0
    lossCount = 0
    com = .01
    pip = .001
    otherPip = 1/pip
    maxTrades = 30
    tempArr = []
    candleArr = []
    balance = 1000
    tr = trade.Trader()
    #cmp = candleCompressor.candleCompressor()
    currentCandle = 0
    length = 118
    #strategy variables
    riskReward = 8
    stopLoss = 10
    lotSizePercent = .001
    movingAverage = 10
    candles = 3 #number of 15m candles, 16 = 4hr
    shouldPrint = False

    def __init__(self, percent,cad,pip,length,shouldPrint):

        self.shouldPrint = shouldPrint
        self.length = length
        self.com = pip
        self.lotSizePercent = percent
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

    def update(self, h, l, print,c):
        self.balance += self.tr.update(h, l, self.balance, print,c)
    def len(self):
        return len(self.candleArr)

    def closeAll(self,c):
        total = self.tr.closeAll(c)
        return total
    def calculateHigh(self):
        high = -9868
        low = 8765875876587
        for x in range (len(self.candleArr)-self.length-1, len(self.candleArr)-1):
            thisHigh = self.candleArr[x].getHigh()
            thisLow = self.candleArr[x].getLow()
            if(thisHigh>high):
                high = thisHigh
            if(thisLow < low):
                low = thisLow
        return high

    def calculateLow(self):
        high = -9868
        low = 8765875876587
        for x in range(len(self.candleArr) - self.length-1, len(self.candleArr)-1):
            thisHigh = self.candleArr[x].getHigh()
            thisLow = self.candleArr[x].getLow()
            if (thisHigh > high):
                high = thisHigh
            if (thisLow < low):
                low = thisLow

        return low


    def nextCandle(self,cand):

        self.tempArr.append(cand)
        self.currentCandle +=1
        self.drawdown(cand.getClose())


        if(self.currentCandle == self.candles):
            thisCand = candleCompressor.candleCompressor().compress(self.tempArr)


            if(len(self.candleArr)>self.length+1):
                #print("trade here")


                if(thisCand.getHigh()>= self.calculateHigh() and thisCand.getLow() < self.calculateHigh() and self.inBuy == False):
                    #print("buy")
                    self.balance += self.tr.crossClose(self.calculateHigh(),self.shouldPrint)
                    self.tr.crossOpen(self.calculateHigh(), self.com, True, self.balance, self.lotSizePercent,self.shouldPrint)
                    self.totalTrades += 1
                    self.inBuy = True


                elif(thisCand.getLow() <= self.calculateLow() and thisCand.getHigh() > self.calculateLow() and self.inBuy ==True):
                    #print("sell")
                    self.balance += self.tr.crossClose(self.calculateLow(),self.shouldPrint)
                    self.tr.crossOpen(self.calculateLow(), self.com, False, self.balance, self.lotSizePercent,self.shouldPrint)
                    self.totalTrades += 1
                    self.inBuy = False
            self.candleArr.append(thisCand)
            self.currentCandle = 0
            self.tempArr = []



