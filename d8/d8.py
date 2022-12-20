#! /usr/bin/python

import sys
import numpy as np


with open(sys.argv[1], "r") as f:
    grid = np.array([list(line) for line in f.read().strip().split("\n")]).astype(int)


# Return (visible, distance) where:
# visible - is the tree visible from the edge in this direction
# distance - how far can be seen from this tree in this direction
def check_one_direction(h, arr):
    for i, val in enumerate(arr):
        if val >= h:
            return False, i + 1

    return True, len(arr)


# Return (visible, score) where:
# visible - is the tree visible from the edge in any direction
# score - product of the distance that can be seen in each direction
def get_scenic_score(x, y):
    h = grid[y, x]
    vl, l = check_one_direction(h, np.flip(grid[y, 0:x]))
    vr, r = check_one_direction(h, grid[y, x+1:])
    vu, u = check_one_direction(h, np.flip(grid[0:y, x]))
    vd, d = check_one_direction(h, grid[y+1:, x])
    visible = vl or vr or vu or vd
    score = l * r * u * d

    return visible, score

pt1 = 0
pt2 = 0
height, width = grid.shape
for row in range(width):
    for col in range(height):
        v, score = get_scenic_score(col, row)
        if score > pt2:
            pt2 = score
        if v:
            pt1 += 1

print(f"Part 1: {pt1}")
print(f"Part 2: {pt2}")