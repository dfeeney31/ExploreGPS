from fitparse import FitFile
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import scipy
from scipy import signal
import mplleaflet
import seawater as sw


fitfile = FitFile('/Users/danielfeeney/python-fitparse/Tempo.FIT')
#fitfile = FitFile('/Users/danielfeeney/python-fitparse/Cycling.fit')

cadence = []
dist_1 = []
hr_1 = []
pos_lat = []
pos_long = []
speed_1 = []
time_stp = []
hr = []
altitude_1 = []
power = []


for record in fitfile.get_messages('record'):
    for record_data in record:
        if record_data.name == 'enhanced_speed':
            speed_1.append(record_data.value)
        if record_data.name == 'position_lat':
            pos_lat.append(record_data.value)
        if record_data.name == 'position_long':
            pos_long.append(record_data.value)
        if record_data.name == 'timestamp':
            time_stp.append(record_data.value)
        if record_data.name == 'cadence':
            cadence.append(record_data.value)
        if record_data.name == 'distance':
            dist_1.append(record_data.value)
        if record_data.name == 'heart_rate':
            hr.append(record_data.value)
        if record_data.name == 'altitude':
            altitude_1.append(record_data.value)
        if record_data.name == 'power':
            power.append(record_data.value)
        else:
            pass

#Cycling
df = pd.DataFrame(
    {'Time': time_stp,
     'Speed': speed_1,
     'Distance': dist_1,
     'Power': power,
     'Elevation': altitude_1
    })

len_lat = len(pos_lat)
time_ltd = time_stp[0:len_lat]
speed_ltd = speed_1[0:len_lat]

map_df = pd.DataFrame(
    {'Time': time_ltd,
     'Latitude': pos_lat,
     'Longitude': pos_long,
     'Speed': speed_ltd
    })
map_df['Latitude'] = map_df['Latitude']*(180/(2**31))
map_df['Longitude'] = map_df['Longitude']*(180/(2**31))

#use lat and longitude to get map. Not correctly implemented yet
_, angles = sw.dist(map_df['Latitude'], map_df['Longitude'])
angles = np.r_[0, np.deg2rad(angles)]

# Normalize the speed to use as the length of the arrows
r = map_df['Speed'] / map_df['Speed'].max()
kw = dict(window_len=31, window='hanning')
map_df['u'] = r * np.cos(angles)
map_df['v'] = r * np.sin(angles)

fig, ax = plt.subplots()
map_df = map_df.dropna()
ax.plot(map_df['Longitude'], map_df['Latitude'],
        color='deepskyblue', linewidth=5, alpha=0.5)
sub = 10
#ax.quiver(map_df['Longitude'][::sub], map_df['Latitude'][::sub], map_df['u'][::sub], map_df['v'][::sub], color='deepskyblue', alpha=0.8, scale=10)

# Just plot longitude vs. latitude
ax = plt.plot(map_df.Longitude, map_df.Latitude, 'b') # Draw blue line
mplleaflet.show()

#end of mapping segment.

#Cycling here
fig=plt.figure(figsize=(12, 9), dpi= 80, facecolor='w', edgecolor='k')
fig.suptitle('Tempo Efforts', fontsize=16)
ax = fig.add_subplot(111, axisbg = 'black')
ax.plot(df['Time'].values, df['Elevation'], color = 'white', zorder = 1)
ax.set_ylabel('Elevation', size = 16, color = 'black')
ax.set_xlabel('Time', size = 16, color = 'black')
ax.yaxis.grid(color='white', linewidth=0.5, zorder = 0)
ax2 = ax.twinx()
ax2.plot(df['Time'].values, df['Power'], color = 'red', zorder = 2)
ax2.set_ylabel('Power (W)', size = 16, color = 'black')

tmp_0 = mpatches.Patch(color='white', label='Elevation (m)')
#tmp_1 = mpatches.Patch(color='red', label='Heart Rate')
tmp_2 = mpatches.Patch(color='red', label='Power (W)')
ax.legend(handles=[tmp_0,tmp_2], loc=2)
plt.show()
