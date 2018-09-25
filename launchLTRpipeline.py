

# Usage: python launchLTRpipeline.py genome.fa
# First set enviroment with setEnv.sh
# Extracts LTRs and retains those with retrotranson domains (based on blastx hits to repbase)

import config, os, sys, time
from Bio import SeqIO
from Bio.Seq import Seq

#####################  Functions ##################################

def wait(filename, seconds):
	size1=os.system("du -h -b *"+filename+" | awk '{print $1}'")
	time.sleep(seconds)
	size2=os.system("du -h -b *"+filename+" | awk '{print $1}'")
	if str(size1) == str(size2):
		print "Blastx finished"
    	else:
		while str(size1) != str(size2):
			print "Blast still working: "+str(time.asctime( time.localtime(time.time()) ))

#####################   LTRharvest    ############################

projectname=str(sys.argv[1])

print '..Running LTRharvest'

# Step 2 - get paths, make dirs
Projectdir=str(os.getcwd())
scriptdir= config.localizaTEv2[0]+'bin/' # PATH/TO/BIN
LTRdir='LTR'
os.mkdir(LTRdir)
os.chdir(LTRdir)
genomeFile=str(Projectdir+'/'+str(sys.argv[1]))
os.symlink(genomeFile, "genome.fa")

# Step 2.1 rename scaffolds

cmd1= 'python '+scriptdir+'renameHeaders.py'
os.system(cmd1)

# Step 2.2. Run LTRharvest

cmd2= 'gt suffixerator -db genome_filtered.fa -indexname genome.fsa -tis -suf -lcp -des -ssp -sds -dna'
os.system(cmd2)

cmd3= 'gt ltrharvest -index genome.fsa -seed 30 -xdrop 5 -mat 2 -mis -2 -ins -3 -del -3 -minlenltr 100 -maxlenltr 1000 mindistltr 1000 -maxdistltr 15000 -similar 90.0 -overlaps all -mintsd 5 -maxtsd 20 -motif tgca -motifmis 0 -vic 60 -out > ltrharvest.out'
os.system(cmd3)

# Step 2.3. Extract fastas

print '...Extracting fastas'

cmd4= 'python '+scriptdir+'extract_ltr.py'
os.system(cmd4)

#####################   BLASTX    ############################

print '.......Running BLASTX'

os.system('blastx -query LTRs.fasta -db '+config.localizaTEv2[0]+'repbase/testdb -evalue 0.00001 -max_target_seqs 1 -outfmt 6 -out blastx.out')

wait("blastx.out", 90)

os.system("grep '#LTR/' blastx.out | awk '{print $1}' | uniq > LTR_with_domains.txt")

infile=open('LTR_with_domains.txt', 'r')
infile2=open('LTRs.fasta', 'r')
outfile2=open('libraryLTRs.fasta', 'w')

recorrido=infile.readlines()

for record in SeqIO.parse(infile2, 'fasta'):
	for line in recorrido:
		line=line.strip()
		if record.id == line:
			outfile2.write('>'+str(record.id)+'\n'+str(record.seq)+'\n')
			print record.id

infile.close()
infile2.close()
outfile2.close()
