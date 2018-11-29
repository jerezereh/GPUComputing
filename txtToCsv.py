import sys
import csv
import os

directory = sys.argv[1]

for filename in os.listdir(os.fsencode(directory)):
	file = filename.decode("utf-8")
	if file.endswith(".txt"):
		print("Converting file " + file + "...")
		with open(os.path.join(directory, file), 'r') as input:
			lines = (line.split(",")[1:] for line in input if line)
			csv_dir = "./csv_files/"
			csv_file = file[:-3] + "csv"
			with open(os.path.join(csv_dir, csv_file), 'w') as output:
				writer = csv.writer(output)
				writer.writerow(('datetime', 'long', 'lat'))
				writer.writerows(lines)
