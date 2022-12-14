#! /usr/bin/python

import sys


with open(sys.argv[1], "r") as f:
    lines = [x.strip() for x in f.readlines() if x.strip()]


def sections_to_set(sections: str) -> set:
    s = [int(num) for num in sections.split('-')]
    assert(len(s) == 2)

    return set(range(s[0], s[1] + 1))


ranges = []

for line in lines:
    spl = line.split(',')
    a = sections_to_set(spl[0])
    b = sections_to_set(spl[1])
    ranges.append((a, b))


# Part 1
pt1 = 0

for a, b in ranges:
    if a.issubset(b) or b.issubset(a):
        pt1 += 1

print(f"Part 1: {pt1}")


# Part 2
pt2 = 0

for a, b in ranges:
    if len(a.intersection(b)) > 0:
        pt2 += 1

print(f"Part 2: {pt2}")