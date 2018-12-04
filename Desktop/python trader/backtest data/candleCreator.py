import candle
class candleCreator(object):
    index = 0

    def __init__(self, name):
        self.cd = candle.Candle(name)
    def getIndex(self):
        return self.index
    def getNext(self, hrs):
        high = -123
        low = 200000
        open = 0
        close = 0
        for y in range (0,int(4*hrs)):
            thisHigh = self.cd.getHigh(self.index)
            thisLow = self.cd.getLow(self.index)
            if(y == 0):
                open = self.cd.getOpen(self.index)

            close = self.cd.getClose(self.index)

            if(thisHigh > high):
                high = thisHigh
            if(thisLow < low):
                low = thisLow
        self.index +=int(hrs*4)
        if(open == 0 or close == 0 or low == 200000 or high ==  -123):
            #self.index += 1
            print('MAYDAY MAYDAY MAYDAY WTF')
        return [open,close,high,low]


