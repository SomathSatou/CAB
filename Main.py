from AEPermutation import AEPermutation
from Parser import Parser
from output import *
from Test import *

import getopt, sys
import numpy as np

def help():
    print("Memetic algorithm for Cyclic Antibandwith problem, made by Thomas Saout for stage of Master 2,\n"
          "supervised by Frederic Lardeux and Eduardo Rodriguez-Tello")
    print("argument list")
    print("\t-p , --p : Size of population")
    print("\t-m , --m : probability of mutation")
    print("\t-c , --c : probability of crossover")
    print("\t-i , --i : number of cycle in algorithm")
    print("\t-f , --f : path for the file contain graph data")
    print("\t-l , --l : list of operator format \"1,1,1,1,1\"\n"
          "\tmutator,select,crossover,insertion\n\n"
          "\t Mutation \n"
          "\t\t1: swap\n"
          "\t\t2: flip\n"
          "\t\t3: slide\n"
          "\t\t4: partialRandom\n"
          "\t\t5: bitSwap\n"
          "\t\t6: localSearchNaivePermutation\n"
          "\t\t7: mutatorUCB\n\n"
          "\t Selection \n"
          "\t\t1: twoBest\n"   
          "\t\t2: twoRandom\n"
          "\t\t3: twoBestIn5Random\n"
          "\t\t4: twoLowIn5Random\n"
          "\t\t5: wheel\n\n"
          "\t Crossover \n"
          "\t1: crossover\n"
          "\t2: Pmx\n"
          "\t3: edge\n"
          "\t4: cycle\n"
          "\t5: crossoverUCB\n\n"
          "\t Insertion \n"
          "\t1: bestoflower\n"
          "\t2: lessoflower\n"
          "\t3: elder\n"
          "\t4: worst\n"
          "\t5: best\n"
          "\t Fitness \n"
          "\t1 : CAB \n"
          "\t2 : function 1\n"
          "\t3 : function 2\n"
          "\t4 : function 3\n"
          )
    print("\t-d , --d : list of display 0 or 1, format \'1,1,1,1,1\"\n"
          "\tmean fitness, display cab graph, diplay fitness graph, "
          "diplay graph of opérator of mutation, same for crossover"
          )
    print("\t-t ,--test : for test function in algorithm, usage be detailled later when implementation is over")
    print("\nArgument not set take a default value, the example below show default value\n"
          "example : <Python interpretor> Main.py -p 100 -m 80 -c 50 -i 1000 -f \"Dataset/Instances/mesh2D5x25.rnd\" -l \"1,4,4,5,2\" -d  \"1,0,1,0,0\"\n")

#default parameters
P = 100 # taille de ma population
M = 80 # probabilité de mutation
C = 50 #probabilité de croissement
CMax = 100000 # nombre limite d'itérations pour l'algoritme
seedMax = 1

# display parameters
displayMoy = True
displayCab = True
displayFitness = True
displayMutator = False
displayCrossover = False
displayCouple = True

#big instance
#file = '../Dataset/Instances/hypercube11.rnd'
#test instance
path = '..'
file = path+'/Dataset/Instances/3dmesh_3.txt'
#path for cluster
#path = /home/tsaout/CAB
#file = path+'/Dataset/Instances/mesh2D5x25.rnd'

#[mutation, selection, crossover, reinsertion, fintness]
#test mimimize
#methodList = [[7, 4, 5, 5, 2]]
#test maximize
#methodList = [[7, 3, 5, 4, 3]]

#test couple
#test mimimize
#methodList = [[8, 4, 6, 5, 2]]
#test maximize
methodList = [[8, 3, 6, 4, 5]]
try:
    opts, args = getopt.getopt(sys.argv[1:], "hp:m:c:i:uf:l:d:s:vt:", ["help",
                                                           "population=",
                                                           "mutation=",
                                                           "crossover=",
                                                           "iteration="
                                                           "file=",
                                                           "methodList=",
                                                           "displayList=",
                                                           "seed=",
                                                           "verbose",
                                                           "test="
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
    if o == "-v":
        verbose = True
    elif o in ("-h", "--help"):
        help()
        sys.exit()
    elif o in ("-p", "--population"):
        P = int(a)
    elif o in ("-m", "--mutation"):
        M = int(a)
    elif o in ("-c", "--crossover"):
        C = int(a)
    elif o in ("-i", "--iteration"):
        CMax = int(a)
    elif o in ("-u", "--cluster"):
        path = '/home/tsaout/CAB'
        #path = '/home/ettignon/CAB'
    elif o in ("-f", "--file"):
        file = str(a)
    elif o in ("-l", "--methodList"):
        tmp = a.split(',')
        if len(tmp) != 5:
            help()
            debug("wrong number of method")
            sys.exit()
        newlist = []
        for elt in tmp:
            newlist.append(int(elt))
        methodList = []
        methodList.append(newlist)
        if methodList[len(methodList)-1] != 1:
            minimize = False
    elif o in ("-d", "--displayList"):
        tmp = a.split(',')
        if len(tmp) != 6:
            help()
            debug("wrong number of options for display")
            sys.exit()
        newlist = []
        for elt in tmp:
            newlist.append(bool(int(elt)))
        displayMoy = newlist[0]
        displayCab = newlist[1]
        displayFitness = newlist[2]
        displayMutator = newlist[3]
        displayCrosover = newlist[4]
        displayCouple = newlist[5]
    elif o in ("-s", "--seed"):
        seedMax = int(a)
    elif o in ("-v", "--verbose"):
        debug("verbose  not implemented yet")
    elif o in ("-t", "--test"):
        testFitness(int(a))
        #testCab()
        exit(0)
    else:
        assert False, "unhandled option "+o

#testFitness(3)
# function for load file
loader = Parser()
loader.load(file)

# default seed
Seed = 9000

#print('debut des test pour la seed ' + str(Seed))
np.random.seed(Seed+seedMax)

#testFitness(2)
# initialisation de la population
Run = AEPermutation(loader, P, M, C, CMax, path)

Run.launch(methodList, displayMoy, displayCab, displayFitness,
           displayMutator, displayCrossover, displayCouple)
