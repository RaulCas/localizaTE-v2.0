#PBS -l nodes=1:ppn=8,mem=16gb,walltime=12:00:00 -q batch -j oe -N mcl

module load ncbi-blast
module load mcl

cd $PBS_O_WORKDIR 

#makeblastdb -in all.fasta -out test.db -dbtype prot -parse_seqids;

#blastp -query ./all.fasta -db ./test.db -evalue 0.0000000000000000000000001 -num_threads 8 -outfmt 6 > output

mcl blast.uniq.out.mci -I 2 -use-tab blast.uniq.out.tab

