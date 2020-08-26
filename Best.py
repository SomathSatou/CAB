# lire de la ligne 6 a la ligne 34 le fichier best.txt
from output import *

import os
import getopt, sys
import numpy as np
from decimal import *

getcontext().prec = 40

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

f = open("best.txt")
contentBest = f.readlines()

Label = [
    ',twoBestIn5Random,crossover,swap,worst,CAB',
    ',twoLowIn5Random,crossover,swap,best,fitness1',
    ',twoBestIn5Random,crossover,swap,worst,fitness2',
    ',twoBestIn5Random,crossover,swap,worst,fitness3',
    ',twoBestIn5Random,crossover,swap,worst,fitness4',
    ',twoLowIn5Random,crossoverUCB,swap,best,fitness1',
    ',twoBestIn5Random,crossoverUCB,swap,worst,fitness2',
    ',twoBestIn5Random,crossoverUCB,swap,worst,fitness4',
    ',twoLowIn5Random,crossover,mutatorUCB,best,fitness1',
    ',twoBestIn5Random,crossover,mutatorUCB,worst,fitness2',
    ',twoBestIn5Random,crossover,mutatorUCB,worst,fitness4',
    ',twoLowIn5Random,crossoverUCB,mutatorUCB,best,fitness1',
    ',twoBestIn5Random,crossoverUCB,mutatorUCB,worst,fitness2',
    ',twoBestIn5Random,crossoverUCB,mutatorUCB,worst,fitness4',
    ',twoLowIn5Random,couple,nothing,best,fitness1',
    ',twoBestIn5Random,couple,nothing,worst,fitness2',
    ',twoBestIn5Random,couple,nothing,worst,fitness4'
]

for i in range(0,len(listname)):
    output = os.popen('find /media/etudiant/TOSHIBA\ EXT/thomas/ -name \"Best_'+listname[i]+'*\"').read()
    listFile = output.split('\n')
    best = 0
    label =",NOT FOUND"
    time = 0
    listFile = listFile[:-1]
    listLabl = []
    cycle = 0
    for path in listFile:
        print(path)
        with open(path) as o:
            content = o.readlines()
            for line in content:
                data = line.split(";")
                if int(data[0]) > best:
                    best = int(data[0])
                    cycle = int(data[1])
                    label = path.split(listname[i])[1]
                    timePath = "/media/etudiant/TOSHIBA EXT/thomas/time_"+listname[i]+label
                    timeFile = open(timePath)
                    contentTime = timeFile.readlines()
                    tmp = []
                    for elt in contentTime:
                        elt = elt.split(";")
                        if(elt[0] != ""):
                            deci = int(float(elt[0]))
                            tmp.append(deci)
                    time = np.mean(tmp)
                    label = label[:-4]
                    listLabl = []
                    listLabl.append(label)
                if int(data[0]) == best:
                    label = path.split(listname[i])[1]
                    label = label[:-4]
                    listLabl.append(label)



    dataline = contentBest[i+5].split("&")
    dataline[-1] = str(best) +"  & "
    for elt in Label:
        if elt in listLabl:
            dataline[-1] += "+ & "
        else:
            dataline[-1] += "- & "
    dataline[-1] += str(cycle) +" \\\ \hline"

    newline = ""
    for elt in dataline:
        newline += str(elt)+"&"
    contentBest[i+5] = newline[:-1]+"\n"

write = open("best.txt",'a')
for line in contentBest:
    write.write(line)