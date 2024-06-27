import requests
from skyfield.api import Loader, EarthSatellite
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

response = requests.get('https://www.celestrak.com/NORAD/elements/stations.txt')
tle_data = response.text.splitlines()

name = tle_data[0].strip()
line1 = tle_data[1].strip()
line2 = tle_data[2].strip()

load = Loader('./skyfield-data')
ts = load.timescale()
satellite = EarthSatellite(line1, line2, name, ts)

times = ts.utc(2023, 6, range(1, 24))  
geocentric_positions = satellite.at(times)

x = geocentric_positions.position.km[0]
y = geocentric_positions.position.km[1]
z = geocentric_positions.position.km[2]

#สร้างกราฟ3มิติ
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

#วาดวงโคจร
ax.plot(x, y, z, label=name)
ax.scatter([0], [0], [0], color='yellow', s=100, label='Earth')

ax.set_xlabel('X (km)')
ax.set_ylabel('Y (km)')
ax.set_zlabel('Z (km)')
ax.set_title('Satellite Orbit in 3D')
ax.legend()

plt.show()
