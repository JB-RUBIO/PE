from lib.simulator import Cplex_Resolution as cr
import datetime

dictToProcess = {'Prod_0': ['Prod_0', 'Prod_1', 'G._Charpak', 'Prod_0'], 'Prod_3': [
    'Prod_3', 'Prod_1', 'G._Charpak', 'Prod_3'], 'Prod_4': ['Prod_4', 'Prod_2', 'Prod_1', 'G._Charpak', 'Prod_4']}
campus = 'G. Charpak'
date = datetime.datetime.strptime('04/01/22', '%d/%m/%y')
print(date.date())

cr.getOrders(dictToProcess, campus, date.date())
