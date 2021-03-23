# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 11:15:13 2021
    
@author: Coopain
"""

import pulp
import math
import pandas as pd
from time import gmtime, strftime
import datetime
import xlwt 
from xlwt import Workbook 



# Arrival_Time : table given the arrival date of the delivery vehicles,
# epsilon : delays time needed to bring the food to the distribution point
# NB_Clients : numbers of commands in each vehicles
# Personnes_Distribution : number of people needed in the distribution point
# Tps_Distribution : Time needed to give the command to one client
#Lmax = Time lapse to give everybody's commands

 
def solveWithSolver(Arrival_Time, epsilon, NB_Clients, Personnes_Distribution, Tps_Distribution, Lmax):
    indice = []
    NB_Clients_Total = 0
    top_inter = 0
    
    for i in NB_Clients:
        NB_Clients_Total += i
        
    for j in range (NB_Clients_Total):
        indice.append(j)
    
    # Decision variables and objective function 
    dvar_arrivee_clients = pulp.LpVariable.dicts("Heure d'arrivée", (indice),0, None, pulp.LpInteger)  
    dvar_depart_clients = pulp.LpVariable.dicts("Heure de départ", (indice),0, None, pulp.LpInteger)
    
    prob = pulp.LpProblem("Coopain_Distribution_Planning_Problem", pulp.LpMinimize)
    prob += pulp.lpSum([dvar_depart_clients[i]-dvar_arrivee_clients[i] for i in indice]), "Waiting_Time_Sum"
       
    for i in indice : 
        prob += (dvar_arrivee_clients[i] + Tps_Distribution <= dvar_depart_clients[i]),\
        "condition_arrivee_distribution_{0}".format(i) 
        prob += (dvar_depart_clients[i]<=Lmax),\
        "Lapse_temps_distribution{0}".format(i)

    
    for j in range(len(NB_Clients)) : 
        for i in range(1, NB_Clients[j]):
            prob += (dvar_arrivee_clients[top_inter+i]>= Arrival_Time[j] + epsilon), "condition_heure_arrivee_clins{0}".format(top_inter+i)
            
            #Condition sur la prise en charge des clients selon le nombre d'agents (x) 
 		    #au point de distribution 
             
            if (dvar_depart_clients[top_inter]<= Arrival_Time[j]):
                prob += (dvar_depart_clients[top_inter+i] >= Arrival_Time[j] + epsilon + \
                     (math.floor((top_inter+i-1)/Personnes_Distribution)+1)*Tps_Distribution),\
                    "condition_depart_{0}".format(i + top_inter)
            else: 
                prob += (dvar_depart_clients[top_inter+i] >= dvar_depart_clients[top_inter] + epsilon +\
                (math.floor((top_inter+i-1)/Personnes_Distribution)+1)*Tps_Distribution),\
                "condition_depart_{0}".format(top_inter+ i)
        top_inter += NB_Clients[j]
        
    for i in range (top_inter-1):
         prob += (dvar_arrivee_clients[i+1] >= dvar_arrivee_clients[i]), "condition_ordre_arrivee_{0}".format(i)
         prob += (dvar_depart_clients[i+1] >= dvar_depart_clients[i]), "condition_ordre_depart_{0}".format(i)
    
    prob.solve(pulp.PULP_CBC_CMD(fracGap=0))
    result = 60* [0]
    # The status of the solution is printed to the screen
    #print("Status:", pulp.LpStatus[prob.status])
    #print(prob.variables())
    # Each significant variables is printed with it's resolved optimum value
    for v in prob.variables():
        #print(v.name)
        #print("/")
        if v.varValue:
            if (v.name.find("Heure_d'") != -1):
                 #print(v.varValue)
                 #print("*")
                 result[int(v.varValue)] += 1
                 print("la case{0}".format(int(v.varValue)), " a pris plus un ")
                 print(v.name, "=", v.varValue)
                 
    print("tableau du cumul")
    print(result)     
    # Workbook is created 
    wb = Workbook() 
    
    # add_sheet is used to create sheet. 
    sheet1 = wb.add_sheet('Sheet 1') 
    style = xlwt.easyxf('font: bold 1') 
    sheet1.write(0, 0, 'Heure',style) 
    sheet1.write(0, 1, 'nombre',style)
    
    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'dd-mm-yyyy hh:mm'
    
    df = pd.DataFrame(columns=['Heure','nombre'])
    
    # result = 60* [0]
    # #print(result)
    # #for i in range(top_inter):
    #     #salve = 0
    # #print(prob.variables())
    # print("Ensemble des solutions")
    # for v in prob.variables():
    #     if (v.name.find("Heure_d'") != -1):
    #     #if v.name == "Heure_d'arrivée_{0}".format(i+1):
    #         #if (A == v.varValue):
    #             #salve +=1
    #         #else : 
    #           #  A = v.varValue
            
    #         print(v.varValue)
    #         result[int(v.varValue)] += 1
    #     #if v.name == "Heure_de_départ_{0}".format(i+1):
    #     #    B=v.varValue
    # # heure = current_date_and_time + datetime.timedelta(minutes=A) 
    #print("tableau du cumul")
    #print(result)
    index = 0
    for i in range(len(result)):
        if result[i] != 0:
            
            time = pd.Timestamp(2021, 3, 19, 12, i)
            #print(time)
            sheet1.write(index+1, 0, time, date_format) 
            sheet1.write(index+1, 1, result[i]) 
            index +=1
             
    #df = df.append({'Heure': time, 'nombre': 1 }, ignore_index=True)

    #df.groupby(['Heure'])    
    #print(df)     
    
    #The optimised objective function value is printed to the screen
    print("Total Cost of Transportation = ",pulp.value(prob.objective))
    
    wb.save('Cplex_Results.xls') 
    df.to_csv(r'CPlex_Results.csv', index = False)
    
#solveWithSolver(Arrival_Time, epsilon, NB_Clients, Personnes_Distribution, Tps_Distribution, Lmax)
solveWithSolver([0,5], 5, [30,22] , 4,1, 45)
