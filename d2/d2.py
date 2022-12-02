#! /usr/bin/python

import sys

with open(sys.argv[1], "r") as f:
    rounds = [x.strip() for x in f.readlines() if x.strip()]


# X = 1, Y = 2, Z = 3
# Loss = 0, draw = 3, win = 6

scores_p1 = {"A X": 1 + 3,
             "A Y": 2 + 6,
             "A Z": 3 + 0,
             "B X": 1 + 0,
             "B Y": 2 + 3,
             "B Z": 3 + 6,
             "C X": 1 + 6,
             "C Y": 2 + 0,
             "C Z": 3 + 3}

# X = lose, Y = draw, Z = win
# A = 1, B = 2, C = 3
# Loss = 0, draw = 3, win = 6

scores_p2 = {"A X": 0 + 3,
             "A Y": 3 + 1,
             "A Z": 6 + 2,
             "B X": 0 + 1,
             "B Y": 3 + 2,
             "B Z": 6 + 3,
             "C X": 0 + 2,
             "C Y": 3 + 3,
             "C Z": 6 + 1}

total_score = sum([scores_p1[x] for x in rounds])

print(f"Part 1: {total_score}")

total_score = sum([scores_p2[x] for x in rounds])

print(f"Part 2: {total_score}")
