import heapq

import numpy as np
import matplotlib.pyplot as plt
from random import *
from output import *


def emptyset(ensemble):
    return len(ensemble) == 0

class AEPermutation:
    def __init__(self, data, pop, mut, rec, nbcMax):
        # region Parameters
        self.x = []
        self.y = []

        self.moyY = []
        self.worstY = []

        self.cab = []

        self.mutationType = 1
        self.mutSwitch = {
            1: self.swap,
            2: self.flip,
            3: self.slide,
            4: self.partialRandom
        }

        self.selectionType = 4
        self.selSwitch = {
            1: self.twoBest,
            2: self.twoRandom,
            3: self.twoBestIn5Random,
            4: self.wheel
        }

        self.recombinationType = 1
        self.recSwitch = {
            1: self.crossover,
            2: self.Pmx,
            3: self.edge,
            4: self.cycle
        }

        self.reinsertionType = 1
        self.reiSwitch = {
            1: self.bestoflower,
            2: self.lessoflower,
            3: self.elder
        }

        self.Size = data.Size
        self.SizePop = pop
        self.MutationProb = mut
        self.RecombinationProp = rec
        self.nbCycleMax = nbcMax

        self.Population = []
        self.nbCycle = 0

        self.parents = []
        self.Childrens = []

        for elt in range(0, self.SizePop):
            tmpIndividu = []
            for i in range(1, self.Size + 1):
                tmpIndividu.append(i)
            shuffle(tmpIndividu)
            self.Population.append(tmpIndividu)

        self.data = data.data
        self.edges = data.edges
        # endregion Parameters

    def launch(self, methodList, displayPlot, displayMoy, displayCab, displayFitness):

        # 4 tab to keep probability of operator
        DataOP = []
        self.nbCycle = 0

        for methodElt in methodList:
            self.nbCycle = 0

            self.mutationType = methodElt[0]
            self.selectionType = methodElt[1]
            self.recombinationType = methodElt[2]
            self.reinsertionType = methodElt[3]
            Label = ""

            select = self.selSwitch.get(self.selectionType, lambda: self.twoBest)
            Label += select.__name__ + ","

            recombine = self.recSwitch.get(self.recombinationType, lambda: self.crossover)
            Label += recombine.__name__ + ","

            mutation = self.mutSwitch.get(self.mutationType, lambda: self.swap)
            Label += mutation.__name__ + ","

            reinsertion = self.reiSwitch.get(self.reinsertionType, lambda: self.bestoflower)
            Label += reinsertion.__name__ + ","

            # as repenser avant
            # initialisation(Size, 100, 40, 100, nbCycleMax)

            self.evaluate()
            self.evaluateCab()
            while self.terminaison():
                # selection
                self.parents = select()

                # Recombine
                self.Childrens = recombine(self.parents)

                # mutation
                mutation()

                # evaluate children
                self.evaluatechildren()

                # Reinsertion
                reinsertion()

                # graph Value
                #self.evaluate()
                #self.evaluateCab()
                self.nbCycle = self.nbCycle + 1
                affichage = "nombre de tour effectuer : " + str(self.nbCycle) + "/" + str(self.nbCycleMax)
                print(affichage)
                #ajouter
                self.x.append(self.nbCycle)
                self.y.append(self.CurrentBest())
                self.moyY.append(np.mean(self.CurrentEval))
                self.cab.append(max(self.CurrentEvalCab))
            print(Label)

            fichier = open(Label + ".txt", "a")

            for elt in self.y:
                fichier.write(str(elt) + ";")

            fichier.write("\n")
            fichier.close()

            if displayFitness:
                plt.plot(self.x, self.y, label=Label)

            if displayMoy:
                tmp = "moy : " + Label
                plt.plot(self.x, self.moyY, label=tmp)

            if displayCab:
                tmp = "cab : " + Label
                plt.plot(self.x, self.cab, label=tmp)

            # if mutation == flipsAdaptatifPursuit:
            #    fichierOP = open(Label + "dataOPAPW.txt", "a")
                # dépendant de opérateur cible , mutation recombinaison, etc ...
            #    for iop in range(0, 2):
            #       for elt in DataOP:
            #            fichierOP.write(str(elt[iop]) + ";")
            #        fichierOP.write("\n")
            #    fichierOP.write("\n")
            #    fichierOP.close()
        if(displayPlot):
            plt.legend()
            plt.show()

    # region Selection
    def twoBest(self):
        ret = []
        best = heapq.nsmallest(2, self.CurrentEval)
        ret.append(self.Population[self.CurrentEval.index(best[0])].copy())
        ret.append(self.Population[self.CurrentEval.index(best[1])].copy())
        return ret

    def twoRandom(self):
        ret = []
        first = 0
        second = 0
        while 1:
            if first != second:
                break
            first = randint(0, self.SizePop - 1)
            second = randint(0, self.SizePop - 1)
        ret.append(self.Population[first].copy())
        ret.append(self.Population[second].copy())
        return ret

    def twoBestIn5Random(self):
        ret = []
        indexRand = []
        evalRand = []
        while len(indexRand) < 5:
            tmp = randint(0, self.SizePop - 1)
            if not indexRand.__contains__(tmp):
                indexRand.append(tmp)
                evalRand.append(self.CurrentEval[tmp])
        best = heapq.nsmallest(2, evalRand)
        ret.append(self.Population[indexRand[evalRand.index(best[0])]].copy())
        ret.append(self.Population[indexRand[evalRand.index(best[1])]].copy())
        return ret

    def wheel(self):
        ret = []
        wheel = []
        perCent = 0
        for child in range(0, len(self.Population)):
            perCent += (self.CurrentEval[child] / (sum(self.CurrentEval) + 1)) * 100
            wheel.append([child, perCent])
        while len(ret) < 2:
            prop = randint(0, 100)
            for elt in wheel:
                if elt[1] < prop:
                    ret.append(self.Population[elt[0]].copy())
                    break;
        return ret

    # endregion Selection

    # region Recombination

    def Pmx(self, parents):
        childs = [0] * self.Size
        if randint(0, 100) < self.RecombinationProp:
            pivot1 = randint(0, self.Size-1)
            pivot2 = randint(pivot1+1, self.Size)



            #k prends le segment du parents 1
            for i in range(pivot1,pivot2):
                childs[i] = parents[0][i]
            # ajouter les elemnents du parents 2 qui ne sont pas déjç présent
            for i in range(pivot1,pivot2):
                if not childs.__contains__(parents[1][i]) :
                    next = parents[0][i]
                    check = parents[1].index(next)

                    while not childs[check] ==0:
                        next = parents[0][check]
                        check = parents[1].index(next)
                    childs[check] = parents[1][i]

            #remplissage des blancs
            for i in range(0, self.Size):
                if childs[i] == 0:
                    childs[i] = parents[1][i]
        else:
            childs = parents[0]
        return childs

    def crossover(self, parents):
        childs = [0] * self.Size

        if randint(0, 100) < self.RecombinationProp:
            pivot1 = randint(0, self.Size - 1)
            pivot2 = randint(pivot1 + 1, self.Size)

            # k prends le segment du parents 1
            for i in range(pivot1, pivot2):
                childs[i] = parents[0][i]

            ajout = []
            for i in range(pivot1, pivot2):
                if not childs.__contains__(parents[1][i]):
                    ajout.append(i)
            for i in range(0, self.Size):
                if childs[i] == 0:
                    if childs.__contains__(parents[1][i]):
                        childs[i] = parents[1][ajout.pop()]
                    else:
                        childs[i] = parents[1][i]
        else:
            childs = parents[0]
        return childs

    # a tester
    # non fonctionnel problème avec les ensembles
    def edge(self,parents):
        childs = [0] * self.Size

        if randint(0, 100) < self.RecombinationProp:

            #création des voisin de chaque sommets

            voisin = [set() for i in range(0, self.Size)]

            for i in range(0, self.Size):
                for j in range(0, 2):
                    if parents[j].index(i + 1) == 0:
                        voisin[i].add(parents[j][self.Size - 1])
                    else:
                        voisin[i].add(parents[j][parents[j].index(i + 1) - 1])
                    if parents[j].index(i + 1) == self.Size - 1:
                        voisin[i].add(parents[j][0])
                    else:
                        print(parents[j].index(i + 1))
                        voisin[i].add(parents[j][parents[j].index(i + 1) + 1])

            # on séléctionne le premiè element de notre progéniture
            first = randint(0,1)
            x = parents[first][0]

            # on le retire de notre voisinage
            for set in voisin:
                set.discard(x)

            # choix du prochain sommets de notre progéniture
            for i in range(0, self.Size):
                childs[i] = x
                if emptyset(voisin[x]) :
                    tirage = randint(1,self.Size)
                    while childs.__contains__(tirage):
                        tirage = randint(1, self.Size)
                    x = tirage
                else:
                    longueur = self.Size
                    for elt in range(0, len(voisin[x])):
                        if len(voisin[elt]) < longueur:
                            longueur = len(voisin[elt])
                            x = elt

            del voisin
        else:
            childs = parents[0]
        return childs

    def cycle(self,parents):
        childs = [0] * self.Size
        if randint(0, 100) < self.RecombinationProp:
            print('encore du travail')

        return childs

    # endregion Recombination

    # region Mutation

    def slide(self, parents):
        childs = [[0] * self.Size, [0] * self.Size]

        return childs

    def partialRandom(self, parents):
        childs = [[0] * self.Size, [0] * self.Size]

        return childs

    def swap(self):
        if randint(0, 100) <= self.MutationProb:
            A = randint(0, len(self.Childrens) - 2)
            B = randint(A + 1, len(self.Childrens) - 1)
            tmp = self.Childrens[A]
            self.Childrens[A] = self.Childrens[B]
            self.Childrens[B] = tmp
        return

    def reinsert(self):
        childs = self.Childrens
        for child in childs:
            print(child)
            if randint(0, 100) <= self.MutationProb:
                A = randint(0, len(childs[0]) - 2)
                B = randint(A + 1, len(childs[0]) - 1)
                tmp = child[B]
                child.remove(B)
                child.insert(tmp, A + 1)
        return

    def flip(self):
        childs = self.Childrens
        if randint(0, 100) <= self.MutationProb:
            A = randint(0, len(childs[0]) - 2)
            B = randint(A + 1, len(childs[0]) - 1)
            for child in childs:
                for i in range(A, B - ((B - A) / 2) - 1):
                    tmp = child[i]
                    child[i] = child[B - (i - A)]
                    child[B - (i - A)] = tmp
                if B - A % 2 != 0:
                    tmp = child[B - ((B - A) / 2)]
                    child[B - ((B - A) / 2)] = child[B - (i - A)]
                    child[B - (i - A)] = tmp
        return

    # endregion Mutation

    # region Insertion

    # essayer d'utiliser min plutot que de parcourir pour tenter de gagner du tempt, regarder pour utiliser la recherche dicotomique
    def bestoflower(self):
        best = self.ChildrenEval
        for j in range(0, self.SizePop - 1):
            if self.CurrentEval[j] < best:
                self.CurrentEval[j] = best
                self.CurrentEvalCab[j] = self.CAB(self.Childrens)
                self.Population[j] = self.Childrens.copy()
                self.Childrens = []
                return
        return

    def lessoflower(self):
        best = self.ChildrenEval
        for j in range(0, self.SizePop - 1):
            if self.CurrentEval[j] > best:
                self.CurrentEval[j] = best
                self.CurrentEvalCab[j] = self.CAB(self.Childrens)
                self.Population[j] = self.Childrens.copy()
                self.Childrens = []
                return
        return

    def elder(self):
        best = self.ChildrenEval
        self.CurrentEvalCab.append(self.CAB(self.Childrens))
        self.CurrentEvalCab.pop(0)
        self.CurrentEval.append(best)
        self.CurrentEval.pop(0)
        self.Population.append(self.Childrens.copy())
        self.Population.pop(0)
        return

    # endregion Insertion

    # region function of algo
    def evaluate(self):
        self.CurrentEval = []
        for elt in self.Population:
            #self.CurrentEval.append(self.fitness(elt))
            self.CurrentEval.append(self.CAB(elt))

        #print(self.CurrentEval)
        return

    def evaluateCab(self):
        self.CurrentEvalCab = []
        for elt in self.Population:
            self.CurrentEvalCab.append(self.CAB(elt))

        #print(self.CurrentEvalCab)
        return

