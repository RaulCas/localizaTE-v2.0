from Bio import SeqIO
from Bio.Seq import Seq


genoma=open('genome.fa', 'r') 
output=open('genome_filtered.fa', 'w')

x=0
for line in genoma:
    line=line.strip()
    if '>' in str(line):
        x=x+1
        scaf=str(x)
        output.write('>scaffold_'+scaf+'\n')
    else:
        output.write(str(line)+'\n')
output.close() 
genoma.close()
