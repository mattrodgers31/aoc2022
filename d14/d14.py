#! /usr/bin/python

import sys
import numpy as np


with open(sys.argv[1], "r") as f:
    lines = [[list(map(int, p.split(","))) for p in line.strip().split(" -> ")] for line in f.readlines()]


maxy = 0
filled = set()
for i, line in enumerate(lines):
    line_offset = line.copy()
    line_offset.pop(0)

    # Iterate over pairs of co-ordinates defining each straight line segment
    for start, end in zip(line, line_offset):
        x = (start[0], end[0])
        y = (start[1], end[1])
        for i in range(min(x), max(x) + 1):
            for j in range(min(y), max(y) + 1):
                filled.add((i, j))
                if j > maxy:
                    maxy = j


def visualise(filled):
    minx = min([pt[0] for pt in filled])
    miny = min([pt[1] for pt in filled])
    maxx = max([pt[0] for pt in filled])
    maxy = max([pt[1] for pt in filled])
    grid = np.zeros((maxy-miny+1, maxx-minx+1))
    for point in filled:
        pt_norm = (point[1] - miny, point[0] - minx)
        grid[pt_norm] = 1

    print(grid)


def drop_one_sand(pos, maxy, filled):
    # Keep iterating until sand position exceeds max y co-ordinate
    start_pos = pos
    floory = maxy + 2
    while pos[1] < floory:
        if pos[1] + 1 == floory:
            filled.add(pos)
            return filled, False
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
            filled.add(pos)
            if pos == start_pos:
                return filled, True
            return filled, False # Not complete

    assert(0)
    return filled, True

n = len(filled)
i = 0
while True:
    filled, complete = drop_one_sand((500, 0), maxy, filled)
    print(i, end="\r")
    if complete:
        break
    i += 1

print(f"Part 2: {len(filled) - n}")