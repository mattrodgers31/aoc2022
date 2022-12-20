#! /usr/bin/python

import sys


with open(sys.argv[1], "r") as f:
    lines = [line.strip().split(" ") for line in f.readlines()]

start = (0, 0)
positions_visited = set([start])

def apply_move(h, t, instr):
    for _ in range(int(instr[1])):
        # Move head
        if instr[0] == "U":
            h = (h[0], h[1] + 1)
        if instr[0] == "R":
            h = (h[0] + 1, h[1])
        if instr[0] == "D":
            h = (h[0], h[1] - 1)
        if instr[0] == "L":
            h = (h[0] - 1, h[1])

        # Move tail
        delta = (h[0] - t[0], h[1] - t[1])
        if max([abs(i) for i in delta]) > 1:
            # Move tail if more than one space away in any direction
            t = (int(t[0] + delta[0] / max(abs(delta[0]), 1)), int(t[1] + delta[1] / max(abs(delta[1]), 1)))

        # Record tail position
        positions_visited.add(t)

    return (h, t)


h = start
t = start
for l in lines:
    h, t = apply_move(h, t, l)

print(f"Part 1: {len(positions_visited)}")