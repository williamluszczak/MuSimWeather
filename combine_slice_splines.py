#!/usr/bin/env python

import sys
import numpy as np
from scipy import interpolate
import pickle

def make_avg_spline(phis, fpath, modelnum, detlon, detlat):
    splinedict_filepath = fpath+'slice_splines_%s_%0.3f_%0.3f.npy'%(str(modelnum).zfill(5), detlon, detlat)
    splinedict_file = np.load(splinedict_filepath, allow_pickle=True)
    splinedict = splinedict_file.item()
    
    slice_vals_list = []
    for phi in phis:
        print(phi)
        slice_spline = splinedict[phi]
        xvals = np.linspace(0,5000,100)
        zvals = np.linspace(0,25,100)

        arr_x = []
        arr_z = []
        slicevals = []
        for x in xvals:
            for z in zvals:
                arr_x.append(x)
                arr_z.append(z)
                splineval = slice_spline(x,z)
                if np.isnan(splineval):
                    slicevals.append(0.)
                else:
                    slicevals.append(splineval)
        outarr = np.array([arr_x, arr_z, slicevals])

        plt_x = outarr[0]
        plt_z = outarr[1]
        slicevals = outarr[2]
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
