import pulp
from typing import Dict, List
from lib.routing import Retailing as rt

# dicProducers = rt.getProducersLists()
# Campus = dicProducers.keys()
# dicDemand = rt.getDemand(dateMin, dateMax, Campus)
# dicCostsMatrix = rt.getTransportationCosts(Campus)
# dicCapacities = rt.getCapacities(Campus)
# dicVehicle = rt.getVehicles(dicCapacities)


def solveWithSolver(dicProducers, Campus, dicDemand, dicCostsMatrix, dicCapacities, dicVehicle, dist):
    for camp in Campus:
        campus = [camp]
        for day in dicDemand[camp]:
            print('campus : ', camp, ', jour : ', day)
            supply = dicDemand[camp][day]
            # print('supply', supply)

            Producers = dicProducers[camp]
            # print('producers', Producers)

            vehicle = dicVehicle[camp]
            # print('vehicle', vehicle)

            Capacity = dicCapacities[camp]
            # print('Capacities', Capacity)

            transportation_costs = dicCostsMatrix[camp]
            # print('Matrix', transportation_costs)

            costs = pulp.makeDict([campus + Producers, campus +
                                   Producers], transportation_costs, 0)

            distance_max = int(dist)
            Np = len(Producers)

            Vehicle = [(i, k) for i in campus + Producers for k in Producers]
            Routes = [(i, j, k) for i in campus + Producers for j in campus +
                      Producers for k in Producers]

            # lp variable declaration
            vars_routes = pulp.LpVariable.dicts(
                "Route", (campus + Producers, campus + Producers, Producers), 0, None, pulp.LpBinary)
            vars_visit = pulp.LpVariable.dicts(
                "Visit", (campus + Producers, Producers), 0, None, pulp.LpBinary)

            # problem and objective fonction
            prob = pulp.LpProblem("Coopain_VRP_Problem", pulp.LpMinimize)
            prob += pulp.lpSum([vars_routes[i][j][k] * costs[i][j]
                                for (i, j, k) in Routes]), "Sum_of_Transporting_Costs"

            # Producers can only be visited 1 time
            for i in Producers:
                prob += pulp.lpSum(vars_visit[i][k]
                                   for k in Producers) == 1, "visit_of_producers{0}".format(i)

            # Only 1 route by producer
            for k in Producers:
                for i in campus + Producers:
                    prob += (pulp.lpSum([vars_routes[i][j][k] for j in campus + Producers])
                             + pulp.lpSum([vars_routes[j][i][k] for j in campus + Producers])) \
                        <= 2, "visit_of_vehicle{0}_{1}".format(k, i)

            # disable routes from a producer to directely himself
            for i in campus + Producers:
                prob += pulp.lpSum([vars_routes[i][i][k]
                                    for k in Producers]) == 0, "no_autovisit{0}".format(i)

            # conservation of flux 1
            for i in campus + Producers:
                for k in Producers:
                    prob += pulp.lpSum([vars_routes[i][j][k] for j in campus + Producers]) \
                        == vars_visit[i][k], "visit_of_producers1_{0}_{1}".format(i, k)

            # conservation of flux 2
            for i in campus + Producers:
                for k in Producers:
                    prob += pulp.lpSum([vars_routes[j][i][k] for j in campus + Producers]) \
                        == vars_visit[i][k], "visit_of_producers2_{0}_{1}".format(i, k)

            # an inexistent vehicle can't do a path
            for k in Producers:
                prob += pulp.lpSum([vars_routes[i][j][k] for i in campus + Producers for j in campus + Producers]) \
                    <= 2*Np*vehicle[k], "vehicle_exists{0}".format(k)

            # a producer who uses his vehicle is at the beginnig of a loop
            for k in Producers:
                prob += pulp.lpSum([vars_visit[i][k] for i in Producers]) \
                    <= 2 * Np * vars_routes[campus[0]][k][k], "first_place{0}".format(k)

            # a producer can't use his vehicle too much
            for k in Producers:
                prob += pulp.lpSum([vars_routes[i][j][k] * costs[i][j] for i in campus + Producers for j in campus + Producers]) \
                    <= distance_max, "distance_max{0}".format(k)

            # a vehicule have a capacity
            for k in Producers:
                prob += pulp.lpSum([vars_visit[i][k] * supply[i] for i in Producers]) \
                    <= Capacity[k], "respect_capacity{0}".format(k)

            # no underloop
            for subset in rt.powerset(Producers):
                longueur = len(subset)
                subset_id = ""
                for m in range(longueur):
                    subset_id += subset[m]+"_"
                for k in Producers:
                    prob += pulp.lpSum([vars_routes[i][j][k] for i in subset for j in subset]) \
                        <= longueur-1, "no_underloop_{0}{1}".format(subset_id, k)

            # The problem data is written to an .lp file
            # prob.writeLP("CoopainVRPProblem.lp")

            # The problem is solved using Cplex
            # prob.solve(pulp.getSolver('GUROBI_CMD', timeLimit=10))
            prob.solve(pulp.PULP_CBC_CMD(fracGap=0))

            # The status of the solution is printed to the screen
            print("Status:", pulp.LpStatus[prob.status])

            # Each significant variables is in listeRoute
            listeRoute = []
            for v in prob.variables():
                if v.varValue and v.name[:6] == 'Route_':
                    listeRoute.append(v.name[6:])
                lenRoute = len(listeRoute)

            # initialisation des dictionnaires
            dictResultat: Dict[str, List[str]] = {}
            dictRoute: Dict[str, List[str]] = {}
            for i in range(lenRoute):
                for j in range(len(listeRoute[i])):
                    if listeRoute[i][-j-1:] in Producers:
                        dictResultat[listeRoute[i][-j - 1:]] = []
                        dictRoute[listeRoute[i][-j-1:]] = []

            # remplissage de dictRoute
            for i in range(lenRoute):
                for j in range(len(listeRoute[i])):
                    if listeRoute[i][-j-1:] in Producers:
                        dictRoute[listeRoute[i][-j-1:]
                                  ].append(listeRoute[i][:-j-2])

            # remplissage de dictResultat
            for vehicule in [*dictRoute]:
                finBoucle = 0
                visiteActuelle = vehicule
                while (finBoucle == 0):
                    for i in range(len(dictRoute[vehicule])):
                        for j in range(len(dictRoute[vehicule][i])):
                            if dictRoute[vehicule][i][:j] == visiteActuelle:
                                dictResultat[vehicule].append(visiteActuelle)
                                visiteActuelle = dictRoute[vehicule][i][j+1:]
                                if visiteActuelle == vehicule:
                                    finBoucle = 1

    print('dic = ', dictResultat)
    return dictResultat, pulp.value(prob.objective)

    # The optimised objective function value is printed to the screen
    # print("Total Cost of Transportation = ",
    #       pulp.value(prob.objective))
