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



N1 = Arc(1,2,3)
N2 = Arc(1,3,4)
N3 = Arc(1,4,1)
N4 = Arc(2,3,1)

array = [N1,N2,N3,N4]

Producers = ["1", "2", "3", "4", "5"]

supply = {"1": 500,
          "2": 900,
          "3": 1800,
          "4": 200,
          "5": 700}

vehicle = {"1": 1,
          "2": 0,
          "3": 1,
          "4": 0,
          "5": 0}

Capacity = {"1": 5000,
          "2": 0,
          "3": 3000,
          "4": 0,
          "5": 1000}

demand = {"1":500,
          "2":900,
          "3":1800,
          "4":200,
          "5":700,}

transportation_costs = [[0, 5, 9, 6, 4, 11],
                        [5, 0, 15, 7, 8, 6],
                        [10, 15, 0, 4, 16, 11],
                        [5, 7, 5, 0, 12, 4],
                        [4, 8, 15, 12, 0, 17],
                        [11, 5, 11, 5, 16, 0]
                       ]

costs = pulp.makeDict([["Campus"] + Producers, ["Campus"] + Producers], transportation_costs, 0)

distance_max = 25
Np = len(Producers)

Vehicle = [(i, k) for i in ["Campus"] + Producers for k in Producers]
Road = []
RoadCost = []
SatisfiedDemand = []



#Créé une route partant du producteur ayant un véhicule
for i in vehicle:
    if(vehicle[i]==1):
        Road.append([i])
        SatisfiedDemand.append(demand[i])
print(len(Producers))
print(Road)
for i in range(len(Road)):
    print("i=",i)
    print(Road)
    for j in Producers: #producer = liste str
        print(Road)
        print("j=",j)
        for k in range(1,len(Producers)-i-1):
            print(Road)
            if(j not in Road[i] and k not in Road[i]):
                print("k=",k)
                to_add = Road[i] + [Producers[k]]
                Road.insert(i+1,to_add)

                print(Road)
        else:
            pass
            
print(Road)



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

