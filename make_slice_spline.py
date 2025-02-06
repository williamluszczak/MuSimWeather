#!/usr/bin/env python

import numpy as np
import sys
import pandas as pd
import geopy.distance
from scipy import interpolate

import time

def make_3d_spline(fpath):
    atm_data = pd.read_pickle(fpath)
    lons = atm_data['longitude (deg E)']
    lats = atm_data['latitude (deg N)']
    hs = atm_data['geopotential height (m)']
    rhos = atm_data['air density (kg/m3)']

    plt_lons = []
    plt_lats = []
    plt_hs = []
    plt_rhos = []

    for ilon in range(0,599,10):
        for ilat in range(0,349,10):
            for ih in range(0,44,1):
                thislat = lats[ilat+5][ilon+5]
                plt_lons.append(lons[ilat+5][ilon+5])
                plt_lats.append(lats[ilat+5][ilon+5])
                plt_hs.append(hs[ih][ilat+5][ilon+5])
                
                bin_values = rhos[ih][ilat:ilat+10,ilon:ilon+10]
                avgd_field = np.average(bin_values)
                plt_rhos.append(avgd_field)

    plt_lons = np.array(plt_lons)
    plt_lats = np.array(plt_lats)
    plt_hs = np.array(plt_hs)/1000.
    plt_rhos = np.array(plt_rhos)
    my_spline = interpolate.LinearNDInterpolator(list(zip(plt_lats,plt_lons,plt_hs)),plt_rhos)
    return my_spline

def make_slice_spline(phi, latlonhspline, detlon, detlat):
    reg_hs = np.linspace(0,25, 100)

    detpos = geopy.Point(detlat, detlon)

    slice_ls = []
    slice_zs = []
    slice_drhos = []

    for l in np.arange(0.,5000.,10):
        d = geopy.distance.geodesic(kilometers = l)
        dest = d.destination(point=detpos, bearing=phi)

        lon = dest.longitude
        lat = dest.latitude

        for h in reg_hs:
            slice_ls.append(l)
            slice_zs.append(h)
            slice_drhos.append(latlonhspline(lat, lon, h))#-latlonhspline(detlat, detlon, h))

    zdrhos = np.array(slice_drhos)

    slice_spline = interpolate.LinearNDInterpolator(list(zip(slice_ls,slice_zs)),zdrhos)
    return slice_spline


modelnum = int(sys.argv[1])
#phi = float(sys.argv[2])
detlon = float(sys.argv[2])
detlat = float(sys.argv[3])
inputdir = str(sys.argv[4])
outdir = str(sys.argv[5])

#this_fpath = '/users/PAS0654/wluszczak/ensda/datafiles/air_density_%s.pkl'%(str(modelnum).zfill(5))
this_fpath = inputdir+'/air_density_%s.pkl'%(str(modelnum).zfill(5))
print("making 3d spline")
full_spline = make_3d_spline(this_fpath)
spline_dict = {}
for phi in np.arange(0,360,1):
    print("making spline for phi", phi)
    slice_spline = make_slice_spline(phi, full_spline, detlon, detlat)
    spline_dict[phi]=slice_spline

#    xvals = np.linspace(0,5000,100)
#    zvals = np.linspace(0,25,100)
#
#    arr_x = []
#    arr_z = []
#    slicevals = []
#    for x in xvals:
#        for z in zvals:
#            arr_x.append(x)
#            arr_z.append(z)
#            splineval = slice_spline(x,z)
#            if np.isnan(splineval):
#                slicevals.append(0.)
#            else:
#                slicevals.append(splineval)
#
#    outarr = np.array([arr_x, arr_z, slicevals])
#    combined_outarr.append(outarr)

#combined_outarr = np.array(combined_outarr)
##splinedir = '/users/PAS0654/wluszczak/ensda/splines/'
splinedir = outdir+'/splines/'
#np.save(splinedir+'slice_spline_%s_%0.3f_%0.3f_%0.3f'%(str(modelnum).zfill(5), phi, detlon, detlat), outarr)
np.save(splinedir+'slice_splines_%s_%0.3f_%0.3f.npy'%(str(modelnum).zfill(5), detlon, detlat), spline_dict)
