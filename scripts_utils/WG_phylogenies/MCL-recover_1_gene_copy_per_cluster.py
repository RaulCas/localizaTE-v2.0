#get genomes present within clusters file, then search for clusters containing at least one gene copy per genome per clusters, takes clusters file as sys.argv[1], AA-seq file (containing all AA seqs used in clustering) as sys.argv[2], and max number of missing taxa per cluster as sys.argv[3], write 'yes' as sys.argv[4] if you want to collect a single copy for each genome from large clusters, write 'no' if not requested, add a file of tab delimited dbIds as sys.argv[5] if you only want a subset of a larger clustering run <- currently untested
import sys, string, os
from Bio import SeqIO

dbIds_fasta=[]
for gene in SeqIO.parse(open(sys.argv[2]), 'fasta'):
	gene_split = string.split(gene.id, '|')
	if gene_split[1] not in dbIds_fasta:
		dbIds_fasta.append(gene_split[1])
print 'genomes in sequence_file: %s' % (' '.join(dbIds_fasta))
dbIds = []
infile = open(sys.argv[1]).readlines()
for line in infile:
	split = string.split(line, '\t')
	for gene in split:
		if string.strip(string.split(gene, ':')[0], '\n') not in dbIds:
			dbIds.append(string.split(gene, ':')[0])
print 'total number of genomes: %i' % (len(dbIds))
print 'dbIds in clustering run: '
number_of_genomes = len(dbIds)
a = ' '.join(dbIds)
print a
a = sorted(dbIds)
b = sorted(dbIds_fasta)
if ' '.join(a) != ' '.join(b):
	print 'Warning: dbIds in fasta file differ from cluster file, collecting clusters only for dbIds from fasta file'
	dbIds=dbIds_fasta
keepers = []
if sys.argv[4] == 'yes':
	print 'looking in big clusters'
	for index, line in enumerate(infile):
		dbIds_per_line = []
		genes_per_line = []
		split = string.split(line, '\t')
		if len(split) < 6*number_of_genomes: #if cluster is not huge
			for gene in split:
				if string.strip(string.split(gene, ':')[0], '\n') not in dbIds_per_line:
					genes_per_line.append(gene)
					dbIds_per_line.append(string.strip(string.split(gene, ':')[0], '\n'))
		if len(genes_per_line) >= len(dbIds) - int(sys.argv[3]):
			count = 1
			for db in dbIds:
				if db in dbIds_per_line:
					count += 1
			if count >= len(dbIds)-int(sys.argv[3]):
				keepers.append('%i\t%s\t' % (index, '\t'.join(genes_per_line)))
	all = '\t'.join(keepers)
else:
	print 'collection from large clusters not requested - continuing with only single copy genes'
	for index, line in enumerate(infile):
		dbIds_per_line = []
		genes_per_line = []
		split = string.split(line, '\t')
		if len(split) < 6*number_of_genomes:
			for gene in split:
				if string.strip(string.split(gene, ':')[0], '\n') not in dbIds_per_line:
					genes_per_line.append(gene)
					dbIds_per_line.append(string.strip(string.split(gene, ':')[0], '\n'))
		if len(dbIds_per_line) == len(split) and len(genes_per_line) >= len(dbIds) - int(sys.argv[3]): #additional criteria of having only single copy genes saved
			count = 1
			for db in dbIds:
				if db in dbIds_per_line:
					count += 1
			if count >= len(dbIds)-int(sys.argv[3]):
				keepers.append('%i\t%s\t' % (index, '\t'.join(genes_per_line)))
	all = '\t'.join(keepers)
all_seqs = []
print len(keepers)
for gene in SeqIO.parse(open(sys.argv[2]), 'fasta'):
	gene_split = string.split(gene.id, '|')
	renamed_gene = '%s:%s:%s' % (gene_split[1], gene_split[2], gene_split[0])
	if renamed_gene in all:
		all_seqs.append([gene.id, gene.seq, renamed_gene])
cls_file = open('keepers.cls', 'w')
for line in keepers:
	cls_file.write('%s\n' % (string.strip(line, '\n\t' '\n')))
	split = string.split(line, '\t')
	outfile = open('%s-AA.cluster' % (split[0]), 'w')
	for gene in split[1:]:
		for sequences in all_seqs:
			try:
				if '%s\t' % (string.strip(gene, '\n')) == '%s\t' % (sequences[2]) and '%s\t' % (string.strip(gene, '\n')) in subset_desired:
					outfile.write('>%s\n%s\n' % (sequences[2], sequences[1]))
			except:
				if '%s\t' % (string.strip(gene, '\n')) == '%s\t' % (sequences[2]):
					outfile.write('>%s\n%s\n' % (sequences[2], sequences[1]))