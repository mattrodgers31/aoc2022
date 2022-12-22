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
for line in lines:
    l = line.split(" ")
    sx = int(l[2][2:-1])
    sy = int(l[3][2:-1])
    bx = int(l[8][2:-1])
    by = int(l[9][2:])
    dist = manhattan_distance((sx, sy), (bx, by))
    sensors.append(((sx, sy), (bx, by), dist))


# Part 1

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
    