#!/usr/bin/env python

import numpy as np
import sys
import math

maxmodelnum = int(sys.argv[1])
fpath = str(sys.argv[2])

summed_mufluxes = []
for modelnum in range(1,maxmodelnum+1):
    combined_muflux = np.load(fpath+'/output/combined_muflux_%s.npy'%(str(modelnum).zfill(5)))
#    print(np.sum(combined_muflux[1]))
    summed_mufluxes.append(np.sum(combined_muflux[1]))


header = """ obs_sequence
obs_type_definitions
          1
          125 MUON_FLUX              
  num_copies:            1  num_qc:            1
  num_obs:            3  max_num_obs:          3
observation                                                     
GSI Quality Control                                             
  first:            1  last:         2
 OBS            1
   100679.998779297     
   1.00000000000000     
          -1           2          -1
obdef
loc3d
     1.845860254193458        0.3658209952390449         100680.0000000000      2
kind
          125
external_FO      {0}       1""".format(maxmodelnum)

footer=""" 21600     152057
   1.69000000000000"""

nrows = math.ceil(len(summed_mufluxes)/3.)
reshaped_arr = []
for i in range(0,int(nrows)):
    rowstart = i*3
    rowend = (i+1)*3
#    print(rowstart, rowend, summed_mufluxes[rowstart:rowend])
    if len(summed_mufluxes[rowstart:rowend])==3:
        reshaped_arr.append(summed_mufluxes[rowstart:rowend])
    else:
        fixedrow = summed_mufluxes[rowstart:rowend]
        while len(fixedrow)<3:
            fixedrow.append(0.)
        reshaped_arr.append(fixedrow)

reshaped_arr = np.array(reshaped_arr)
with open("obs_seq_test.out", "w") as outfile:
    outfile.write(header)
    outfile.write("\n")
    for subarr in reshaped_arr:
        outfile.write("   ")
        for entry in subarr:
            outfile.write("{0:016.12f}        ".format(entry))
        outfile.write("\n")
    outfile.write(footer)
    outfile.write("\n")
