#!/bin/bash

#crossoverUCB
#cf1
echo "python3.7 ReadUCB.py -f /media/etudiant/TOSHIBA\ EXT/thomas/crossoverUCB_$1\,twoLowIn5Random\,crossoverUCB\,swap\,best\,fitness1.txt  -n 100000 -x "Nombre d'itération" -y "Récompense moyenne/pourcentage d'utilisation" -l "crossoverUCB_$1 twoLowIn5Random,crossoverUCB,swap,worst,fitness1" -s "/home/etudiant/Images/graph/crossoverUCB_$1,Cf1.png" -t cr"
python3.7 ReadUCB.py -f /media/etudiant/TOSHIBA\ EXT/thomas/crossoverUCB_$1\,twoLowIn5Random\,crossoverUCB\,swap\,best\,fitness1.txt  -n 100000 -x "Nombre d'itération" -y "Récompense moyenne/pourcentage d'utilisation" -l "crossoverUCB_$1 twoLowIn5Random,crossoverUCB,swap,worst,fitness1" -s "/home/etudiant/Images/graph/crossoverUCB_$1,Cf1.png" -t cr
#cf2
python3.7 ReadUCB.py -f /media/etudiant/TOSHIBA\ EXT/thomas/crossoverUCB_$1\,twoBestIn5Random\,crossoverUCB\,swap\,worst\,fitness2.txt -n 100000 -x "Nombre d'itération" -y "Récompense moyenne/pourcentage d'utilisation" -l "crossoverUCB_$1 twoBestIn5Random,crossoverUCB,swap,worst,fitness2" -s "/home/etudiant/Images/graph/crossoverUCB_$1,Cf2.png" -t cr
#cf4
python3.7 ReadUCB.py -f /media/etudiant/TOSHIBA\ EXT/thomas/crossoverUCB_$1\,twoBestIn5Random\,crossoverUCB\,swap\,worst\,fitness4.txt -n 100000 -x "Nombre d'itération" -y "Récompense moyenne/pourcentage d'utilisation" -l "crossoverUCB_$1 twoBestIn5Random,crossoverUCB,swap,worst,fitness4" -s "/home/etudiant/Images/graph/crossoverUCB_$1,Cf4.png" -t cr

#Crossover/mutator
#cmf1
python3.7 ReadUCB.py -f /media/etudiant/TOSHIBA\ EXT/thomas/crossoverUCB_$1\,twoLowIn5Random\,crossoverUCB\,mutatorUCB\,best\,fitness1.txt -n 100000 -x "Nombre d'itération" -y "Récompense moyenne/pourcentage d'utilisation" -l "crossoverUCB_$1 twoLowIn5Random,crossoverUCB,mutatorUCB,best,fitness1" -s "/home/etudiant/Images/graph/crossoverUCB_$1,CMf1.png" -t cr
#cmf2
python3.7 ReadUCB.py -f /media/etudiant/TOSHIBA\ EXT/thomas/crossoverUCB_$1\,twoBestIn5Random\,crossoverUCB\,mutatorUCB\,worst\,fitness2.txt -n 100000 -x "Nombre d'itération" -y "Récompense moyenne/pourcentage d'utilisation" -l "crossoverUCB_$1 twoBestIn5Random,crossoverUCB,mutatorUCB,worst,fitness2" -s "/home/etudiant/Images/graph/crossoverUCB_$1,CMf2.png" -t cr
#cmf4
python3.7 ReadUCB.py -f /media/etudiant/TOSHIBA\ EXT/thomas/crossoverUCB_$1\,twoBestIn5Random\,crossoverUCB\,mutatorUCB\,worst\,fitness4.txt -n 100000 -x "Nombre d'itération" -y "Récompense moyenne/pourcentage d'utilisation" -l "crossoverUCB_$1 twoBestIn5Random,crossoverUCB,mutatorUCB,worst,fitness4" -s "/home/etudiant/Images/graph/crossoverUCB_$1,CMf4.png" -t cr
