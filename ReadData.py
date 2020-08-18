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

x = range(1,nbrCycle+1,1)
temp = []
for i in range(0,nbrCycle):
    tmp = []
    temp.append(tmp)
y = []

file = open(path)
content = file.readlines()

for line in content:
    tab = line.split(";")
    tab = tab[:-1]
    for i in range(0, nbrCycle):
        add = Decimal(tab[i])
        temp[i].append(add)

for elt in temp:
    y.append(np.mean(elt))

plt.plot(x, y, label=label)

if moy:
    temp = []
    for i in range(0, nbrCycle):
        tmp = []
        temp.append(tmp)
    y = []

    file = open(chem)
    content = file.readlines()

    for line in content:
        tab = line.split(";")
        tab = tab[:-1]
        for i in range(0, nbrCycle):
            add = Decimal(tab[i])
            temp[i].append(add)

    for elt in temp:
        y.append(np.mean(elt))

    plt.plot(x, y, label="mean")


plt.ylabel(ylabel)
plt.xlabel(xlabel)

plt.legend()
plt.savefig(save, dpi=750, bbox_inches='tight')
plt.clf()
