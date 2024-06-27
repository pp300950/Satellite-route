import requests
from skyfield.api import Loader, EarthSatellite, Topos
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from datetime import datetime, timedelta

response = requests.get('https://www.celestrak.com/NORAD/elements/stations.txt')
tle_data = response.text.splitlines()

name = tle_data[0].strip()
line1 = tle_data[1].strip()
line2 = tle_data[2].strip()

load = Loader('./skyfield-data')
ts = load.timescale()
satellite = EarthSatellite(line1, line2, name, ts)

times = ts.utc(2024, 6, 26, range(0, 24, 1))
geocentric_positions = satellite.at(times)

latitudes, longitudes = geocentric_positions.subpoint().latitude.degrees, geocentric_positions.subpoint().longitude.degrees

fig, ax = plt.subplots(figsize=(12, 8))
m = Basemap(projection='mill', resolution='c', ax=ax)

m.drawcoastlines()
m.drawcountries()
m.drawmapboundary()

x, y = m(longitudes, latitudes)

#วาดเส้นทางการบิน
m.plot(x, y, marker=None, color='r')

current_time = datetime.utcnow()
end_time = current_time + timedelta(hours=24)
current_time = current_time.replace(tzinfo=None)
end_time = end_time.replace(tzinfo=None)
m.nightshade(current_time)
m.nightshade(end_time)

plt.title(f'Satellite Path and Day/Night on {current_time.strftime("%Y-%m-%d")}')
plt.show()
