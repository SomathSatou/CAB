import math
from random import *

import matplotlib.pyplot as plt
import numpy as np
import time

from output import *


def emptyset(ensemble):
    return len(ensemble) == 0

class UCB:
    def __init__(self, NbrOP):
        self.NbrOP = NbrOP
        self.sums_of_reward = [0] * self.NbrOP
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
    def __init__(self, size):
        self.label = []
        for i in range(1, size + 1):
            self.label.append(i)
        shuffle(self.label)
        self.cab = 0
        self.fitness = 0
        self.weightCount = [0] * ((size//2)+1)

    def __setitem__(self, indice, new):
        self.label[indice] = new

    def __getitem__(self, indice):
        return self.label[indice]

    def __contains__(self, item):
        return self.label.__contains__(item)

    def __len__(self):
        return len(self.label)

    def index(self, ind):
        return self.label.index(ind)

    def child(self, size):
        child = Individu(size)
        child.label = [0]*size
        child.fitness = 0
        child.cab = 0
        child.weightCount = [0] * ((size//2)+1)
        return child

    def copyIndividu(self):
        copy = Individu(len(self.label))
        copy.label = self.label.copy()
        copy.cab = self.cab
        copy.fitness = self.fitness
        copy.weightCount = self.weightCount
        return copy



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
            4: self.partialRandom,
            5: self.bitSwap,
            6: self.localSearchNaivePermutation,
            7: self.mutatorUCB
        }

        self.selectionType = 4
        self.selSwitch = {
            1: self.twoBest,
            2: self.twoRandom,
            3: self.twoBestIn5Random,
            4: self.twoLowIn5Random,
            5: self.wheel
        }

        self.recombinationType = 1
        self.recSwitch = {
            1: self.crossover,
            2: self.Pmx,
            3: self.edge,
            4: self.cycle,
            5: self.crossoverUCB
        }

        self.reinsertionType = 1
        self.reiSwitch = {
            1: self.bestoflower,
            2: self.lessoflower,
            3: self.elder,
            4: self.worst,
            5: self.best
        }

        self.Size = data.Size
        self.SizePop = pop
        self.MutationProb = mut
        self.RecombinationProp = rec
        self.nbCycleMax = nbcMax

        self.nbCycle = 0

        self.parents = []
        self.Childrens = Individu(self.Size)

        self.data = data.data
        self.edges = data.edges

        self.Population = [Individu(self.Size) for i in range(0, self.SizePop)]

        self.UCB_mutator = UCB(6)
        self.UCB_crossover = UCB(4)

        self.quickEval = []
        self.aux = [0] * ((self.Size//2)+1)
        self.affected = []

        self.minimize = True
        # endregion Parameters


    def launch(self, methodList, displayMoy, displayCab, displayFitness,
               displayMutator, displayCrossover, minimize):

        self.minimize = minimize

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

            # partie ou on rempli
            if minimize:
                delta = 0
                for elt in self.data:
                    if len(elt) > delta:
                        delta = len(elt)
                for i in range(0, (self.Size // 2) + 1):
                    self.quickEval.append(delta * ((self.Size // 2) - i + 1))
            else:
                comment('il faut implémenter F3 avant')

            self.evaluate()
            #self.evaluateCab()
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

                # graph Value
                self.nbCycle = self.nbCycle + 1
                affichage = "nombre de tour effectuer : " + str(self.nbCycle) + "/" + str(self.nbCycleMax)
                print(affichage)
                # ajouter
                self.x.append(self.nbCycle)
                if minimize:
                    self.y.append(self.Population[self.CurrentLow()].fitness)
                else:
                    self.y.append(self.Population[self.CurrentBest()].fitness)

                self.moyY.append(self.mean())
                self.cab.append(self.Population[self.CurrentBest()].cab)

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

        if displayFitness or displayMoy:
            plt.legend()
            plt.show()
            plt.clf()

        if displayCab:
            tmp = "cab : " + Label
            plt.plot(self.x, self.cab, label=tmp)
            plt.legend()
            plt.show()
            plt.clf()

        if displayMutator:
            for i in range(0, self.UCB_mutator.NbrOP):
                title = self.mutSwitch.get(i + 1, lambda: self.crossoverUCB).__name__
                plt.plot(self.x, self.UCB_mutator.output[i], label=title)
            plt.legend()
            plt.show()
            plt.clf()

        if displayCrossover:
            for i in range(0, self.UCB_crossover.NbrOP):
                title = self.recSwitch.get(i + 1, lambda: self.mutatorUCB).__name__
                plt.plot(self.x, self.UCB_crossover.output[i], label=title)
            plt.legend()
            plt.show()
            plt.clf()


    def launch2UCB(self, displayPlot, displayMoy, displayCab, displayFitness,
                   displayMutator, displayCrossover, displayOP, minimize):
        # cette fonction as pour but de tester notre algorithme avec 2 bandit manchot, un seul les opérateur
        # de croissement et l'autre sur les opérateur de mutations
        # 5 list pour conserver l'évolution des opérateur de mutation
        # 4 autre pour celle de croissement
        self.minimize = minimize
        self.nbCycle = 0

        self.mutationType = 7
        self.recombinationType = 5
        if minimize:
            self.reinsertionType = 5
            self.selectionType = 4  # selection par tournoi
        else:
            self.reinsertionType = 4
            self.selectionType = 3  # selection par tournoi
        Label = ""

        select = self.selSwitch.get(self.selectionType, lambda: self.twoBest)
        Label += select.__name__ + ","

        recombine = self.recSwitch.get(self.recombinationType, lambda: self.crossover)
        Label += recombine.__name__ + ","

        mutation = self.mutSwitch.get(self.mutationType, lambda: self.swap)
        Label += mutation.__name__ + ","

        reinsertion = self.reiSwitch.get(self.reinsertionType, lambda: self.bestoflower)
        Label += reinsertion.__name__ + ","

        # valeur de debug
        # last = 0

        # partie ou on rempli quickEval
        if minimize:
            delta = 0
            for elt in self.data:
                if len(elt) > delta:
                    delta = len(elt)
            for i in range(0, (self.Size // 2)+1):
                self.quickEval.append(delta * ((self.Size // 2) - i + 1))
        else:
            comment('il faut implémenter F3 avant')

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
            # self.evaluate()
            # self.evaluateCab()
            self.nbCycle = self.nbCycle + 1
            affichage = "nombre de tour effectuer : " + str(self.nbCycle) + "/" + str(self.nbCycleMax)
            print(affichage)
            # ajouter
            self.x.append(self.nbCycle)
            if minimize:
                self.y.append(self.Population[self.CurrentLow()].fitness)
            else:
                self.y.append(self.Population[self.CurrentBest()].fitness)

            self.moyY.append(self.mean())
            self.cab.append(self.Population[self.CurrentBest()].cab)

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

        if displayMutator:
            for i in range (0, self.UCB_mutator.NbrOP):
                title = self.mutSwitch.get(i+1, lambda: self.crossoverUCB).__name__
                plt.plot(self.x, self.UCB_mutator.output[i], label=title)

        if displayCrossover:
            for i in range (0, self.UCB_crossover.NbrOP):
                title = self.recSwitch.get(i+1, lambda: self.mutatorUCB).__name__
                plt.plot(self.x, self.UCB_crossover.output[i], label=title)

        if displayOP:
            for i in range(1, self.UCB_mutator.NbrOP):
                title = self.mutSwitch.get(i+1, lambda: self.mutatorUCB).__name__
                plt.plot(self.x, self.UCB_mutator.utilisation[i], label=title)

            for i in range (1, self.UCB_crossover.NbrOP):
                title = self.recSwitch.get(i+1, lambda: self.crossoverUCB).__name__
                plt.plot(self.x, self.UCB_crossover.utilisation[i], label=title)



        # if mutation == flipsAdaptatifPursuit:
        #    fichierOP = open(Label + "dataOPAPW.txt", "a")
        # dépendant de opérateur cible , mutation recombinaison, etc ...
        #    for iop in range(0, 2):
        #       for elt in DataOP:
        #            fichierOP.write(str(elt[iop]) + ";")
        #        fichierOP.write("\n")
        #    fichierOP.write("\n")
        #    fichierOP.close()
        if (displayPlot):
            plt.legend()
            plt.show()

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

                    #boucle infinie
                    while not childs[check] == 0:
                        next = parents[0][check]
                        check = parents[1].label.index(next)
                    childs[check] = parents[1][i]

            # remplissage des blancs
            for i in range(0, self.Size):
                if childs[i] == 0:
                    childs[i] = parents[1][i]
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
        else:
            childs = parents[0]
        return childs

    def crossoverUCB(self, parents):
        childs = parents[0]
        if randint(0, 100) < self.RecombinationProp:
            meanParentsEval = (parents[0].fitness + parents[1].fitness) / 2

            crossover_selected = 0
            max_upper_bound = 0

            for i in range(0, self.UCB_crossover.NbrOP):
                if self.UCB_crossover.numbers_of_mutation[i] > 0:
                    average_reward = self.UCB_crossover.sums_of_reward[i] / self.UCB_crossover.numbers_of_mutation[i]
                    delta_i = math.sqrt(2 * math.log(self.nbCycle + 1) / self.UCB_crossover.numbers_of_mutation[i])
                    upper_bound = average_reward + delta_i
                else:
                    upper_bound = 1e400
                if upper_bound > max_upper_bound:
                    max_upper_bound = upper_bound
                    crossover_selected = i
            self.UCB_crossover.numbers_of_mutation[crossover_selected] += 1
            tmp = self.recSwitch.get(crossover_selected + 1, lambda: self.crossover())
            childs = tmp(parents)
            reward = self.fitness(childs) - meanParentsEval
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
                swapA = swapB
        return

    def partialRandom(self):
        if randint(0, 100) <= self.MutationProb:
            A = randint(0, len(self.Childrens) - 2)
            B = randint(A + 1, len(self.Childrens) - 1)
            tmp = []
            for i in range(A, B):
                tmp.append(self.Childrens[i])
            shuffle(tmp)
            for i in range(A, B):
                self.Childrens[i] = tmp[i - A]

        return

    def swap(self):
        if randint(0, 100) <= self.MutationProb:
            A = randint(0, len(self.Childrens.label) - 2)
            B = randint(A + 1, len(self.Childrens.label) - 1)
            tmp = self.Childrens.label[A]
            self.Childrens.label[A] = self.Childrens.label[B]
            self.Childrens.label[B] = tmp
        return

    def permutation(self, A, B):
        tmp = self.Childrens[A]
        self.Childrens[A] = self.Childrens[B]
        self.Childrens[B] = tmp
        return

    def bitSwap(self):
        if randint(0, 100) <= self.MutationProb:
            for A in range(0, len(self.Childrens)-1):
                if randint(0, 100) <= ((1 / self.Size) * 100):
                    B = randint(A + 1, len(self.Childrens)-1)
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
        childs = self.Childrens.copyIndividu()
        if randint(0, 100) <= self.MutationProb:
            A = randint(0, len(childs) - 2)
            B = randint(A + 1, len(childs) - 1)
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
        return

    # region local research
    def localSearchNaivePermutation(self):
        comment(self.Childrens.fitness)
        if randint(0, 100) <= self.MutationProb:
            for i in range(0, len(self.Childrens.label)-2):
                B = randint(i+1, len(self.Childrens.label)-1)
                tmp = self.partialEvaluate(i,B,self.Childrens).copyIndividu()
                if self.minimize:
                    if(tmp.fitness < self.Childrens.fitness):
                        self.permutation(i,B)
                        self.updateWeightCounts(self.Childrens)
                else:
                    if(tmp.fitness > self.Childrens.fitness):
                        self.permutation(i,B)
                        self.updateWeightCounts(self.Childrens)
        comment(self.Childrens.fitness)

        return
    # endregion local research

    def mutatorUCB(self):
        if randint(0, 100) <= self.MutationProb:
            self.evaluatechildren()
            OldChildrenEval = self.Childrens.fitness

            mutation_selected = 0
            max_upper_bound = 0

            for i in range(0, self.UCB_mutator.NbrOP):
                if self.UCB_mutator.numbers_of_mutation[i] > 0:
                    average_reward = self.UCB_mutator.sums_of_reward[i] / self.UCB_mutator.numbers_of_mutation[i]
                    delta_i = math.sqrt(2 * math.log(self.nbCycle + 1) / self.UCB_mutator.numbers_of_mutation[i])
                    upper_bound = average_reward + delta_i
                else:
                    upper_bound = 1e400
                if upper_bound > max_upper_bound:
                    max_upper_bound = upper_bound
                    mutation_selected = i
            self.UCB_mutator.numbers_of_mutation[mutation_selected] += 1
            mutator = self.mutSwitch.get(mutation_selected + 1, lambda: self.swap)
            mutator()

            self.evaluatechildren()
            reward = self.Childrens.fitness - OldChildrenEval
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
        self.Population[indice].fitness = self.Childrens.fitness
        self.Population[indice].cab = self.CAB(self.Childrens)
        self.Population[indice] = self.Childrens.copyIndividu()

    def best(self):
        indice = self.CurrentBest()
        self.Population[indice].fitness = self.Childrens.fitness
        self.Population[indice].cab = self.CAB(self.Childrens)
        self.Population[indice] = self.Childrens.copyIndividu()
    # endregion Insertion

    # region function of algo
    def evaluate(self):
        start_time = time.time()
        individual_time = []
        for elt in self.Population:
            elt_time = time.time()
            elt.fitness = self.fitness(elt)
            elt.cab = self.CAB(elt)
            individual_time.append(time.time() - elt_time)
        print("evaluation complete in %d minute %s seconds with  %s second mean per individual"% (((time.time() - start_time)//60), ((time.time() - start_time)%60), (np.mean(individual_time))))
        return

    def evaluateIndividu(self, individu):
        individu.fitness = self.fitness(individu)
        individu.cab = self.CAB(individu)
        return

    # à tester
    def partialEvaluate(self, A, B, individu):
        tmp = individu.copyIndividu()
        labelA = individu[A]
        labelB = individu[B]
        for elt in self.data[A]:
            if not individu[elt-1] == B:
                oldw = abs(labelA - individu[elt-1])
                neww = abs(labelB - individu[elt-1])
                oldcw = min(oldw, self.Size - oldw)
                newcw = min(neww, self.Size - neww)
                self.aux[oldcw] = self.aux[oldcw] - 1
                self.aux[newcw] = self.aux[newcw] + 1
                self.affected.append(oldcw);
                self.affected.append(newcw);
                tmp.fitness = tmp.fitness + self.quickEval[newcw] - self.quickEval[oldcw]

        for elt in self.data[B]:
            if not individu[-1] == A:
                oldw = abs(labelB - individu[elt-1])
                neww = abs(labelA - individu[elt-1])
                oldcw = min(oldw, self.Size - oldw)
                newcw = min(neww, self.Size - neww)
                self.aux[oldcw] = self.aux[oldcw] - 1
                self.aux[newcw] = self.aux[newcw] + 1
                self.affected.append(oldcw);
                self.affected.append(newcw);
                tmp.fitness = tmp.fitness + self.quickEval[newcw] - self.quickEval[oldcw]

        d = self.fillD(tmp)
        indice = 1
        while d[indice] + self.aux[indice] == 0:
            indice = indice + 1
        tmp.cab = indice
        return tmp

    def updateWeightCounts(self, individu):
        for i in range(0, len(self.affected)):
            individu.weightCount[self.affected[i]] = individu.weightCount[self.affected[i]] + self.aux[self.affected[i]]
            self.aux[self.affected[i]] = 0
            self.affected[i] = 0

    def fitness(self, elt):
        return self.fitness1(elt)

    def CAB(self, elt):
        cab = self.Size
        for i in range(0, len(self.data)):
            for j in self.data[i]:
                if (i + 1) < j:
                    absDiff = abs(elt[i] - elt[j - 1])
                    cyclicdiff = min(absDiff, self.Size - absDiff)
                    elt.weightCount[cyclicdiff] = elt.weightCount[cyclicdiff] +1
                    if cyclicdiff < cab:
                        cab = cyclicdiff
        return cab

    def fillD(self, elt):
        ret = []
        for i in range(0, (self.Size // 2) - 1):
            tmp = 0
            for j in range(0, len(self.data)):
                for k in range(0, len(self.data[j])):
                    if abs(elt[j] - elt[k]) == i:
                        tmp = tmp + 1
            ret.append(tmp // 2)
        return ret

    def fitness1(self, elt):
        d = self.fillD(elt)
        ret = 0
        for i in range(1, self.Size // 2):
            ret = ret + (self.quickEval[i-1] * d[i - 1])
        return ret

    def terminaison(self):
        if self.nbCycle >= self.nbCycleMax:
            return False
        return True

    def evaluatechildren(self):
        self.Childrens.fitness = self.fitness(self.Childrens)
        self.Childrens.cab = self.CAB(self.Childrens)
        return

    def CurrentBest(self):
        max = 0
        indMax = 0
        for i in range(0, len(self.Population)):
            if self.Population[i].fitness > max:
                max = self.Population[i].fitness
                indMax = i
        return indMax

    def CurrentLow(self):
        min = 99999999999
        indMin = 0
        for i in range(0, len(self.Population)):
            if self.Population[i].fitness < min:
                min = self.Population[i].fitness
                indMin = i
        return indMin

    def mean(self):
        meanList = []
        for elt in self.Population:
            meanList.append(elt.fitness)
        ret = np.mean(meanList)
        return ret

    # endregion function of algo
