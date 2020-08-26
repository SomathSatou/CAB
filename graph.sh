#!/bin/bash

#temoin
python3.7 ReadData.py -f /media/etudiant/TOSHIBA\ EXT/thomas/$1\,twoBestIn5Random\,crossover\,swap\,worst\,CAB.txt -n 100000 -x "Nombre d'itération" -y "Valeur de la fonction d'évaluation" -l "$1 twoBestIn5Random,crossover,swap,worst,CAB" -m /media/etudiant/TOSHIBA\ EXT/thomas/Mean_$1\,twoBestIn5Random\,crossover\,swap\,worst\,CAB.txt -s "/home/etudiant/Images/graph/100000_$1 ,temoin.png"
#f1
python3.7 ReadData.py -f /media/etudiant/TOSHIBA\ EXT/thomas/$1\,twoLowIn5Random\,crossover\,swap\,best\,fitness1.txt  -n 100000 -x "Nombre d'itération" -y "Valeur de la fonction d'évaluation" -l "$1 twoLowIn5Random,crossover,swap,best,fitness1" -m /media/etudiant/TOSHIBA\ EXT/thomas/Mean_$1\,twoLowIn5Random\,crossover\,swap\,best\,fitness1.txt -s "/home/etudiant/Images/graph/100000_$1,f1.png"
#f2
python3.7 ReadData.py -f /media/etudiant/TOSHIBA\ EXT/thomas/$1\,twoBestIn5Random\,crossover\,swap\,worst\,fitness2.txt -n 100000 -x "Nombre d'itération" -y "Valeur de la fonction d'évaluation" -l "$1 twoBestIn5Random,crossover,swap,worst,fitness2" -m /media/etudiant/TOSHIBA\ EXT/thomas/Mean_$1\,twoBestIn5Random\,crossover\,swap\,worst\,fitness2.txt -s "/home/etudiant/Images/graph/100000_$1,f2.png"
#f3
python3.7 ReadData.py -f /media/etudiant/TOSHIBA\ EXT/thomas/$1\,twoBestIn5Random\,crossover\,swap\,worst\,fitness3.txt -n 100000 -x "Nombre d'itération" -y "Valeur de la fonction d'évaluation" -l "$1 twoBestIn5Random,crossover,swap,worst,fitness3" -m /media/etudiant/TOSHIBA\ EXT/thomas/Mean_$1\,twoBestIn5Random\,crossover\,swap\,worst\,fitness3.txt -s "/home/etudiant/Images/graph/100000_$1,f3.png"
#f4
python3.7 ReadData.py -f /media/etudiant/TOSHIBA\ EXT/thomas/$1\,twoBestIn5Random\,crossover\,swap\,worst\,fitness4.txt -n 100000 -x "Nombre d'itération" -y "Valeur de la fonction d'évaluation" -l "$1 twoBestIn5Random,crossover,swap,worst,fitness4" -m /media/etudiant/TOSHIBA\ EXT/thomas/Mean_$1\,twoBestIn5Random\,crossover\,swap\,worst\,fitness4.txt -s "/home/etudiant/Images/graph/100000_$1,f4.png"

#crossoverUCB
#cf1
python3.7 ReadData.py -f /media/etudiant/TOSHIBA\ EXT/thomas/$1\,twoLowIn5Random\,crossoverUCB\,swap\,best\,fitness1.txt  -n 100000 -x "Nombre d'itération" -y "Valeur de la fonction d'évaluation" -l "$1 twoLowIn5Random,crossoverUCB,swap,best,fitness1" -m /media/etudiant/TOSHIBA\ EXT/thomas/Mean_$1\,twoLowIn5Random\,crossoverUCB\,swap\,best\,fitness1.txt -s "/home/etudiant/Images/graph/100000_$1,Cf1.png"
#cf2
python3.7 ReadData.py -f /media/etudiant/TOSHIBA\ EXT/thomas/$1\,twoBestIn5Random\,crossoverUCB\,swap\,worst\,fitness2.txt -n 100000 -x "Nombre d'itération" -y "Valeur de la fonction d'évaluation" -l "$1 twoBestIn5Random,crossoverUCB,swap,worst,fitness2" -m /media/etudiant/TOSHIBA\ EXT/thomas/Mean_$1\,twoBestIn5Random\,crossoverUCB\,swap\,worst\,fitness2.txt -s "/home/etudiant/Images/graph/100000_$1,Cf2.png"
#cf4
python3.7 ReadData.py -f /media/etudiant/TOSHIBA\ EXT/thomas/$1\,twoBestIn5Random\,crossoverUCB\,swap\,worst\,fitness4.txt -n 100000 -x "Nombre d'itération" -y "Valeur de la fonction d'évaluation" -l "$1 twoBestIn5Random,crossoverUCB,swap,worst,fitness4" -m /media/etudiant/TOSHIBA\ EXT/thomas/Mean_$1\,twoBestIn5Random\,crossoverUCB\,swap\,worst\,fitness4.txt -s "/home/etudiant/Images/graph/100000_$1,Cf4.png"

