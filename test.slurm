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

RANGE=($(ls -1 /home/tsaout/CAB/*))

PARAM_VALUE=${RANGE[$SLURM_ARRAY_TASK_ID]}

echo "c instance $PARAM_VALUE"

srun grep "c " $PARAM_VALUE ; grep "p " $PARAM_VALUE ; grep -v "p " $PARAM_VALUE | grep -v "c " &

wait
