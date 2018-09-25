#PBS -l nodes=1:ppn=8,mem=12gb,walltime=24:00:00 -q batch -j oe -N bbh

module load ncbi-blast

cd $PBS_O_WORKDIR 

python /bigdata/castaneralab/shared/scripts_utils/blast_rbh.py -a prot -t blastp -o output Pleurotus_PC15.fasta uniprot_human_reference.fasta
