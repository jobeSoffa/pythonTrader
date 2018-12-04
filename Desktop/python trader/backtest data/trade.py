import math

class Trader(object):
    arr = []
    crossArr = []
    winCount = 0
    lossCount = 0
    tieCount = 0
    lastTradeWin = 0
    totalPL = 0
    totalVolume = 0
    def __init__(self):
        self.crossArr = []
        self.arr = []
        self.winCount = 0
        self.lossCount = 0
        self.tieCount = 0
        #self.lastTradeWin = 0
    def getNumTrades(self):
        return self.winCount + self.lossCount
    def crossOpen(self,entry,spread,isBuy, balance, margin,shouldPrint):
        units = (balance*margin)/entry
        self.crossArr.append([entry,units,spread,isBuy])
        if(shouldPrint):
            print(' balance: ', balance, 'entry/units/spread/buy: ',[entry,units,spread,isBuy])

    def crossClose(self,price,shouldPrint):
        totalWinnings = 0
        if(len(self.crossArr)== 1):


            entry = self.crossArr[0][0]
            units = self.crossArr[0][1]
            spread = self.crossArr[0][2]
            isBuy = self.crossArr[0][3]
            profitLoss = spread*units
            self.totalPL += profitLoss


            if(isBuy):
                totalWinnings += (price-entry-spread) * units
                self.totalVolume +=abs((price-entry-spread) * units)
            else:
                totalWinnings += (entry-price - spread) * units
                self.totalVolume += abs((entry-price - spread) * units)
            if(shouldPrint):
                print('trade closed. winnings: ',totalWinnings)#,' entry/units/spread/isBuy: ', self.crossArr[0]
            self.crossArr.pop(0)
        return totalWinnings



    def addTrade(self, entry, stop, take, win, loss):
        self.arr.append([entry,stop,take,win,loss,False])
    def getWinRate(self):
        if(self.winCount  == 0):
            return 0
        else:
            return self.winCount/(self.winCount+self.lossCount)
    def closeAll(self,price):
        total = 0
        for i in range(0,len(self.arr)):
            entry = self.arr[i][0]
            stop = self.arr[i][1]
            tp = self.arr[i][2]
            win = self.arr[i][3]
            tpTotal = entry - tp
            downTotal = price-entry

            percentDown = downTotal/tpTotal
            total -= percentDown*win
        return total

    def tradesOpen(self):
        return len(self.arr)
    def clear(self):
        self.arr = []
        self.winCount = 0
        self.lossCount = 0
        self.tieCount = 0
        self.lastTradeWin = 0
    def update(self, hprice, lprice,balance,shouldPrint,closePrice):
        total = 0
        for x in range  (0,len(self.arr)):
            thisEntry = self.arr[x][0]
            thisStop = self.arr[x][1]
            thisTake = self.arr[x][2]
            thisWin = self.arr[x][3]
            thisLoss = self.arr[x][4]
            #print('entry: ', thisEntry, 'h/l',hprice,'/',lprice)
            if(thisStop >thisTake):
                isBuy = False
            else:
                isBuy = True

            if(isBuy):
                if(hprice >thisTake and lprice < thisStop):
                    self.arr[x][5] = True  # removes trade from array
                    self.tieCount +=1
                    if(shouldPrint):
                        print(len(self.arr), 'tie, balance: ', (balance+self.closeAll(closePrice)), 'wins: ', self.winCount, 'losses: ', self.lossCount, 'ties: ', self.tieCount, 'win rate: ', self.getWinRate(), 'entry: ', thisEntry,'tp/sl:',thisTake,'',thisStop)
                elif(hprice >thisTake ):
                    #win!
                    total += thisWin
                    self.winCount += 1
                    self.arr[x][5] = True #removes trade from array
                    if (shouldPrint):

                        print(len(self.arr), 'win, balance: ', (balance+thisWin)+self.closeAll(closePrice), 'wins: ', self.winCount, 'losses: ', self.lossCount, 'ties: ', self.tieCount, 'win rate: ', self.getWinRate(), 'entry: ', thisEntry,'tp/sl:',thisTake,'',thisStop)
                elif(lprice < thisStop):
                    #loss!
                    total -= thisLoss
                    self.lossCount+=1
                    self.arr[x][5] = True #removes trade from array
                    if (shouldPrint):
                        print(len(self.arr), 'loss! balance: ', (balance-thisLoss)+self.closeAll(closePrice), 'wins: ', self.winCount, 'losses: ', self.lossCount, 'ties: ', self.tieCount, 'win rate: ', self.getWinRate(), 'entry: ', thisEntry,'tp/sl:',thisTake,'',thisStop)
            else:
                if (lprice < thisTake and hprice > thisStop ):
                    self.arr[x][5] = True  # removes trade from array
                    self.tieCount += 1
                    if (shouldPrint):
                        print(len(self.arr), 'tie! balance: ', (balance+self.closeAll(closePrice)), 'wins: ', self.winCount, 'losses: ', self.lossCount, 'ties: ', self.tieCount, 'win rate: ', self.getWinRate(), 'entry: ', thisEntry,'tp/sl:',thisTake,'',thisStop)
                elif (lprice < thisTake):
                    # win!
                    total += thisWin
                    self.winCount+=1
                    self.arr[x][5] = True #removes trade from array
                    if (shouldPrint):
                        print(len(self.arr), 'win! balance: ', (balance+thisWin)+self.closeAll(closePrice), 'wins: ', self.winCount, 'losses: ', self.lossCount, 'ties: ', self.tieCount, 'win rate: ', self.getWinRate(), 'entry: ', thisEntry,'tp/sl:',thisTake,'',thisStop)
                        #print('price: ',lprice,'<',thisTake)
                elif (hprice > thisStop):
                    # loss!
                    total -= thisLoss
                    self.lossCount+=1
                    self.arr[x][5] = True #removes trade from array
                    if (shouldPrint):
                        print(len(self.arr), ' loss! balance: ', (balance-thisLoss)+self.closeAll(closePrice), 'wins: ', self.winCount, 'losses: ', self.lossCount, 'ties: ', self.tieCount, 'win rate: ', self.getWinRate(), 'entry: ', thisEntry,'tp/sl:',thisTake,'',thisStop)
                        #print('price: ', hprice, '>', thisStop)
        counter = 0
        for y in range (0,len(self.arr)):
            if self.arr[y-counter][5] == True:
                self.arr.pop(y-counter)
                counter +=1

        return total