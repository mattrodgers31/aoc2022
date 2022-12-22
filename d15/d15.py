#! /usr/bin/python

import sys
from math import floor
import time


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


# Part 2


# Return True if the rectangle is fully covered by any one sensor
# i.e. all corners are covered by the sensor
def check_rectangle(rectangle, sl):
    x0, x1, y0, y1 = rectangle
    corners = [(x0, y0), (x0, y1), (x1, y0), (x1, y1)]
    for s, d in sl:
        covered = True
        for c in corners:
            if manhattan_distance(s, c) > d:
                covered = False
                break
        if covered:
            return True
    return False


# Split a rectangle into quarters
def split(rectangle):
    x0, x1, y0, y1 = rectangle
    xm = x0 + floor((x1 - x0) / 2) # Midpoint of x
    ym = y0 + floor((y1 - y0) / 2) # Midpoint of y
    tl = (x0,     xm, y0,     ym)
    tr = (xm + 1, x1, y0,     ym) if x1 > xm else (xm, x1, y0, ym)
    bl = (x0,     xm, ym + 1, y1) if y1 > ym else (x0, xm, ym, y1)
    if x1 > xm and y1 > ym:
        br = (xm + 1, x1, ym + 1, y1)
    elif x1 > xm: # and y1 == ym
        br = (xm + 1, x1, ym, y1)
    elif y1 > ym: # and x1 == xm
        br = (xm, x1, ym + 1, y1)
    else: # x1 == xm and y1 == ym
        br = (xm, x1, ym, y1)
    return [tl, tr, bl, br]


# Recursively split the given rectangle into four, and check whether the beacon
# can be located inside it
def reduce_rectangles(rectangle, sl, depth):
    covered = check_rectangle(rectangle, sl)
    if covered:
        # Rectangle is fully covered by a sensor, beacon cannot be here
        return None

    # Recursion end condition
    x0, x1, y0, y1 = rectangle
    if x0 == x1 and y0 == y1: # and not covered by any sensor (must be true if we got here)
        return (x0, y0)

    # Rectangle is not fully covered by a sensor, beacon could still be here
    new_rectangles = split(rectangle)
    for r in new_rectangles:
        loc = reduce_rectangles(r, sl, depth + 1)
        if loc:
            return loc
        
    return None


START_RECTANGLE = (MINIMUM, MAXIMUM, MINIMUM, MAXIMUM)
t0 = time.time()
loc = reduce_rectangles(START_RECTANGLE, sensors, 0)
t1 = time.time()

# Calculate tuning frequency
pt2 = 4000000 * loc[0] + loc[1]
print(f"Part 2: {pt2}")
print(f"Part 2 time: {t1 - t0} s")