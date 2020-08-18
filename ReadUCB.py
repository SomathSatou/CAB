import getopt, sys
import numpy as np
import matplotlib.pyplot as plt
from output import *
from decimal import *

def Crossover(content):
    global nbrOP, listLabel

    x = range(1, nbrCycle + 1, 1)
    temp = []
    for i in range(0, nbrCycle):
        tmp = []
        temp.append(tmp)
    y = []
    for i in range(0,nbrOP-1):
        tmp = []
        y.append(tmp)

    content = [elem for elem in content if elem != ""]

    for i in range(0, len(content) - 1):
        tab = np.load(content[i])
        for i in range(0, nbrCycle):
            add = Decimal(tab[i])
            temp[i].append(add)

        for elt in temp:
            y[i % nbrOP].append(np.mean(elt))

    for i in range(0, nbrOP - 1):
        plt.plot(x, y[i], label=listLabel)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)

    plt.legend()
    plt.show()
    #plt.savefig(save, dpi=750, bbox_inches='tight')
    plt.clf()

    return

def Muatotor():
    return

def Couple():
    return

try:
    opts, args = getopt.getopt(sys.argv[1:], "f:n:x:y:l:s:t:", ["file",
                                                            "nbrCycle",
                                                            "xlabel",
                                                            "ylabel",
                                                            "label",
                                                            "mean",
                                                            "saveFile",
                                                            "type"
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
listLabel = []

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
    elif o in ("-s", "--saveFile"):
        save = str(a)
    elif o in ("-t", "--type"):
        if str(a) in ("m", "mutator"):
            listLabel = ["swap", "flip", "slide", "partialRandom", "bitSwap", "localSearchNaivePermutation"]
        elif str(a) in ("cr", "crossover"):
            listLabel = ["crossover", "Pmx", "edge", "cycle"]
        elif str(a) in ("cp", "couple"):
            listLabel = ["swap,crossover", "flip,crossover", "slide,crossover", "partialRandom,crossover", "bitSwap,crossover", "localSearchNaivePermutation,crossover",
                         "swap,Pmx", "flip,Pmx", "slide,Pmx", "partialRandom,Pmx", "bitSwap,Pmx", "localSearchNaivePermutation,Pmx",
                         "swap,edge", "flip,edge", "slide,edge", "partialRandom,edge", "bitSwap,edge", "localSearchNaivePermutation,edge",
                         "swap,cycle", "flip,cycle", "slide,cycle", "partialRandom,cycle", "bitSwap,cycle", "localSearchNaivePermutation,cycle"]
    else:
        assert False, "unhandled option "+o

nbrOP = len(listLabel)


file = open(path)
content = file.readlines()

#typeSwitch = {
#    4 : Crossover,
#    6 : Mutator,
#    24 : Couple,
#}

x = range(1, nbrCycle + 1, 1)
temp = []
for i in range(0, nbrCycle):
    tmp = []
    temp.append(tmp)
y = []
for i in range(0, nbrOP - 1):
    tmp = []
    y.append(tmp)

content = [elem for elem in content if elem != "\n"]

for i in range(0, len(content) - 1):
    line = content[i].plit(";")
    for i in range(0, nbrCycle):
        add = Decimal(tab[i])
        temp[i].append(add)

    for elt in temp:
        y[i % nbrOP].append(np.mean(elt))

for i in range(0, nbrOP - 1):
    plt.plot(x, y[i], label=listLabel)
plt.ylabel(ylabel)
plt.xlabel(xlabel)

plt.legend()
plt.show()
# plt.savefig(save, dpi=750, bbox_inches='tight')
plt.clf()

#select = typeSwitch.get(nbrOP, lambda: Crossover)
#select(content)

