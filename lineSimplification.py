import sys
import os
import geojson
import random

# input: geojson file, file of coordinates to check for
# check_file also geojson file, has point features that will be read
# output: new geojson file with new, simplified linestrings


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


def isLeftTurn( p1,p2,p3):
        '''
        tests if when traveling from point p1 to point p2, and then on to p3, whether the traveler must make a left or right turn at p2 in order to reach p3.

        uses sign of the area of the triangle computation.

        **input**:

        p1,p2,p3: points of the format (x,y)

        **output**:

        -1 if a left turn is needed

        0 if the points are collinear

        1 if a right turn is needed
        '''
        p1x = p1[0]
        p1y = p1[1]
        p2x = p2[0]
        p2y = p2[1]
        p3x = p3[0]
        p3y = p3[1]
        result =  ((p3y - p1y) * (p2x - p1x)) - ((p2y - p1y) * (p3x - p1x))
        if result > 0:
                return 1
        elif result == 0:
                return 0
        return -1


def save_geojson(features, filename="./result.geojson"):
	print("Saving to GeoJSON format...")
	feature_coll = geojson.FeatureCollection(features)
	with open(filename, 'w') as output:
		geojson.dump(feature_coll, output, indent=1)

check_points = []
features = []
linestrings = []
ids = []

with open(sys.argv[1], 'r') as geo_file:
	data = geojson.load(geo_file)

with open(sys.argv[2], 'r') as check_file:
	for line in check_file:
		split_line = line.split(",")
		if len(split_line) is 2:
			point = geojson.Point((float(split_line[0]), float(split_line[1])))
			check_points.append(point)

for feature in data['features']:
	linestring = list(geojson.utils.coords(feature))
	new_linestring = []
	triangle = []
	for point in linestring:
		triangle.append(point)
		if len(triangle) is 3:
			for point in check_points:
				return_vals = []
				if len(triangle) is 3:
					return_vals.append(isLeftTurn(triangle[0], triangle[2], point["coordinates"]))
					return_vals.append(isLeftTurn(triangle[2], triangle[1], point["coordinates"]))
					return_vals.append(isLeftTurn(triangle[1], triangle[0], point["coordinates"]))
					# if each set of points returns a left turn (-1), then the point is inside the triangle
					if sum(return_vals) is -3 or sum(return_vals) is 3:
						print("point inside triangle")
						new_linestring.append(triangle[0])
						del triangle[0]
			# after ensuring all points outside, delete middle point of triangle to simplify
			if len(triangle) is 3:
				del triangle[1]
	new_linestring.append(triangle[0])
	if len(triangle) is 2:
		new_linestring.append(triangle[1])
	linestrings.append(new_linestring)
	ids.append(feature['properties']['id'])

for i in range(len(linestrings)):
	feature = TaxiTrajectory(ids[i], linestrings[i])
	features.append(feature)

save_geojson(features, "./simplified_features.geojson")
