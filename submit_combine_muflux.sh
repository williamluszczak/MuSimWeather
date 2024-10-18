#!/usr/bin/bash

#SBATCH --job-name=combine_muflux_$1
#SBATCH --account=pas2277
#SBATCH --mem=3gb
#SBATCH --time=1:00:00

echo "starting muflux combiner" $1
python3 combine_muflux_files.py $1 $2
echo "finished combining slices" $1
