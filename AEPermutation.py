import heapq

import numpy as np
import matplotlib.pyplot as plt
from random import *


class AEPermutation:
    def __init__(self, taille, pop, mut, rec, nbcMax):
        # region Parameters
        self.x = []
        self.y = []

        self.moyY = []
        self.worstY = []

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
            1: self.lessoflower,
            2: self.elder
        }

        self.Size = taille
        self.SizePop = pop
        self.MutationProb = mut
        self.RecombinationProp = rec
        self.nbCycleMax = nbcMax

        self.Population = []
        self.nbCycle = 0

        for elt in range(0, self.SizePop):
            tmpIndividu = []
            for i in range(1, self.Size + 1):
                tmpIndividu.append(i)
            shuffle(tmpIndividu)
            self.Population.append(tmpIndividu)

        # endregion Parameters

    def launch(self, methodList, displayMoy):

        # 4 tab to keep probability of operator
        DataOP = []
        nbCycle = 0

        for methodElt in methodList:

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
                self.evaluate()
                nbCycle = nbCycle + 1
                affichage = "nombre de tour effectuer : " + str(nbCycle) + "/" + str(self.nbCycleMax)
                # print(affichage)
                self.x.append(nbCycle)
                self.y.append(self.CurrentBest())
                self.moyY.append(np.mean(self.CurrentEval))
            print(Label)
            #   plt.plot(x, y, label=Label)

            fichier = open(Label + ".txt", "a")

            for elt in y:
                fichier.write(str(elt) + ";")

            fichier.write("\n")
            fichier.close()

            if displayMoy:
                Label = "moy : " + Label
                plt.plot(self.x, self.moyY, label=Label)

            if mutation == self.flipsAdaptatifPursuit:
                fichierOP = open(Label + "dataOPAPW.txt", "a")
                # dépendant de opérateur cible , mutation recombinaison, etc ...
                for iop in range(0, 2):
                    for elt in DataOP:
                        fichierOP.write(str(elt[iop]) + ";")
                    fichierOP.write("\n")
                fichierOP.write("\n")
                fichierOP.close()
        # plt.legend()
        # plt.show()

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
    def Pmx_nreine(self, parents):
        childs = self.parents.copy()
        indexRand = []
        if randint(0, 100) < self.RecombinationProp:
            while len(indexRand) < 3:
                tmp = randint(0, self.Size - 1)
                if not indexRand.__contains__(tmp):
                    indexRand.append(tmp)
            childs[0] = [0] * self.Size
            for elt in indexRand:
                childs[0][elt] = parents[0][elt]
                childs[1][elt] = parents[1][elt]
            index = 0
            print(childs[0])
            for i in range(0, indexRand[0] - 1):
                while childs[0][i] == 0:
                    if not childs.__contains__(parents[1][index]):
                        childs[0][i] = parents[1][index]
                        childs[1][i] = parents[0][index]
                    index += 1
            print(childs[0])
            for i in range(indexRand[0] + 1, indexRand[1] - 1):
                while childs[0][i] == 0:
                    if not childs.__contains__(parents[1][index]):
                        childs[0][i] = parents[1][index]
                        childs[1][i] = parents[0][index]
                    index += 1
            print(childs[0])
            for i in range(indexRand[1] + 1, indexRand[2] - 1):
                while childs[0][i] == 0:
                    if not childs.__contains__(parents[1][index]):
                        childs[0][i] = parents[1][index]
                        childs[1][i] = parents[0][index]
                    index += 1
            print(childs[0])
            for i in range(indexRand[2] + 1, len(childs[0]) - 1):
                while childs[0][i] == 0 and index == len(parents[1]):
                    if not childs.__contains__(parents[1][index]):
                        childs[0][i] = parents[1][index]
                        childs[1][i] = parents[0][index]
                    index += 1
            print(childs[0])
            print("rcombinaitionDone")
        return childs

    def Pmx(self, parents):
        childs = [[0] * self.Size, [0] * self.Size]
        if randint(0, 100) < self.RecombinationProp:
            pivot1 = randint(0, self.Size-1)
            pivot2 = randint(pivot1+1, self.Size)



            #k prends le segment du parents 1
            for i in range(pivot1,pivot2):
                childs[0][i] = parents[0][i]

            # ajouter les elemnents du parents 2 qui ne sont pas déjç présent
            for i in range(pivot1,pivot2):
                if not childs[0].__contains__(parents[1][i]) :
                    next = parents[0][i]
                    check = parents[1].index(next)

                    while childs[0].__contains__(check):
                        next = parents[0][check]
                        check = parents[1].index(next)

                    childs[0][check] = parents[0][i]

            #remplissage des blancs 
            for i in range(0, self.Size):
                if childs[0][i] == 0:
                    childs[0][i] = parents[1][i]

        return childs

    def crossover_nreine(self, parents):

        # initialization
        childs = [[0] * self.Size, [0] * self.Size]
        indexRand = []
        if randint(0, 100) < self.RecombinationProp:
            while len(indexRand) < 2:
                tmp = randint(0, self.Size - 1)
                if not indexRand.__contains__(tmp):
                    indexRand.append(tmp)
            indexRand.sort()

            # preservate part
            for i in range(indexRand[0], indexRand[1] + 1):
                childs[0][i] = parents[0][i]
                childs[1][i] = parents[1][i]

            # keep the order in way of crossover recombination child 0 to child 1 to se preservate part
            index = 0
            for index in range(0, self.Size):
                if not childs[0].__contains__(parents[1][index]):
                    childs[0][childs[0].index(0)] = parents[1][index]
                if not childs[1].__contains__(parents[0][index]):
                    childs[1][childs[1].index(0)] = parents[0][index]

        else:
            childs = parents.copy()

        return childs

    def crossover(self,parents):
        if randint(0, 100) < self.RecombinationProp:
            pivot1 = randint(0, self.Size - 1)
            pivot2 = randint(pivot1 + 1, self.Size)

            childs = [[0] * self.Size, [0] * self.Size]

            # k prends le segment du parents 1
            for i in range(pivot1, pivot2):
                childs[0][i] = parents[0][i]

            ajout = []
            for i in range(0, self.Size):
                if not childs[0].__contains__(parents[1][i]):
                    ajout.append(i)

            for i in range(self.Size, 0):
                if childs[0][i] == 0:
                    childs[0][i] = parents[1][ajout.pop()]

        return childs

    def slide(self, parents):
        childs = [[0] * self.Size, [0] * self.Size]

        return childs

    def partialRandom(self, parents):
        childs = [[0] * self.Size, [0] * self.Size]

        return childs
    # endregion Recombination

    # region Mutation
    def swap(self):
        childs = self.Childrens
        for child in childs:
            if randint(0, 100) <= self.MutationProb:
                A = randint(0, len(child) - 2)
                B = randint(A + 1, len(child) - 1)
                tmp = child[A]
                child[A] = child[B]
                child[B] = tmp
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

    def edge(self):
        return

    def cycle(self):
        return

    # endregion Mutation

    # region Insertion
    def bestoflower(self):
        best = self.ChildrenEval.index(max(self.ChildrenEval))
        for j in range(0, self.SizePop - 1):
            if self.CurrentEval[j] < self.ChildrenEval[best]:
                self.CurrentEval[j] = self.ChildrenEval[best]
                self.Population[j] = self.Childrens[best].copy()
                self.ChildrenEval = []
                self.Childrens = []
                return
        return

    def lessoflower(self):
        best = self.ChildrenEval.index(max(self.ChildrenEval))
        for j in range(0, self.SizePop - 1):
            if self.CurrentEval[j] > self.ChildrenEval[best]:
                self.CurrentEval[j] = self.ChildrenEval[best]
                self.Population[j] = self.Childrens[best].copy()
                self.ChildrenEval = []
                self.Childrens = []
                return
        return

    def elder(self):
        best = self.ChildrenEval.index(max(self.ChildrenEval))
        self.Population.append(self.Childrens[best].copy())
        self.Population.pop(0)
        return

    # endregion Insertion

    # region function of algo
    def evaluate(self):
        self.CurrentEval = []
        for elt in self.Population:
            self.CurrentEval.append(self.fitness(elt))
        return

    def objectif(self, elt):
        global Size
        if self.fitness(elt) == 0:
            return True
        return False

    def fitness(self, elt):
        ret = 0
        for i in range(0, self.Size - 2):
            for j in range(0, self.Size - 1):
                if i < j:
                    dif = elt[i] - elt[j]
                    if dif == 0:
                        ret += 1
                    if dif == i - j:
                        ret += 1
                    if dif == j - i:
                        ret += 1
        return ret

    def terminaison(self):
        if self.nbCycle >= self.nbCycleMax:
            return False
        return True

    def evaluatechildren(self):
        self.ChildrenEval = []
        for elt in self.Childrens:
            self.ChildrenEval.append(self.fitness(elt))
        return

    def CurrentBest(self):
        return max(self.CurrentEval)

    def CurrentLow(self):
        return min(self.CurrentEval)

    # endregion function of algo
