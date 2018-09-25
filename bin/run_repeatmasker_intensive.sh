#!/bin/sh
#SBATCH --nodes=1
#SBATCH --ntasks=24
#SBATCH --mem=32G
#SBATCH --time=36:00:00   
#SBATCH --job-name="Repeatmasker1"


#alias="$1"
#library="$2"
#folder="$3"

cd $SLURM_SUBMIT_DIR 

mkdir "$3" 

cd "$3"

module load RepeatMasker
module load ncbi-blast

RepeatMasker -pa 24 -s -e ncbi -frag 40000 -gff -lib "$2" "$1"

