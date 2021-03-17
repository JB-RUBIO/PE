from tkinter import *
from tkinter import ttk
# from lib.formatter import DataGenerator as dg
from lib.routing import Retailing as rt
from lib.routing import RoutingSolver as rs
import time
import threading

TITLE = "Coop'Pain 95 edition"
TITLE_LABEL = "Generate the delivery schedule"
CAMPUS_LABEL = "Campus :"
DATE_LABEL = "Date (dd/mm/yy) :"
SOLVER_LABEL = "Method :"
# dateMin = '04/01/22'
# dateMax = '05/01/22'

root = Tk()
root.geometry('500x300')
root.title(TITLE)
# 5442


dicFile = rt.createDicFile()
dicToProcess = rt.createDicToProcess(dicFile)
dicProducers = rt.createDicProducersLists(dicFile)

listeCampus = []
for key in dicProducers:
    listeCampus.append(key)

listeMethod = ['Solver', 'Heuristic']


def process():

    Campus = [entryCampus.get()]
    dateMin = entryDate.get()
    dateMax = entryDate.get()

    dicDemand = rt.getDemand(dicToProcess, dateMin, dateMax, Campus)
    dicCostsMatrix = rt.getTransportationCosts(Campus)
    dicCapacities = rt.getCapacities(dicProducers, Campus)
    dicVehicle = rt.getVehicles(dicCapacities)

    if entrySolver.get() == 'Solver':
        rs.solveWithSolver(dicProducers, Campus, dicDemand,
                           dicCostsMatrix, dicCapacities, dicVehicle)
    else:
        print('en cours de dev')
    print(dicDemand)
    return None


x_SmallOffest = 30
y_SmallOffset = 30

x_BigOffest = 300
y_BigOffset = 80

x_LabelCampus, y_LabelCampus = 30, 70
x_EntryCampus, y_EntryCampus = x_LabelCampus, y_LabelCampus + y_SmallOffset

x_LabelDate, y_LabelDate = x_LabelCampus, y_LabelCampus + y_BigOffset
x_EntryDate, y_EntryDate = x_LabelDate, y_LabelDate + y_SmallOffset

x_LabelSolver, y_LabelSolver = x_LabelCampus + x_BigOffest, y_LabelCampus
x_EntrySolver, y_EntrySolver = x_LabelSolver, y_LabelSolver + y_SmallOffset


labelTitle = Label(root, text=TITLE_LABEL, font=('arial', 20, 'bold'))
labelTitle.pack(side=TOP, fill=X)

labelCampus = Label(root, text=CAMPUS_LABEL, font=('arial', 13, 'bold'))
labelCampus.place(x=x_LabelCampus, y=y_LabelCampus)
entryCampus = ttk.Combobox(root, values=listeCampus)
entryCampus.current(0)
entryCampus.place(x=x_EntryCampus, y=y_EntryCampus)

labelDate = Label(root, text=DATE_LABEL, font=('arial', 13, 'bold'))
labelDate.place(x=x_LabelDate, y=y_LabelDate)
entryDate = Entry(root, width=23)
entryDate.insert(END, '04/01/22')
entryDate.place(x=x_EntryDate, y=y_EntryDate)

labelSolver = Label(root, text=SOLVER_LABEL, font=('arial', 13, 'bold'))
labelSolver.place(x=x_LabelSolver, y=y_LabelSolver)
entrySolver = ttk.Combobox(root, values=listeMethod)
entrySolver.current(0)
entrySolver.place(x=x_EntrySolver, y=y_EntrySolver)

b = Button(root, text="Execute", command=process)
b.place(x=220, y=230)

root.mainloop()
