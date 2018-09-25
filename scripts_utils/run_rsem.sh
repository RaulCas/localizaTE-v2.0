#PBS -l nodes=1:ppn=8,mem=12gb,walltime=24:00:00 -q batch -j oe -N rsem_PC9_L

module load bowtie
module load rsem
module load samtools

cd $PBS_O_WORKDIR

rsem-calculate-expression --paired-end /rhome/rcastanera/bigdata/RNAseq_luz/Sample_PC9-L/mapeo/PC9_L_R1.fastq /rhome/rcastanera/bigdata/RNAseq_luz/Sample_PC9-L/mapeo/PC9_L_R2.fastq PleosPC9 PC9_L

