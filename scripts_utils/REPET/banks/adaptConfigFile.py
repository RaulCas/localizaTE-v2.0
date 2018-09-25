#!/usr/bin/env python3
import fileinput, sys

fileToSearch="PASTEClassifier_parallelized.cfg"
textToSearch =str(sys.argv[1])
textToReplace=str(sys.argv[2])

with fileinput.FileInput( fileToSearch, inplace=True, backup='.bak') as file:
    for line in file:
        print(line.replace( textToSearch,textToReplace), end='')
