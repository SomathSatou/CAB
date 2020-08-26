import getopt, sys
import numpy as np
import matplotlib.pyplot as plt
from output import *
from decimal import *

try:
    opts, args = getopt.getopt(sys.argv[1:], "f:n:x:y:l:m:s:", ["file",
                                                            "nbrCycle",
                                                            "xlabel",
                                                            "ylabel",
                                                            "label",
                                                            "mean",
                                                            "saveFile"
                                                            ])
except getopt.GetoptError as err:
    # print help information and exit:
    help()
    debug(err)  # will print something like "option -a not recognized"
    sys.exit(2)

# default value for diplay parameters
output = None
verbose = False
moy = False

label = ""
getcontext().prec = 20

# setting of paramaters
for o, a in opts:
    if o in ("-f", "--file"):
        path = str(a)
    elif o in ("-n", "--nbrCycle"):
        nbrCycle = int(a)
    elif o == "-x":
        xlabel = str(a)
    elif o == "-y":
        ylabel = str(a)
    elif o in ("-l", "--label"):
        label = str(a)
    elif o in ("-m", "--mean"):
        chem = str(a)
        moy = True
    elif o in ("-s", "--saveFile"):
        save = str(a)
    else:
        assert False, "unhandled option "+o

listname = ["cycle_50",
            "cycle_200",
            "toroidalmesh_4",
            "toroidalmesh_15",
            "hamming4x5x5",
            "hamming2x2x5x6x7",
            "mesh9_9",
            "mesh50_20",
            "path_50",
            "path_200",
            "3dmesh_2_2_3",
            "3dmesh_4_4_68",
            "double_star_15_5",
            "double_star_40_20",
            "hypercube_4_16",
            "hypercube_7_128",
            "cbt_30",
            "cbt_500",
            "D-bcsstk01.mtx",
            "ash85.mtx",
            "662_bus.mtx",
            "caterpillar_5_4",
            "caterpillar_10_6",
            "random-graph-250-01",
            "random-graph-750-05",
            "R-dwt_503.mtx",
            "jgl009.mtx",
            "p1_100",
            "p21_200"
            ]
