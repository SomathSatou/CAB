from AEPermutation import *
from Parser import Parser

def getTestInstance(chemin):
    loader = Parser()
    loader.load(chemin)

    instance = AEPermutation(loader, 1, 100, 100, 100)

    return instance

def testFitness(function):
    instance = getTestInstance('Dataset/Test/test.rnd')

    outputF1 = []
    partialF1 = []
    outputF2 = []
    partialF2 = []
    outputCAB = []
    partialCAB = []

    solution = [1,3, 4, 5, 2]
    individu = Individu(0).child(instance.Size).copyIndividu()
    individu.label = solution
    instance.Population = [individu]

    #test initial function 1
    instance.functionEval = instance.fitSwitch.get(function, lambda: 1)

    if function == 2:
        instance.minimize = True
        delta = 0
        for elt in instance.data:
            if len(elt) > delta:
                delta = len(elt)
        instance.quickEval.append(delta * (instance.limits - 0 + 1))
        for i in range(1, instance.limits + 1):
            instance.quickEval.append(pow(delta * (instance.limits - i + 1), 2))

    elif function == 3:
        instance.minimize = False
        instance.quickEval.append(Decimal(1) / Decimal(instance.Size * pow(2, 0)))
        for i in range(1, instance.limits + 1):
            instance.quickEval.append(Decimal(1) / Decimal((instance.Size * pow(2, i))) + instance.quickEval[i - 1])

    elif function == 4:
        instance.minimize = False
        instance.quickEval = [0] * (instance.limits+1)

    comment(instance.quickEval)
    comment(instance.data)
    #initial state
    instance.evaluate()

    outputF1.append(instance.Population[0].fitness)
    outputCAB.append(instance.Population[0].cab)
    partialF1.append(instance.Population[0].fitness)
    partialCAB.append(instance.Population[0].cab)

    # permute 0--4
    tmp = instance.partialEvaluate(0,4,instance.Population[0])

    partialF1.append(instance.Population[0].fitness+tmp[0])
    partialCAB.append(tmp[1])

    instance.permutationIndividu(0,4, instance.Population[0])
    instance.updateWeightCounts(instance.Population[0], 1)

    instance.evaluate()

    outputF1.append(instance.Population[0].fitness)
    outputCAB.append(instance.Population[0].cab)

    # permute 4 -- 0
    tmp = instance.partialEvaluate(4, 0, instance.Population[0])

    partialF1.append(instance.Population[0].fitness+tmp[0])
    partialCAB.append(tmp[1])

    instance.permutationIndividu(4, 0, instance.Population[0])
    instance.updateWeightCounts(instance.Population[0], 1)

    instance.evaluate()

    outputF1.append(instance.Population[0].fitness)
    outputCAB.append(instance.Population[0].cab)

    # permute 2 -- 3
    tmp = instance.partialEvaluate(2, 3, instance.Population[0])

    partialF1.append(instance.Population[0].fitness+tmp[0])
    partialCAB.append(tmp[1])

    instance.permutationIndividu(2, 3, instance.Population[0])
    instance.updateWeightCounts(instance.Population[0], 1)

    instance.evaluate()

    outputF1.append(instance.Population[0].fitness)
    outputCAB.append(instance.Population[0].cab)

    # permute 3 -- 2
    tmp = instance.partialEvaluate(3, 2, instance.Population[0])

    partialF1.append(instance.Population[0].fitness+tmp[0])
    partialCAB.append(tmp[1])

    instance.permutationIndividu(3, 2, instance.Population[0])
    instance.updateWeightCounts(instance.Population[0], 1)

    instance.evaluate()

    outputF1.append(instance.Population[0].fitness)
    outputCAB.append(instance.Population[0].cab)

    # permute 4 -- 2
    tmp = instance.partialEvaluate(4, 2, instance.Population[0])

    partialF1.append(instance.Population[0].fitness+tmp[0])
    partialCAB.append(tmp[1])

    instance.permutationIndividu(4, 2, instance.Population[0])
    instance.updateWeightCounts(instance.Population[0], 1)

    instance.evaluate()

    outputF1.append(instance.Population[0].fitness)
    outputCAB.append(instance.Population[0].cab)

    # permute 2 -- 4
    tmp = instance.partialEvaluate(2, 4, instance.Population[0])

    partialF1.append(instance.Population[0].fitness+tmp[0])
    partialCAB.append(tmp[1])

    instance.permutationIndividu(2, 4, instance.Population[0])
    instance.updateWeightCounts(instance.Population[0], 1)

    instance.evaluate()

    outputF1.append(instance.Population[0].fitness)
    outputCAB.append(instance.Population[0].cab)

    comment("out F1 "+str(outputF1))
    comment("par F1 " +str(partialF1))

    comment("out cab "+str(outputCAB))
    comment("par cab "+str(partialCAB))

    return

    """
    #test initial function 2
    instance.functionEval = instance.fitSwitch.get(3, lambda: 1)

    instance.minimize = False
    for i in range(0, (instance.Size // 2) + 1):
        instance.quickEval.append(1 / (instance.Size * pow(2, i)))

    instance.evaluate()

    outputF2.append(instance.Population[0].fitness)
    
    comment("out F2 "+str(outputF2))
    comment("par F2 "+str(partialF2))
    """

def testCab():
    instance = getTestInstance('Dataset/Test/test.rnd')

    solution = [1, 2, 3, 4, 5]
    individu = Individu(0).child(instance.Size).copyIndividu()
    individu.label = solution
    instance.Population = [individu]

    func = instance.fitSwitch.get(2, lambda: 1)

    if func.__name__ == "fitness1":
        instance.minimize = True
        delta = 0
        for elt in instance.data:
            if len(elt) > delta:
                delta = len(elt)
        for i in range(0, (instance.Size // 2) + 1):
            instance.quickEval.append(delta * ((instance.Size // 2) - i + 1))
    elif func.__name__ == "fitness2":
        instance.minimize = False
        for i in range(0, (instance.Size // 2) + 1):
            instance.quickEval.append(1 / (instance.Size * pow(2, i)))

    instance.evaluate()

    comment("cab = "+str(instance.Population[0].cab)+" on devrait obtenir 2")
    debug("function CAB() return "+str(instance.CAB(instance.Population[0])))
    return
