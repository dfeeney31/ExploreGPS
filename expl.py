import gpxpy
import os
import matplotlib.pyplot as plt
import mplleaflet
import numpy as np
import seawater as sw
from pandas import DataFrame

os.chdir('/Users/danielfeeney/Documents/DataScience/GPSfiles')
gpx_file = open('Eldo_yo.gpx', 'r')
gpx = gpxpy.parse(gpx_file)

lat = []
lon = []

for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            lat.append(point.latitude)
            lon.append(point.longitude)

%matplotlib inline



data = []
segment_length = segment.length_3d()
for point_idx, point in enumerate(segment.points):
    data.append([point.longitude, point.latitude,
                 point.elevation, point.time, segment.get_speed(point_idx)])

columns = ['Longitude', 'Latitude', 'Altitude', 'Time', 'Speed']
df = DataFrame(data, columns=columns)
df.head()
df.Speed

_, angles = sw.dist(df['Latitude'], df['Longitude'])
angles = np.r_[0, np.deg2rad(angles)]

# Normalize the speed to use as the length of the arrows
r = df['Speed'] / df['Speed'].max()
kw = dict(window_len=31, window='hanning')
df['u'] = r * np.cos(angles)
df['v'] = r * np.sin(angles)

fig, ax = plt.subplots()
df = df.dropna()
ax.plot(df['Longitude'], df['Latitude'],
        color='deepskyblue', linewidth=5, alpha=0.5)
sub = 10
ax.quiver(df['Longitude'][::sub], df['Latitude'][::sub], df['u'][::sub], df['v'][::sub], color='deepskyblue', alpha=0.8, scale=10)

# Just plot longitude vs. latitude
ax = plt.plot(df.Longitude, df.Latitude, 'b') # Draw blue line
mplleaflet.show()
