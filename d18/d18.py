#! /usr/bin/python

import sys
from collections import deque


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


# Part 2

def get_reachable_points(cubes):
    # Get size of grid
    x0 = min(c[0] for c in cubes) - 1
    y0 = min(c[1] for c in cubes) - 1
    z0 = min(c[2] for c in cubes) - 1
    x1 = max(c[0] for c in cubes) + 1
    y1 = max(c[1] for c in cubes) + 1
    z1 = max(c[2] for c in cubes) + 1

    # BFS
    start = (x0, y0, z0) # Start from arbitrary position on edge
    visited = set(start)
    q = deque([start])

    while q:
        next = q.pop()
        x, y, z = next
        for ax, ay, az in ADJACENT:
            nx = x + ax
            ny = y + ay
            nz = z + az
            if nx >= x0 and nx <= x1 and ny >= y0 and ny <= y1 and nz >= z0 and nz <= z1:
                neighbor = (nx, ny, nz)
                if neighbor not in visited:
                    if neighbor not in cubes:
                        q.append(neighbor)
                        visited.add(neighbor)

    return visited

reachable = get_reachable_points(cubes)

surface_area = 0
for cx, cy, cz in cubes:
    for ax, ay, az in ADJACENT:
        neighbor = (cx + ax, cy + ay, cz + az)
        if neighbor not in cubes:
            if neighbor in reachable:
                surface_area += 1

print(f"Part 2: {surface_area}")