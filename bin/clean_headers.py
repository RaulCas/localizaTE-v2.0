import sys
from Bio import SeqIO
from Bio.Seq import Seq


infile=open(sys.argv[1], 'r')

for record in SeqIO.parse(infile, 'fasta'): 
	print'>'+str(record.id)+'\n'+str(record.seq)
