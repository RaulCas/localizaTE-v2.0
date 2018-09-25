#!/usr/bin/env bash
#module load RepeatMasker
module load RepeatModeler

BuildDatabase -name RMdatabase -engine ncbi ${BASH_ARGV[*]}
