#!/bin/bash

#couple
#couplef1
python3.7 ReadUCB.py -f /media/etudiant/TOSHIBA\ EXT/thomas/coupleUCB_$1\,twoLowIn5Random\,coupleUCB\,nothing\,best\,fitness1.txt -n 10000 -x "Nombre d'itération" -y "Récompense moyenne/pourcentage d'utilisation" -l "coupleUCB_$1 twoLowIn5Random,couple,nothing,best,fitness1" -s "/home/etudiant/Images/graph/coupleUCB_$1,couplef1.png" -t cp
#couplef2
python3.7 ReadUCB.py -f /media/etudiant/TOSHIBA\ EXT/thomas/coupleUCB_$1\,twoBestIn5Random\,coupleUCB\,nothing\,worst\,fitness2.txt -n 10000 -x "Nombre d'itération"  -y "Récompense moyenne/pourcentage d'utilisation" -l "coupleUCB_$1 twoBestIn5Random,couple,nothing,worst,fitness2" -s "/home/etudiant/Images/graph/coupleUCB_$1,couplef2.png" -t cp
#couplef4
python3.7 ReadUCB.py -f /media/etudiant/TOSHIBA\ EXT/thomas/coupleUCB_$1\,twoBestIn5Random\,coupleUCB\,nothing\,worst\,fitness4.txt -n 10000 -x "Nombre d'itération"  -y "Récompense moyenne/pourcentage d'utilisation" -l "coupleUCB_$1 twoBestIn5Random,couple,nothing,worst,fitness4" -s "/home/etudiant/Images/graph/coupleUCB_$1,couplef4.png" -t cp
