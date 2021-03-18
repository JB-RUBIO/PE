from tkinter import *
from tkinter import ttk
# from lib.formatter import DataGenerator as dg
from lib.routing import Retailing as rt
from lib.routing import RoutingSolver as rs
from lib.routing import RoutingHeuristic as rh

TITLE = "Coop'Pain 95 edition"
TITLE_LABEL = "Generate the delivery schedule"
CAMPUS_LABEL = "Campus :"
DATE_LABEL = "Date (dd/mm/yy) :"
SOLVER_LABEL = "Method :"
DIST_LABEL = "Max cost (minutes):"

root = Tk()
root.geometry('500x305')
root.title(TITLE)

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
    dist = entryDist.get()

    dicDemand = rt.getDemand(dicToProcess, dateMin, dateMax, Campus)
    dicCostsMatrix = rt.getTransportationCosts(Campus)
    dicCapacities = rt.getCapacities(dicProducers, Campus)
    dicVehicle = rt.getVehicles(dicCapacities)

    if entrySolver.get() == 'Solver':
        rs.solveWithSolver(dicProducers, Campus, dicDemand,
                           dicCostsMatrix, dicCapacities, dicVehicle, int(dist))

        # showResults(Campus[0], dateMin, 'voici les résultats!')
    else:
        try:
            dicToPrint = rh.driverHeuristic(dicProducers, Campus, dicDemand,
                                            dicCostsMatrix, dicCapacities, int(dist))
            print(dicToPrint)
            showResults(Campus[0], dateMin, dicToPrint)
        except KeyError:
            print('The heuristic can\'t find solution with parameter : \'Max cost\' = ', dist,
                  ' minutes. Please, try an other value for \'Max cost\' or use the solver for a better result.')
    print('The demand is : ', dicDemand)
    return None


def showResults(Campus, dateMin, dicToPrint):
    res = Tk()
    res.geometry('700x700')
    res.title('Coop\'Pain_Delivery_Schedule_' + Campus + '_' + dateMin)
    x_LabelResRoute, y_LabelResRoute = 10, 60
    x_Offset, y_Offset = 30, 60

    strResTitle = ('Delivery schedule for the campus ' +
                   Campus + ' at the date ' + dateMin + '.')

    Label(res, text=strResTitle,  font=('arial', 14, 'bold')).pack()
    strResRoutes = str(len(dicToPrint)) + ' route(s) needed :'

    Label(res, text=strResRoutes,  font=('arial', 12, 'bold')).place(
        x=x_LabelResRoute, y=y_LabelResRoute)

    nRoute = 1
    for route in dicToPrint:
        currentRoute = 'Route ' + str(nRoute) + ' :'
        Label(res, text=currentRoute,  font=('arial', 12)).place(
            x=x_LabelResRoute, y=y_LabelResRoute + nRoute * y_Offset)

        strRes = '    '
        for producer in dicToPrint[route]:
            strRes += ' --- ' + producer.getName
        # strRes + ' end.'
        Label(res, text=strRes, font=('arial', 12)).place(
            x=x_LabelResRoute + x_Offset, y=y_LabelResRoute + nRoute * y_Offset + 20)
        nRoute += 1

    res.mainloop()


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

x_LabelDist, y_LabelDist = x_LabelCampus + \
    x_BigOffest, y_LabelCampus + y_BigOffset
x_EntryDist, y_EntryDist = x_LabelDist, y_LabelDist + y_SmallOffset

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

labelDist = Label(root, text=DIST_LABEL, font=('arial', 13, 'bold'))
labelDist.place(x=x_LabelDist, y=y_LabelDist)
entryDist = Entry(root, width=23)
entryDist.insert(END, 200)
entryDist.place(x=x_EntryDist, y=y_EntryDist)

buttonExec = Button(root, text="Execute", command=process)
buttonExec.place(x=220, y=230)

root.mainloop()
