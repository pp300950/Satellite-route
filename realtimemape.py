import requests
from skyfield.api import Loader, EarthSatellite
from datetime import datetime
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.animation import FuncAnimation
import numpy as np

response = requests.get('https://www.celestrak.com/NORAD/elements/stations.txt')
tle_data = response.text.splitlines()

#TLE
name = tle_data[0].strip()
line1 = tle_data[1].strip()
line2 = tle_data[2].strip()

#ใช้ Skyfield 
load = Loader('./skyfield-data')
ts = load.timescale()
satellite = EarthSatellite(line1, line2, name, ts)

#สร้างแผนที่โลก
fig, ax = plt.subplots(figsize=(12, 8))
m = Basemap(projection='mill', resolution='c', ax=ax)

#วาดแผนที่โลก
m.drawcoastlines()
m.drawcountries()
m.drawmapboundary(fill_color='aqua')

#ฟังก์ชันวาดพื้นที่ส่วนที่เป็นกลางคืน
def draw_nightshade():
    current_time = datetime.utcnow()
    m.nightshade(current_time)
positions = []

def update(frame):
    ax.clear()
    m.drawcoastlines()
    m.drawcountries()
    m.drawmapboundary(fill_color='aqua')
    draw_nightshade()

    #คำนวณตำแหน่งของดาวเทียมในเวลาปัจจุบัน
    time = ts.now()
    geocentric = satellite.at(time)
    subpoint = geocentric.subpoint()

    #ดึงข้อมูลพิกัดละติจูดและลองจิจูด
    latitude = subpoint.latitude.degrees
    longitude = subpoint.longitude.degrees
    positions.append((longitude, latitude))

    #พิกัดละติจูดและลองจิจูดให้อยู่ในรูปพิกัดแผนที่
    x, y = m(longitude, latitude)

    #ตำแหน่งดาวเทียม
    m.plot(x, y, marker='o', color='r', markersize=10, label=name)

    if len(positions) > 1:
        lons, lats = zip(*positions)
        x, y = m(lons, lats)
        m.plot(x, y, linestyle='-', color='b', alpha=0.5)

    current_time = datetime.utcnow()
    ax.set_title(f'Real-Time Satellite Position on {current_time.strftime("%Y-%m-%d %H:%M:%S UTC")}')
    ax.legend(loc='upper right')

ani = FuncAnimation(fig, update, interval=500)

plt.show()
