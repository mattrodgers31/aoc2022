#! /usr/bin/python

import sys


with open(sys.argv[1], "r") as f:
    lines = [line.strip() for line in f.readlines()]

MINIMUM = 0
if "example" in sys.argv[1]:
    Y_POS = 10
    MAXIMUM = 20
else:
    Y_POS = 2000000
    MAXIMUM = 4000000


def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

sensors = []
beacons = set()
for line in lines:
    l = line.split(" ")
    sx = int(l[2][2:-1])
    sy = int(l[3][2:-1])
    bx = int(l[8][2:-1])
    by = int(l[9][2:])
    dist = manhattan_distance((sx, sy), (bx, by))
    sensors.append(((sx, sy), dist))
    beacons.add((bx, by))


# Part 1

# Find the min and max X values in the chosen row covered by any sensor
minx = 2**32
maxx = 0
for (sx, sy), d in sensors:
    dy = abs(Y_POS - sy)
    if d >= dy:
        dx = d - dy
        if sx + dx > maxx:
            maxx = sx + dx
        if sx - dx < minx:
            minx = sx - dx

# Now that we have min and max X values, scan through row to find any points not covered by sensor
x = minx
not_covered_count = 0
while x < maxx:
    for (sx, sy), d in sensors:
        ds = manhattan_distance((sx, sy), (x, Y_POS))
        if ds <= d:
            # We are in range of this sensor
            # Increment X by the remaining manhattan distance plus 1 to get the next non-covered point
            x += d - ds + 1
            break
    else:
        # Found a point not covered by any sensor
        x += 1

# Find the number of beacons already existing in this row (these don't count towards positions where we can't place a new beacon)
beacons_in_row = sum(beacon[1] == Y_POS for beacon in beacons)
pt1 = maxx + 1 - minx - not_covered_count - beacons_in_row
print(f"Part 1: {pt1}")

sys.exit()
# Part 2

x, y = MINIMUM, MINIMUM
while True:
    for (sx, sy), (_, _), d  in sensors:
        if x > MAXIMUM:
            x = 0
            y += 1
            if y % 10000 == 0:
                print(y, end="\r")
        ds = manhattan_distance((sx, sy), (x, y))
        if ds <= d:
            x += d - ds + 1
            break
    else:
        print(f"Part 2: {(x, y)}")
        break
    