import pandas as pd


def readFile(path):
    try:
        file = pd.ExcelFile(path)
        dicFile = {}
        for sheetName in file.sheet_names:
            dicFile[sheetName] = file.parse(sheetName)
        print('file successfully read')
        return dicFile

    except OSError as e:
        print('The file is missing : ', e)
        exit(0)


def preProcessing(dicFile):
    for campus in dicFile:
        del dicFile[campus]['Unnamed: 0']
        dicFile[campus]['date'] = dicFile[campus]['date'].dt.strftime(
            '%d/%m/%y')
    return dicFile


def createDicProducersLists(dicFile):
    dicProducersLists = {}

    for campus in dicFile:
        dicProducersLists[campus] = []
        for producer in dicFile[campus].columns:
            if producer != 'date':
                dicProducersLists[campus].append(producer)
    return dicProducersLists


def createDicCostsLists(dicFile, dicProducersLists):
    dicToProcess = {}

    for campus in dicFile:
        dicCampus = {}
        for day in dicFile[campus]['date']:
            dicProducer = {}
            for producer in dicProducersLists[campus]:
                cost = dicFile[campus].loc[dicFile[campus]
                                           ['date'] == day, producer].values.tolist()[0]
                dicProducer[producer] = cost
            dicCampus[day] = dicProducer
        dicToProcess[campus] = dicCampus

    return dicToProcess


def createTimeInterval(dicToProcess, dateMin, dateMax):
    interval = []
    for day in dicToProcess['G. Charpak']:
        if day != dateMax:
            interval.append(day)
        else:
            break

    start = interval.index(dateMin)
    return interval[start:]


def getCosts(dicToProcess, date=['04/01/22'], campus=['G. Charpak']):
    res = {}
    if len(campus) == 1 and len(date) == 1:
        for camp in campus:
            for day in date:
                for prod in dicToProcess[camp][day]:
                    res[prod] = dicToProcess[camp][day][prod]
        return res
    elif len(campus) == 1 and len(date) != 1:
        for camp in campus:
            for day in date:
                bufferDate = {}
                for prod in dicToProcess[camp][day]:
                    bufferDate[prod] = dicToProcess[camp][day][prod]
                res[day] = bufferDate
        return res
    else:

        for camp in campus:
            bufferCampus = {}
            for day in date:
                bufferDate = {}
                for prod in dicToProcess[camp][day]:
                    bufferDate[prod] = dicToProcess[camp][day][prod]
                bufferCampus[day] = bufferDate
            res[camp] = bufferCampus
        return res


if __name__ == "__main__":
    # File path delaration
    path = r'res\routing\DailyGroupedOrders.xlsx'

    dicFile = readFile(path)
    dicFile = preProcessing(dicFile)

    dicProducersLists = createDicProducersLists(dicFile)
    dicToProcess = createDicCostsLists(dicFile, dicProducersLists)

    dateMin = '01/01/22'
    dateMax = '30/01/22'
    timeInterval = createTimeInterval(dicToProcess, dateMin, dateMax)

    res = getCosts(dicToProcess, timeInterval)
    print(res)

    print('The main execution routine is finished')
