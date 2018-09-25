#!/bin/bash -l

## USAGE: sbatch -p batch launchLTR.sh
#SBATCH --nodes=1
#SBATCH --ntasks=12
#SBATCH --mem=16G
#SBATCH --time=1:00:00
#SBATCH --output=output
#SBATCH --mail-type=ALL
#SBATCH --job-name="LTRpipeline"

module load Python

declare -rx localizaTEpath=/bigdata/castaneralab/shared/marcos/localizaTE-v2
declare -rx projectPath=/bigdata/castaneralab/shared/marcos/slurm/pleos6
declare -rx projectName=pleostest
declare -rx projectFile=$projectName.fa

. $localizaTEpath/setEnv.sh


##source /scratch/.../env/bin/activate

srun python $localizaTEpath/launchLTRpipeline.py $projectFile

## srun python3 script.py
## deactivate