for path in listname:
    listeT = [
    "/media/etudiant/TOSHIBA EXT/thomas/"+path+",twoBestIn5Random,crossover,swap,worst,CAB.txt",
    #"/media/etudiant/TOSHIBA EXT/thomas/"+path+",twoLowIn5Random,crossover,swap,best,fitness1.txt",
    "/media/etudiant/TOSHIBA EXT/thomas/"+path+",twoBestIn5Random,crossover,swap,worst,fitness2.txt",
    "/media/etudiant/TOSHIBA EXT/thomas/"+path+",twoBestIn5Random,crossover,swap,worst,fitness3.txt",
    "/media/etudiant/TOSHIBA EXT/thomas/"+path+",twoBestIn5Random,crossover,swap,worst,fitness4.txt"
    ]
    labelT = [
        "temoin",
    #    "f1",
        "f2",
        "f3",
        "f4"
    ]

    listeC =[
    #"/media/etudiant/TOSHIBA EXT/thomas/"+path+",twoLowIn5Random,crossoverUCB,swap,best,fitness1.txt",
    "/media/etudiant/TOSHIBA EXT/thomas/"+path+",twoBestIn5Random,crossoverUCB,swap,worst,fitness2.txt",
    "/media/etudiant/TOSHIBA EXT/thomas/"+path+",twoBestIn5Random,crossoverUCB,swap,worst,fitness4.txt"
    ]
    labelC = [
        "Cf2",
        "Cf4"
    ]

    listeM = [
    #"/media/etudiant/TOSHIBA EXT/thomas/"+path+",twoLowIn5Random,crossover,mutatorUCB,best,fitness1.txt",
    "/media/etudiant/TOSHIBA EXT/thomas/"+path+",twoBestIn5Random,crossover,mutatorUCB,worst,fitness2.txt",
    "/media/etudiant/TOSHIBA EXT/thomas/"+path+",twoBestIn5Random,crossover,mutatorUCB,worst,fitness4.txt"
    ]
    labelM = [
        "Mf2",
        "Mf4"
    ]

    listeCM = [
     #"/media/etudiant/TOSHIBA EXT/thomas/"+path+",twoLowIn5Random,crossoverUCB,mutatorUCB,best,fitness1.txt",
     "/media/etudiant/TOSHIBA EXT/thomas/"+path+",twoBestIn5Random,crossoverUCB,mutatorUCB,worst,fitness2.txt",
     "/media/etudiant/TOSHIBA EXT/thomas/"+path+",twoBestIn5Random,crossoverUCB,mutatorUCB,worst,fitness4.txt"
     ]
    labelCM = [
        "CMf2",
        "CMf4"
    ]

    listecouple = [
    #"/media/etudiant/TOSHIBA EXT/thomas/"+path+",twoLowIn5Random,coupleUCB,nothing,best,fitness1.txt",
    "/media/etudiant/TOSHIBA EXT/thomas/"+path+",twoBestIn5Random,coupleUCB,nothing,worst,fitness2.txt",
    "/media/etudiant/TOSHIBA EXT/thomas/"+path+",twoBestIn5Random,coupleUCB,nothing,worst,fitness4.txt"
    ]
    labelCp = [
        "Cpf2",
        "Cpf4"
    ]

    for i in range(0, len(listeT)):
        x = range(1,nbrCycle+1,1)
        temp = []
        for j in range(0,nbrCycle):
            tmp = []
            temp.append(tmp)
        y = []

        file = open(listeT[i])
        content = file.readlines()

        for line in content:
            tab = line.split(";")
            tab = tab[:-1]
            for j in range(0, nbrCycle):
                try:
                    add = Decimal(tab[j])
                    temp[j].append(add)
                except IndexError:
                    debug(path)
                    debug(j)

        for elt in temp:
            y.append(np.mean(elt))

        plt.plot(x, y, label=labelT[i])


        plt.ylabel(ylabel)
        plt.xlabel(xlabel)

    plt.legend()
    plt.savefig("/home/etudiant/Images/graph/"+path+"GroupeTemoin.png", dpi=750, bbox_inches='tight')
    #plt.show()
    plt.clf()

    for i in range(0, len(listeC)):
        x = range(1,nbrCycle+1,1)
        temp = []
        for j in range(0,nbrCycle):
            tmp = []
            temp.append(tmp)
        y = []

        file = open(listeC[i])
        content = file.readlines()

        for line in content:
            tab = line.split(";")
            tab = tab[:-1]
            for j in range(0, nbrCycle):
                try:
                    add = Decimal(tab[j])
                    temp[j].append(add)
                except IndexError:
                    debug(path)
                    debug(j)

        for elt in temp:
            y.append(np.mean(elt))

        plt.plot(x, y, label=labelC[i])


        plt.ylabel(ylabel)
        plt.xlabel(xlabel)

    plt.legend()
    plt.savefig("/home/etudiant/Images/graph/"+path+"GroupeCrossover.png", dpi=750, bbox_inches='tight')
    #plt.show()
    plt.clf()

    for i in range(0, len(listeM)):
        x = range(1,nbrCycle+1,1)
        temp = []
        for j in range(0,nbrCycle):
            tmp = []
            temp.append(tmp)
        y = []

        file = open(listeM[i])
        content = file.readlines()

        for line in content:
            tab = line.split(";")
            tab = tab[:-1]
            for j in range(0, nbrCycle):
                try:
                    add = Decimal(tab[j])
                    temp[j].append(add)
                except IndexError:
                    debug(path)
                    debug(j)

        for elt in temp:
            y.append(np.mean(elt))

        plt.plot(x, y, label=labelM[i])


        plt.ylabel(ylabel)
        plt.xlabel(xlabel)

    plt.legend()
    plt.savefig("/home/etudiant/Images/graph/"+path+"GroupeMutator.png", dpi=750, bbox_inches='tight')
    #plt.show()
    plt.clf()

    for i in range(0, len(listeCM)):
        x = range(1,nbrCycle+1,1)
        temp = []
        for j in range(0,nbrCycle):
            tmp = []
            temp.append(tmp)
        y = []

        file = open(listeCM[i])
        content = file.readlines()

        for line in content:
            tab = line.split(";")
            tab = tab[:-1]
            for j in range(0, nbrCycle):
                try:
                    add = Decimal(tab[j])
                    temp[j].append(add)
                except IndexError:
                    debug(path)
                    debug(j)

        for elt in temp:
            y.append(np.mean(elt))

        plt.plot(x, y, label=labelCM[i])


        plt.ylabel(ylabel)
        plt.xlabel(xlabel)

    plt.legend()
    plt.savefig("/home/etudiant/Images/graph/"+path+"GroupeCM.png", dpi=750, bbox_inches='tight')
    #plt.show()
    plt.clf()

    for i in range(0, len(listecouple)):
        x = range(1,10000+1,1)
        temp = []
        for j in range(0,10000):
            tmp = []
            temp.append(tmp)
        y = []

        file = open(listecouple[i])
        content = file.readlines()

        for line in content:
            tab = line.split(";")
            tab = tab[:-1]
            for j in range(0, 10000):
                try:
                    add = Decimal(tab[j])
                    temp[j].append(add)
                except IndexErrror:
                    debug(listecouple[i])
                    debug(j)

        for elt in temp:
            y.append(np.mean(elt))

        plt.plot(x, y, label=labelCp[i])


        plt.ylabel(ylabel)
        plt.xlabel(xlabel)

    plt.legend()
    plt.savefig("/home/etudiant/Images/graph/"+path+"Groupecouple.png", dpi=750, bbox_inches='tight')
    #plt.show()
    plt.clf()

    for i in range(0, len(listeT)):
        x = range(1,nbrCycle+1,1)
        temp = []
        for j in range(0,nbrCycle):
            tmp = []
            temp.append(tmp)
        y = []

        file = open(listeT[i])
        content = file.readlines()

        for line in content:
            tab = line.split(";")
            tab = tab[:-1]
            for j in range(0, nbrCycle):
                try:
                    add = Decimal(tab[j])
                    temp[j].append(add)
                except IndexError:
                    debug(path)
                    debug(j)

        for elt in temp:
            y.append(np.mean(elt))

        plt.plot(x, y, label=labelT[i])


        plt.ylabel(ylabel)
        plt.xlabel(xlabel)

    for i in range(0, len(listeC)):
        x = range(1,nbrCycle+1,1)
        temp = []
        for j in range(0,nbrCycle):
            tmp = []
            temp.append(tmp)
        y = []

        file = open(listeC[i])
        content = file.readlines()

        for line in content:
            tab = line.split(";")
            tab = tab[:-1]
            for j in range(0, nbrCycle):
                try:
                    add = Decimal(tab[j])
                    temp[j].append(add)
                except IndexError:
                    debug(path)
                    debug(j)

        for elt in temp:
            y.append(np.mean(elt))

        plt.plot(x, y, label=labelC[i])


        plt.ylabel(ylabel)
        plt.xlabel(xlabel)

    for i in range(0, len(listeM)):
        x = range(1,nbrCycle+1,1)
        temp = []
        for j in range(0,nbrCycle):
            tmp = []
            temp.append(tmp)
        y = []

        file = open(listeM[i])
        content = file.readlines()

        for line in content:
            tab = line.split(";")
            tab = tab[:-1]
            for j in range(0, nbrCycle):
                try:
                    add = Decimal(tab[j])
                    temp[j].append(add)
                except IndexError:
                    debug(path)
                    debug(j)

        for elt in temp:
            y.append(np.mean(elt))

        plt.plot(x, y, label=labelM[i])


        plt.ylabel(ylabel)
        plt.xlabel(xlabel)

    for i in range(0, len(listeCM)):
        x = range(1,nbrCycle+1,1)
        temp = []
        for j in range(0,nbrCycle):
            tmp = []
            temp.append(tmp)
        y = []

        file = open(listeCM[i])
        content = file.readlines()

        for line in content:
            tab = line.split(";")
            tab = tab[:-1]
            for j in range(0, nbrCycle):
                try:
                    add = Decimal(tab[j])
                    temp[j].append(add)
                except IndexError:
                    debug(path)
                    debug(j)

        for elt in temp:
            y.append(np.mean(elt))

        plt.plot(x, y, label=labelCM[i])


        plt.ylabel(ylabel)
        plt.xlabel(xlabel)

    for i in range(0, len(listecouple)):
        x = range(1,10000+1,1)
        temp = []
        for j in range(0,10000):
            tmp = []
            temp.append(tmp)
        y = []

        file = open(listecouple[i])
        content = file.readlines()

        for line in content:
            tab = line.split(";")
            tab = tab[:-1]
            for j in range(0, 10000):
                try:
                    add = Decimal(tab[j])
                    temp[j].append(add)
                except IndexError:
                    debug(path)
                    debug(j)

        for elt in temp:
            y.append(np.mean(elt))

        plt.plot(x, y, label=labelCp[i])


        plt.ylabel(ylabel)
        plt.xlabel(xlabel)

    plt.legend()
    plt.savefig("/home/etudiant/Images/graph/"+path+"All.png", dpi=750, bbox_inches='tight')
    #plt.show()
    plt.clf()