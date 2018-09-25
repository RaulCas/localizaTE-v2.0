#!/usr/local/bin/python
import commands, os, subprocess, config, time, sys, shutil

# ======================
# Functions
# ======================
def prepareRModeler():
    # Step 1 - get paths, make dirs and buid RepeatModeler database
    Projectdir=config.projectPath[0]
    RMOdir='RModeler'
    os.mkdir(RMOdir)
    os.chdir(RMOdir)
    genomeFile=str(Projectdir+config.projectFile)
    os.symlink(genomeFile, "genome.fa")

    # Step 1.1 buid RepeatModeler database
    cmd = 'bash makedb.sh genome.fa'
    os.system(cmd)

    # Step 1.2 run RepeatModeler
    shutil.copy2(config.localizaTEv2[0]+'bin/runRModeler.sh', './runRModeler.sh')



# ======================
# TE discovery
# ======================
# /bigdata/castaneralab/shared/
# /rhome/rcastanera/bigdata/localizaTE-v2/

#declare -rx localizaTEpath=/bigdata/castaneralab/shared/marcos/localizaTE-v2
#declare -rx projectPath=/bigdata/castaneralab/shared/marcos/slurm/pleos3
#declare -rx projectName=pleostest
#declare -rx projectFile=$projectName.fa
cmd = config.localizaTEv2[0] +"setEnv.sh"
os.system(cmd)

# ssh -x gpisabarro@biocluster.ucr.edu
# submit the first job
#2. Launch LTR
cmd = "touch nohup.out && nohup python "+config.localizaTEv2[0]+"launchLTRpipeline.py "+config.projectFile
os.system(cmd)
## Wait for LTR
nohupFile = config.projectPath[0] + "nohup.out"
print nohupFile
while not os.path.isfile(nohupFile):
    time.sleep(30)

## nohup file exists
## @@TODO: Search for errors

#3. Launch runRModeler
cmd = "sbatch -p batch runRModeler.sh "
print "Submitting: %s" % cmd
status, jobnum = commands.getstatusoutput(cmd)
if (status == 0 ):
    print "runRModeler is %s" % jobnum
else:
    print "Error submitting runRModeler"


4. Launch PASTEC
# SLURM:OK
# in library folder: et:100 sec
# IMPORTANT: RUN IN Library Folder
os.system("bash $localizaTEpath/bin/prepare_pastec.sh")

os.system("sbatch -p batch $localizaTEpath/bin/prepare_pastec.sh")

#adapt configfile and run PASTEC (project name and project dir)
# renamee cleanlibrary.fa --> projectName.fa
# et 10'
#editing for execution through slurm

    # first of all we must adapt configfile 
#        module unload python/2.7.5
#        module load python/3.4.3
        os.system("python3 adaptConfigFile.py projectDir $projectPath/Library/pastec")
        os.system("python3 adaptConfigFile.py projectName $projectName")
        
        
    # second, rename cleanlibrary.fa --> projectName.fa
        os.system("cp cleanlibrary.fa $projectFile")
    
    # third, edit PASTEClassigier.py to lauch though slurm like launchLTR

os.system("nohup PASTEClassifier.py -i $projectFile -C PASTEClassifier_parallelized.cfg -p &")

#get classified library:
# Manually revise the "unknown_elements.txt" file to be sure nothing is left and obtain final library, including reference fungal ClassII elements

os.system(" $localizaTEpath/bin/GetclassifiedLibrary.py cleanlibrary.fa $projectName.classif")
os.system(" $localizaTEpath/bin/create_final_lib.py $projectName")

# ...* renamed.fa: Libraries with their own seqs, with aliasname included
# ...* _locTE_v2_RefSeq.fa: Final libraries with elements from *renamed + ClassII
# Final libraries: $projectPath/FINAL/

#6. Launch RepeatMasker
os.system("sbatch -p intel $localizaTEpath/bin/run_repeatmasker.sh \
$projectPath/pleostest.fa \
$projectPath/FINAL/classified_library_renamed.fa_locTE_v2_RefSeq.fa \
pleostest")


os.system("RepeatMasker -pa 12 -s -e ncbi -frag 40000 -gff -lib $projectPath/FINAL/classified_library_renamed.fa_locTE_v2_RefSeq.fa $projectPath/pleostest.fa	")
	
print "\nCurrent status:\n"
#show the current status with 'sjobs'
#os.system("sjobs")
