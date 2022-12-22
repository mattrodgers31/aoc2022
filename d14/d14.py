#! /usr/bin/python

import sys


with open(sys.argv[1], "r") as f:
    lines = [[list(map(int, p.split(","))) for p in line.strip().split(" -> ")] for line in f.readlines()]


class Cave():
    def __init__(self, filled: set) -> None:
        self.filled = filled
        self.filled_at_start = len(self.filled)
        self.maxy = max(y for x, y in filled)

    def __repr__(self) -> str:
        return f"Filled at start: {self.filled_at_start}, max y: {self.maxy}"

    @classmethod
    def from_lines(cls, lines: list):
        filled = set()
        for i, line in enumerate(lines):
            # Iterate over pairs of co-ordinates defining each straight line segment
            for start, end in zip(line, line[1:]):
                x = (start[0], end[0])
                y = (start[1], end[1])
                for i in range(min(x), max(x) + 1):
                    for j in range(min(y), max(y) + 1):
                        filled.add((i, j))
        return cls(filled)

    def _drop_one_sand(self, start_pos, pt2):
        pos = start_pos
        if pt2:
            maxy = self.maxy + 2
        else:
            maxy = self.maxy

        while pos[1] <= maxy:
            if pos[1] + 1 == maxy and pt2:
                # Sand has reached floor and is blocked
                self.filled.add(pos)
                return False
            # Try to drop directly down
            if (pos[0], pos[1] + 1) not in self.filled:
                pos = (pos[0], pos[1] + 1)
            # Try to drop down and left
            elif (pos[0] - 1, pos[1] + 1) not in self.filled:
                pos = (pos[0] - 1, pos[1] + 1)
            # Try to drop down and right
            elif (pos[0] + 1, pos[1] + 1) not in self.filled:
                pos = (pos[0] + 1, pos[1] + 1)
            # Blocked
            else:
                self.filled.add(pos)
                if not pt2:
                    return False # Sand did not drop off bottom of grid
                else:
                    if pos == start_pos:
                        return True # Sand has reached start point
                    return False # Sand has not reached start point

        assert not pt2
        return True # Sand dropped off bottom of grid (can only reach here for pt1)

    def run(self, start, pt2):
        complete = False
        while not complete:
            complete = self._drop_one_sand(start, pt2)
        return len(self.filled) - self.filled_at_start


START = (500, 0)

c = Cave.from_lines(lines)
pt1 = c.run(START, False)
print(f"Part 1: {pt1}")

c = Cave.from_lines(lines)
pt2 = c.run(START, True)
print(f"Part 2: {pt2}")
