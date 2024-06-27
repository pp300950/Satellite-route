import requests
from skyfield.api import Loader, EarthSatellite, utc
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.animation import FuncAnimation
import numpy as np

#TLE
response = requests.get('https://www.celestrak.com/NORAD/elements/stations.txt')
tle_data = response.text.splitlines()

name = tle_data[0].strip()
line1 = tle_data[1].strip()
line2 = tle_data[2].strip()
 
load = Loader('./skyfield-data')
ts = load.timescale()
satellite = EarthSatellite(line1, line2, name, ts)

fig, ax = plt.subplots(figsize=(12, 8))
m = Basemap(projection='mill', resolution='c', ax=ax)

m.drawcoastlines()
m.drawcountries()
m.drawmapboundary(fill_color='aqua')

def draw_nightshade(time):
    m.nightshade(time)

positions = []

def update(frame):
    ax.clear()
    m.drawcoastlines()
    m.drawcountries()
    m.drawmapboundary(fill_color='aqua')

    current_time = datetime.utcnow().replace(tzinfo=utc) - timedelta(minutes=30 * frame)
    ax.set_title(f'Satellite Position at {current_time.strftime("%Y-%m-%d %H:%M:%S UTC")}')

    time = ts.utc(current_time)
    geocentric = satellite.at(time)
    subpoint = geocentric.subpoint()

    latitude = subpoint.latitude.degrees
    longitude = subpoint.longitude.degrees
    positions.append((longitude, latitude))
    x, y = m(longitude, latitude)
    m.plot(x, y, marker='o', color='r', markersize=10, label=name)

    if len(positions) > 1:
        lons, lats = zip(*positions)
        x, y = m(lons, lats)
        m.plot(x, y, linestyle='-', color='b', alpha=0.5)

    ax.legend(loc='upper right')

ani = FuncAnimation(fig, update, frames=60, interval=500)

plt.show()
