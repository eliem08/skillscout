import csv
import sys

for row in csv.reader(sys.stdin):
    print(",".join(c.strip() for c in row))
