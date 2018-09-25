#!/usr/bin/env bash
# run it in Library dir: bash prepare_Pastec.sh
# After running, chanche the name of "cleanlibrary.fa" to "Projectname_cleanlibrary.fa".
# Then, modify PASTEClassifier_parallelized.cfg

mkdir PASTEC
cd PASTEC

declare -rx  localizaTEpath=/bigdata/castaneralab/shared/marcos/localizaTE-v2

python $localizaTEpath/bin/clean_headers.py ../library_unclassified_sorted_centroids_0.9.fasta > cleanlibrary.fa

#load modules:

module load ncbi-blast
module load repet
module load trf
module load hmmer

#Create symlinks and copy files:

#downloading... 1h aprox
#Copiar en localizaTE-v2
ln -s $localizaTEpath/banks/ProfilesBankForREPET_Pfam27.0_GypsyDB.hmm .
ln -s $localizaTEpath/banks/rRNA_Eukaryota.fsa .
ln -s $localizaTEpath/banks/repbase20.05_ntSeq_cleaned_TE.fa .
ln -s $localizaTEpath/banks/repbase20.05_aaSeq_cleaned_TE.fa .

cp $localizaTEpath/banks/repbase20.05_aaSeq_cleaned_TE.phr .
cp $localizaTEpath/banks/repbase20.05_aaSeq_cleaned_TE.pin .
cp $localizaTEpath/banks/repbase20.05_aaSeq_cleaned_TE.psq .
cp $localizaTEpath/banks/PASTEClassifier_parallelized.cfg .
