# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 14:13:59 2020

@author: Daniel.Feeney
"""

import gpxpy
import os
import matplotlib.pyplot as plt
import mplleaflet
import numpy as np
import seawater as sw
from pandas import DataFrame

os.chdir('C:/Users/Daniel.Feeney/OneDrive - Boa Technology Inc/Desktop/')
gpx_file = open('Current.gpx', 'r')
gpx = gpxpy.parse(gpx_file)

lat = []
lon = []

for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            lat.append(point.latitude)
            lon.append(point.longitude)


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

df['Speedmph'] = df.Speed * 2.23694
plt.plot(df.Speedmph)
plt.ylabel('Speed (mph)')

import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6372800  # Earth radius in meters
    
    phi1, phi2 = math.radians(lat1), math.radians(lat2) 
    dphi       = math.radians(lat2 - lat1)
    dlambda    = math.radians(lon2 - lon1)
    
    a = math.sin(dphi/2)**2 + \
        math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    
    return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))

totDist = []
for index, row in df.iterrows():
    totDist.append(haversine(row['Longitude'], row['Latitude'], df['Longitude'].iloc[index-1], df['Latitude'].iloc[index-1]))
    
np.sum(totDist)
plt.plot(totDist)    
    
