import math
from random import *
from decimal import *

import matplotlib.pyplot as plt
import numpy as np
import time

from output import *

# function for test if a set is empty
def emptyset(ensemble):
    return len(ensemble) == 0

class UCB:
    # class for Method who use UCB method and for display state and value of opérator
    def __init__(self, NbrOP):
        self.NbrOP = NbrOP
        self.sums_of_reward = [0] * self.NbrOP
        self.normalize_reward = [0] * self.NbrOP
        self.numbers_of_mutation = [0] * self.NbrOP
        self.output = []
        for i in range(0, self.NbrOP):
            tmp = []
            self.output.append(tmp)

        self.utilisation = []
        for i in range(0, self.NbrOP):
            tmp = []
            self.utilisation.append(tmp)

class Individu:
    # class for each solution in Population
    def __init__(self, size):
        self.label = []
        for i in range(1, size + 1):
            self.label.append(i)
        shuffle(self.label)
        self.cab = 0
        self.fitness = 0.0
        self.weightCount = [0] * ((size//2)+1)

    # surchage of opérator setitem for treat individu like a simple array
    def __setitem__(self, indice, new):
        self.label[indice] = new

    # same thing for getitem
    def __getitem__(self, indice):
        return self.label[indice]

    # method for test if individu contain some item
    # using for make sure all solution is complete and keep every label
    def __contains__(self, item):
        return self.label.__contains__(item)

    def __len__(self):
        return len(self.label)

    # return the position of a labal "ind"
    def index(self, ind):
        return self.label.index(ind)

    # create a empty solution with specific size
    # using for initialize child or temporary Individu
    def child(self, size):
        child = Individu(size)
        child.label = [0]*size
        child.fitness = 0.0
        child.cab = 0
        child.weightCount = [0] * ((size//2)+1)
        return child

    # create a copy of the target individu
    # using for try some swap in local research
    def copyIndividu(self):
        copy = Individu(len(self.label))
        copy.label = self.label.copy()
        copy.cab = self.cab
        copy.fitness = self.fitness
        copy.weightCount = self.weightCount
        return copy



class AEPermutation:
    getcontext().prec = 40
    # its the controler in this algorithm
    def __init__(self, data, pop, mut, rec, nbcMax):
        # method for initialize data structure

        # region Parameters
        # number of offspring for plot
        self.x = []
        # store best fitness evalution for each offspring
        self.y = []

        # store mean fitness of each offspring
        self.moyY = []
        # store worst fitness of each offspring
        # not use it anymore
        self.worstY = []

        # store best CAB evalution for each offspring
        self.cab = []

        # switch of lambda function for change method without rewrite code
        # for mutation operator
        self.mutationType = 1
        self.mutSwitch = {
            1: self.swap,
            2: self.flip,
            3: self.slide,
            4: self.partialRandom,
            5: self.bitSwap,
            6: self.localSearchNaivePermutation,
            7: self.mutatorUCB
        }

        # for selection operator
        self.selectionType = 4
        self.selSwitch = {
            1: self.twoBest,
            2: self.twoRandom,
            3: self.twoBestIn5Random,
            4: self.twoLowIn5Random,
            5: self.wheel
        }

        # for crossover operator
        self.recombinationType = 1
        self.recSwitch = {
            1: self.crossover,
            2: self.Pmx,
            3: self.edge,
            4: self.cycle,
            5: self.crossoverUCB
        }

        # for insertion operator
        self.reinsertionType = 1
        self.reiSwitch = {
            1: self.bestoflower,
            2: self.lessoflower,
            3: self.elder,
            4: self.worst,
            5: self.best
        }

        # setting of parameters for instance give in paramters
        self.Size = data.Size
        self.limits = self.Size//2
        self.SizePop = pop
        self.MutationProb = mut
        self.RecombinationProp = rec
        self.nbCycleMax = nbcMax

        # initialize the count of cycle/offspring
        self.nbCycle = 0

        # initialize of datastruct for selected parents and store child
        self.parents = []
        self.Childrens = Individu(self.Size)

        self.data = data.data
        self.edges = data.edges

        # initialize data structure for population
        self.Population = [Individu(self.Size) for i in range(0, self.SizePop)]

        # initialize datastructure for UCB method
        # see class UCB for more info
        self.UCB_mutator = UCB(6)
        self.UCB_crossover = UCB(4)

        # initialize data struc for partial evaluation
        self.quickEval = []
        self.aux = [0] * ((self.limits)+1)
        self.affected = [0] * ((self.limits)+1)

        # self.minimize = True
        # endregion Parameters

        # switch of lambda function for evaluation function
        self.fitnessType = 2
        self.fitSwitch = {
            1 : self.CAB,
            2 : self.fitness1,
            3 : self.fitness2,
            4 : self.fitness3,
            5 : self.fitness4
        }
        self.functionEval = self.fitSwitch.get(self.fitnessType, lambda: self.fitness1)

        # initialise data struc for best solution
        self.Best = Individu(0)

        #name of instances
        self.name = data.name

        # data for normalize UCB
        self.min = 0
        self.max = 0

    def launch(self, methodList, displayMoy, displayCab, displayFitness,
               displayMutator, displayCrossover):
        # execute genetic algorithm

        # this for is for test many couple of operator with same seed
        for methodElt in methodList:
            self.nbCycle = 0

            # part for choose requiere operator
            self.mutationType = methodElt[0]
            self.selectionType = methodElt[1]
            self.recombinationType = methodElt[2]
            self.reinsertionType = methodElt[3]
            self.fitnessType = methodElt[4]
            Label = ""

            select = self.selSwitch.get(self.selectionType, lambda: self.twoBest)
            Label += select.__name__ + ","

            recombine = self.recSwitch.get(self.recombinationType, lambda: self.crossover)
            Label += recombine.__name__ + ","

            mutation = self.mutSwitch.get(self.mutationType, lambda: self.swap)
            Label += mutation.__name__ + ","

            reinsertion = self.reiSwitch.get(self.reinsertionType, lambda: self.bestoflower)
            Label += reinsertion.__name__ + ","

            self.functionEval = self.fitSwitch.get(self.fitnessType, lambda: self.fitness1)
            Label += self.functionEval.__name__



            # set correct value for quickEval and minimize
            if self.functionEval.__name__ == "CAB":
                self.minimize = False
                self.quickEval = [0] * (self.limits+1)
                # data for normalize reward for ucb
                self.min = 1
                self.max = self.limits
            elif self.functionEval.__name__ == "fitness1":
                self.minimize = True
                self.Best.fitness = 1e400
                delta = 0
                for elt in self.data:
                    if len(elt) > delta:
                        delta = len(elt)
                self.quickEval.append(pow(delta * (self.limits - 0 + 1), 5))
                for i in range(1, self.limits + 1):
                    self.quickEval.append(pow(delta * (self.limits - i + 1), 5))
                # data for normalize reward for ucb
                self.min = self.quickEval[1] * self.edges
                self.max = self.quickEval[-1] * self.edges
            elif self.functionEval.__name__ == "fitness2":
                self.minimize = False
                self.quickEval.append(Decimal(1) / Decimal(self.Size * pow(2, 0)))
                for i in range(1, self.limits + 1):
                    self.quickEval.append(Decimal(1) / Decimal((self.Size * pow(2, i)))+self.quickEval[i-1])
                # data for normalize reward for ucb
                self.min = 1
                self.max = self.limits
            elif (self.functionEval.__name__ == "fitness3") or (self.functionEval.__name__ == "fitness4"):
                self.minimize = False
                for i in range(0, self.limits + 1):
                    self.quickEval.append(0)
                # data for normalize reward for ucb
                self.min = 1
                self.max = self.limits

            #debug(self.quickEval)
            # evaluate initial population
            self.evaluate()

            # end case when number of cycle max it's reach
            # can be improve if we know optimal solution
            while self.terminaison():
                # selection
                self.parents = select()

                # Recombine
                self.Childrens = recombine(self.parents).copyIndividu()

                # mutation
                mutation()

                # evaluate children
                self.evaluatechildren()

                # Reinsertion
                reinsertion()

                # Save best Solution
                if self.minimize:
                    if self.Best.fitness > self.Population[self.CurrentLow()].fitness:
                        self.Best = self.Population[self.CurrentLow()].copyIndividu()
                else:
                    if self.Best.fitness < self.Population[self.CurrentBest()].fitness:
                        self.Best = self.Population[self.CurrentBest()].copyIndividu()

                # graph Value
                self.nbCycle = self.nbCycle + 1
                affichage = "nombre de tour effectuer : " + str(self.nbCycle) + "/" + str(self.nbCycleMax)
                #print(affichage)
                # ajouter
                self.x.append(self.nbCycle)
                if self.minimize:
                    self.y.append(self.Population[self.CurrentLow()].fitness)
                    self.cab.append(self.Population[self.CurrentLow()].cab)
                else:
                    self.y.append(self.Population[self.CurrentBest()].fitness)
                    self.cab.append(self.Population[self.CurrentBest()].cab)
                self.moyY.append(self.mean())



        # part for write result in file
        fichier = open("/home/tsaout/CAB/output/"+ self.name +","+ Label + ".txt", "a")

        for elt in self.y:
            fichier.write(str(elt) + ";")

        fichier.write("\n")
        fichier.close()

        # part for diplay
        if displayFitness:
            plt.plot(self.x, self.y, label=Label)

        if displayMoy:
            tmp = "moy : " + Label
            plt.plot(self.x, self.moyY, label=tmp)

        if displayFitness or displayMoy:
            plt.ylabel("Valeur de la function d'évaluation")
            plt.xlabel("Nombre d'itération")

            plt.legend()
            plt.show()
            plt.clf()

        if displayCab:
            tmp = "cab : " + Label
            plt.plot(self.x, self.cab, label=tmp)
            plt.ylabel("Ciclyc antibanwitdh")
            plt.xlabel("Nombre d'itération")
            plt.legend()
            plt.show()
            plt.clf()

        if displayMutator:
            for i in range(0, self.UCB_mutator.NbrOP):
                title = self.mutSwitch.get(i + 1, lambda: self.crossoverUCB).__name__
                plt.plot(self.x, self.UCB_mutator.output[i], label=title)

            plt.ylabel("Valeur moyenne de récompense pour l'opérateur")
            plt.xlabel("Nombre d'itération")

            plt.legend()
            plt.show()
            plt.clf()

        if displayCrossover:
            for i in range(0, self.UCB_crossover.NbrOP):
                title = self.recSwitch.get(i + 1, lambda: self.mutatorUCB).__name__
                plt.plot(self.x, self.UCB_crossover.output[i], label=title)

            plt.ylabel("Valeur moyenne de récompense pour l'opérateur")
            plt.xlabel("Nombre d'itération")

            plt.legend()
            plt.show()
            plt.clf()

        print("La meilleur solution que l'algorithme as trouvé est :\n\t" + str(self.Best.label))
        print("elle as un cab = "+ str(self.Best.cab))

    # region Selection
    def twoBest(self):
        ret = []
        best = heapq.nlargest(2, self.Population)
        ret.append(self.Population[best[0]].copyIndividu())
        ret.append(self.Population[best[1]].copyIndividu())
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
        ret.append(self.Population[first].copyIndividu())
        ret.append(self.Population[second].ccopyIndividu())
        return ret

    def twoBestIn5Random(self):
        ret = []
        indexRand = []
        evalRand = []
        while len(indexRand) < 5:
            tmp = randint(0, self.SizePop - 1)
            if not indexRand.__contains__(tmp):
                indexRand.append(tmp)
                evalRand.append(self.Population[tmp].fitness)
        best = heapq.nlargest(2, evalRand)
        ret.append(self.Population[indexRand[evalRand.index(best[0])]].copyIndividu())
        ret.append(self.Population[indexRand[evalRand.index(best[1])]].copyIndividu())
        return ret

    def twoLowIn5Random(self):
        ret = []
        indexRand = []
        evalRand = []
        while len(indexRand) < 5:
            tmp = randint(0, self.SizePop - 1)
            if not indexRand.__contains__(tmp):
                indexRand.append(tmp)
                evalRand.append(self.Population[tmp].fitness)

        best = heapq.nsmallest(2, evalRand)
        ret.append(self.Population[indexRand[evalRand.index(best[0])]].copyIndividu())
        ret.append(self.Population[indexRand[evalRand.index(best[1])]].copyIndividu())
        return ret

    def wheel(self):
        ret = []
        wheel = []
        perCent = 0
        somme = 0
        for elt in self.Population:
            somme = somme + elt.fitness
        for child in range(0, len(self.Population)):
            perCent += (self.Population[child].fitness / (somme + 1)) * 100
            wheel.append([child, perCent])
        while len(ret) < 2:
            prop = randint(0, 100)
            for elt in wheel:
                if elt[1] < prop:
                    ret.append(self.Population[elt[0]].copyIndividu())
                    break;
        return ret

    # endregion Selection

    # region Recombination
    def Pmx(self, parents):
        childs = Individu(0).child(self.Size)
        if randint(0, 100) < self.RecombinationProp:
            pivot1 = randint(0, self.Size - 1)
            pivot2 = randint(pivot1 + 1, self.Size)

            # k prends le segment du parents 1
            for i in range(pivot1, pivot2):
                childs[i] = parents[0][i]

            # ajouter les elemnents du parents 2 qui ne sont pas déjç présent
            for i in range(pivot1, pivot2):
                if not childs.label.__contains__(parents[1][i]):
                    next = parents[0][i]
                    check = parents[1].index(next)

                    while not childs[check] == 0:
                        next = parents[0][check]
                        check = parents[1].label.index(next)
                    childs[check] = parents[1][i]

            # remplissage des blancs
            for i in range(0, self.Size):
                if childs[i] == 0:
                    childs[i] = parents[1][i]
            self.evaluateIndividu(childs)
        else:
            childs = parents[0]
        return childs

    def crossover(self, parents):
        childs = Individu(0).child(self.Size)

        if randint(0, 100) < self.RecombinationProp:
            pivot1 = randint(0, self.Size - 1)
            pivot2 = randint(pivot1 + 1, self.Size)

            # k prends le segment du parents 1
            for i in range(pivot1, pivot2):
                childs.label[i] = parents[0][i]

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
            self.evaluateIndividu(childs)
        else:
            childs = parents[0]
        return childs

    def edge(self, parents):
        # bug
        childs = Individu(0).child(self.Size)

        if randint(0, 100) < self.RecombinationProp:

            # création des voisin de chaque sommets
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
                        voisin[i].add(parents[j][parents[j].index(i + 1) + 1])

            # on séléctionne le premiè element de notre progéniture
            first = randint(0, 1)
            x = parents[first][0]

            # choix du prochain sommets de notre progéniture
            for i in range(0, self.Size):
                childs[i] = x
                # on le retire de notre voisinage
                for ensemble in voisin:
                    ensemble.discard(x)

                if childs.__contains__(0):
                    if emptyset(voisin[x - 1]):
                        tirage = randint(1, self.Size)
                        while childs.__contains__(tirage):
                            tirage = randint(1, self.Size)
                        x = tirage
                    else:
                        longueur = self.Size
                        for elt in voisin[x - 1]:
                            if len(voisin[elt - 1]) < longueur:
                                longueur = len(voisin[elt - 1])
                                x = elt
            self.evaluateIndividu(childs)
        else:
            childs = parents[0]
        return childs

    def cycle(self, parents):
        childs = Individu(0).child(self.Size)
        if randint(0, 100) < self.RecombinationProp:
            ite = 0
            while childs.__contains__(0):
                ite = ite + 1
                cycle = []
                next = parents[0][childs.index(0)]
                while not cycle.__contains__(next):
                    cycle.append(next)
                    next = parents[1][parents[0].index(next)]
                if (ite % 2) == 0:
                    for elt in cycle:
                        childs[parents[1].index(elt)] = elt
                else:
                    for elt in cycle:
                        childs[parents[0].index(elt)] = elt
            self.evaluateIndividu(childs)
        else:
            childs = parents[0]
        return childs

    def crossoverUCB(self, parents):
        childs = parents[0]
        meanParentsEval = (parents[0].fitness + parents[1].fitness) / 2

        crossover_selected = 0
        max_upper_bound = -1e400

        for i in range(0, self.UCB_crossover.NbrOP):
            if self.UCB_crossover.numbers_of_mutation[i] > 10:
                average_reward = self.UCB_crossover.sums_of_reward[i] / self.UCB_crossover.numbers_of_mutation[i]
                delta_i = math.sqrt(2 * math.log(self.nbCycle + 1) / self.UCB_crossover.numbers_of_mutation[i])


                upper_bound = Decimal(average_reward) + Decimal(delta_i)
            else:
                upper_bound = Decimal(1e400)
            if upper_bound > max_upper_bound:
                max_upper_bound = upper_bound
                crossover_selected = i
        self.UCB_crossover.numbers_of_mutation[crossover_selected] += 1
        tmp = self.recSwitch.get(crossover_selected + 1, lambda: self.crossover)
        #comment(tmp.__name__)
        childs = tmp(parents)
        reward = self.fitness(childs) - meanParentsEval
        #comment('crossover reward = '+ str(reward))
        if self.minimize:
            self.UCB_crossover.sums_of_reward[crossover_selected] -= reward
        else:
            self.UCB_crossover.sums_of_reward[crossover_selected] += reward

        for i in range(0,self.UCB_crossover.NbrOP):
            self.UCB_crossover.output[i].append(
                self.UCB_crossover.sums_of_reward[i] / (self.UCB_crossover.numbers_of_mutation[i]+1)
            )
            self.UCB_crossover.utilisation[i].append(self.UCB_crossover.numbers_of_mutation)
        return childs

    # endregion Recombination

    # region Mutation

    def slide(self):
        if randint(0, 100) <= self.MutationProb:
            nbrSwap = randint(2, len(self.Childrens) // 2)
            Ltirage = []
            last = -1
            while len(Ltirage) < nbrSwap:
                last = randint(last + 1, len(self.Childrens) - (nbrSwap - len(Ltirage)))
                Ltirage.append(last)
            swapA = Ltirage.pop()
            while len(Ltirage) > 0:
                swapB = Ltirage.pop()
                self.permutation(swapA, swapB)
                self.updateWeightCounts(self.Childrens, 1)
                swapA = swapB
        return

    def partialRandom(self):
        if randint(0, 100) <= self.MutationProb:
            A = randint(0, len(self.Childrens) - 2)
            B = randint(A + 1, len(self.Childrens) - 1)
            tmp = []
            for i in range(A, B):
                tmp.append(self.Childrens[i])
            olds = tmp.copy()
            shuffle(tmp)
            for i in range(A, B):
                self.Childrens[i] = tmp[i - A]
            self.updateWeightCountRange(A,B, olds)
        return

    def swap(self):
        if randint(0, 100) <= self.MutationProb:
            A = randint(0, len(self.Childrens.label) - 2)
            B = randint(A + 1, len(self.Childrens.label) - 1)
            self.permutation(A, B)
            self.updateWeightCounts(self.Childrens, 1)
        return

    def permutation(self, A, B):
        labelA = self.Childrens[A]
        labelB = self.Childrens[B]
        for elt in self.data[A]:
            if not self.Childrens[elt] == B:
                oldw = abs(labelA - self.Childrens[elt])
                neww = abs(labelB - self.Childrens[elt])
                oldcw = min(oldw, self.Size - oldw)
                newcw = min(neww, self.Size - neww)
                self.aux[oldcw] = self.aux[oldcw] - 1
                self.aux[newcw] = self.aux[newcw] + 1
                self.affected.append(oldcw);
                self.affected.append(newcw);

        for elt in self.data[B]:
            if not self.Childrens[elt] == A:
                oldw = abs(labelB - self.Childrens[elt])
                neww = abs(labelA - self.Childrens[elt])
                oldcw = min(oldw, self.Size - oldw)
                newcw = min(neww, self.Size - neww)
                self.aux[oldcw] = self.aux[oldcw] - 1
                self.aux[newcw] = self.aux[newcw] + 1
                self.affected.append(oldcw);
                self.affected.append(newcw);

        tmp = self.Childrens[A]
        self.Childrens[A] = self.Childrens[B]
        self.Childrens[B] = tmp


        return

    def permutationIndividu(self, A, B, individu):
        tmp = individu[A]
        individu[A] = individu[B]
        individu[B] = tmp
        return

    def bitSwap(self):
        if randint(0, 100) <= self.MutationProb:
            for A in range(0, len(self.Childrens)-1):
                if randint(0, 100) <= ((1 / self.Size) * 100):
                    B = randint(A + 1, len(self.Childrens)-1)
                    self.permutation(A,B)
                    self.updateWeightCounts(self.Childrens, 1)
        return

    def reinsert(self):
        childs = self.Childrens.copyIndividu()
        if randint(0, 100) <= self.MutationProb:
            A = randint(0, len(childs) - 2)
            B = randint(A + 1, len(childs) - 1)
            olds = []
            for i in range(A, B):
                olds.append(self.Childrens[i])
            tmp = childs[B]
            childs.label.remove(B)
            childs.label.insert(tmp, A + 1)
            self.updateWeightCountRange(A,B, olds)
        self.Childrens = childs.copyIndividu()
        return

    def flip(self):
        childs = self.Childrens.copyIndividu()
        if randint(0, 100) <= self.MutationProb:
            A = randint(0, len(childs) - 2)
            B = randint(A + 1, len(childs) - 1)
            olds = []
            for i in range(A, B):
                olds.append(self.Childrens[i])
            for i in range(A, B - ((B - A) // 2) - 1):
                tmp = childs[i]
                childs[i] = childs[B - (i - A)]
                childs[B - (i - A)] = tmp
            if (B - A % 2 != 0) and (B-A > 1):
                last = B - ((B - A) // 2)
                tmp = childs[last]
                childs[last] = childs[last+1]
                childs[last+1] = tmp

            self.Childrens = childs
            self.updateWeightCountRange(A,B, olds)

        return

    # region local research
    def localSearchNaivePermutation(self):
        if randint(0, 100) <= self.MutationProb:
            for i in range(0, len(self.Childrens.label)-2):
                B = randint(i+1, len(self.Childrens.label)-1)
                tmp = self.partialEvaluate(i,B,self.Childrens)
                if self.minimize:
                    if(tmp[0] < 0):
                        self.permutationIndividu(i,B, self.Childrens)
                        self.updateWeightCounts(self.Childrens, 1)
                        self.Childrens.fitness += tmp[0]
                        return
                else:
                    if(tmp[0] > 0):
                        self.permutationIndividu(i,B, self.Childrens)
                        self.updateWeightCounts(self.Childrens, 1)
                        self.Childrens.fitness += tmp[0]
                        return
        self.updateWeightCounts(self.Childrens, 0)
        return
    # endregion local research

    def mutatorUCB(self):
        self.evaluatechildren()
        OldChildrenEval = self.Childrens.fitness
        #debug(self.Childrens.fitness)
        mutation_selected = 0
        max_upper_bound = -1e400

        for i in range(0, self.UCB_mutator.NbrOP):
            if self.UCB_mutator.numbers_of_mutation[i] > 10:
                average_reward = self.UCB_mutator.sums_of_reward[i] / self.UCB_mutator.numbers_of_mutation[i]
                delta_i = math.sqrt(2 * math.log(self.nbCycle + 1) / self.UCB_mutator.numbers_of_mutation[i])
                upper_bound = Decimal(average_reward) + Decimal(delta_i)
            else:
                upper_bound = 1e400
            if upper_bound > max_upper_bound:
                max_upper_bound = upper_bound
                mutation_selected = i
        self.UCB_mutator.numbers_of_mutation[mutation_selected] += 1
        mutator = self.mutSwitch.get(mutation_selected + 1, lambda: self.swap)

        #debug(mutator.__name__)
        mutator()

        self.evaluatechildren()
        #debug(self.Childrens.fitness)
        reward = self.Childrens.fitness - OldChildrenEval
        #debug('mutator reward = '+ str(reward))

        if self.minimize:
            self.UCB_mutator.sums_of_reward[mutation_selected] -= reward
        else:
            self.UCB_mutator.sums_of_reward[mutation_selected] += reward
        for i in range(0,self.UCB_mutator.NbrOP):
            self.UCB_mutator.output[i].append(
                self.UCB_mutator.sums_of_reward[i] / (self.UCB_mutator.numbers_of_mutation[i]+1)
            )
            self.UCB_mutator.utilisation[i].append(self.UCB_mutator.numbers_of_mutation)

        return

    # endregion Mutation

    # region Insertion

    # essayer d'utiliser min plutot que de parcourir pour tenter de gagner du tempt, regarder pour utiliser la recherche dicotomique
    def bestoflower(self):
        best = self.Childrens.fitness
        for j in range(0, self.SizePop - 1):
            if self.Population[j].fitness < best:
                self.Population[j] = self.Childrens.copyIndividu()
                return
        return

    def lessoflower(self):
        best = self.Childrens.fitness
        for j in range(0, self.SizePop - 1):
            if self.Population[j].fitness > best:
                self.Population[j] = self.Childrens.copyIndividu()
                return
        return

    def elder(self):
        best = self.Childrens.fitness
        self.Population.append(self.Childrens.copyIndividu())
        self.Population.pop(0)
        return

    def worst(self):
        indice = self.CurrentLow()
        self.Population[indice] = self.Childrens.copyIndividu()

    def best(self):
        indice = self.CurrentBest()
        self.Population[indice] = self.Childrens.copyIndividu()
    # endregion Insertion

    # region function of algo

    # method for evaluate a Population of Individu
    def evaluate(self):
        start_time = time.time()
        individual_time = []
        for elt in self.Population:
            elt_time = time.time()
            elt.cab = self.CAB(elt)
            elt.fitness = self.fitness(elt)
            individual_time.append(time.time() - elt_time)
        print("evaluation complete in %d minute %s seconds with  %s second mean per individual"% (((time.time() - start_time)//60), ((time.time() - start_time)%60), (np.mean(individual_time))))
        return

    # method for evaluate a single individu
    def evaluateIndividu(self, individu):
        individu.cab = self.CAB(individu)
        individu.fitness = self.fitness(individu)
        return

    # method for make evaluation quickest
    # pincipaly use un local research method
    def partialEvaluate(self, A, B, individu):
        oldfitness = individu.fitness
        deltafitness = 0
        labelA = individu[A]
        labelB = individu[B]
        for elt in self.data[A]:
            if not individu[elt] == labelB:
                oldw = abs(labelA - individu[elt])
                neww = abs(labelB - individu[elt])
                oldcw = min(oldw, self.Size - oldw)
                newcw = min(neww, self.Size - neww)
                self.aux[oldcw] = self.aux[oldcw] - 1
                self.aux[newcw] = self.aux[newcw] + 1
                self.affected.append(oldcw)
                self.affected.append(newcw)
                #comment(str(deltafitness)+" + " + str(self.quickEval[newcw]) + " - " + str(self.quickEval[oldcw]))
                deltafitness = deltafitness + self.quickEval[newcw] - self.quickEval[oldcw]
                #comment("result = "+str(tmp.fitness))


        for elt in self.data[B]:
            if not individu[elt] == labelA:
                oldw = abs(labelB - individu[elt])
                neww = abs(labelA - individu[elt])
                oldcw = min(oldw, self.Size - oldw)
                newcw = min(neww, self.Size - neww)
                self.aux[oldcw] = self.aux[oldcw] - 1
                self.aux[newcw] = self.aux[newcw] + 1
                self.affected.append(oldcw);
                self.affected.append(newcw);
                #debug(str(deltafitness)+" + " + str(self.quickEval[newcw]) + " - " + str(self.quickEval[oldcw]))
                deltafitness = deltafitness + self.quickEval[newcw] - self.quickEval[oldcw]
                #debug("result = "+str(tmp.fitness))

        indice = 0
        while individu.weightCount[indice] + self.aux[indice] == 0:
            indice = indice + 1
        deltaCAB = indice
        delta = []

        if self.functionEval.__name__ == "fitness2":
            deltafitness += deltaCAB - individu.cab
        if self.functionEval.__name__ == "fitness3" :
            card = 0
            for A in range(0, len(self.data)):
                if len(self.data[A]) != 0:
                    card += len(self.data[A])
            newfitness = deltaCAB + ((individu.weightCount[deltaCAB]+self.aux[deltaCAB]) / card)

            deltafitness = newfitness-oldfitness
        if self.functionEval.__name__ == "fitness4":
            card = 0
            for A in range(0, len(self.data)):
                if len(self.data[A]) != 0:
                    card += len(self.data[A])
            newfitness = deltaCAB + 1 -((individu.weightCount[deltaCAB]+self.aux[deltaCAB]) / card)

            deltafitness = newfitness-oldfitness
        delta.append(deltafitness)
        delta.append(deltaCAB)
        return delta

    def updateWeightCountRange(self, A, B, olds):
        check = []
        for indice in range(A,B):
            label = self.Childrens[indice]
            labelOld = olds[indice-A]
            check.append(label)
            for elt in self.data[indice]:
                if not check.__contains__(self.Childrens[elt]):
                    oldw = abs(labelOld - self.Childrens[elt])
                    neww = abs(label - self.Childrens[elt])
                    oldcw = min(oldw, self.Size - oldw)
                    newcw = min(neww, self.Size - neww)
                    self.aux[oldcw] = self.aux[oldcw] - 1
                    self.aux[newcw] = self.aux[newcw] + 1
                    self.affected.append(oldcw)
                    self.affected.append(newcw)
        self.updateWeightCounts(self.Childrens, 1)
        return

    # part of partialEvaluate
    # launch if result of partialEvaluate is better then current children
    def updateWeightCounts(self, individu, accepted):
        for i in range(0, len(self.affected)):
            if(accepted):
                individu.weightCount[self.affected[i]] = individu.weightCount[self.affected[i]] + self.aux[self.affected[i]]
            self.aux[self.affected[i]] = 0
        self.affected = []

    # method for use the same method for all function of evalutation selected
    def fitness(self, elt):
        return self.functionEval(elt)

    # evaluation function for CAB
    def CAB(self, elt):
        cab = self.Size
        elt.weightCount = [0] * (self.limits+1)
        for i in range(0, len(self.data)):
            for j in self.data[i]:
                if i < j:
                    absDiff = abs(elt[i] - elt[j])
                    cyclicdiff = min(absDiff, self.Size - absDiff)
                    elt.weightCount[cyclicdiff] = elt.weightCount[cyclicdiff] +1
                    if cyclicdiff < cab:
                        cab = cyclicdiff
        return cab

    # method for fill D a data struct need in some evaluation function
    def fillD(self, elt):
        ret = []
        for i in range(0, (self.limits)+1):
            tmp = 0
            for j in range(0, len(self.data)):
                for k in range(0, len(self.data[j])):

                    diff = abs(elt[j] - elt[self.data[j][k] - 1])
                    cyclicdiff = min(diff, self.Size - diff)

                    if cyclicdiff == i:
                        tmp = tmp + 1
            ret.append(tmp // 2)
        return ret

    # evaluation function provide by the papers "Adaptive evaluation functions for the cyclic bandwidth problem" f1
    # and equation (4) in work document
    def fitness1(self, elt):
        ret = 0
        for i in range(1, self.limits+1):
            ret = ret + (self.quickEval[i] * elt.weightCount[i])
            #ret = ret + (pow((self.quickEval[i]),2)) * elt.weightCount[i]
        return ret

    # evaluation function provide by the papers "Adaptive evaluation functions for the cyclic bandwidth problem" f3
    # and equation (6) in work document
    def fitness2(self, elt):
        ret = elt.cab
        for i in range(1, self.limits+1):
            ret += self.quickEval[i] * elt.weightCount[i]
        return ret

    # method for calculate the number of edges who have a certain weight
    def numE(self, elt):
        elt.cab = self.CAB(elt)
        ret = 0
        for A in range(0, len(self.data)):
            if len(self.data[A]) != 0:
                for B in range(0, len(self.data[A])):
                    absDiff = abs(elt[A] - elt[B])
                    cyclicdiff = min(absDiff, self.Size - absDiff)
                    if cyclicdiff == elt.cab:
                        ret += 1
        return ret

    # evaluation function provide by the papers "An Iterated Three-Phase Search Approach forSolving the Cyclic Bandwidth Problem" fe
    # and equation (8) in work document
    def fitness3(self, elt):
        ret = elt.cab
        card = 0
        for A in range(0, len(self.data)):
            if len(self.data[A]) != 0:
                card += len(self.data[A])

        #comment(elt.weightCount)
        ret += elt.weightCount[ret]/card # ret here have CAB value
        return ret

    # evaluation function provide by the papers "An Iterated Three-Phase Search Approach forSolving the Cyclic Bandwidth Problem" fe
    # and equation (9) in work document
    def fitness4(self, elt):
        ret = elt.cab
        card = 0
        for A in range(0, len(self.data)):
            if len(self.data[A]) != 0:
                card += len(self.data[A])

        #comment(elt.weightCount)
        ret += 1 - elt.weightCount[ret]/card # ret here have CAB value
        return ret

    # method for end case of algorithm
    def terminaison(self):
        if self.nbCycle >= self.nbCycleMax:
            return False
        return True

    # method who evaluate the current children
    def evaluatechildren(self):
        self.Childrens.cab = self.CAB(self.Childrens)
        self.Childrens.fitness = self.fitness(self.Childrens)
        return

    # method who return index of Best value of fitness in population
    def CurrentBest(self):
        max = 0
        indMax = 0
        for i in range(0, len(self.Population)):
            if self.Population[i].fitness > max:
                max = self.Population[i].fitness
                indMax = i
        #debug(self.Population[indMax].fitness)
        return indMax

    # method who return index of Worst value of fitness in population
    def CurrentLow(self):
        min = 1e400
        indMin = 0
        for i in range(0, len(self.Population)):
            if self.Population[i].fitness < min:
                min = self.Population[i].fitness
                indMin = i
        return indMin

    # method for calculate the mean of fitness for a Population
    def mean(self):
        meanList = []
        for elt in self.Population:
            meanList.append(elt.fitness)
        ret = np.mean(meanList)
        return ret

    # endregion function of algo
