import pulp
import itertools

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

def costProcess(road):
    cost = 0
    lastNode = road[0]
    for i in road:
        if(i=='Campus'):
            cost += transportation_costs[int(lastNode[5:])][-1]
            lastNode = i
        elif(i in road):
            cost += transportation_costs[int(lastNode[5:])][int(i[5:])]
            lastNode = i
        else:
            lastNode = i
    return cost
        



N1 = Arc(1,2,3)
N2 = Arc(1,3,4)
N3 = Arc(1,4,1)
N4 = Arc(2,3,1)

array = [N1,N2,N3,N4]
insertion_sort(array, lambda a,b : a.c > b.c)

for arc in array:
    print(arc)



Producers = ["Prod_0", "Prod_1", "Prod_2", "Prod_3", "Prod_4"]

supply = {"Prod_0": 500,
          "Prod_1": 900,
          "Prod_2": 1800,
          "Prod_3": 200,
          "Prod_4": 700}


Capacity = {"Prod_0": 5000,
          "Prod_1": 0,
          "Prod_2": 3000,
          "Prod_3": 0,
          "Prod_4": 1000}

#La dernière colonne/ligne et transportation_costs correspond au campus
transportation_costs = [[0, 5, 9, 6, 4, 11],
                        [5, 0, 15, 7, 8, 6],
                        [10, 15, 0, 4, 16, 11],
                        [5, 7, 5, 0, 12, 4],
                        [4, 8, 15, 12, 0, 17],
                        [11, 5, 11, 5, 16, 0]
                       ]

distance_max = 25
Np = len(Producers)

Road = {}
RoadCost = []
SatisfiedDemand = {}



#Créé une route partant du producteur ayant un véhicule

for i in Capacity:
    if(Capacity[i]!=0):
        if(i not in SatisfiedDemand):
            SatisfiedDemand[i] = supply[i]
        else:
            SatisfiedDemand[i] += supply[i]
        Road[i] = [i]

print(SatisfiedDemand)
for i in Road:
    for j in Producers:
        if(j not in Road[i]):
                Road[i].append(j)

for i in Road:
    Road[i].append('Campus')
print(Road)

for i in Road:
    print(costProcess(Road[i]))




# for i in range(len(Road)):
#     s = 0
#     for j in range(len(Road[0])-1):
#         print()
#         #s += transportation_costs[Road[i][j]-1][Road[i][j+1]-1]
#     RoadCost.append(s)

       # s += transportation_costs[Road[i][j]][Road[i][j+1]]

# vars_Road = pulp.LpVariable.dicts(("Route", ["Campus"] + Producers, ["Campus"] + Producers, Producers), 0, None, pulp.LpInteger)
# vars_visit = pulp.LpVariable.dicts(("Route", ["Campus"] + Producers, Producers), 0, None, pulp.LpInteger)

# prob = pulp.LpProblem("Coopain VRP Problem",pulp.LpMinimize)
# prob += pulp.lpSum([vars_Road[i][j][k] * costs[i][j] for (i, j, k) in Road]), "Sum_of_Transporting_Costs"

