from netCDF4 import Dataset
from wrf import getvar, interplevel, ll_to_xy, ALL_TIMES
#import numpy as np
import pandas as pd

# Open the NetCDF file
wrfin = Dataset("wrfout_d01.nc")

# Convert the lat/lon coordinates to x/y coordinates
lat = 51.147222
lon = 71.422222
x_y = ll_to_xy(wrfin, lat, lon)
locx = x_y[0]
locy = x_y[1]

# Get the WRF variables:
# height_agl - Model Height for Mass Grid (AGL)
# tc - Temperature in Celsius
ht = getvar(wrfin, "height_agl", timeidx=ALL_TIMES, units="m")
tc = getvar(wrfin, "tc", timeidx=ALL_TIMES)
# Interpolate "tc" at 750m and 1500m
tc_750 = interplevel(tc, ht, 750.0)
tc_1500 = interplevel(tc, ht, 1500.0)
# Extract "tc" by x/y coordinates
tc1 = tc_750[:, locx, locy].values.tolist()
tc2 = tc_1500[:, locx, locy].values.tolist()
print(tc.shape[0])
# Create dataframe    
df = pd.DataFrame()
ntimes = tc.shape[0]
df['Time'] = [x*3 for x in range(ntimes)]
df['750m'] = [round(elem, 1) for elem in tc1]
df['1500m'] = [round(elem, 1) for elem in tc2]
print(df)

