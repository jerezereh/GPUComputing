import sys
import os
import geojson
import random
import re
import datetime

class TaxiTrajectory():
	def __init__(self, idNum, coordinates):
		self.idNum = idNum
		self.coordinates = coordinates
		self.color = self.random_color(idNum)
		self.r = self.color[0]
		self.g = self.color[1]
		self.b = self.color[2]
	
	@property
	def __geo_interface__(self):
		return {'type': 'Feature', 'properties': { 'id': self.idNum, 'r': self.r, 'g': self.g, 'b': self.b }, 'geometry': { 'type': 'LineString',  'coordinates': self.coordinates, } }
	
	def random_color(self, idNum):
		ret = []
		r = int(random.random() * 100 * int(idNum) % 256)
		g = int(random.random() * 100 * int(idNum) % 256)
		b = int(random.random() * 100 * int(idNum) % 256)
		ret.append(r)
		ret.append(g)
		ret.append(b)
		return ret


directory = sys.argv[1]
features = []
filecount = 0
threshold = datetime.timedelta(minutes=15)

def save_geojson(features):
	print("Saving to GeoJSON format...")
	feature_coll = geojson.FeatureCollection(features)
	with open("./result.geojson", 'a') as output:
		geojson.dump(feature_coll, output, indent=1)

with open("./result.geojson", 'w') as output:
	output.seek(0)
	output.truncate()

for filename in os.listdir(os.fsencode(directory)):
	file = filename.decode("utf-8")
	if file.endswith(".txt"):
		filecount += 1
		print("Converting file " + str(filecount) + "...")
		with open(os.path.join(directory, file), 'r') as input:
			points = []
			date_time = None
			for line in input:
				split_line = line.split(",")
				last_date_time = date_time
				date_and_time = split_line[1].split(" ")
				date = date_and_time[0].split("-")
				time = date_and_time[1].split(":")
				date_time = datetime.datetime(int(date[0]), int(date[1]),int(date[2]), int(time[0]), 
					int(time[1]), int(time[2]))
				if last_date_time is not None and date_time - last_date_time > threshold:
					if len(points) > 1:
						feature = TaxiTrajectory(split_line[0], points)
						features.append(feature)
					points = []
				if date_time != last_date_time:
					point = geojson.Point((float(split_line[2]), float(split_line[3])))
					points.append(point)
			# remove some erroneous data (individual points, repeated time/location pairs)
			if len(points) > 1:
				feature = TaxiTrajectory(split_line[0], points)
				features.append(feature)
	if(filecount % 100 == 0):
		save_geojson(features)
		features = []
save_geojson(features)