#mutator
#mf1
python3.7 ReadData.py -f /media/etudiant/TOSHIBA\ EXT/thomas/$1\,twoLowIn5Random\,crossover\,mutatorUCB\,best\,fitness1.txt -n 100000 -x "Nombre d'itération" -y "Valeur de la fonction d'évaluation" -l "$1 twoLowIn5Random,crossover,mutatorUCB,best,fitness1" -m /media/etudiant/TOSHIBA\ EXT/thomas/Mean_$1\,twoLowIn5Random\,crossover\,mutatorUCB\,best\,fitness1.txt -s "/home/etudiant/Images/graph/100000_$1,Mf1.png"
#mf2
python3.7 ReadData.py -f /media/etudiant/TOSHIBA\ EXT/thomas/$1\,twoBestIn5Random\,crossover\,mutatorUCB\,worst\,fitness2.txt -n 100000 -x "Nombre d'itération" -y "Valeur de la fonction d'évaluation" -l "$1 twoBestIn5Random,crossover,mutatorUCB,worst,fitness2" -m /media/etudiant/TOSHIBA\ EXT/thomas/Mean_$1\,twoBestIn5Random\,crossover\,mutatorUCB\,worst\,fitness2.txt -s "/home/etudiant/Images/graph/100000_$1,Mf2.png"
#mf4
python3.7 ReadData.py -f /media/etudiant/TOSHIBA\ EXT/thomas/$1\,twoBestIn5Random\,crossover\,mutatorUCB\,worst\,fitness4.txt -n 100000 -x "Nombre d'itération" -y "Valeur de la fonction d'évaluation" -l "$1 twoBestIn5Random,crossover,mutatorUCB,worst,fitness4" -m /media/etudiant/TOSHIBA\ EXT/thomas/Mean_$1\,twoBestIn5Random\,crossover\,mutatorUCB\,worst\,fitness4.txt -s "/home/etudiant/Images/graph/100000_$1,Mf4.png"

#Crossover/mutator
#cmf1
python3.7 ReadData.py -f /media/etudiant/TOSHIBA\ EXT/thomas/$1\,twoLowIn5Random\,crossoverUCB\,mutatorUCB\,best\,fitness1.txt -n 100000 -x "Nombre d'itération" -y "Valeur de la fonction d'évaluation" -l "$1 twoLowIn5Random,crossoverUCB,mutatorUCB,best,fitness1" -m /media/etudiant/TOSHIBA\ EXT/thomas/Mean_$1\,twoLowIn5Random\,crossoverUCB\,mutatorUCB\,best\,fitness1.txt -s "/home/etudiant/Images/graph/100000_$1,CMf1.png"
#cmf2
python3.7 ReadData.py -f /media/etudiant/TOSHIBA\ EXT/thomas/$1\,twoBestIn5Random\,crossoverUCB\,mutatorUCB\,worst\,fitness2.txt -n 100000 -x "Nombre d'itération" -y "Valeur de la fonction d'évaluation" -l "$1 twoBestIn5Random,crossoverUCB,mutatorUCB,worst,fitness2" -m /media/etudiant/TOSHIBA\ EXT/thomas/Mean_$1\,twoBestIn5Random\,crossoverUCB\,mutatorUCB\,worst\,fitness2.txt -s "/home/etudiant/Images/graph/100000_$1,CMf2.png"
#cmf4
python3.7 ReadData.py -f /media/etudiant/TOSHIBA\ EXT/thomas/$1\,twoBestIn5Random\,crossoverUCB\,mutatorUCB\,worst\,fitness4.txt -n 100000 -x "Nombre d'itération" -y "Valeur de la fonction d'évaluation" -l "$1 twoBestIn5Random,crossoverUCB,mutatorUCB,worst,fitness4" -m /media/etudiant/TOSHIBA\ EXT/thomas/Mean_$1\,twoBestIn5Random\,crossoverUCB\,mutatorUCB\,worst\,fitness4.txt -s "/home/etudiant/Images/graph/100000_$1,CMf4.png"

