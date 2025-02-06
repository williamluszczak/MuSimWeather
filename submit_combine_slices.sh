#!/usr/bin/bash

#SBATCH --job-name=combine_slice_$1_$2_$3
#SBATCH --mem=5gb
#SBATCH --time=1:00:00

echo "starting slice combiner" $1 $2 $3
#cd /users/PAS0654/wluszczak/ensda/
python3 combine_slice_splines.py $1 $2 $3 $4
retVal=$?
if [ $retVal -eq 0 ]; then
    echo "cleaning up old files" $modelnum
    #rm $4/splines/slice_spline_$(printf "%05g" $1)*.npy
fi
echo "finished combining slices" $1 $2 $3
