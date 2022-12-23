#! /usr/bin/python

import sys
from collections import deque


INF = 2 ** 32


# Parse input into dictionary of Valve: (flow rate, (other reachable valves))
with open(sys.argv[1], "r") as f:
    lines = [line.strip() for line in f.readlines()]
    valves = {}
    for l in lines:
        l = l.split(" ")
        id = l[1]
        flow = int(l[4][5:-1])
        paths = [node.strip(",") for node in l[9:]]
        valves[id] = (flow, paths)


# Return a dictionary of Valve: [Valve: distance] to store the shortest
# distance between each pair of valves
def floyd_warshall(valves) -> dict:

    # Initialise distances with moves that can be made in one step
    d = {}
    for i, (_, paths_i) in valves.items():
        d[i] = {}
        for j, (_, paths_j) in valves.items():
            if i == j:
                d[i][j] = 0
            elif j in paths_i:
                d[i][j] = 1
            else:
                d[i][j] = INF

    # Loop through vertices
    for k in valves:
        for i in valves:
            for j in valves:
                d[i][j] = min(d[i][j], d[i][k] + d[k][j])

    return d


def generate_max_relief(start, time, valves, distances):
    # Queue: (current valve, time remaining, pressure relief, open valves)
    q = deque([(start, time, 0, set())])

    # Dict of [frozen set of visited valves: max relief]
    max_relief = {}

    while q: # Converts to false if empty
        id, time_remaining, relief, open = q.pop()
        for v, d in distances[id].items():
            if d < time_remaining - 1:
                # We can reach this node AND open the valve in the time remaining
                flow, _ = valves[v]
                if v not in open and flow > 0:
                    # The valve is not already open, and is worth opening
                    new_tr = time_remaining - d - 1 # Subtract distance to get here and 1 step to open valve
                    new_relief = relief + new_tr * flow
                    new_open = open | {v} # New set consisting of old set plus this valve
                    new_key = frozenset(new_open)
                    q.append((v, new_tr, new_relief, new_open))

                    # Update max relief
                    max_relief[new_key] = max(max_relief.get(new_key, 0), new_relief)

    return max_relief



d = floyd_warshall(valves)
m = generate_max_relief("AA", 30, valves, d)

print(f"Part 1: {max(m.values())}")

m = generate_max_relief("AA", 26, valves, d)

pt2 = 0
for k0, v0 in m.items():
    for k1, v1 in m.items():
        if k0.isdisjoint(k1):
            pt2 = max(pt2, v0 + v1)

print(f"Part 2: {pt2}")