import sys
import geojson
import random

minLat = float("inf")
maxLat = float("-inf")
minLon = float("inf")
maxLon = float("-inf")
numPoints = sys.argv[2]
points = []

def save_geojson(features):
	print("Saving to GeoJSON format...")
	feature_coll = geojson.FeatureCollection(features)
	with open("output_data/randomPoints.geojson", 'a') as output:
		geojson.dump(feature_coll, output, indent=1)

with open(sys.argv[1], 'r') as geo_file:
	data = geojson.load(geo_file)

for feature in data['features']:
	linestring = list(geojson.utils.coords(feature))
	for point in linestring:
		if minLon > point[0]:
			minLon = point[0]
		elif maxLon < point[0]:
			maxLon = point[0]
		if minLat > point[1]:
			minLat = point[1]
		elif maxLat < point[1]:
			maxLat = point[1]

new_linestring = []

for i in range(int(numPoints)):
	x = random.uniform(minLon, maxLon)
	y = random.uniform(minLat, maxLat)
	point = geojson.Point((x,y))
	points.append((x,y))

new_linestring = geojson.LineString(points)
feature = geojson.Feature(geometry=new_linestring)

with open("output_data/randomPoints.geojson", 'w') as output:
	output.seek(0)
	output.truncate()

with open("output_data/randomPoints.txt", 'w') as txtout:
	txtout.seek(0)
	txtout.truncate()
	for point in points:
		txtout.write(str(point[0]) + "," + str(point[1]) + "\n")

save_geojson(feature)