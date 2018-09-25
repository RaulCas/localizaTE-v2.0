
# ================================================================================================================
# Prints REpet library with information about TE superfamily (blastx) in the fasta headers - requires classif file in dir -
# Usage -- python GetclassifiedLibrary.py Library classif_file
# ================================================================================================================

import sys
from Bio import SeqIO

library=open(sys.argv[1], 'r')          #   Library
class_file=open(sys.argv[2], 'r')       #   Classif file
out1=open('classified_library.fa', 'a+')
out2=open('unknown_elements.fa', 'a+')
               
 
loop=class_file.readlines()


for record in SeqIO.parse(library, 'fasta'):
	seqname=str(record.id)
	sequence=str(record.seq)
	for item in loop:
		name_class=str(item.split('\t')[0])
		te_class=str(item.split('\t')[4])
		order=str(item.split('\t')[5])
		completeness=str(item.split('\t')[3])
		description=str(item.split('\t')[7])
		if seqname == name_class:
			# Remove non-TE repeats, redirect chimeric elements and true helitrons
			if completeness == 'PotentialChimeric':
				out1.write('>'+seqname+'#'+order+'/PotentialChimeric'+'\n'+sequence+'\n')
			elif order == 'Helitron' and 'TE_BLRx' not in description:  
				if 'Helitron' in description:
					out1.write('>'+seqname+'#'+'ClassII/Helitron'+'\n'+sequence+'\n')
				elif 'PIF1_NA_HEL' in description:
					out1.write('>'+seqname+'#'+'ClassII/Helitron'+'\n'+sequence+'\n')
				else:
					out2.write('>'+seqname+'#'+order+'/Unknown'+description)
			elif order == 'SSR':
				out2.write('>'+seqname+'#SSR'+description)
			elif order == 'PotentialHostGene':
				out2.write('>'+seqname+'#PotentialHostGene'+description)
			else:	
				# Classification at the SUPERFAMILY level
				if 'TE_BLRx' in description:	
					fam=description
					family=fam.split(':')[4]
					if order == 'Helitron':
						out1.write('>'+seqname+'#'+'ClassII/Helitron'+'\n'+sequence+'\n')
					else:
						out1.write('>'+seqname+'#'+order+'/'+str(family)+'\n'+sequence+'\n')
				# Classification  at the ORDER level  
				elif order != 'noCat':			
					if te_class == 'I' and order == 'LTR': 
						out1.write('>'+seqname+'#LTR/Unknown'+'\n'+sequence+'\n')
					elif te_class == 'I' and order == 'DIRS': 
						out1.write('>'+seqname+'#DIRS/Unknown'+'\n'+sequence+'\n')
					elif te_class == 'I' and order == 'PLE': 
						out1.write('>'+seqname+'#PLE/Unknown'+'\n'+sequence+'\n')
					elif te_class == 'I' and order == 'LINE': 
						out1.write('>'+seqname+'#LINE/Unknown'+'\n'+sequence+'\n')
					elif te_class == 'I' and order == 'SINE': 
						out1.write('>'+seqname+'#SINE/Unknown'+'\n'+sequence+'\n')
					elif te_class == 'II' and order == 'MITE':
						out1.write('>'+seqname+'#TIR/MITE'+'\n'+sequence+'\n')
					elif te_class == 'II' and order == 'TIR':
						out1.write('>'+seqname+'#TIR/Unknown'+'\n'+sequence+'\n')
					elif te_class == 'II' and order == 'Maverick':
						out1.write('>'+seqname+'#Maverick/Unknown'+'\n'+sequence+'\n')
					elif te_class == 'II' and order == 'Helitron':
						out1.write('>'+seqname+'#Helitron/Unknown'+'\n'+sequence+'\n')
					elif te_class == 'II' and order == 'Crypton':
						out1.write('>'+seqname+'#Crypton/Unknown'+'\n'+sequence+'\n')
					else:
						out1.write('>'+seqname+'#Class'+te_class+'/'+order+'\n'+sequence+'\n')
				#  Classification  at the CLASS level 
				elif order == 'noCat':						
					if te_class == 'I':
						out1.write('>'+seqname+'#'+'ClassI/Unknown'+'\n'+sequence+'\n')
					if te_class == 'II':	
						out1.write('>'+seqname+'#'+'ClassII/Unknown'+'\n'+sequence+'\n')				
					if te_class == 'noCat': 
						out2.write('>'+seqname+'#'+order+'/Unknown'+description)

class_file.close()
library.close()
out1.close()
out2.close()
