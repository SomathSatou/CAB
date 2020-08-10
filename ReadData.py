import getopt, sys
import numpy as np
import matplotlib.pyplot as plt
from output import *

try:
    opts, args = getopt.getopt(sys.argv[1:], "f:n:x:y:l:", ["file",
                                                            "nbrCycle",
                                                            "xlabel",
                                                            "ylabel",
                                                            "label"
                                                            ])
except getopt.GetoptError as err:
    # print help information and exit:
    help()
    debug(err)  # will print something like "option -a not recognized"
    sys.exit(2)

# default value for diplay parameters
output = None
verbose = False

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
    elif o == "-l":
        label = str(a)
    else:
        assert False, "unhandled option "+o

x = range(1,nbrCycle,1)
temp = [[]] * nbrCycle
y = []

file = open(path)
content = file.readlines()
for line in content:
    tab = line.split(";")
    for i in range(0, len(tab)-2):
        print(len(tab))
        print(len(temp))
        osef = temp[i]
        osef = tab[i]
        temp[i].append(tab[i])

for elt in temp:
    y.append(np.mean(elt))

    plt.plot(x, y, label=label)
    plt.ylabel("Valeur de la function d'évaluation")
    plt.xlabel("Nombre d'itération")

    plt.legend()
    plt.show()
    plt.clf()
