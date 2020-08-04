# lire de la ligne 6 a la ligne 34 le fichier best.txt
from output import *

import os
import getopt, sys

listname = ["cycle_50",
            "cycle_200",
            "toroidalmesh_4",
            "toroidalmesh_15",
            "hamming4x4x5",
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
            "bcsstk01.mtx",
            "ash85.mtx",
            "662_bus.mtx",
            "caterpillar_5_4",
            "caterpillar_10_6",
            "random-graph-250-01",
            "random-graph-750-05",
            "dwt_503.mtx",
            "jgl009.mtx",
            "p1_100_200",
            "p21_200_400"
            ]

f = open("best.txt")
contentBest = f.readlines()

for i in range(0,len(listname)):
    output = os.system('find output/ -name \"Best_'+lisname[i]+'*\"')
    listFile = output.readlines()
    best = 0
    for path in listFile:
        with open(path) as o:
            content = o.readlines()
            for line in content:
                data = line.split(";")
                if int(data[0]) > best:
                    best = int(data[0])

    dataline = contentBest[i+6].split("&")
    dataline[-1] = str(best) +"                                        \\ \hline"

    newline = ""
    for elt in dataline:
        newline += str(elt)+"&"
    contentBest[i+6] = newline[:-1]+"\n"

for line in contentBest:
    f.write(line)