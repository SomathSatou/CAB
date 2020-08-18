#!/bin/bash

#mutator
#mf1
python3.7 ReadUCB.py -f /media/etudiant/TOSHIBA\ EXT/thomas/mutatorUCB_$1\,twoLowIn5Random\,crossover\,mutatorUCB\,best\,fitness1.txt -n 20000 -x "Nombre d'utilisation" -y "Nombre d'itération" -l "$1 mutatorUCB_twoLowIn5Random,crossover,mutatorUCB,best,fitness1" -s "/home/etudiant/Images/graph/mutatorUCB_$1,Mf1.png"
#mf2
python3.7 ReadUCB.py -f /media/etudiant/TOSHIBA\ EXT/thomas/mutatorUCB_$1\,twoBestIn5Random\,crossover\,mutatorUCB\,worst\,fitness2.txt -n 20000 -x "Nombre d'utilisation" -y "Nombre d'itération" -l "$1 mutatorUCB_twoBestIn5Random,crossover,mutatorUCB,worst,fitness2" -s "/home/etudiant/Images/graph/mutatorUCB_$1,Mf2.png"
#mf4
python3.7 ReadUCB.py -f /media/etudiant/TOSHIBA\ EXT/thomas/mutatorUCB_$1\,twoBestIn5Random\,crossover\,mutatorUCB\,worst\,fitness4.txt -n 20000 -x "Nombre d'utilisation" -y "Nombre d'itération" -l "$1 mutatorUCB_twoBestIn5Random,crossover,mutatorUCB,worst,fitness4" -s "/home/etudiant/Images/graph/mutatorUCB_$1,Mf4.png"

#Crossover/mutator
#cmf1
python3.7 ReadUCB.py -f /media/etudiant/TOSHIBA\ EXT/thomas/mutatorUCB_$1\,twoLowIn5Random\,crossoverUCB\,mutatorUCB\,best\,fitness1.txt -n 20000 -x "Nombre d'utilisation" -y "Nombre d'itération" -l "$1 mutatorUCB_twoLowIn5Random,crossoverUCB,mutatorUCB,best,fitness1" -s "/home/etudiant/Images/graph/mutatorUCB_$1,CMf1.png"
#cmf2
python3.7 ReadUCB.py -f /media/etudiant/TOSHIBA\ EXT/thomas/mutatorUCB_$1\,twoBestIn5Random\,crossoverUCB\,mutatorUCB\,worst\,fitness2.txt -n 20000 -x "Nombre d'utilisation" -y "Nombre d'itération" -l "$1 mutatorUCB_twoBestIn5Random,crossoverUCB,mutatorUCB,worst,fitness2" -s "/home/etudiant/Images/graph/mutatorUCB_$1,CMf2.png"
#cmf4
python3.7 ReadUCB.py -f /media/etudiant/TOSHIBA\ EXT/thomas/mutatorUCB_$1\,twoBestIn5Random\,crossoverUCB\,mutatorUCB\,worst\,fitness4.txt -n 20000 -x "Nombre d'utilisation" -y "Nombre d'itération" -l "$1 mutatorUCB_twoBestIn5Random,crossoverUCB,mutatorUCB,worst,fitness4" -s "/home/etudiant/Images/graph/mutatorUCB_$1,CMf4.png"

