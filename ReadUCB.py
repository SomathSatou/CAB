import getopt, sys
import numpy as np
import matplotlib.pyplot as plt
from output import *
from decimal import *
import itertools

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
save = "error.png"

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
        if str(a) in ("mu", "mutator"):
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
try:
    x = range(1, nbrCycle + 1, 1)
    temp = []
    for i in range(0, nbrCycle):
        tmp = []
        temp.append(tmp)
    y = []
    for i in range(0, nbrOP):
        tmp = []
        y.append(tmp)

    content = [elem for elem in content if elem != "\n"]

    data = []
    for i in range(0, nbrOP):
        tmp = []
        data.append(tmp)

    for i in range(0, len(content) - 1, 2):
        line1 = content[i].split(";")
        line2 = content[i+1].split(";")
        for j in range(0, nbrOP):
            try:
                data[j].append([float(a) / ((float(b)+1)/c) for a, b, c in zip(eval(line1[j]), eval(line2[j]), x)])
            except SyntaxError:
                j = len(content)-1
            except IndexError:
                j = len(content)-1

    for i in range(0, nbrOP):
        temp = data[i]
        y[i] = [float(sum(col))/50 for col in itertools.zip_longest(*iter(temp))]
        plt.plot(x, y[i], label=listLabel[i])

    plt.ylabel(ylabel)
    plt.xlabel(xlabel)

    plt.legend(loc='upper right')
    #plt.show()
    plt.savefig(save, dpi=750, bbox_inches='tight')
    comment(save)
    plt.clf()
except ValueError:
    debug(path)
    debug(nbrCycle)
    debug(nbrOP)
    debug(i)



#select = typeSwitch.get(nbrOP, lambda: Crossover)
#select(content)

