import pandas as pd
import os


def readCampus(path):
    try:
        campus = pd.read_excel(
            path, sheet_name='Nombre campus', header=3, index_col=0, engine='openpyxl')
        campus = campus.loc[:, ['Liste']]
        return campus

    except OSError as e:
        print('The file is missing : ', e)
        exit(0)


def readForecast(path):
    try:
        data = pd.read_excel(path, sheet_name='Real Model', engine='openpyxl')
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


if __name__ == "__main__":
    # File path delaration
    path = r'res\\formatter\\example.xlsm'
    # path = 'example.xlsm'

    campusDataFrame = readCampus(path)
    forecastDataFrame = readForecast(path)

    dfOrders = createDateDataFrame(forecastDataFrame)
    dfOrders = preprocessing(dfOrders, forecastDataFrame, campusDataFrame)

    dfCampus = campusCompletion(path, campusDataFrame)

    print(dfCampus.head(50))
