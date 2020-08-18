#!/bin/bash

#temoin
python3.7 ReadData.py -f /media/etudiant/TOSHIBA\ EXT/thomas/$1\,twoBestIn5Random\,crossover\,swap\,worst\,CAB.txt -n 20000 -x "Valeur de la fonction d'évaluation" -y "Nombre d'itération" -l "$1 twoBestIn5Random,crossover,swap,worst,CAB" -m /media/etudiant/TOSHIBA\ EXT/thomas/Mean_$1\,twoBestIn5Random\,crossover\,swap\,worst\,CAB.txt -s "/home/etudiant/Images/graph/$1,temoin.png"
#f1
python3.7 ReadData.py -f /media/etudiant/TOSHIBA\ EXT/thomas/$1\,twoLowIn5Random\,crossover\,swap\,best\,fitness1.txt  -n 20000 -x "Valeur de la fonction d'évaluation" -y "Nombre d'itération" -l "$1 twoLowIn5Random,crossover,swap,worst,fitness1" -m /media/etudiant/TOSHIBA\ EXT/thomas/Mean_$1\,twoLowIn5Random\,crossover\,swap\,best\,fitness1.txt -s "/home/etudiant/Images/graph/$1,f1.png"
#f2
python3.7 ReadData.py -f /media/etudiant/TOSHIBA\ EXT/thomas/$1\,twoBestIn5Random\,crossover\,swap\,worst\,fitness2.txt -n 20000 -x "Valeur de la fonction d'évaluation" -y "Nombre d'itération" -l "$1 twoBestIn5Random,crossover,swap,worst,fitness2" -m /media/etudiant/TOSHIBA\ EXT/thomas/Mean_$1\,twoBestIn5Random\,crossover\,swap\,worst\,fitness2.txt -s "/home/etudiant/Images/graph/$1,f2.png"
#f3
python3.7 ReadData.py -f /media/etudiant/TOSHIBA\ EXT/thomas/$1\,twoBestIn5Random\,crossover\,swap\,worst\,fitness3.txt -n 20000 -x "Valeur de la fonction d'évaluation" -y "Nombre d'itération" -l "$1 twoBestIn5Random,crossover,swap,worst,fitness3" -m /media/etudiant/TOSHIBA\ EXT/thomas/Mean_$1\,twoBestIn5Random\,crossover\,swap\,worst\,fitness3.txt -s "/home/etudiant/Images/graph/$1,f3.png"
#f4
python3.7 ReadData.py -f /media/etudiant/TOSHIBA\ EXT/thomas/$1\,twoBestIn5Random\,crossover\,swap\,worst\,fitness4.txt -n 20000 -x "Valeur de la fonction d'évaluation" -y "Nombre d'itération" -l "$1 twoBestIn5Random,crossover,swap,worst,fitness4" -m /media/etudiant/TOSHIBA\ EXT/thomas/Mean_$1\,twoBestIn5Random\,crossover\,swap\,worst\,fitness4.txt -s "/home/etudiant/Images/graph/$1,f4.png"

#crossoverUCB
#cf1
python3.7 ReadData.py -f /media/etudiant/TOSHIBA\ EXT/thomas/$1\,twoLowIn5Random\,crossoverUCB\,swap\,best\,fitness1.txt  -n 20000 -x "Valeur de la fonction d'évaluation" -y "Nombre d'itération" -l "$1 twoLowIn5Random,crossoverUCB,swap,worst,fitness1" -m /media/etudiant/TOSHIBA\ EXT/thomas/Mean_$1\,twoLowIn5Random\,crossoverUCB\,swap\,best\,fitness1.txt -s "/home/etudiant/Images/graph/$1,Cf1.png"
#cf2
python3.7 ReadData.py -f /media/etudiant/TOSHIBA\ EXT/thomas/$1\,twoBestIn5Random\,crossoverUCB\,swap\,worst\,fitness2.txt -n 20000 -x "Valeur de la fonction d'évaluation" -y "Nombre d'itération" -l "$1 twoBestIn5Random,crossoverUCB,swap,worst,fitness2" -m /media/etudiant/TOSHIBA\ EXT/thomas/Mean_$1\,twoBestIn5Random\,crossoverUCB\,swap\,worst\,fitness2.txt -s "/home/etudiant/Images/graph/$1,Cf2.png"
#cf4
python3.7 ReadData.py -f /media/etudiant/TOSHIBA\ EXT/thomas/$1\,twoBestIn5Random\,crossoverUCB\,swap\,worst\,fitness4.txt -n 20000 -x "Valeur de la fonction d'évaluation" -y "Nombre d'itération" -l "$1 twoBestIn5Random,crossoverUCB,swap,worst,fitness4" -m /media/etudiant/TOSHIBA\ EXT/thomas/Mean_$1\,twoBestIn5Random\,crossoverUCB\,swap\,worst\,fitness4.txt -s "/home/etudiant/Images/graph/$1,Cf4.png"

