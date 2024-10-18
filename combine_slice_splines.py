#!/usr/bin/env python

import sys
import numpy as np
from scipy import interpolate
import pickle

def make_avg_spline(phis, fpath, modelnum, detlon, detlat):
    slice_vals_list = []
    for phi in phis:
        phifilepath = fpath+'/slice_spline_%s_%0.3f_%0.3f_%0.3f.npy'%(str(modelnum).zfill(5), phi, detlon, detlat)        
        phifile = np.load(phifilepath)

        plt_x = phifile[0]
        plt_z = phifile[1]
        slicevals = phifile[2]
        slice_vals_list.append(slicevals)
    slice_vals_list = np.array(slice_vals_list)
    slice_avg = np.average(slice_vals_list, axis=0)

    spline_arrs = np.array([plt_x, plt_z, slice_avg])
    return spline_arrs
    #avg_spline = interpolate.LinearNDInterpolator(list(zip(plt_x, plt_z)), slice_avg)
    #return avg_spline

modelnum = int(sys.argv[1])
detlon = float(sys.argv[2])
detlat = float(sys.argv[3])
outpath = str(sys.argv[4])
fpath = outpath+'/splines/'
#fpath = '/users/PAS0654/wluszczak/ensda/splines/'

phis = np.arange(0,360,1)
avg_spline = make_avg_spline(phis, fpath, modelnum, detlon, detlat)
np.save(fpath+'/avg_spline_%s.npy'%(str(modelnum).zfill(5)), avg_spline)
