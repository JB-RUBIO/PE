import numpy as np
import copy
# import Retailing as rt

# TODO: transform matrix to place campus as last index
# max_distance = 150


class Prod:
    def __init__(self, name, Id, Group=0):
        self.name = name
        self.Id = Id

    def getId(self):
        if(self.name == 'Campus'):
            return -1
        else:
            return int(self.name[5:])

    def __repr__(self):
        return "%s" % self.name

    # def __str__(self):
    #     return "Producteur %s" % self.Id

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


def costProcess(road, campus, transportation_costs):
    cost = 0
    lastNode = road[0]
    for i in road:
        if(i == campus):
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
                if j - i == 1:
                    continue
                if cost_change(cost_mat, best[i - 1].getId(), best[i].getId(), best[j - 1].getId(), best[j].getId()) < 0:
                    best[i:j] = best[j - 1:i - 1:-1]
                    improved = True
        route = best
    return best


def addNode(road, group, GroupRoad, Road, Producers, supply, SatisfiedDemand, Capacity, transportation_costs, dist):

    if(len(GroupRoad[group]) == 1):  # Add nodes for one truck
        for j in Producers:
            if((j.getName != road[0].getName) and Capacity[road[0].getName] >= (SatisfiedDemand[road[0].getName] + supply[j.getName])):
                road.append(j)
                SatisfiedDemand[road[0].getName] += supply[j.getName]
    else:
        visited = np.zeros(len(Producers), dtype=bool)
        for i in GroupRoad[group]:
            # Add producers of the group to visited producers
            visited[i.Id] = 1
        for i in Producers:  # Attribute producers to closer truck in the group
            if(visited[i.Id] == 0):
                cost = dist
                cheaper = 0
                for j in GroupRoad[group]:
                    if(cost > transportation_costs[j.Id+1][i.Id+1]) and (SatisfiedDemand[j.getName] < Capacity[j.getName]):
                        cost = transportation_costs[j.Id+1][i.Id+1]
                        cheaper = copy.deepcopy(j)
                Road[cheaper.getName].append(i)
                SatisfiedDemand[cheaper.getName] += supply[i.getName]
                visited[i.Id] = 1


def processWithHeuristic(readProd, supply, Capacity, transportation_costs, campus, dist):
    Producers = []
    for i in readProd:
        Producers.append(Prod(i, int(i[5:])))

    Road = {}
    SatisfiedDemand = {}
    total_demand = 0
    for i in supply:
        total_demand += supply[i]

    GroupRoad = {}
    GroupCapacity = []

    # Create road that starts where vehicles are available and group by round

    grp_size = 0
    grp_index = 0
    for i in Capacity:
        if(Capacity[i] != 0):

            if(i not in SatisfiedDemand):
                SatisfiedDemand[i] = supply[i]
            else:
                SatisfiedDemand[i] += supply[i]
            Road[i] = [Prod(i, int(i[5:]))]
            if(Capacity[i] >= total_demand):
                grp_size = 0
                grp_index += 1
                GroupRoad[i] = [copy.deepcopy(Road[i][0])]
                GroupCapacity.append(Capacity[i])

            elif(Capacity[i] < total_demand or GroupCapacity[grp_index] < total_demand):
                #SatisfiedDemand[i] +=  supply[i]
                if(grp_size == 0):
                    start_prod = i
                    GroupCapacity.append(Capacity[i])

                    GroupRoad[i] = [copy.deepcopy(Road[i][0])]
                    grp_size += 1
                else:
                    GroupCapacity[grp_index] = Capacity[i] + \
                        GroupCapacity[grp_index]
                    GroupRoad[start_prod].append(Road[i][0])
                    grp_size += 1
            if(Capacity[i] >= total_demand or GroupCapacity[grp_index] >= total_demand):
                grp_size = 0

    # Add nodes to roads taking into account groups
    for i in GroupRoad:
        addNode(Road[i], i, GroupRoad, Road, Producers, supply,
                SatisfiedDemand, Capacity, transportation_costs, dist)

    # Roads enhacement

    for i in Road:
        Road[i] = two_opt(Road[i], transportation_costs)

    # Add campus to roads
    for i in Road:
        Road[i].append(Prod('Campus', -1))

    # Producers returns at home
    for i in Road:
        Road[i].append(Road[i][0])

    ind = 0
    toDel = np.zeros(len(GroupRoad), dtype=int)
    toDel -= 1
    cost_min = dist

    cost = [0] * len(GroupRoad)
    for i in GroupRoad:
        if(GroupCapacity[ind] < total_demand):
            toDel[ind] = ind
        for j in GroupRoad[i]:
            cost[ind] = cost[ind] + \
                costProcess(Road[j.getName], campus, transportation_costs)
            if(cost[ind] > dist or cost[ind] == 0):
                toDel[ind] = ind
        ind += 1

    index = list(GroupRoad)
    best_ind = None
    bestRoad = {}
    deleted = 0
    for i in toDel:
        if(i != -1):
            del GroupRoad[index[i]]
            del cost[i - deleted]
            deleted += 1
    if len(cost) == 0:
        raise KeyError
        # print("No solution found.")
    else:
        index = list(GroupRoad)
        for i in range(len(cost)):
            if cost_min > cost[i]:
                cost_min = cost[i]
                best_ind = i
        for i in GroupRoad[index[best_ind]]:
            bestRoad[i.getName] = Road[i.getName]
    print(total_demand)

    return bestRoad, cost[best_ind]


def driverHeuristic(dicProducers, Campus, dicDemand, dicCostsMatrix, dicCapacities, dist):

    for camp in Campus:
        # campus = [camp]
        for day in dicDemand[camp]:
            print('campus : ', camp, ', jour : ', day)
            supply = dicDemand[camp][day]

            Producers = dicProducers[camp]
            # print('producers', Producers)

            Capacity = dicCapacities[camp]
            # print('Capacities', Capacity)

            transportation_costs = dicCostsMatrix[camp]
            # print('Matrix', transportation_costs)

            return processWithHeuristic(
                Producers, supply, Capacity, transportation_costs, camp, dist)
