#! /usr/bin/python

import sys
from functools import cmp_to_key


with open(sys.argv[1], "r") as f:
    pairs = [p.split("\n") for p in f.read().strip().split("\n\n")]


ALLOWED_CHARS = "[],0123456789"


def sanitiser_check(packet):
    for ch in packet:
        if ch not in ALLOWED_CHARS:
            assert(0)


# Return values: < 0 = WRONG
#                  0 = MAYBE
#                > 0 = CORRECT
def cmp(l, r):
    if isinstance(l, list) and isinstance(r, list):
        # Compare each item in list, until one or more of the lists runs out of items
        for li, ri in zip(l, r):
            res = cmp(li, ri)
            if res != 0:
                # Only return the result if it's not MAYBE, otherwise move on to next item
                return res
        # Ran out of items, return CORRECT if left ran out, MAYBE if both ran out, WRONG if right ran out
        return len(r) - len(l)
    elif isinstance(l, list) and not isinstance(r, list):
        return cmp(l, [r])
    elif not isinstance(l, list) and isinstance(r, list):
        return cmp([l], r)
    else:
        return int(r) - int(l)


correct_list = []
for i, p in enumerate(pairs):
    l = p[0]
    r = p[1]
    sanitiser_check(l)
    sanitiser_check(r)
    l = eval(l)
    r = eval(r)
    res = cmp(l, r)
    if res >= 0: # MAYBE also counts as correct if we have traversed the whole list
        correct_list.append(i + 1)

print(f"Part 1: {sum(correct_list)}")


# Part 2
all_packets = [[[2]], [[6]]] # Start with divider packets

# Construct list of inputs
for l, r in pairs:
    sanitiser_check(l)
    sanitiser_check(r)
    all_packets.append(eval(l))
    all_packets.append(eval(r))

# Custom comparison function for sorted()
def final_cmp(l, r):
    ret = cmp(l, r)
    if ret >=0:
        return -1
    return 1

# Sort the list
s = sorted(all_packets, key=cmp_to_key(final_cmp))

div1 = s.index([[2]]) + 1
div2 = s.index([[6]]) + 1

print(f"Part 2: {div1 * div2}")