class Reader(object):
    fileName = ""
    arr = []
    def __init__(self, name):

        self.fileName = name
        self.arr = []
        with open (self.fileName, 'r') as f:
            header = f.readline()
            for line in f:
                ln = line

                thisOpen = ''
                thisClose = ''
                thisLow = ''
                thisHigh = ''
                one = True
                two = False
                three = False
                four = False

                for letter in ln:
                    lt = letter

                    if(lt == ","):
                        if(one):
                            two = True
                            one = False
                        elif (two):
                            three = True
                            two = False
                        elif (three):
                            four = True
                            three = False

                    elif (one):
                        thisOpen = thisOpen + lt
                    elif (two):
                        thisClose = thisClose + lt
                    elif(three):
                        thisLow = thisLow + lt
                    elif(four):
                        thisHigh = thisHigh + lt
                self.arr.append([thisOpen, thisClose, thisLow, thisHigh])
    def getOpen(self, index):
        return float(self.arr[index][0])


    def getClose(self, index):
        return float(self.arr[index][1])


    def getLow(self,index):
        return float(self.arr[index][2])


    def getHigh(self,index):
        return float(self.arr[index][3])

    def getSize(self):
        return len(self.arr)


