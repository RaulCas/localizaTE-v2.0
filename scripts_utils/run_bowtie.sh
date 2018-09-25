#PBS -l nodes=1:ppn=12,mem=24gb,walltime=24:00:00 -q batch -j oe -N Bowtie_PC15 

module load bowtie

cd $PBS_O_WORKDIR 

bowtie -n 3 -l 15 -e 800 -k 1 TElib -q -1 /rhome/rcastanera/bigdata/review_PLOS/PC9_clean_1.fastq -2 /rhome/rcastanera/bigdata/review_PLOS/PC9_clean_2.fastq -S reads_to_TE.sam
