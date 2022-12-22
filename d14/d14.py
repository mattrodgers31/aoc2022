#! /usr/bin/python

import sys
from collections import deque
import numpy as np


with open(sys.argv[1], "r") as f:
    lines = [[list(map(int, p.split(","))) for p in line.strip().split(" -> ")] for line in f.readlines()]


maxx = 0
minx = np.inf
maxy = 0
miny = np.inf
filled = deque([])
for i, line in enumerate(lines):
    line_offset = line.copy()
    line_offset.pop(0)

    # Iterate over pairs of co-ordinates defining each straight line segment
    for start, end in zip(line, line_offset):
        x = (start[0], end[0])
        y = (start[1], end[1])
        for i in range(min(x), max(x) + 1):
            for j in range(min(y), max(y) + 1):
                filled.append((i, j))
                if i < minx:
                    minx = i
                if i > maxx:
                    maxx = i
                if j < miny:
                    miny = j
                if j > maxy:
                    maxy = j

assert minx > 0
assert miny > 0


def visualise(minx, maxx, miny, maxy, filled):
    grid = np.zeros((maxy-miny+1, maxx-minx+1))
    for point in filled:
        pt_norm = (point[1] - miny, point[0] - minx)
        grid[pt_norm] = 1

    print(grid)


def drop_one_sand(pos, maxy, filled):
    # Keep iterating until sand position exceeds max y co-ordinate
    while pos[1] <= maxy:
        # Try to drop directly down
        if (pos[0], pos[1] + 1) not in filled:
            pos = (pos[0], pos[1] + 1)
        # Try to drop down and left
        elif (pos[0] - 1, pos[1] + 1) not in filled:
            pos = (pos[0] - 1, pos[1] + 1)
        # Try to drop down and right
        elif (pos[0] + 1, pos[1] + 1) not in filled:
            pos = (pos[0] + 1, pos[1] + 1)
        # Blocked
        else:
            filled.append(pos)
            return filled, False # Not complete

    return filled, True


i = 0
while True:
    filled, complete = drop_one_sand((500, 0), maxy, filled)
    print(i, end="\r")
    if complete:
        break
    i += 1

print(f"Part 1: {i}")