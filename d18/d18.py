#! /usr/bin/python

import sys


with open(sys.argv[1], "r") as f:
    cubes = [tuple(map(int, line.strip().split(","))) for line in f.readlines()]


ADJACENT = [(1, 0, 0), 
            (0, 1, 0),
            (0, 0, 1),
            (-1, 0, 0),
            (0, -1, 0),
            (0, 0, -1)]


adj_count = 0
for cx, cy, cz in cubes:
    for ax, ay, az in ADJACENT:
        if (cx + ax, cy + ay, cz + az) in cubes:
            adj_count += 1


pt1 = len(cubes) * 6 - adj_count
print(f"Part 1: {pt1}")