#mutator
#mf1
python3.7 ReadData.py -f /media/etudiant/TOSHIBA\ EXT/thomas/$1\,twoLowIn5Random\,crossover\,mutatorUCB\,best\,fitness1.txt -n 20000 -x "Valeur de la fonction d'évaluation" -y "Nombre d'itération" -l "$1 twoLowIn5Random,crossover,mutatorUCB,best,fitness1" -m /media/etudiant/TOSHIBA\ EXT/thomas/Mean_$1\,twoLowIn5Random\,crossover\,mutatorUCB\,best\,fitness1.txt -s "/home/etudiant/Images/graph/$1,Mf1.png"
#mf2
python3.7 ReadData.py -f /media/etudiant/TOSHIBA\ EXT/thomas/$1\,twoBestIn5Random\,crossover\,mutatorUCB\,worst\,fitness2.txt -n 20000 -x "Valeur de la fonction d'évaluation" -y "Nombre d'itération" -l "$1 twoBestIn5Random,crossover,mutatorUCB,worst,fitness2" -m /media/etudiant/TOSHIBA\ EXT/thomas/Mean_$1\,twoBestIn5Random\,crossover\,mutatorUCB\,worst\,fitness2.txt -s "/home/etudiant/Images/graph/$1,Mf2.png"
#mf4
python3.7 ReadData.py -f /media/etudiant/TOSHIBA\ EXT/thomas/$1\,twoBestIn5Random\,crossover\,mutatorUCB\,worst\,fitness4.txt -n 20000 -x "Valeur de la fonction d'évaluation" -y "Nombre d'itération" -l "$1 twoBestIn5Random,crossover,mutatorUCB,worst,fitness4" -m /media/etudiant/TOSHIBA\ EXT/thomas/Mean_$1\,twoBestIn5Random\,crossover\,mutatorUCB\,worst\,fitness4.txt -s "/home/etudiant/Images/graph/$1,Mf4.png"

#Crossover/mutator
#cmf1
python3.7 ReadData.py -f /media/etudiant/TOSHIBA\ EXT/thomas/$1\,twoLowIn5Random\,crossoverUCB\,mutatorUCB\,best\,fitness1.txt -n 20000 -x "Valeur de la fonction d'évaluation" -y "Nombre d'itération" -l "$1 twoLowIn5Random,crossoverUCB,mutatorUCB,best,fitness1" -m /media/etudiant/TOSHIBA\ EXT/thomas/Mean_$1\,twoLowIn5Random\,crossoverUCB\,mutatorUCB\,best\,fitness1.txt -s "/home/etudiant/Images/graph/$1,CMf1.png"
#cmf2
python3.7 ReadData.py -f /media/etudiant/TOSHIBA\ EXT/thomas/$1\,twoBestIn5Random\,crossoverUCB\,mutatorUCB\,worst\,fitness2.txt -n 20000 -x "Valeur de la fonction d'évaluation" -y "Nombre d'itération" -l "$1 twoBestIn5Random,crossoverUCB,mutatorUCB,worst,fitness2" -m /media/etudiant/TOSHIBA\ EXT/thomas/Mean_$1\,twoBestIn5Random\,crossoverUCB\,mutatorUCB\,worst\,fitness2.txt -s "/home/etudiant/Images/graph/$1,CMf2.png"
#cmf4
python3.7 ReadData.py -f /media/etudiant/TOSHIBA\ EXT/thomas/$1\,twoBestIn5Random\,crossoverUCB\,mutatorUCB\,worst\,fitness4.txt -n 20000 -x "Valeur de la fonction d'évaluation" -y "Nombre d'itération" -l "$1 twoBestIn5Random,crossoverUCB,mutatorUCB,worst,fitness4" -m /media/etudiant/TOSHIBA\ EXT/thomas/Mean_$1\,twoBestIn5Random\,crossoverUCB\,mutatorUCB\,worst\,fitness4.txt -s "/home/etudiant/Images/graph/$1,CMf4.png"

#couple
#couplef1
python3.7 ReadData.py -f /media/etudiant/TOSHIBA\ EXT/thomas/$1\,twoLowIn5Random\,coupleUCB\,nothing\,best\,fitness1.txt -n 10000 -x "Valeur de la fonction d'évaluation" -y "Nombre d'itération" -l "$1 twoLowIn5Random,couple,nothing,best,fitness1" -m /media/etudiant/TOSHIBA\ EXT/thomas/Mean_$1\,twoLowIn5Random\,coupleUCB\,nothing\,best\,fitness1.txt -s "/home/etudiant/Images/graph/$1,couplef1.png"
#couplef2
python3.7 ReadData.py -f /media/etudiant/TOSHIBA\ EXT/thomas/$1\,twoBestIn5Random\,coupleUCB\,nothing\,worst\,fitness2.txt -n 10000 -x "Valeur de la fonction d'évaluation" -y "Nombre d'itération" -l "$1 twoBestIn5Random,couple,nothing,worst,fitness2" -m /media/etudiant/TOSHIBA\ EXT/thomas/Mean_$1\,twoBestIn5Random\,coupleUCB\,nothing\,worst\,fitness2.txt -s "/home/etudiant/Images/graph/$1,couplef2.png"
#couplef4
python3.7 ReadData.py -f /media/etudiant/TOSHIBA\ EXT/thomas/$1\,twoBestIn5Random\,coupleUCB\,nothing\,worst\,fitness4.txt -n 10000 -x "Valeur de la fonction d'évaluation" -y "Nombre d'itération" -l "$1 twoBestIn5Random,couple,nothing,worst,fitness4" -m /media/etudiant/TOSHIBA\ EXT/thomas/Mean_$1\,twoBestIn5Random\,coupleUCB\,nothing\,worst\,fitness4.txt -s "/home/etudiant/Images/graph/$1,couplef4.png"
