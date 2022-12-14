#! /usr/bin/python

import sys


with open(sys.argv[1], "r") as f:
    rucksacks = [x.strip() for x in f.readlines() if x.strip()]


def get_score(letter: str) -> int:
    ascii_val = ord(letter)

    if ascii_val >= ord('a'):
        score = ascii_val - ord('a') + 1
    else:
        score = ascii_val - ord('A') + 27

    return score


pt1 = 0

for r in rucksacks:
    assert(len(r) % 2 == 0)

    first_half = set(r[:int(len(r)/2)])
    second_half = set(r[int(len(r)/2):])
    shared_letter = first_half.intersection(second_half)
    assert(len(shared_letter) == 1)

    pt1 += get_score(shared_letter.pop())

print(f"Part 1: {pt1}")


# Part 2

assert(len(rucksacks) % 3 == 0)
pt2 = 0

for i in range(int(len(rucksacks) / 3)):
    a = set(rucksacks[3*i])
    b = set(rucksacks[3*i + 1])
    c = set(rucksacks[3*i + 2])

    shared = a.intersection(b).intersection(c)
    assert(len(shared) == 1)

    pt2 += get_score(shared.pop())

print(f"Part 2: {pt2}")