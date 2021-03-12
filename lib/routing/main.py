import pulp
from itertools import chain, combinations
from pathlib import Path

import Retailing as rt
CUR_DIR = Path(__file__).parent
INPUT_FILE = CUR_DIR.parent.parent / 'res' / 'routing' / 'DailyGroupedOrders.xlsx'
rt.readFile(INPUT_FILE)
exit(0)
#fonction to get subsets
def powerset(iterable):
    "powerset([1,2,3]) --> (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(2, len(s)))

#List of producers
Producers = ["1", "2", "3", "4", "5"]

supply = {"1": 500,
          "2": 900,
          "3": 1800,
          "4": 200,
          "5": 700}

#if the producers have an available vehicle or not
vehicle = {"1": 1,
          "2": 0,
          "3": 1,
          "4": 0,
          "5": 0}

#capacity of vehicles
Capacity = {"1": 5000,
          "2": 0,
          "3": 3000,
          "4": 0,
          "5": 0}

#cost matrix. The first index is the campus
transportation_costs = [[0, 5, 7 , 5, 5, 5],
                        [5, 0, 2, 111, 0, 11],
                        [7, 2, 0, 112, 12, 12],
                        [5, 111, 112, 0, 111, 265],
                        [5, 10, 1, 111, 0, 1],
                        [5, 171, 12, 112, 1, 0]
                       ]

costs = pulp.makeDict([["Campus"] + Producers, ["Campus"] + Producers], transportation_costs, 0)

distance_max = 25
Np = len(Producers)

Vehicle = [(i, k) for i in ["Campus"] + Producers for k in Producers]
Routes = [(i, j, k) for i in ["Campus"] + Producers for j in ["Campus"] + Producers for k in Producers]

#lp variable declaration
vars_routes = pulp.LpVariable.dicts("Route", (["Campus"] + Producers, ["Campus"] + Producers, Producers), 0, None, pulp.LpBinary)
vars_visit = pulp.LpVariable.dicts("Visit", (["Campus"] + Producers, Producers), 0, None, pulp.LpBinary)

#problem and objective fonction
prob = pulp.LpProblem("Coopain_VRP_Problem", pulp.LpMinimize)
prob += pulp.lpSum([vars_routes[i][j][k] * costs[i][j] for (i, j, k) in Routes]), "Sum_of_Transporting_Costs"

#Producers can only be visited 1 time
for i in Producers:
    prob += pulp.lpSum(vars_visit[i][k] for k in Producers) == 1, "visit_of_producers{0}".format(i)

#Only 1 route by producer
for k in Producers:
    for i in ["Campus"] + Producers :
        prob += (pulp.lpSum([vars_routes[i][j][k] for j in ["Campus"] + Producers])
                 + pulp.lpSum([vars_routes[j][i][k] for j in ["Campus"] + Producers])) \
                <= 2, "visit_of_vehicle{0}_{1}".format(k, i)

#disable routes from a producer to directely himself
for i in ["Campus"] + Producers:
    prob += pulp.lpSum([vars_routes[i][i][k] for k in Producers]) == 0, "no_autovisit{0}".format(i)

#conservation of flux 1
for i in ["Campus"] + Producers:
    for k in Producers:
        prob += pulp.lpSum([vars_routes[i][j][k] for j in ["Campus"] + Producers]) \
                == vars_visit[i][k], "visit_of_producers1_{0}_{1}".format(i,k)

#conservation of flux 2
for i in ["Campus"] + Producers:
    for k in Producers:
        prob += pulp.lpSum([vars_routes[j][i][k] for j in ["Campus"] + Producers]) \
                == vars_visit[i][k], "visit_of_producers2_{0}_{1}".format(i,k)

#an inexistent vehicle can't do a path
for k in Producers :
    prob += pulp.lpSum([vars_routes[i][j][k] for i in ["Campus"] + Producers for j in ["Campus"] + Producers]) \
                <= 2*Np*vehicle[k], "vehicle_exists{0}".format(k)

#a producer who uses his vehicle is at the beginnig of a loop
for k in Producers :
    prob += pulp.lpSum([vars_visit[i][k] for i in Producers]) \
                <= 2 * Np * vars_routes["Campus"][k][k], "first_place{0}".format(k)

#a producer can't use his vehicle too much
for k in Producers :
    prob += pulp.lpSum([vars_routes[i][j][k] * costs[i][j] for i in ["Campus"] + Producers for j in ["Campus"] + Producers]) \
                <= distance_max, "distance_max{0}".format(k)

#a vehicule have a capacity
for k in Producers :
    prob += pulp.lpSum([vars_visit[i][k] * supply[i] for i in Producers]) \
                <= Capacity[k], "respect_capacity{0}".format(k)


#no underloop
for subset in powerset(Producers):
    longueur = len(subset)
    subset_id = ""
    for m in range(longueur):
        subset_id += subset[m]+"_"
    for k in Producers :
        prob += pulp.lpSum([vars_routes[i][j][k] for i in subset for j in subset]) \
                <= longueur-1, "no_underloop_{0}{1}".format(subset_id, k)

# The problem data is written to an .lp file
prob.writeLP("CoopainVRPProblem.lp")

# The problem is solved using Cplex
prob.solve(pulp.getSolver('CPLEX_CMD', timeLimit=10))

# The status of the solution is printed to the screen
print("Status:", pulp.LpStatus[prob.status])

# Each significant variables is printed with it's resolved optimum value
for v in prob.variables():
    if v.varValue:
        print(v.name, "=", v.varValue)

# The optimised objective function value is printed to the screen
print("Total Cost of Transportation = ", pulp.value(prob.objective))