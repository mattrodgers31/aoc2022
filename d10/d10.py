#! /usr/bin/python

import sys
import math


with open(sys.argv[1], "r") as f:
    lines = [line.strip() for line in f.readlines()]


class Cpu():
    def __init__(self) -> None:
        self.cycle_counter = 0
        self.x = 1
        self.image = []
        self.signal_sum = 0

    def _check_signal(self):
        if self.cycle_counter in [20, 60, 100, 140, 180, 220]:
            self.signal_sum += self.cycle_counter * self.x

    def _draw(self):
        sprite = int(self.x + math.floor(self.cycle_counter / 40) * 40)
        if abs(sprite - (self.cycle_counter - 1)) <= 1:
            self.image.append("#")
        else:
            self.image.append(".")

    def _increment_cycle(self):
        self.cycle_counter += 1
        self._check_signal()
        self._draw()

    def execute(self, cmd):
        if cmd == "noop":
            self._increment_cycle()
        elif cmd[0:4] == "addx":
            val = int(cmd[5:])
            self._increment_cycle()
            self._increment_cycle()
            self.x += val
        else:
            assert 0, "Instruction not valid"


c = Cpu()
for line in lines:
    c.execute(line)

print(f"Part 1: {c.signal_sum}")

n = 40
image = ["".join(c.image[i:i+n]) for i in range(0, len(c.image), n)]

print("Part 2:")
for line in image:
    print(line)