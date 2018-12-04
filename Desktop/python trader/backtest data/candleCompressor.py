import candle
class candleCompressor(object):
    def compress(self,candleArr):
        thisHigh = 0
        thisLow = 1000000
        thisOpen = candleArr[0].getOpen()
        thisClose = candleArr[len(candleArr)-1].getClose()
        for i in range(0,len(candleArr)):
            if(candleArr[i].getHigh()>thisHigh):
                thisHigh = candleArr[i].getHigh()
            if (candleArr[i].getLow() < thisLow):
                thisLow = candleArr[i].getLow()
        newCandle = candle.Candle(thisHigh,thisLow,thisOpen, thisClose)
        return newCandle