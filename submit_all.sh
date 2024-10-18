#!/usr/bin/bash

detlon=70.7030029296875
detlat=-9.714359283447266
inputdir=/users/PAS0654/wluszczak/ensda/datafiles/
outdir=/users/PAS0654/wluszczak/ensda/

if ! test -d $outdir/output/; then
  echo "Making output directory" $outdir/output/
  mkdir $outdir/output/
fi

if ! test -d $outdir/splines/; then
  echo "Making splines directory" $outdir/splines/
  mkdir $outdir/splines/
fi


for modelnum in {1..2..1}; do
  model_complete=0
  while [ $model_complete -eq 0 ]; do
    squeue_out=$(squeue -u wluszczak | wc)
    job_count=$(echo $squeue_out | cut -d ' ' -f 1)  
    echo $job_count
    if ((job_count<600)); then
      for ph in {0..360..1}; do
        echo "submitting job " $modelnum $ph
        sbatch --output=/dev/null --error=/dev/null submit_slice_spline.sh $modelnum $ph $detlon $detlat $inputdir $outdir
      done
      model_complete=1
      echo "submitted model" $modelnum
    fi
    sleep 30s
  done
done

part1_complete=0
while [ $part1_complete -eq 0 ]; do
  squeue_out=$(squeue -u wluszczak | wc)
  job_count=$(echo $squeue_out | cut -d ' ' -f 1)
  if [ $job_count -eq 1 ]; then
    part1_complete=1
    echo "all slices calculated, proceeding with combining"
  fi
  sleep 30s
done


outputdir=$outdir/output/
for modelnum in {1..2..1}; do
  sbatch submit_combine_slices.sh $modelnum $detlon $detlat $outdir
  strnum=$(printf "%05g" $modelnum)
  if ! test -d $outputdir/$strnum/; then
    echo "Making output directory" $outputdir/$strnum
    mkdir $outputdir/$strnum
  fi
done

for modelnum in {1..2..1}; do
  model_complete=0
  while [ $model_complete -eq 0 ]; do
    squeue_out=$(squeue -u wluszczak | wc)
    job_count=$(echo $squeue_out | cut -d ' ' -f 1)
    echo $job_count
    if ((job_count<900)); then
      echo "Submitting jobs for model" $modelnum
      for th in {5..81..5}; do
        sbatch submit_muflux_calc.sh $modelnum $th $outdir
      done
      model_complete=1
    fi
  done
done


muflux_complete=0
while [ $muflux_complete -eq 0 ]; do
  squeue_out=$(squeue -u wluszczak | wc)
  job_count=$(echo $squeue_out | cut -d ' ' -f 1)
  if [ $job_count -eq 1 ]; then
    muflux_complete=1
    echo "all mufluxes calculated, proceeding with combining"
  fi
  sleep 30s
done


for modelnum in {1..2..1}; do
  sbatch submit_combine_muflux.sh $modelnum $outdir
done

echo "Finished everything"
