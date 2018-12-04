

def createCandle(year):
    writeFile = open('xauusd_years' + '/xauusd' + str(year) + '.csv', 'w')
    for x in range (1,54):
        string = 'xauusd_years/' + str(year) + '/' + str(x) + '.csv'

        readFile = open(string)
        thisHigh = 0
        thisLow = 200000
        thisOpen = 0
        foundOpen = False
        firstLine = readFile.readline()
        prevMin = 0
        for line in readFile:
            comma = 0
            priceStr = ''
            dateStr = ''
            date = ''
            for char in line:

                if(char == ','):
                    comma +=1
                elif(comma == 3):
                    dateStr = dateStr + str(char)
                elif(comma == 4):
                    priceStr = priceStr + str(char)
            colon = 0
            for c in dateStr:
                if(c == ':'):
                    colon +=1
                elif(colon == 1):
                    date = date + str(c)

            thisPrice = float(priceStr)
            if(thisPrice > thisHigh):
                thisHigh = thisPrice
            if(thisPrice < thisLow):
                thisLow = thisPrice
            if(foundOpen == False):
                thisOpen = thisPrice
                foundOpen = True

            if((prevMin%15)>7 and int(date)%15 <=7):
                thisClose = thisPrice
                thisOpen = "%.5f" % thisOpen
                thisClose = "%.5f" % thisClose
                thisLow = "%.5f" % thisLow
                thisHigh = "%.5f" % thisHigh
                strToWrite = str(thisOpen) + ',' + str(thisClose) + ',' + str(thisLow) + ',' + str(thisHigh) + '\n'
                writeFile.write(strToWrite)

                thisHigh = 0
                thisLow = 200000
                thisOpen = 0

                foundOpen = False


            prevMin = int(date)


        readFile.close()



    writeFile.close()
createCandle(2010)