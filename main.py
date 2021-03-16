from tkinter import *
from tkinter import ttk
from lib.formatter import DataGenerator as dg
from lib.routing import Retailing as rt
from lib.routing import Routingsolver as rs

TITLE = "Coop'Pain 95 edition"
TITLE_LABEL = "Generate the delivery schedule"
CAMPUS_LABEL = "Campus :"
DATE_LABEL = "Date (dd/mm/yyyy) :"
SOLVER_LABEL = "Method :"

dicProducers = rt.getProducersLists()
listeCampus = []
for key in dicProducers:
    listeCampus.append(key)

listeMethod = ['Solver', 'Heuristic']


root = Tk()
root.geometry('500x300')
root.title(TITLE)
# 5442


def process():
    print(entryCampus.get(),
          entryDate.get(),
          entrySolver.get())
    print(type(entryDate.get()))
    dicProducers = rt.getProducersLists()
    Campus = dicProducers.keys()
    dateMin = '04/01/22'
    dateMax = '05/01/22'
    dicDemand = rt.getDemand(dateMin, dateMax, Campus)
    dicCostsMatrix = rt.getTransportationCosts(Campus)
    dicCapacities = rt.getCapacities(Campus)
    dicVehicle = rt.getVehicles(dicCapacities)

    rs.solveWithSolver(dicProducers, Campus, dicDemand,
                       dicCostsMatrix, dicCapacities, dicVehicle)
    return None


labelTitle = Label(root, text=TITLE_LABEL, font=('arial', 20, 'bold'))
labelTitle.pack(side=TOP, fill=X)

labelCampus = Label(root, text=CAMPUS_LABEL, font=('arial', 13, 'bold'))
labelCampus.place(x=30, y=70)
entryCampus = ttk.Combobox(root, values=listeCampus)
entryCampus.current(0)
entryCampus.place(x=30, y=100)

labelDate = Label(root, text=DATE_LABEL, font=('arial', 13, 'bold'))
labelDate.place(x=30, y=150)
entryDate = Entry(root, width=23)
entryDate.place(x=30, y=180)

labelSolver = Label(root, text=SOLVER_LABEL, font=('arial', 13, 'bold'))
labelSolver.place(x=330, y=70)
entrySolver = ttk.Combobox(root, values=listeMethod)
entrySolver.current(0)
entrySolver.place(x=330, y=100)

b = Button(root, text="Execute", command=process)
b.place(x=220, y=230)

root.mainloop()
