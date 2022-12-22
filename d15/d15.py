#! /usr/bin/python

import sys


with open(sys.argv[1], "r") as f:
    lines = [line.strip() for line in f.readlines()]

if "example" in sys.argv[1]:
    Y_POS = 10
else:
    Y_POS = 2000000


def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

sensors = []
for line in lines:
    l = line.split(" ")
    sx = int(l[2][2:-1])
    sy = int(l[3][2:-1])
    bx = int(l[8][2:-1])
    by = int(l[9][2:])
    dist = manhattan_distance((sx, sy), (bx, by))
    sensors.append(((sx, sy), (bx, by), dist))

beacons = set()
no_beacons = set()
for (sx, sy), (bx, by), db in sensors:
    beacons.add((bx, by))
    closest = (sx, Y_POS)
    d = manhattan_distance((sx, sy), closest)
    delta = db - d
    if delta >= 0:
        for dx in range(-delta, delta + 1):
            no_beacons.add((sx + dx, Y_POS))

no_beacons = no_beacons - beacons
print(f"Part 1: {len(no_beacons)}")