

import os
import time

genoma='genome_filtered.fa'   # Type here the name of the input file
infile=open('ltrharvest.out', 'r')
outfile1=open('listaLTR', 'w')


def filtrar(filename):
        x=0
	for line in filename.readlines():
		if '#' in line:
			pass
		else:
                        x+=1
			dividir=line.split('  ')
			scaffold=int(dividir[-1])+1
			inicio=dividir[0]
			final=dividir[1]
                        name='LTR_'+str(x)+'_'+'scaffold'+str(scaffold)+'_'+str(inicio)+'_'+str(final)
			outfile1.write('scaffold_'+str(scaffold)+'\t'+inicio+'\t'+final+'\t'+name+'\n')

filtrar(infile)
outfile1.close()

time.sleep(5)

print 'extracting elements in fasta'


cmd1= 'bedtools getfasta -fi genome_filtered.fa -bed listaLTR -fo LTRs.fasta -name'
os.system(cmd1)
