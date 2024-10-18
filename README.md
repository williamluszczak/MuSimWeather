# MuSimWeather
This is a set of scripts that will take in a set of files containing information about the atmospheric density field, and return maps of the average muon flux as a function of elevation for a user-provided detector location.

Prerequisites (will add version numbers later):
- Geopy (https://geopy.readthedocs.io/en/stable/)
- MCEq (https://github.com/mceq-project/MCEq/tree/master)
- Pandas (https://pandas.pydata.org/)
- Scipy (https://scipy.org/)
- Numpy (https://numpy.org/)

# Instructions
You should only have to interface with the `submit_all` script. Before running this script, you will need to set a few variables:
- `detlon` is the longitude of the simulated muon detector location
- `detlat` is the latitude of the simulated muon detector location
- `inputdir` is the directory containing all the `.pkl` files that have information about the density field for each atmospheric model
- `outdir` is where you want the output files (as well as temporary spline files) to be written. There will be a lot of temporary files written to this directory, but the scripts should autmatically clean up intermediate files at the end
- `username` is your OSC username (used for `squeue` commands)

Once these variables are set, you should just be able to run `./submit_all.sh` to generate your muon flux output. Output `.npy` files describing the average muon flux as a function of declination will be written to `$(outdir)/output/`/ 
 
Note that this will submit a LOT of jobs to the OSC cluster. These scripts include framework for throttling the number of submitted jobs to keep it below the limit of 1000, though if you're running other stuff on the cluster at the same time the checks I have in place might not work as well. I have also not been terribly careful about the amount of resources requested by each job. The settings I have in place seem to work, though I'm pretty sure you could get away with adjusting the `submit*.sh` files to request less memory/runtime. Optimizing this will require some more testing. 
