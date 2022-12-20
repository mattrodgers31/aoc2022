#! /usr/bin/python

import sys


with open(sys.argv[1], "r") as f:
    lines = [line.strip().split(" ") for line in f.readlines()]


def apply_move(positions, instr, record):
    for _ in range(int(instr[1])):
        # Move head
        h = positions[0]
        if instr[0] == "U":
            h = (h[0], h[1] + 1)
        if instr[0] == "R":
            h = (h[0] + 1, h[1])
        if instr[0] == "D":
            h = (h[0], h[1] - 1)
        if instr[0] == "L":
            h = (h[0] - 1, h[1])
        positions[0] = h
        
        for i in range(1, len(positions)):
            h = positions[i - 1]
            t = positions[i]
            delta = (h[0] - t[0], h[1] - t[1])
            if max([abs(i) for i in delta]) > 1:
                # Move tail if more than one space away in any direction
                t = (int(t[0] + delta[0] / max(abs(delta[0]), 1)), int(t[1] + delta[1] / max(abs(delta[1]), 1)))
            positions[i] = t

        record.add(positions[-1])

    return positions


positions_visited = set([(0, 0)])
positions = [(0, 0), (0, 0)]
for l in lines:
    positions = apply_move(positions, l, positions_visited)

print(f"Part 1: {len(positions_visited)}")


positions_visited = set([(0, 0)])
positions = [(0, 0) for _ in range(10)]
for l in lines:
    positions = apply_move(positions, l, positions_visited)
    
print(f"Part 2: {len(positions_visited)}")