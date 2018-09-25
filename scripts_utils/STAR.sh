#!/bin/bash -l

#SBATCH --nodes=1
#SBATCH --ntasks=12
#SBATCH --mem=24G 
#SBATCH --time=0-08:00:00
#SBATCH --output=out.txt
#SBATCH --job-name="STAR"


module load STAR


cd $SLURM_SUBMIT_DIR


STAR --genomeDir /bigdata/castaneralab/shared/RNAseq_mon/FastqFiles_NS068_Ramirez_RNAseq_Reads/database --outReadsUnmapped Fastx --outFilterMismatchNoverLmax 0.04 --outFilterMultimapNmax 1 --readFilesIn $SLURM_SUBMIT_DIR/"$1" $SLURM_SUBMIT_DIR/"$2" --outSAMtype BAM SortedByCoordinate

