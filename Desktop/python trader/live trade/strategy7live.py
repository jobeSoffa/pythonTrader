import trade
import candleCompressor
import liveTrade
import v20
import pythonicMT4


mt4 = pythonicMT4.zmq_python()
api = v20.Context(
        'api-fxpractice.oanda.com',
        '443',
        token='4d778d7e11d347105a31f006b4fca635-f45fb14af82de2821630117d3571d598')

#
# response = api.order.market(
#              '101-001-6583838-001',
#              instrument='EUR_USD',
#              units=-5000)
#

class strategy7(object):
    highestBalance = 1000
    highestDrawdown = 0
    shouldPrint = True

    firstTrade = True
    liveBuy = False
    inBuy = False
    totalTrades = 0
    winCounter = 0
    lossCount = 0
    com = .2
    pip = .0001
    otherPip = 1/pip
    maxTrades = 30
    tempArr = []
    candleArr = []
    balance = 70000
    tr = trade.Trader()
    #cmp = candleCompressor.candleCompressor()
    currentCandle = 0
    length = 118
    #strategy variables
    riskReward = 8
    stopLoss = 10
    lotSizePercent = .001
    movingAverage = 10
    candles = 16 #number of 15m candles, 16 = 4hr

    def __init__(self, percent,cad,pip,length):


        self.length = length

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

    def updateStrat(self,price):
        if (len(self.candleArr) > self.length + 1):
            margin = self.lotSizePercent
            units = (self.balance * margin) / price
            if (price>= self.calculateHigh() and self.liveBuy == False):
                print('live buy. entry: ' + str(price) + 'units: ' + str(units))
                self.liveBuy = True
                if(not self.firstTrade):
                    mt4.close_sell_order()

                mt4.buy_order(symbol="USDJPY_", stop_loss=10000, take_profit=10000)
                print("buy order sucess")
                self.firstTrade = False
            elif (price <= self.calculateLow() and self.liveBuy == True):
                print('live sell. entry: ' + str(price) + 'units: ' + str(units))
                self.liveBuy = False
                if (not self.firstTrade):
                    mt4.close_buy_order()
                mt4.sell_order(symbol="USDJPY_", stop_loss=10000, take_profit=10000)
                print("sell order sucess")
                self.firstTrade = False


    def nextCandle(self,cand):

        self.tempArr.append(cand)
        self.currentCandle +=1
        self.drawdown(cand.getClose())


        if(self.currentCandle == self.candles):
            thisCand =candleCompressor.candleCompressor().compress(self.tempArr)

            print("# of candles: "+str(len(self.candleArr)) + "needed length to trade: >" + str(self.length+1))
            if(len(self.candleArr)>self.length+1):
                print("high channel: " + str(self.calculateHigh()) + "low channel: " + str(self.calculateLow())+ "this candle low and high: " + str(thisCand.getLow()) + ', ' + str(thisCand.getHigh()))


                if(thisCand.getHigh()>= self.calculateHigh() and thisCand.getLow() < self.calculateHigh() and self.inBuy == False):
                    #print("buy")
                    self.balance += self.tr.crossClose(self.calculateHigh(), self.shouldPrint)
                    self.tr.crossOpen(self.calculateHigh(), .00003, True, self.balance, self.lotSizePercent,
                                      self.shouldPrint)
                    self.totalTrades += 1
                    self.inBuy = True
                    print('backtester entered buy(and closed sell) at: ' + str(self.calculateHigh()))





                elif(thisCand.getLow() <= self.calculateLow() and thisCand.getHigh() > self.calculateLow() and self.inBuy ==True):
                    #print("sell")
                    self.balance += self.tr.crossClose(self.calculateLow(), self.shouldPrint)
                    self.tr.crossOpen(self.calculateLow(), .00003, False, self.balance, self.lotSizePercent,
                                      self.shouldPrint)
                    self.totalTrades += 1
                    self.inBuy = False
                    print('backtester entered sell(and closed buy) at: ' + str(self.calculateLow()))
            self.candleArr.append(thisCand)
            self.currentCandle = 0
            self.tempArr = []





