import folium
import pandas
import json
import os

basePath = os.path.dirname(os.path.abspath(__file__))
df = pandas.read_json(basePath + '/castles_archive.json', orient='records', encoding="utf8")

name = list(df["Name"])
country = list(df["Country"])
place = list(df["Place"])
era = list(df["Era"])
type_ = list(df["Type"])
condition = place = list(df["Condition"])
lat = list(df["Latitude"])
lon = list(df["Longitude"])

html = """
<center>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a>
<br>%s
<br>%s
<br>%s
</center>
"""

def color_marker(period):
	if period == "9-th century":
		return 'darkred'
	elif period == "10-th century":
		return 'orange'
	elif period == "11-th century":
		return 'darkgreen'
	elif period == "12-th century":
		return 'cadetblue'
	elif period == "13-th century":
		return 'darkblue'
	elif period == "14-th century":
		return 'darkpurple'
	elif period == "15-th century":
		return 'pink'
	elif period == "16-th century":
		return 'gray'
	elif period == "17-th century":
		return 'beige'

map = folium.Map(location=[36, 0], zoom_start=3, tiles="Stamen Terrain")
fg = folium.FeatureGroup(name="Era")

for lt, ln, n, er, ty, con in zip(lat, lon, name, era, type_, condition):
	iframe = folium.IFrame(html=html % (n, n, er, ty, con), width=175, height=100)
	fg.add_child(folium.Marker(location=[lt, ln], popup=folium.Popup(iframe), icon = folium.Icon(color = color_marker(er))))


map.add_child(fg)
map.save("castles_map.html")

