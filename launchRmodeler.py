#
# Usage: python launchRmodeler.py genome.fa
# FIRST OF ALL: Set your enviroment with setEnv.sh
# Creates RM database and qsubs the job

import sys ,os ,shutil ,config

projectname=str(sys.argv[1])

# Step 1 - get paths, make dirs and buid RepeatModeler database

Projectdir=str(os.getcwd())
scriptdir=Projectdir+'/bin/'
RMOdir='RModeler'
os.mkdir(RMOdir)
os.chdir(RMOdir)
genomeFile=str(Projectdir+'/'+str(sys.argv[1]))
os.symlink(genomeFile, "genome.fa")

# Step 1.1 buid RepeatModeler database

cmd = 'bash '+config.localizaTEv2[0]+'bin/makedb.sh genome.fa'
os.system(cmd)

# Step 1.2 run RepeatModeler

shutil.copy2(config.localizaTEv2[0]+'bin/runRModeler.sh', './runRModeler.sh')
cmd = 'sbatch -p batch runRModeler.sh'
os.system(cmd)
