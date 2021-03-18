# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 11:15:13 2021
    
@author: Coopain
"""

from xlwt import Workbook
import xlwt
import datetime
from time import gmtime, strftime
import pulp
import math
import pandas as pd

# Arrival_Time : table given the arrival date of the delivery vehicles,
# epsilon : delays time needed to bring the food to the distribution point
# NB_Clients : numbers of commands in each vehicles
# Personnes_Distribution : number of people needed in the distribution point
# Tps_Distribution : Time needed to give the command to one client
# Lmax = Time lapse to give everybody's commands


def solveWithSolver(Arrival_Time, epsilon, NB_Clients, Personnes_Distribution, Tps_Distribution, Lmax):
    indice = []
    NB_Clients_Total = 0
    top_inter = 0

    for i in NB_Clients:
        NB_Clients_Total += i

    for j in range(NB_Clients_Total):
        indice.append(j)

    # Decision variables and objective function
    dvar_arrivee_clients = pulp.LpVariable.dicts(
        "Heure d'arrivée", (indice), 0, None, pulp.LpInteger)
    dvar_depart_clients = pulp.LpVariable.dicts(
        "Heure de départ", (indice), 0, None, pulp.LpInteger)

    prob = pulp.LpProblem(
        "Coopain_Distribution_Planning_Problem", pulp.LpMinimize)
    prob += pulp.lpSum([dvar_depart_clients[i]-dvar_arrivee_clients[i]
                        for i in indice]), "Waiting_Time_Sum"

    for i in indice:
        prob += (dvar_arrivee_clients[i] + Tps_Distribution <= dvar_depart_clients[i]),\
            "condition_arrivee_distribution_{0}".format(i)
        prob += (dvar_depart_clients[i] <= Lmax),\
            "Lapse_temps_distribution{0}".format(i)

    for j in range(len(NB_Clients)):

        for i in range(1, NB_Clients[j]):
            prob += (dvar_arrivee_clients[top_inter+i] >= Arrival_Time[j] +
                     epsilon), "condition_heure_arrivee_clins{0}".format(top_inter+i)

            # Condition sur la prise en charge des clients selon le nombre d'agents (x)
            # au point de distribution

            if (dvar_depart_clients[top_inter] <= Arrival_Time[j]):
                prob += (dvar_depart_clients[top_inter+i] >= Arrival_Time[j] + epsilon +
                         (math.floor((top_inter+i-1)/Personnes_Distribution)+1)*Tps_Distribution),\
                    "condition_depart_{0}".format(i + top_inter)
            else:
                prob += (dvar_depart_clients[top_inter+i] >= dvar_depart_clients[top_inter] + epsilon +
                         (math.floor((top_inter+i-1)/Personnes_Distribution)+1)*Tps_Distribution),\
                    "condition_depart_{0}".format(top_inter + i)
        top_inter += NB_Clients[j]

    for i in range(top_inter-1):
        prob += (dvar_arrivee_clients[i+1] >= dvar_arrivee_clients[i]
                 ), "condition_ordre_arrivee_{0}".format(i)
        prob += (dvar_depart_clients[i+1] >= dvar_depart_clients[i]
                 ), "condition_ordre_depart_{0}".format(i)

    prob.solve(pulp.PULP_CBC_CMD(fracGap=0))

    # # The status of the solution is printed to the screen
    # print("Status:", pulp.LpStatus[prob.status])
    # print(prob.variables())
    # # Each significant variables is printed with it's resolved optimum value
    # for v in prob.variables():
    #     if v.varValue:
    #         print(v.name, "=", v.varValue)

    df = pd.DataFrame(columns=['Heure_darrivée', 'Heure_de_depart'])
    for i in range(top_inter):
        for v in prob.variables():
            if v.name == "Heure_d'arrivée_{0}".format(i+1):
                A = v.varValue
            if v.name == "Heure_de_départ_{0}".format(i+1):
                B = v.varValue
        df = df.append(
            {'Heure_darrivée': A, 'Heure_de_depart': B}, ignore_index=True)

    print(df)
    # The optimised objective function value is printed to the screen
    print("Total Cost of Transportation = ",
          pulp.value(prob.objective))

    df.to_csv(r'CPlex_Results.csv', index=False)


#solveWithSolver(Arrival_Time, epsilon, NB_Clients, Personnes_Distribution, Tps_Distribution, Lmax)
solveWithSolver([0, 5], 5, [30, 22], 4, 1, 45)
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 11:15:13 2021
    
@author: Coopain
"""


# Arrival_Time : table given the arrival date of the delivery vehicles,
# epsilon : delays time needed to bring the food to the distribution point
# NB_Clients : numbers of commands in each vehicles
# Personnes_Distribution : number of people needed in the distribution point
# Tps_Distribution : Time needed to give the command to one client
# Lmax = Time lapse to give everybody's commands


