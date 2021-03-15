import pulp
import itertools

class Arc:
    def __init__(self, n1, n2, c):
        self.n1 = n1
        self.n2 = n2
        self.c = c
    def __str__(self):
        return str.format("({},{},{}))", self.n1, self.n2, self.c)
    
class Prod:
    def __init__(self, name, Id):
        self.name = name
        self.Id = Id

    def getId(self):
        if(self.name == 'Campus'):
            return -1
        else:
            return int(self.name[5:])
    def __repr__(self):
        return "%s" % self.name
    def __str__(self):
        return  "Producteur %s" % self.Id

    @property
    def getName(self):
        return self.name
    
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
            cost += transportation_costs[lastNode.getId()][-1]
            lastNode = i
        elif(i in road):
            cost += transportation_costs[lastNode.getId()][i.getId()]
            lastNode = i
        else:
            lastNode = i
    return cost
        
def cost_change(cost_mat, n1, n2, n3, n4):
    return cost_mat[n1][n3] + cost_mat[n2][n4] - cost_mat[n1][n2] - cost_mat[n3][n4]

def two_opt(route, cost_mat):
    best = route
    improved = True
    while improved:
        improved = False
        for i in range(2, len(route) - 2):
            for j in range(i + 1, len(route)):
                if j - i == 1: continue
                if cost_change(transportation_costs, best[i - 1].getId(), best[i].getId(), best[j - 1].getId(), best[j].getId()) < 0:
                    best[i:j] = best[j - 1:i - 1:-1]
                    improved = True
        route = best
    return best

readProd = ["Prod_0", "Prod_1", "Prod_2", "Prod_3", "Prod_4"]
Producers = []
for i in readProd:
    Producers.append(Prod(i, int(i[5:])))

supply = {"Prod_0": 500,
          "Prod_1": 900,
          "Prod_2": 1800,
          "Prod_3": 200,
          "Prod_4": 700}


Capacity = {"Prod_0": 5000,
          "Prod_1": 0,
          "Prod_2": 3000,
          "Prod_3": 0,
          "Prod_4": 1500}

#La dernière colonne/ligne et transportation_costs correspond au campus
transportation_costs = [[0, 5, 9, 6, 4, 11],
                        [5, 0, 15, 7, 8, 6],
                        [10, 15, 0, 4, 16, 11],
                        [5, 7, 5, 0, 12, 4],
                        [4, 8, 15, 12, 0, 17],
                        [11, 5, 11, 5, 16, 0]
                       ]

max_distance = 25
Np = len(Producers)

Road = {}
RoadCost = []
finalRoad = {}
SatisfiedDemand = {}
total_demand = 0
for i in supply:
    total_demand += supply[i]



#Create road that starts where vehicles are available

for i in Capacity:
    if(Capacity[i]!=0):
        if(i not in SatisfiedDemand):
            SatisfiedDemand[i] = supply[i]
        else:
            SatisfiedDemand[i] += supply[i]
        Road[i] = [Prod(i, int(i[5:]))]

print(SatisfiedDemand)

#Add nodes to roads
#TO ADD: Taking into accounts unvisited producers when missing capacities
#Suggest additionnal tour
for i in Road:
    for j in Producers:
        if((j.getId() != Road[i][0].getId())  and Capacity[i] >= (SatisfiedDemand[i] + supply[j.getName])):
            Road[i].append(j)
            SatisfiedDemand[i] += supply[j.getName]


#Add campus to roads
for i in Road:
    Road[i].append(Prod('Campus', -1))



#Costs display
for i in Road: 
    print("Coût de la route", i, ": ", costProcess(Road[i]))
for i in SatisfiedDemand:
    print("Demande de la route", i, ": ", SatisfiedDemand[i])


#Roads enhacement 

deltaMin = 0

for i in Road:
    print(Road[i])

t = two_opt(Road[i], transportation_costs)
for i in Road:
    print("Le camion part de", i)
    Road[i] = two_opt(Road[i], transportation_costs)
    print("Route empruntée :", two_opt(Road[i], transportation_costs))
    print("Le coût est désormais de :", costProcess(Road[i]))

cost_min = max_distance * Np
demand_max = 0
bestRoad = []
tempRoad = []



for i in Road:
    print(SatisfiedDemand[i])
    if demand_max == SatisfiedDemand[i]:    #Si la demande est satisfaite
        demand_max = SatisfiedDemand[i]
        tempRoad = Road[i]
        cost = costProcess(tempRoad)
        if cost_min > cost:
            cost_min = cost
            bestRoad = Road[i]

print(bestRoad)
print(finalRoad)
#succ(k) = Road[i][rang+1]
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