'''
    def objectif(self, elt):
        global Size
        if self.fitness(elt) == 0:
            return True
        return False
'''

    def fitness(self, elt):
        return self.fitness1(elt)

    def CAB(self,elt):
        cab = self.Size
        for i in range(0,len(self.data)):
            for j in self.data[i]:
                if (i+1) < j:
                    absDiff = abs((elt.index(i+1)+1) - (elt.index(j)+1))
                    cyclicdiff = min(absDiff, self.Size - absDiff)
                    if cyclicdiff < cab :
                        cab = cyclicdiff
        return cab

    def fillD(self, elt):
        ret = []
        for i in range(0, (self.Size//2)-1):
            tmp = 0
            for j in range(0, len(self.data)):
                for k in range(0, len(self.data[j])):
                    if abs(elt[j]-elt[k]) == i:
                        tmp = tmp +1
            ret.append(tmp//2)
        return ret

    def maxDelta(self):
        max = 0
        for elt in self.data:
            if len(elt) > max:
                max = len(elt)
        return max

    def fitness1(self, elt):
        delta = self.maxDelta()
        d = self.fillD(elt)
        ret = 0
        for i in range(1, self.Size//2):

            ret = ret + (delta * ((self.Size//2) - i + 1) * d[i-1])
        return ret

    def terminaison(self):
        if self.nbCycle >= self.nbCycleMax:
            return False
        return True

    def evaluatechildren(self):
        #self.ChildrenEval = self.fitness(self.Childrens)
        self.ChildrenEval = self.CAB(self.Childrens)
        return

    def CurrentBest(self):
        return max(self.CurrentEval)

    def CurrentLow(self):
        return min(self.CurrentEval)

    # endregion function of algo
