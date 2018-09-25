#
# Script to include alias name in every record of TE library and add fungal ClassII reference elements
#
# Usage: python create_final_lib.py alias_name
#

import sys, os, time, config
from Bio import SeqIO

path=str(os.getcwd())
alias=str(sys.argv[1])

def filtrar(infile):
	library=str(infile)
	name=str(library)
	lib=open(library, 'r')
	outname=name.replace('.fa', '_renamed.fa')
	outfile=open(outname, 'w')
	for line in lib:
		line=line.strip()
		if '>' in line:
			header=str(line)
			newheader=header.replace('>', '>'+alias+'_')
			outfile.write(str(newheader)+'\n')
		else:
			outfile.write(str(line)+'\n')


for item in os.listdir(path):
	if 'classified_library.fa' in str(item):
		name=str(item)
		filtrar(name)
time.sleep(5)

for item in os.listdir(path):
	if 'renamed.fa' in str(item):
		name=str(item)
		alias=name.split('_TE')[0]
		newname=alias+'_locTE_v2_RefSeq.fa'
		os.system('cat '+item +' '+ config.localizaTEv2[0]+'databases/ClassII_library.fa > '+newname)
