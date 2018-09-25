
#
#  Usage: python remove_contigs.py genome.fasta outfile.fasta size (nt)
#


import sys
from Bio import SeqIO
from Bio.Seq import Seq


genoma=open(sys.argv[1], 'r')
output=open(sys.argv[2], 'w')
size=int(sys.argv[3])


x=0
for record in SeqIO.parse(genoma, 'fasta'): 
    if len(record.seq) > size:
        x+=1
        output.write('>'+str(record.id)+'\n'+str(record.seq)+'\n')
print x
output.close()
genoma.close()

