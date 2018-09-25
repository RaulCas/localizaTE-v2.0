# README

## Install requirements

$ sudo pip install -r requirements.txt

## Launch localizaTE-v2

1. Edit config.py
2. Launch LTR
3. Launch Rmodeler
4. Create Consensues
5. Launch Pastec
6. Launch RepeatMasker
7. Get Statistics
8. Obtain anotation in gff format
9. Reconstruct fragments

1. Edit config.py

declare -rx localizaTEpath=/bigdata/castaneralab/shared/marcos/localizaTE-v2
declare -rx projectPath=/bigdata/castaneralab/shared/marcos/slurm/pleos7
declare -rx projectName=pleostest
declare -rx projectFile=$projectName.fa

. $localizaTEpath/setEnv.sh


2. Launch LTR with interactive session

2.1. Launch LTR with SLURM
sbatch -p batch $localizaTEpath/launchLTR.sh

3. Launch runRModeler
python $localizaTEpath/launchRmodeler.py $projectFile & 

3.1 Vamos a buscar el nombre del directorio"RM" en el que se nos han guardado las coasa

rmFolder="$(find RModeler/ -type d | grep "RM_" | head -n 1 | cut -d'/' -f2)"

# in Project folder: et:20 sec
# SLURM:OK
# with slurm takes litle longer couse the time waiting to start execution
sbatch -p batch $localizaTEpath/bin/create_consensus.sh $rmFolder 

4. Launch PASTEC
# SLURM:OK
# in library folder: et:100 sec
# IMPORTANT: RUN IN Library Folder
bash $localizaTEpath/bin/prepare_pastec.sh

sbatch -p batch $localizaTEpath/bin/prepare_pastec.sh

#adapt configfile and run PASTEC (project name and project dir)
# renamee cleanlibrary.fa --> projectName.fa
# et 10'
#editing for execution through slurm

    # first of all we must adapt configfile 
        module unload python/2.7.5
        module load python/3.4.3
        python3 adaptConfigFile.py projectDir $projectPath/Library/pastec
        python3 adaptConfigFile.py projectName $projectName
        
        

        
    # second, rename cleanlibrary.fa --> projectName.fa
        cp cleanlibrary.fa $projectFile
    
    # third, edit PASTEClassigier.py to lauch though slurm like launchLTR

nohup PASTEClassifier.py -i $projectFile -C PASTEClassifier_parallelized.cfg -p &

#get classified library:
# Manually revise the "unknown_elements.txt" file to be sure nothing is left and obtain final library, including reference fungal ClassII elements

python $localizaTEpath/bin/GetclassifiedLibrary.py cleanlibrary.fa $projectName.classif
python $localizaTEpath/bin/create_final_lib.py $projectName

# ...* renamed.fa: Libraries with their own seqs, with aliasname included
# ...* _locTE_v2_RefSeq.fa: Final libraries with elements from *renamed + ClassII
# Final libraries: $projectPath/FINAL/

6. Launch RepeatMasker
sbatch -p intel $localizaTEpath/bin/run_repeatmasker.sh \
$projectPath/pleostest.fa \
$projectPath/FINAL/classified_library_renamed.fa_locTE_v2_RefSeq.fa \
pleostest


RepeatMasker -pa 12 -s -e ncbi -frag 40000 -gff -lib $projectPath/FINAL/classified_library_renamed.fa_locTE_v2_RefSeq.fa $projectPath/pleostest.fa
