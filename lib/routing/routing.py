import pulp
import itertools
import numpy as np
import pandas as pd
import Retailing as ret

path = r'res\routing\DailyGroupedOrders.xlsx'

# dicFile = ret.readFile(path)
# dicFile = ret.preProcessing(dicFile)

# dicProducersLists = ret.createDicProducersLists(dicFile)
# dicToProcess = ret.createDicCostsLists(dicFile, dicProducersLists)

# dateMin = '01/01/22'
# dateMax = '30/01/22'
# timeInterval = ret.createTimeInterval(dicToProcess, dateMin, dateMax)

# dailyOrders = ret.getCosts(dicToProcess, ['04/01/22'])


print('Data collected.')

class Arc:
    def __init__(self, n1, n2, c):
        self.n1 = n1
        self.n2 = n2
        self.c = c
    def __str__(self):
        return str.format("({},{},{}))", self.n1, self.n2, self.c)

def insertion_sort(array, compare_function):
    for index in range(1, len(array)):
        currentValue = array[index]
        currentPosition = index
        
        while currentPosition > 0 and compare_function(array[currentPosition - 1], currentValue):
            array[currentPosition] = array[currentPosition - 1]
            currentPosition = currentPosition - 1
            
        array[currentPosition] = currentValue

def processCost(road):
    cost = 0
    lastProd = road[0]
    for i in road:
        if i == 'Campus':
            cost += transportation_costs[int(lastProd[5:])][-1]
        elif i == road[0]:
            lastProd=i
        else:
            cost += transportation_costs[int(lastProd[5:])][int(i[5:])]
            lastProd = i
    return cost

N1 = Arc(1,2,3)
N2 = Arc(1,3,4)
N3 = Arc(1,4,1)
N4 = Arc(2,3,1)

array = [N1,N2,N3,N4]
insertion_sort(array, lambda a,b : a.c > b.c)

# for arc in array:
#     print(arc)

Producers = {'G. Charpak': ['Prod_0', 'Prod_1', 'Prod_2', 'Prod_3', 'Prod_4']}

dailyOrders = {'Prod_0': 62, 'Prod_1': 58, 'Prod_2': 59, 'Prod_3': 59, 'Prod_4': 76}
#Producers = dicProducersLists["G. Charpark"]
print(Producers)
print(dailyOrders)


Capacity = {"Prod_0": 5000,
          "Prod_1": 0,
          "Prod_2": 3000,
          "Prod_3": 0,
          "Prod_4": 1000}
transportation_costs = [[0, 5, 9, 6, 4, 11],
                        [5, 0, 15, 7, 8, 6],
                        [10, 15, 0, 4, 16, 11],
                        [5, 7, 5, 0, 12, 4],
                        [4, 8, 15, 12, 0, 17],
                        [11, 5, 11, 5, 16, 0]
                       ]
print("cout :", transportation_costs[2][0])
distance_max = 100
Np = len(Producers)

RoadCost = []
SatisfiedDemand = []

Road = {}

#Créé une route partant du producteur ayant un véhicule
for i in Capacity:
    if(Capacity[i]!=0):
        Road[i] = [i]
        SatisfiedDemand.append(dailyOrders[i])
for i in Road:
    for j in Producers['G. Charpak']:
        if(j not in Road[i]):
            Road[i].append(j)

for i in Road:
    Road[i].append('Campus')
print("Road :",Road)


for i in Road:
    print(processCost(Road[i]))