#couple
#couplef1
python3.7 ReadData.py -f /media/etudiant/TOSHIBA\ EXT/thomas/$1\,twoLowIn5Random\,coupleUCB\,nothing\,best\,fitness1.txt -n 10000 -x "Nombre d'itération" -y "Valeur de la fonction d'évaluation" -l "$1 twoLowIn5Random,couple,nothing,best,fitness1" -m /media/etudiant/TOSHIBA\ EXT/thomas/Mean_$1\,twoLowIn5Random\,coupleUCB\,nothing\,best\,fitness1.txt -s "/home/etudiant/Images/graph/$1,couplef1.png"
#couplef2
python3.7 ReadData.py -f /media/etudiant/TOSHIBA\ EXT/thomas/$1\,twoBestIn5Random\,coupleUCB\,nothing\,worst\,fitness2.txt -n 10000 -x "Nombre d'itération" -y "Valeur de la fonction d'évaluation" -l "$1 twoBestIn5Random,couple,nothing,worst,fitness2" -m /media/etudiant/TOSHIBA\ EXT/thomas/Mean_$1\,twoBestIn5Random\,coupleUCB\,nothing\,worst\,fitness2.txt -s "/home/etudiant/Images/graph/$1,couplef2.png"
#couplef4
python3.7 ReadData.py -f /media/etudiant/TOSHIBA\ EXT/thomas/$1\,twoBestIn5Random\,coupleUCB\,nothing\,worst\,fitness4.txt -n 10000 -x "Nombre d'itération" -y "Valeur de la fonction d'évaluation" -l "$1 twoBestIn5Random,couple,nothing,worst,fitness4" -m /media/etudiant/TOSHIBA\ EXT/thomas/Mean_$1\,twoBestIn5Random\,coupleUCB\,nothing\,worst\,fitness4.txt -s "/home/etudiant/Images/graph/$1,couplef4.png"


python3.7 ReadData.py -f /media/etudiant/TOSHIBA\ EXT/thomas/cycle_50\,twoLowIn5Random\,crossover\,mutatorUCB\,best\,fitness1.txt -n 100000 -x "Nombre d'itération" -y "Valeur de la fonction d'évaluation" -l "cycle_50 twoLowIn5Random,crossover,mutatorUCB,best,fitness1" -m /media/etudiant/TOSHIBA\ EXT/thomas/Mean_cycle_50\,twoLowIn5Random\,crossover\,mutatorUCB\,best\,fitness1.txt -s "/home/etudiant/Images/graph/100000_cycle_50,Mf1.png"

python3.7 ReadData.py -f /media/etudiant/TOSHIBA\ EXT/thomas/cycle_200\,twoLowIn5Random\,crossover\,mutatorUCB\,best\,fitness1.txt -n 100000 -x "Nombre d'itération" -y "Valeur de la fonction d'évaluation" -l "cycle_200 twoLowIn5Random,crossover,mutatorUCB,best,fitness1" -m /media/etudiant/TOSHIBA\ EXT/thomas/Mean_cycle_200\,twoLowIn5Random\,crossover\,mutatorUCB\,best\,fitness1.txt -s "/home/etudiant/Images/graph/100000_cycle_200,Mf1.png"

python3.7 ReadData.py -f /media/etudiant/TOSHIBA\ EXT/thomas/cycle_200\,twoBestIn5Random\,crossover\,mutatorUCB\,worst\,fitness4.txt -n 100000 -x "Nombre d'itération" -y "Valeur de la fonction d'évaluation" -l "cycle_200 twoBestIn5Random,crossover,mutatorUCB,worst,fitness4" -m /media/etudiant/TOSHIBA\ EXT/thomas/Mean_cycle_200\,twoBestIn5Random\,crossover\,mutatorUCB\,worst\,fitness4.txt -s "/home/etudiant/Images/graph/100000_cycle_200,Mf4.png"
