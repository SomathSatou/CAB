#!/bin/bash
#SBATCH --job-name=cab
#SBATCH --mail-user=thomas.saout@etud.univ-angers.fr
#SBATCH --mail-type=end,fail
#SBATCH --ntasks-per-node=1
#SBATCH --nodes=1
#SBATCH --partition=intel-E5-2695
#SBATCH --mem-per-cpu=256
#SBATCH --output=%x-%A-%a.out
#SBATCH --error=%x-%A-%a.err
#SBATCH --array=0-59
#SBATCH --time=10
#SBATCH --signal=SIGINT@30

PATHS= "/home/tsaout/CAB/Dataset/Instances/"

for VARIABLE in $(ls -1 /home/tsaout/CAB/Dataset/Instances)
do
CHEMIN= "${PATHS}${VARIABLE}"

echo "groupe témoin"
srun python3.7 Main.py -p 100 -m 80 -c 50 -i 1000 -f $CHEMIN -l "1,3,1,4,1" -d "0,0,0,0,0" -s 50
srun python3.7 Main.py -p 100 -m 80 -c 50 -i 1000 -f $CHEMIN -l "1,4,1,5,2" -d "0,0,0,0,0" -s 50
srun python3.7 Main.py -p 100 -m 80 -c 50 -i 1000 -f $CHEMIN -l "1,3,1,4,3" -d "0,0,0,0,0" -s 50
srub python3.7 Main.py -p 100 -m 80 -c 50 -i 1000 -f $CHEMIN -l "1,3,1,4,4" -d "0,0,0,0,0" -s 50
srub python3.7 Main.py -p 100 -m 80 -c 50 -i 1000 -f $CHEMIN -l "1,3,1,4,5" -d "0,0,0,0,0" -s 50

echo "Crossover"
srub python3.7 Main.py -p 100 -m 80 -c 50 -i 1000 -f $CHEMIN -l "1,4,5,5,2" -d "0,0,0,0,0" -s 50
srub python3.7 Main.py -p 100 -m 80 -c 50 -i 1000 -f $CHEMIN -l "1,3,5,4,3" -d "0,0,0,0,0" -s 50
srub python3.7 Main.py -p 100 -m 80 -c 50 -i 1000 -f $CHEMIN -l "1,3,5,4,5" -d "0,0,0,0,0" -s 50

echo "Mutator"
srub python3.7 Main.py -p 100 -m 80 -c 50 -i 1000 -f $CHEMIN -l "7,4,1,5,2" -d "0,0,0,0,0" -s 50
srub python3.7 Main.py -p 100 -m 80 -c 50 -i 1000 -f $CHEMIN -l "7,3,1,4,3" -d "0,0,0,0,0" -s 50
srub python3.7 Main.py -p 100 -m 80 -c 50 -i 1000 -f $CHEMIN -l "7,3,1,4,5" -d "0,0,0,0,0" -s 50

echo "duo UCB"
srub python3.7 Main.py -p 100 -m 80 -c 50 -i 1000 -f $CHEMIN -l "7,4,5,5,2" -d "0,0,0,0,0" -s 50
srub python3.7 Main.py -p 100 -m 80 -c 50 -i 1000 -f $CHEMIN -l "7,3,5,4,3" -d "0,0,0,0,0" -s 50
srub python3.7 Main.py -p 100 -m 80 -c 50 -i 1000 -f $CHEMIN -l "7,3,5,4,5" -d "0,0,0,0,0" -s 50

echo "Couple"
srub python3.7 Main.py -p 100 -m 80 -c 50 -i 1000 -f $CHEMIN -l "8,4,6,5,2" -d "0,0,0,0,0" -s 50
srub python3.7 Main.py -p 100 -m 80 -c 50 -i 1000 -f $CHEMIN -l "8,3,6,4,3" -d "0,0,0,0,0" -s 50
srub python3.7 Main.py -p 100 -m 80 -c 50 -i 1000 -f $CHEMIN -l "8,3,6,4,5" -d "0,0,0,0,0" -s 50
wait
