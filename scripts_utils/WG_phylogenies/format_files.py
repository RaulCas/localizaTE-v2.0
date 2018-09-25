
# 
#  This script formats protein file and blast.output to the style required for stevens pipeline. Use it before running mcl, just after all_by_all_blast.
# 
#
# Usage: python format_files.py ./fasta_AA.file ./blast_out 
#

import sys
from Bio import SeqIO

fasta_file=open((sys.argv[1]), 'r')
fasta_out=open('all_AA.fasta', 'w')

blast_infile=open((sys.argv[2]), 'r')
blast_out=open('blast.uniq.out.abc', 'w')


def reformat_seqs(infile, outfile):
	for record in SeqIO.parse(infile, 'fasta'):
		gene=str(record.id.strip())
		sequence=str(record.seq.strip())
		gene=gene.split('|')
		outfile.write('>'+gene[2]+'|'+gene[1]+'|'+'FilteredModels'+'\n'+sequence+'\n')
		#print '>'+gene[2]+'|'+gene[1]+'|'+'FilteredModels'

	
def reformat_blast_out(infile, outfile):
	for line in infile.readlines():
		line=line.strip()
		line=line.split('\t')
		query=str(line[0]).split('|')
		hit=str(line[1]).split('|')
		new_query=str(query[1]+':'+'FilteredModels'+':'+query[2])
		new_hit=str(hit[1]+':'+'FilteredModels'+':'+hit[2])
		outfile.write(new_query+'\t'+new_hit+'\t'+line[10]+'\n')
		#print new_query+'\t'+new_hit+'\t'+line[10]

reformat_seqs(fasta_file, fasta_out)
reformat_blast_out(blast_infile, blast_out)
