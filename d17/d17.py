#! /usr/bin/python

import sys
import numpy as np
from math import floor


np.set_printoptions(edgeitems=8, linewidth=120)
with open(sys.argv[1], "r") as f:
    ip = f.read().strip()
    jet = [1 if ch == ">" else -1 for ch in ip]


PT1_STEPS = 2022
PT2_STEPS = 1000000000000


rocks = [np.array([[1, 1, 1, 1]]),
         np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]]),
         np.array([[1, 1, 1], [0, 0, 1], [0, 0, 1]]),
         np.array([[1], [1], [1], [1]]),
         np.array([[1, 1], [1, 1]])]


w = 9        # Width of 7 plus two edges
startw = 3   # Offset of 2 plus the edge
starth = 4   # Offset of 3 plus the floor
maxh = max(r.shape[0] for r in rocks) * PT1_STEPS * 5 # 5 for pt2 safety factor!
grid = np.zeros((maxh, w))
grid[:, 0] = 1        # Left wall
grid[:, w - 1] = 1    # Right wall
grid[0, :] = 1        # Floor


jet_num = 0
last_repeat = {}
rock_num = 0
pt2_extra = 0

while rock_num < PT2_STEPS: # Should break well before we reach PT2_STEPS !
    # Part 1 answer
    if rock_num == PT1_STEPS:
        pt1 = max(np.where(grid[:, 1:-1] > 0)[0])
        print(f"Part 1: {pt1}")

    r = rocks[rock_num % len(rocks)]
    x = startw
    y = max(np.where(grid[:,1:-1] > 0)[0]) + starth
    rh, rw = r.shape

    while True:
        # Find where the pattern repeats for pt2
        if jet_num % len(jet) == 0:
            top = max(np.where(grid[:, 1:-1] > 0)[0])
            dy = y - top
            slc = grid[top-15:top, :] # Take a slice of the grid to compare

            if "x" in last_repeat: # Just check for existence of one value

                if (rock_num % len(rocks)) == last_repeat["rock"] and x == last_repeat["x"] and dy == last_repeat["dy"] and np.array_equal(slc, last_repeat["slc"]):
                    # Pattern has repeated exactly! We can skip a load of steps now.

                    nrocks_per_repeat = rock_num - last_repeat["rock_num"] # Number of rocks per repeat of the pattern
                    nrocks_to_go = PT2_STEPS - rock_num # Number of rocks left to go in the simulation
                    pattern_repeats = floor(nrocks_to_go / nrocks_per_repeat) # How many times should we repeat the pattern?
                    pt2_extra = pattern_repeats * (top - last_repeat["top"]) # How much extra we should add on to account for all of the pattern repeats
                    rock_num += pattern_repeats * nrocks_per_repeat # Skip some rocks and then let the simulation continue
            
            last_repeat["rock_num"] = rock_num
            last_repeat["rock"] = rock_num % len(rocks)
            last_repeat["x"] = x
            last_repeat["dy"] = dy
            last_repeat["top"] = top
            last_repeat["slc"] = slc.copy()

        j = jet[jet_num % len(jet)]
        jet_num += 1


        # Test sideways move
        sideways = grid[y:y+rh, x+j:x+rw+j] + r
        if not np.any(sideways > 1):
            # Can make sideways move
            # Increment x, we cannot come to rest on a sideways move
            x += j
        
        # Test downwards move
        down = grid[y-1:y+rh-1, x:x+rw] + r
        if not np.any(down > 1):
            # Can make downwards move
            y -= 1
        else:
            # Can't move down, rock comes to rest.
            # Put rock in grid
            grid[y:y+rh, x:x+rw] += r
            break
    
    rock_num += 1


# Simulation done, calculate final pt2 result
top = max(np.where(grid[:, 1:-1] > 0)[0])
print(f"Part 2: {top + pt2_extra}")

# Note: doesn't terminate for the example input!!!
# Perhaps we need to look back more than one repeat of the jet sequence for that...