def solveWithSolver(Arrival_Time, epsilon, NB_Clients, Personnes_Distribution, Tps_Distribution, Lmax):
    indice = []
    NB_Clients_Total = 0
    top_inter = 0

    for i in NB_Clients:
        NB_Clients_Total += i

    for j in range(NB_Clients_Total):
        indice.append(j)

    # Decision variables and objective function
    dvar_arrivee_clients = pulp.LpVariable.dicts(
        "Heure d'arrivée", (indice), 0, None, pulp.LpInteger)
    dvar_depart_clients = pulp.LpVariable.dicts(
        "Heure de départ", (indice), 0, None, pulp.LpInteger)

    prob = pulp.LpProblem(
        "Coopain_Distribution_Planning_Problem", pulp.LpMinimize)
    prob += pulp.lpSum([dvar_depart_clients[i]-dvar_arrivee_clients[i]
                        for i in indice]), "Waiting_Time_Sum"

    for i in indice:
        prob += (dvar_arrivee_clients[i] + Tps_Distribution <= dvar_depart_clients[i]),\
            "condition_arrivee_distribution_{0}".format(i)
        prob += (dvar_depart_clients[i] <= Lmax),\
            "Lapse_temps_distribution{0}".format(i)

    for j in range(len(NB_Clients)):
        for i in range(1, NB_Clients[j]):
            prob += (dvar_arrivee_clients[top_inter+i] >= Arrival_Time[j] +
                     epsilon), "condition_heure_arrivee_clins{0}".format(top_inter+i)

            # Condition sur la prise en charge des clients selon le nombre d'agents (x)
            # au point de distribution

            if (dvar_depart_clients[top_inter] <= Arrival_Time[j]):
                prob += (dvar_depart_clients[top_inter+i] >= Arrival_Time[j] + epsilon +
                         (math.floor((top_inter+i-1)/Personnes_Distribution)+1)*Tps_Distribution),\
                    "condition_depart_{0}".format(i + top_inter)
            else:
                prob += (dvar_depart_clients[top_inter+i] >= dvar_depart_clients[top_inter] + epsilon +
                         (math.floor((top_inter+i-1)/Personnes_Distribution)+1)*Tps_Distribution),\
                    "condition_depart_{0}".format(top_inter + i)
        top_inter += NB_Clients[j]

    for i in range(top_inter-1):
        prob += (dvar_arrivee_clients[i+1] >= dvar_arrivee_clients[i]
                 ), "condition_ordre_arrivee_{0}".format(i)
        prob += (dvar_depart_clients[i+1] >= dvar_depart_clients[i]
                 ), "condition_ordre_depart_{0}".format(i)

    prob.solve(pulp.PULP_CBC_CMD(fracGap=0))

    # # The status of the solution is printed to the screen
    # print("Status:", pulp.LpStatus[prob.status])
    # print(prob.variables())
    # # Each significant variables is printed with it's resolved optimum value
    # for v in prob.variables():
    #     if v.varValue:
    #         print(v.name, "=", v.varValue)

    # Workbook is created
    wb = Workbook()

    # add_sheet is used to create sheet.
    sheet1 = wb.add_sheet('Sheet 1')
    style = xlwt.easyxf('font: bold 1')
    sheet1.write(0, 0, 'Heure', style)
    sheet1.write(0, 1, 'nombre', style)

    df = pd.DataFrame(columns=['Heure', 'nombre'])
    for i in range(top_inter):
        for v in prob.variables():
            if v.name == "Heure_d'arrivée_{0}".format(i+1):
                A = v.varValue
            # if v.name == "Heure_de_départ_{0}".format(i+1):
            #    B=v.varValue
        #heure = current_date_and_time + datetime.timedelta(minutes=A)
        time = datetime.time(12, int(A))
        sheet1.write(i+1, 0, str(time))
        #sheet1.write(i+1, 0, '18-03-2021 ' + str(time) + ' AM')
        sheet1.write(i+1, 1, 1)

        df = df.append({'Heure': datetime.time(12, int(A)),
                        'nombre': 1}, ignore_index=True)

    # df.groupby(['Heure'])
    # print(df)

    # The optimised objective function value is printed to the screen
    print("Total Cost of Transportation = ", pulp.value(prob.objective))

    wb.save('Cplex_Results.xls')
    df.to_csv(r'CPlex_Results.csv', index=False)


#solveWithSolver(Arrival_Time, epsilon, NB_Clients, Personnes_Distribution, Tps_Distribution, Lmax)
solveWithSolver([0, 5], 5, [30, 22], 4, 1, 45)
