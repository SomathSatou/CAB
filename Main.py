from AEPermutation import AEPermutation
from Parser import Parser

import numpy as np

loader = Parser()
#big instance
#loader.load('../Dataset/Instances/hypercube11.rnd')
#test instance
loader.load('../Dataset/Instances/mesh2D5x25.rnd')

P = 100 # taille de ma population
M = 80 # probabilité de mutation
C = 50 #probabilité de croissement
CMax = 100 # nombre limite d'itérations pour l'algoritme

Seed = 9001
for i in range(0,1):
    print('debut des test pour la seed ' + str(Seed))
    np.random.seed(Seed)
    Seed = Seed+1

    # initialisation de la population
    Run = AEPermutation(loader, P, M, C, CMax)

    # exécution simple pour première face de test

    # [mutation, selection,recombinaison, reinsertion]
    # methodList = [[1, 1, 1, 2], [2, 1, 1, 1], [1, 1, 2, 1], [1 ,1 ,1 ,1], [1, 2, 1, 1]]

    # Mutation set of parameter
    # methodList = [[1, 1, 1, 1], [2, 1, 1, 1], [3, 1, 1, 1], [4, 1, 1, 1], [5, 1, 1, 1], [6, 1, 1, 1],[7, 1, 1, 1], [8, 1, 1, 1]]

    # selection set of parameter
    # methodList = [[1, 1, 1, 1], [1, 2, 1, 1], [1, 3, 1, 1], [1, 4, 1, 1]]

    # recombinaison set of parameter
    # methodList = [[1, 1, 1, 1], [1, 1, 2, 1], [1, 1, 3, 1]]

    # reinsertion set of parameter
    # methodList = [[1, 1, 1, 1], [1, 1, 1, 2]]

    # test
    methodList = [[4, 3, 2, 3]]

    #launch(self, methodList, displayPlot, displayMoy, displayCab, displayFitness)
    # display F1
    #Run.launch(methodList, True, True, False, True)
    # display CAB
    #Run.launch(methodList, True, False, True, False)

    #display all
    #Run.launch(methodList, True, True, True, True)


    # Test UCB
    # affiche les coubes de fitness
    #Run.launch2UCB(True, True, False, True, False, False)
    # affiche les courbes d'utilité des opérateurInstances//home/etudiant/Bureau/CyclicBandwith/DInstances//home/etudiant/Bureau/CyclicBandwith/Dataset/ataset/
    #
    #Run.launch2UCB(True, False, True, False, False, False, False, True)
    Run.launch2UCB(True, True, False, True, False, False, False, True)

    #not F1
    #Run.launch2UCB(True, False, True, False, False, False, False)
