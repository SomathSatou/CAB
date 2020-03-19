from AEPermutation import AEPermutation

import numpy as np

N = 10 # nombre de sommet du graphe
P = 1000 # taille de ma population
M = 80 # probabilité de mutation
C = 50 #probabilité de croissement
CMax =10000 # nombre limite d'itérations pour l'algoritme

Seed = 9001
for i in range(0,50):
    np.random.seed(Seed)
    Seed = Seed+1

    # initialisation de la population
    Run = AEPermutation(N, P, M, C, CMax)

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
    methodList = [[1, 1, 2, 1]]
    Run.launch(methodList, False)
