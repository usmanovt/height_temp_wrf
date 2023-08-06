from netCDF4 import Dataset
from wrf import getvar, interplevel, ll_to_xy
# import numpy as np
import pandas as pd

# Open the NetCDF file
wrfin = Dataset("wrfout_d01.nc")

# Convert the lat/lon coordinates to x/y coordinates
lat = 51.147222
lon = 71.422222
x_y = ll_to_xy(wrfin, lat, lon)
locx = x_y[0]
locy = x_y[1]


res1, res2 = [], []
for time in range(13):
    # Get the WRF variables:
    # height_agl - Model Height for Mass Grid (AGL)
    # tc - Temperature in Celsius
    ht = getvar(wrfin, "height_agl", timeidx=time, units="m")
    tc = getvar(wrfin, "tc", timeidx=time)
    # Interpolate "tc" at 750m and 1500m
    tc_750 = interplevel(tc, ht, 750.0)
    tc_1500 = interplevel(tc, ht, 1500.0)
    # Extract "tc" by x/y coordinates
    tc1 = tc_750[locx][locy]
    tc2 = tc_1500[locx][locy]
    # Append results to lists
    res1.append(tc1.values)
    res2.append(tc2.values)

# Create dataframe    
df = pd.DataFrame()
df['Time'] = [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]
df['750m'] = res1
df['1500m'] = res2
print(df)

# Write csv-file
df.to_csv("df_temp.csv", sep = ';', index = False)
