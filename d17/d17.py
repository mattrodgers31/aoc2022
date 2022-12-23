#! /usr/bin/python

import sys
import numpy as np

np.set_printoptions(edgeitems=8, linewidth=120)
with open(sys.argv[1], "r") as f:
    ip = f.read().strip()
    jet = [1 if ch == ">" else -1 for ch in ip]


STEPS = 2022


rocks = [np.array([[1, 1, 1, 1]]),
         np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]]),
         np.array([[1, 1, 1], [0, 0, 1], [0, 0, 1]]),
         np.array([[1], [1], [1], [1]]),
         np.array([[1, 1], [1, 1]])]


w = 9        # Width of 7 plus two edges
startw = 3   # Offset of 2 plus the edge
starth = 4   # Offset of 3 plus the floor
maxh = max(r.shape[0] for r in rocks) * STEPS + 1
grid = np.zeros((maxh, w))
grid[:, 0] = 1        # Left wall
grid[:, w - 1] = 1    # Right wall
grid[0, :] = 1        # Floor


jet_num = 0
for rock_num in range(STEPS):
    r = rocks[rock_num % len(rocks)]
    x = startw
    y = max(np.where(grid[:,1:-1] > 0)[0]) + starth
    rh, rw = r.shape

    while True:
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


pt1 = max(np.where(grid[:, 1:-1] > 0)[0])
print(f"Part 1: {pt1}")