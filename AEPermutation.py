import heapq

import numpy as np
import matplotlib.pyplot as plt
from random import *

# region Selection
def twoBest():
    global CurrentEval, Population
    ret = []
    best = heapq.nsmallest(2, CurrentEval)
    ret.append(Population[CurrentEval.index(best[0])].copy())
    ret.append(Population[CurrentEval.index(best[1])].copy())
    return ret


def twoRandom():
    global Population, SizePop
    ret = []
    first = 0
    second = 0
    while 1:
        if first != second:
            break
        first = randint(0, SizePop-1)
        second = randint(0, SizePop-1)
    ret.append(Population[first].copy())
    ret.append(Population[second].copy())
    return ret


def twoBestIn5Random():
    global Population, SizePop, CurrentEval
    ret = []
    indexRand = []
    evalRand = []
    while len(indexRand) < 5:
        tmp = randint(0, SizePop - 1)
        if not indexRand.__contains__(tmp):
            indexRand.append(tmp)
            evalRand.append(CurrentEval[tmp])
    best = heapq.nsmallest(2, evalRand)
    ret.append(Population[indexRand[evalRand.index(best[0])]].copy())
    ret.append(Population[indexRand[evalRand.index(best[1])]].copy())
    return ret


def wheel():
    global Population, SizePop, CurrentEval, Size
    ret = []
    wheel = []
    perCent = 0
    for child in range(0, len(Population)):
        perCent += (CurrentEval[child]/(sum(CurrentEval)+1))*100
        wheel.append([child, perCent])
    while len(ret) < 2:
        prop = randint(0, 100)
        for elt in wheel:
            if elt[1] < prop:
                ret.append(Population[elt[0]].copy())
                break;
    return ret


# endregion Selection

# region Recombination
def Pmx(parents):
    global Size
    childs = parents.copy()
    indexRand = []
    if randint(0,100) < RecombinationProp:
        while len(indexRand) < 3:
            tmp = randint(0, Size - 1)
            if not indexRand.__contains__(tmp):
                indexRand.append(tmp)
        childs[0] = [0]*Size
        for elt in indexRand:
            childs[0][elt] = Parents[0][elt]
            childs[1][elt] = Parents[1][elt]
        index = 0
        print(childs[0])
        for i in range (0, indexRand[0]-1):
            while childs[0][i] == 0:
                if not childs.__contains__(parents[1][index]):
                    childs[0][i] = parents[1][index]
                    childs[1][i] = parents[0][index]
                index += 1
        print(childs[0])
        for i in range (indexRand[0]+1, indexRand[1]-1):
            while childs[0][i] == 0:
                if not childs.__contains__(parents[1][index]):
                    childs[0][i] = parents[1][index]
                    childs[1][i] = parents[0][index]
                index += 1
        print(childs[0])
        for i in range (indexRand[1]+1, indexRand[2]-1):
            while childs[0][i] == 0:
                if not childs.__contains__(parents[1][index]):
                    childs[0][i] = parents[1][index]
                    childs[1][i] = parents[0][index]
                index += 1
        print(childs[0])
        for i in range (indexRand[2]+1, len(childs[0])-1):
            while childs[0][i] == 0 and index == len(parents[1]):
                if not childs.__contains__(parents[1][index]):
                    childs[0][i] = parents[1][index]
                    childs[1][i] = parents[0][index]
                index += 1
        print(childs[0])
        print("rcombinaitionDone")
    return childs


def crossover(parents):
    global Size

    # initialization
    childs = [[0] * Size, [0] * Size]
    indexRand = []
    if randint(0, 100) < RecombinationProp:
        while len(indexRand) < 2:
            tmp = randint(0, Size - 1)
            if not indexRand.__contains__(tmp):
                indexRand.append(tmp)
        indexRand.sort()


        # preservate part
        for i in range(indexRand[0], indexRand[1] + 1):
            childs[0][i] = Parents[0][i]
            childs[1][i] = Parents[1][i]


        # keep the order in way of crossover recombination child 0 to child 1 to se preservate part
        index = 0
        for index in range(0, Size):
            if not childs[0].__contains__(Parents[1][index]):
                childs[0][childs[0].index(0)] = Parents[1][index]
            if not childs[1].__contains__(Parents[0][index]):
                childs[1][childs[1].index(0)] = Parents[0][index]


    else:
        childs = Parents.copy()


    return childs


# endregion Recombination

# region Mutation
def swap():
    global Childrens
    childs = Childrens
    for child in childs:
        if randint(0, 100) <= MutationProb:
            A = randint(0, len(child)-2)
            B = randint(A+1, len(child)-1)
            tmp = child[A]
            child[A] = child[B]
            child[B] = tmp
    return


def reinsert():
    global Childrens
    childs = Childrens
    for child in childs:
        print(child)
        if randint(0, 100) <= MutationProb:
            A = randint(0, len(childs[0]) - 2)
            B = randint(A + 1, len(childs[0]) - 1)
            tmp = child[B]
            child.remove(B)
            child.insert(tmp, A+1)
    return


def flip():
    global Childrens
    childs = Childrens
    if randint(0, 100) <= MutationProb:
        A = randint(0, len(childs[0])-2)
        B = randint(A+1, len(childs[0])-1)
        for child in childs:
            for i in range(A, B-((B-A)/2)-1):
                tmp = child[i]
                child[i] = child[B-(i-A)]
                child[B-(i-A)] = tmp
            if B-A % 2 != 0:
                tmp = child[B-((B - A) / 2)]
                child[B - ((B - A) / 2)] = child[B-(i-A)]
                child[B-(i-A)] = tmp
    return


