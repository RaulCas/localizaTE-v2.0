#!/bin/sh
#SBATCH --nodes=1
#SBATCH --ntasks=12
#SBATCH --mem=18G
#SBATCH --time=12:00:00
#SBATCH --job-name="Repeatmasker1"


#alias="$1"
#library="$2"
#folder="$3"

cd $SLURM_SUBMIT_DIR

mkdir "$3"

#mv "$1" "$3"
#mv "$2" "$3"

cd "$3"

module load RepeatMasker
module load ncbi-blast

RepeatMasker -pa 12 -s -e ncbi -no_is -frag 40000 -gff -lib "$2" "$1"
