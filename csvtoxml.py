import sys
import csv
import json

def processFile(csv_file):
    csvfile = open(csv_file, 'r')
    with open(csv_file) as csvfile:
        reader = csv.DictReader(csvfile)
        out = json.dumps([row for row in reader])
        print(out)

if __name__ == '__main__':
	script, args = sys.argv[0], sys.argv[1:]
	processFile(args[0])