# endregion Mutation

# region Insertion
def bestoflower():
    global Childrens, ChildrenEval, Population, CurrentEval
    best = ChildrenEval.index(max(ChildrenEval))
    for j in range(0, SizePop-1):
        if CurrentEval[j] < ChildrenEval[best]:
            CurrentEval[j] = ChildrenEval[best]
            Population[j] = Childrens[best].copy()
            ChildrenEval = []
            Childrens = []
            return
    return

def lessoflower():
    global Childrens, ChildrenEval, Population, CurrentEval
    best = ChildrenEval.index(max(ChildrenEval))
    for j in range(0, SizePop-1):
        if CurrentEval[j] > ChildrenEval[best]:
            CurrentEval[j] = ChildrenEval[best]
            Population[j] = Childrens[best].copy()
            ChildrenEval = []
            Childrens = []
            return
    return


def elder():
    global Childrens, ChildrenEval, Population, CurrentEval
    best = ChildrenEval.index(max(ChildrenEval))
    Population.append(Childrens[best].copy())
    Population.pop(0)
    return


# endregion Insertion

# region function of algo
def evaluate():
    global Population, CurrentEval
    CurrentEval = []
    for elt in Population:
        CurrentEval.append(fitness(elt))
    return


def objectif(elt):
    global Size
    if fitness(elt) == 0:
        return True
    return False


def fitness(elt):
    ret = 0
    for i in range(0, Size-2):
        for j in range(0, Size-1):
            if i < j :
                dif = elt[i] - elt[j]
                if dif == 0:
                    ret += 1
                if dif == i-j:
                    ret += 1
                if dif == j-i:
                    ret +=1
    return ret


def terminaison():
    global nbCycleMax
    if nbCycle >= nbCycleMax:
        return False
    return True


def evaluatechildren():
    global Childrens, ChildrenEval
    ChildrenEval = []
    for elt in Childrens:
        ChildrenEval.append(fitness(elt))
    return


def CurrentBest():
    return max(CurrentEval)


def CurrentLow():
    return min(CurrentEval)


# endregion function of algo

# region Parameters
x = []
y = []

moyY = []
worstY = []

mutationType = 1
mutSwitch = {
    1: swap,
    2: reinsert,
    3: flip
}

selectionType = 4
selSwitch = {
    1: twoBest,
    2: twoRandom,
    3: twoBestIn5Random,
    4: wheel
}

recombinationType = 1
recSwitch = {
    1: Pmx,
    2: crossover
}

reinsertionType = 1
reiSwitch = {
    1: lessoflower,
    2: elder
}



def initialisation(taille, pop, mut, rec, nbcMax):
    global Size, SizePop, MutationProb, RecombinationProp, nbCycleMax, x, y, Population, nbCycle, moyY, worstY
    x = []
    y = []
    moyY = []
    worstY = []
    Size = taille
    SizePop = pop
    MutationProb = mut
    RecombinationProp = rec
    nbCycleMax = nbcMax
    Population = []
    nbCycle = 0
    for osef in range (0, SizePop):
        tmpIndividu = []
        for i in range(1, Size+1):
            tmpIndividu.append(i)
        shuffle(tmpIndividu)
        Population.append(tmpIndividu)
    return


# endregion Parameters

# region Main
moy = "moy"
worst = "worst"
indexMethod = 0

methodList = [[1, 3, 2, 1]]
for methodElt in methodList:
    indexMethod += 1
    mutationType = methodElt[0]
    selectionType = methodElt[1]

    recombinationType = methodElt[2]
    reinsertionType = methodElt[3]
    Label = ""

    select = selSwitch.get(selectionType, lambda: twoBest)
    Label += select.__name__ + ", "

    recombine = recSwitch.get(recombinationType, lambda: Pmx)
    Label += recombine.__name__ + ", "

    mutation = mutSwitch.get(mutationType, lambda: swap)
    Label += mutation.__name__ + ", "

    reinsertion = reiSwitch.get(reinsertionType, lambda: bestoflower())
    Label += reinsertion.__name__ + ", "

    # initialisation(taille, pop, mut, rec, nbcMax)
    initialisation(48, 200, 40, 100, 8000)
    evaluate()
    while terminaison():
        #selection

        Parents = select()

        #Recombine

        Childrens = recombine(Parents)

        #mutation

        mutation()

        #evaluate children
        evaluatechildren()

        #Reinsertion

        reinsertion()

        #graph Value
        evaluate()
        nbCycle = nbCycle +1
        affichage = "nombre de tour effectuer : "+str(nbCycle)+"/"+str(nbCycleMax)
        print(affichage)
        x.append(nbCycle)
        y.append(CurrentBest())
        moyY.append(np.mean(CurrentEval))
        worstY.append(CurrentLow())
    moy = "moy"+str(indexMethod)
    worst = "worst" + str(indexMethod)
    plt.plot(x, y, label=Label)
    plt.plot(x, moyY, label=moy)
    plt.plot(x, worstY, label=worst)


    # Affichage de debug
    #print(Population)
    #print("method")
plt.legend()
plt.show()
# endregion Main
