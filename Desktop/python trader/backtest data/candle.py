class Candle(object):
    candHigh = 0
    candLow = 0
    candOpen = 0
    candClose = 0
    def __init__(self,high,low,open,close):
        self.candHigh = high
        self.candLow = low
        self.candOpen = open
        self.candClose = close
    def getHigh(self):
        return self.candHigh
    def getLow(self):
        return self.candLow
    def getOpen(self):
        return self.candOpen
    def getClose(self):
        return self.candClose