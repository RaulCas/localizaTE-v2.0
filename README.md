

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


### 1. Edit config.py

declare -rx localizaTEpath=/bigdata/castaneralab/shared/marcos/localizaTE-v2
declare -rx projectPath=/bigdata/castaneralab/shared/marcos/slurm/pleos6
declare -rx projectName=pleostest
declare -rx projectFile=$projectName.fa

. $localizaTEpath/setEnv.sh


### 2. Launch LTR
```bash
# Start Interactive session
srun --pty bash -i
# srun --x11 --mem=6gb --cpus-per-task 8 --ntasks 1 --time 3:00:00 --pty bash -i
# exit --> exit from interactive session

touch nohup.out && nohup python $localizaTEpath/launchLTRpipeline.py $projectFile &
```


### 3. Launch runRModeler
```bash
python $localizaTEpath/launchRmodeler.py $projectFile
```

### 4. Create Consensues
```bash
# in Project folder: et:20 sec
bash $localizaTEpath/bin/create_consensus.sh RM_10649.TueApr181106352017 &
```

### 5. Launch PASTEC
````bash
# in library folder: et:100 sec
bash $localizaTEpath/bin/prepare_pastec.sh
````

````bash
#adapt configfile and run PASTEC (project name and project dir)
# renamee cleanlibrary.fa --> projectName.fa
# et 10'
nohup PASTEClassifier.py -i $projectFile -C PASTEClassifier_parallelized.cfg -p &

#get classified library:
# Manually revise the "unknown_elements.txt" file to be sure nothing is left and obtain final library, including reference fungal ClassII elements

python $localizaTEpath/bin/GetclassifiedLibrary.py cleanlibrary.fa $projectName.classif
python $localizaTEpath/bin/create_final_lib.py $projectName

# ...* renamed.fa: Libraries with their own seqs, with aliasname included
# ...* _locTE_v2_RefSeq.fa: Final libraries with elements from *renamed + ClassII
# Final libraries: $projectPath/FINAL/
````

### 6. Launch RepeatMasker
````bash
sbatch -p intel $localizaTEpath/bin/run_repeatmasker.sh \
$projectPath/pleostest.fa \
$projectPath/FINAL/classified_library_renamed.fa_locTE_v2_RefSeq.fa \
pleostest


RepeatMasker -pa 12 -s -e ncbi -frag 40000 -gff -lib $projectPath/FINAL/classified_library_renamed.fa_locTE_v2_RefSeq.fa $projectPath/pleostest.fa

````
