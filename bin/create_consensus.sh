#!/usr/bin/env bash

# run it in Project_dir folder

module load usearch

cd LTR/
mkdir Consensus 			 # create folder
cp libraryLTRs.fasta Consensus/

cd Consensus/
usearch -sortbylength libraryLTRs.fasta -fastaout libraryLTRs_sorted.fasta
usearch --cluster_fast libraryLTRs_sorted.fasta -strand both -id 0.8 -consout LTR_consensus.fasta

cd ../../   # Folder del mongo

mkdir Library
cd Library/

cat ../LTR/Consensus/LTR_consensus.fasta ../RModeler/"$1"/consensi.fa > library_unclassified.fa

usearch -sortbylength library_unclassified.fa -fastaout library_unclassified_sorted.fasta
usearch --cluster_fast library_unclassified_sorted.fasta -strand both -id 0.9 -centroids library_unclassified_sorted_centroids_0.9.fasta
