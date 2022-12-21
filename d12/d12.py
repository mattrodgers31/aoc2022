#! /usr/bin/python

import sys
import numpy as np


with open(sys.argv[1], "r") as f:
    ip = f.read().strip()


grid = np.array([[ch for ch in s] for s in ip.split("\n")])
start = np.where(grid == "S")
start = (start[0][0], start[1][0])
end = np.where(grid == "E")
end = (end[0][0], end[1][0])

# After we have recorded start and end, replace with their height
grid[start] = "a"
grid[end] = "z"

# Convert character heights to numerical
grid = np.vectorize(ord)(grid) - ord("a")

# Directions we can go from a grid square
NEIGHBORS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def get_smallest(d):
    return min(d, key=d.get)

def add_coords(a, b):
    return tuple(map(sum, zip(a, b)))

def point_exists(loc, h, w):
    if loc[0] not in range(0, h):
        return False
    if loc[1] not in range(0, w):
        return False
    return True

def reachable_pt1(a, b, grid):
    return grid[a] <= grid[b] + 1

# Reverse direction for pt2
def reachable_pt2(a, b, grid):
    return grid[a] >= grid[b] - 1

# Dijkstra's shortest path (see https://brilliant.org/wiki/dijkstras-short-path-finder/)
def dijkstra(graph, source, reachable):
    h, w = graph.shape
    distances = {}
    unvisited = {}

    # Construct queue of unvisited co-ordinates
    unvisited[source] = 0
    for a in range(h):
        for b in range(w):
            if (a, b) != source:
                unvisited[(a, b)] = np.inf

    # Visit each square from queue in distance order
    while len(unvisited) > 0:
        v = get_smallest(unvisited) # Vertex with smallest distance
        cur_d = unvisited.pop(v)    # Distance of this vertex from source
        distances[v] = cur_d        # Can be removed from unvisited and added to final distances

        # Move in each possible direction, if the point exists check whether we can visit it
        for dir in NEIGHBORS:
            loc = add_coords(v, dir)
            if point_exists(loc, h, w):
                if reachable(loc, v, grid):
                    # Can move to this location in 1 step
                    d = cur_d + 1
                    if loc in unvisited:
                        if d < unvisited[loc]:
                            # This is the new shortest path to loc
                            unvisited[loc] = d
                else:
                    # Cannot be visited
                    pass

    return distances


# Part 1
d = dijkstra(grid, start, reachable_pt1)
print(f"Part 1: {d[end]}")


# For part 2 do it backwards: start at the end and reverse the condition for being able to reach a
# grid square. Then we can just check the min distance for any square that's an "a".
d = dijkstra(grid, end, reachable_pt2)
a_locations = np.where(grid == 0)
min_distance = np.inf
for i in range(len(a_locations[0])):
    loc = (a_locations[0][i], a_locations[1][i])
    distance = d[loc]
    if distance < min_distance:
        min_distance = distance

print(f"Part 2: {min_distance}")