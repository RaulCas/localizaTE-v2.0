#!/bin/bash -l


#SBATCH --nodes=1
#SBATCH --ntasks=12
#SBATCH --mem=16G
#SBATCH --time=24:00:00    
#SBATCH --output=output
#SBATCH --mail-type=ALL
#SBATCH --job-name="RM"


cd $SLURM_SUBMIT_DIR

module load RepeatMasker
module load ncbi-blast
module load RepeatScout
module load RECON
module load RepeatModeler

RepeatModeler -database RMdatabase -engine ncbi -pa 11
