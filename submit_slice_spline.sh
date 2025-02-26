#!/usr/bin/bash

#SBATCH --job-name=slice_spline_$1_$2_$3_$4
#SBATCH --mem=10gb

echo "starting slice spline" $1 $2 $3 $4
python3 make_slice_spline.py $1 $2 $3 $4 $5
echo "finished spline for" $1 $2 $3 $4
