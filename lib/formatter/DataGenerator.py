import pandas as pd
import os
import random
import xlsxwriter
from datetime import datetime


def readCampus(path):
    try:
        campus = pd.read_excel(
            path, sheet_name='Nombre campus', header=3, index_col=0, engine='openpyxl')
        campus = campus.loc[:, ['Liste']]
        print('campus ok')
        return campus

    except OSError as e:
        print('The file is missing : ', e)
        exit(0)


def readForecast(path):
    try:
        data = pd.read_excel(path, sheet_name='Real Model', engine='openpyxl')
        print('forecast ok')
        return data

    except OSError as e:
        print('The file is missing : ', e)
        exit(0)


def createDateDataFrame(data):
    frame = {'date': data.iloc[13:, 0]}
    df = pd.DataFrame(frame)
    df.reset_index(inplace=True)
    df = pd.DataFrame(df.iloc[:, 1])
    return df


def preprocessing(df, forecastDataFrame, campusDataFrame):
    # nCampus: nombre de campus à étudier
    # colOffset: nombre de colonnes entre 2 campus dans le fichier source
    # indexFirstCol: position de la premiere colonne à lire dans le fichier source
    # indexStart: index de la premiere ligne de donnée dans le fichier source
    # indexStop: index de la derniere ligne de donnée dans le fichier source
    NUMBER_OF_CAMPUS = len(campusDataFrame)
    COLUMN_OFFSET = 4
    INDEX_FIRST_COLUMN = 3
    INDEX_START = 13
    INDEX_STOP = len(forecastDataFrame.index)-1

    # cursorCampus: curseur désignant le campus en cours de traitement
    cursorCampus = 0
    intermediaire = df
    frame = {campusDataFrame.iloc[cursorCampus, 0]
        : forecastDataFrame.iloc[INDEX_START:INDEX_STOP+1, INDEX_FIRST_COLUMN]}
    buffer = pd.DataFrame(frame)
    buffer.reset_index(inplace=True)
    buffer = pd.DataFrame(buffer.iloc[:, 1])

    intermediaire[campusDataFrame.iloc[cursorCampus, 0]] = buffer.iloc[:, 0]
    intermediaire.loc[~(intermediaire[campusDataFrame.iloc[0, 0]]
                        > 0), campusDataFrame.iloc[0, 0]] = 0
    cursorCampus += 1

    for i in range(1, NUMBER_OF_CAMPUS):
        frame = {campusDataFrame.iloc[cursorCampus, 0]
            : forecastDataFrame.iloc[INDEX_START:INDEX_STOP+1, INDEX_FIRST_COLUMN + i*COLUMN_OFFSET]}
        buffer = pd.DataFrame(frame)
        buffer.reset_index(inplace=True)
        buffer = pd.DataFrame(buffer.iloc[:, 1])
        intermediaire[campusDataFrame.iloc[cursorCampus, 0]
                      ] = buffer.iloc[:, 0]
        intermediaire.loc[~(intermediaire[campusDataFrame.iloc[cursorCampus, 0]]
                            > 0), campusDataFrame.iloc[cursorCampus, 0]] = 0
        cursorCampus += 1

    return intermediaire


def campusCompletion(path, campusDataFrame):
    PRODUCER_SCOPE = 20

    nb = pd.read_excel(path, sheet_name='Nombre campus',
                       header=3, index_col=0, engine='openpyxl')
    campusDataFrame['Taille'] = nb.loc[:, [
        'tailletot (étudiants + chercheurs)']]
    campusDataFrame['Esperance'] = nb.loc[:, ['esperance']]

    supplierList = []
    for i in range(0, len(campusDataFrame)):
        n = campusDataFrame.iloc[i, 2]//PRODUCER_SCOPE
        supplierList.append(n)
    campusDataFrame['N. Producteurs'] = supplierList

    return campusDataFrame


def createProducerDataFrame(campusDataFrame):
    tabCamp = []
    tabProd = []

    for name in campusDataFrame['Liste']:
        val = campusDataFrame.loc[campusDataFrame['Liste']
                                  == name, 'N. Producteurs'].iloc[0]
        for n in range(0, val):
            char = "Prod_" + str(n)
            tabCamp.append(name)
            tabProd.append(char)

    producers = pd.DataFrame(tabCamp, columns=['Id_Campus'])
    producers['Id_Prod'] = pd.DataFrame(tabProd)

    return producers


def uniformDistribution(forecastDataFrame, producerDataFrame):
    iterator = forecastDataFrame.columns.values.tolist()
    iterator.remove('date')
    orderList = {}

    for camp in iterator:
        # Caclul des paramètres de chaque campus
        n = producerDataFrame['Id_Campus'].str.count(camp).sum()
        p = 1/n
        buffer = pd.DataFrame({'date': forecastDataFrame['date']})
        prod = producerDataFrame.loc[producerDataFrame['Id_Campus']
                                     == camp, 'Id_Prod']
        orders = []

        # Calcul du nombre de commandes pour chaque jour de l'année
        # et pour chaque producteur suivant une loi uniforme
        for i in range(len(forecastDataFrame[camp])):
            consumers = round(forecastDataFrame[camp][i]*p)
            orders.append(consumers)

        # Pour chaque jour et chaque campus, ajout de la quantité de commande pour
        for element in prod:
            buffer[element] = orders

        orderList[camp] = buffer

    return orderList


def addWeight(dicOrders):
    iterator = []
    meal = [1, 2, 3, 4, 5, 6]

    for camp in dicOrders:
        # campName est le campus courant sous forme de string
        #     print(camp)

        iterator = dicOrders[camp].columns.values.tolist()
        iterator.remove('date')
        # iterator est la liste des producteurs pour chaque campus

        for prod in iterator:

            for day in dicOrders[camp]['date']:
                amount = 0
                if not (dicOrders[camp].loc[dicOrders[camp]['date'] == day, prod].iloc[0] == 0):
                    for consummer in range(0, dicOrders[camp].loc[dicOrders[camp]['date'] == day, prod].iloc[0]):
                        amount += random.choice(meal)
                    print(camp, amount)
                    dicOrders[camp].loc[dicOrders[camp]
                                        ['date'] == day, prod] = amount
                    amount = 0

    return dicOrders


def writeFile(writingPath, dicWeights):
    with pd.ExcelWriter(writingPath, engine='xlsxwriter', datetime_format='dd mm yyyy') as writer:
        for camp in dicWeights:
            dicWeights[camp].to_excel(writer, sheet_name=camp)


if __name__ == "__main__":
    # File path delaration
    path = r'res\formatter\forecast.xlsm'

    campusDataFrame = readCampus(path)
    forecastDataFrame = readForecast(path)

    dfOrders = createDateDataFrame(forecastDataFrame)
    dfOrders = preprocessing(dfOrders, forecastDataFrame, campusDataFrame)

    dfCampus = campusCompletion(path, campusDataFrame)
    dfProducer = createProducerDataFrame(dfCampus)

    dicOrders = uniformDistribution(dfOrders, dfProducer)
    dicWeights = addWeight(dicOrders)

    writingPath = r'res\routing\DailyGroupedOrders.xlsx'
    writeFile(writingPath, dicWeights)

    print(dicWeights)
