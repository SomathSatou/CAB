#!/bin/bash
#SBATCH --job-name=cab
#SBATCH --mail-user=thomas.saout@etud.univ-angers.fr
#SBATCH --mail-type=end,fail
#SBATCH --ntasks-per-node=1
#SBATCH --nodes=1
#SBATCH --partition=std
#SBATCH --mem-per-cpu=256
#SBATCH --output=cluster/output/%x-%A-%a.out
#SBATCH --error=cluster/error/cluster%x-%A-%a.err
#SBATCH --array=1-50
#SBATCH --time=14400
#SBATCH --signal=SIGINT@30

PATHS="/home/tsaout/CAB/Dataset/Instances2/"
echo $PATHs

for VARIABLE in $(ls -1 /home/tsaout/CAB/Dataset/Instances2)
do
CHEMIN="${PATHS}${VARIABLE}"

echo "groupe témoin"
srun python3.7 Main.py -p 100 -m 80 -c 50 -i 100000 -u -f $CHEMIN -l "1,3,1,4,1" -d "0,0,0,0,0,0" -s $SLURM_ARRAY_TASK_ID
srun python3.7 Main.py -p 100 -m 80 -c 50 -i 100000 -u -f $CHEMIN -l "1,4,1,5,2" -d "0,0,0,0,0,0" -s $SLURM_ARRAY_TASK_ID
srun python3.7 Main.py -p 100 -m 80 -c 50 -i 100000 -u -f $CHEMIN -l "1,3,1,4,3" -d "0,0,0,0,0,0" -s $SLURM_ARRAY_TASK_ID
srun python3.7 Main.py -p 100 -m 80 -c 50 -i 100000 -u -f $CHEMIN -l "1,3,1,4,4" -d "0,0,0,0,0,0" -s $SLURM_ARRAY_TASK_ID
srun python3.7 Main.py -p 100 -m 80 -c 50 -i 100000 -u -f $CHEMIN -l "1,3,1,4,5" -d "0,0,0,0,0,0" -s $SLURM_ARRAY_TASK_ID

echo "Crossover"
srun python3.7 Main.py -p 100 -m 80 -c 50 -i 100000 -u -f $CHEMIN -l "1,4,5,5,2" -d "0,0,0,0,0,0" -s $SLURM_ARRAY_TASK_ID
srun python3.7 Main.py -p 100 -m 80 -c 50 -i 100000 -u -f $CHEMIN -l "1,3,5,4,3" -d "0,0,0,0,0,0" -s $SLURM_ARRAY_TASK_ID
srun python3.7 Main.py -p 100 -m 80 -c 50 -i 100000 -u -f $CHEMIN -l "1,3,5,4,5" -d "0,0,0,0,0,0" -s $SLURM_ARRAY_TASK_ID

echo "Mutator"
srun python3.7 Main.py -p 100 -m 80 -c 50 -i 100000 -u -f $CHEMIN -l "7,4,1,5,2" -d "0,0,0,0,0,0" -s $SLURM_ARRAY_TASK_ID
srun python3.7 Main.py -p 100 -m 80 -c 50 -i 100000 -u -f $CHEMIN -l "7,3,1,4,3" -d "0,0,0,0,0,0" -s $SLURM_ARRAY_TASK_ID
srun python3.7 Main.py -p 100 -m 80 -c 50 -i 100000 -u -f $CHEMIN -l "7,3,1,4,5" -d "0,0,0,0,0,0" -s $SLURM_ARRAY_TASK_ID

echo "duo UCB"
srun python3.7 Main.py -p 100 -m 80 -c 50 -i 100000 -u -f $CHEMIN -l "7,4,5,5,2" -d "0,0,0,0,0,0" -s $SLURM_ARRAY_TASK_ID
srun python3.7 Main.py -p 100 -m 80 -c 50 -i 100000 -u -f $CHEMIN -l "7,3,5,4,3" -d "0,0,0,0,0,0" -s $SLURM_ARRAY_TASK_ID
srun python3.7 Main.py -p 100 -m 80 -c 50 -i 100000 -u -f $CHEMIN -l "7,3,5,4,5" -d "0,0,0,0,0,0" -s $SLURM_ARRAY_TASK_ID

echo "Couple"
srun python3.7 Main.py -p 100 -m 80 -c 50 -i 10000 -u -f $CHEMIN -l "8,4,6,5,2" -d "0,0,0,0,0,0" -s $SLURM_ARRAY_TASK_ID
srun python3.7 Main.py -p 100 -m 80 -c 50 -i 10000 -u -f $CHEMIN -l "8,3,6,4,3" -d "0,0,0,0,0,0" -s $SLURM_ARRAY_TASK_ID
srun python3.7 Main.py -p 100 -m 80 -c 50 -i 10000 -u -f $CHEMIN -l "8,3,6,4,5" -d "0,0,0,0,0,0" -s $SLURM_ARRAY_TASK_ID
wait
done