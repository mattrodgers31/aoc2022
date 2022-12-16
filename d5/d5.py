#! /usr/bin/python

import sys
import re


STACK_SPACING = 4
INSTR_REGEX = r"move (\d+) from (\d+) to (\d+)"


with open(sys.argv[1], "r") as f:
    ip = f.read().split("\n\n")


def parse_crates(crates_input: str) -> list:
    lines = crates_input.split("\n")

    # Validate that each input line is padded to the same size
    expected_len = len(lines[0])
    for line in lines:
        assert(len(line) == expected_len)

    # Create empty stacks
    num_stacks = len(lines[-1].split())
    stacks = [[] for _ in range(num_stacks)]

    # Add each crate to relevant stack
    for line in reversed(lines[:-1]):
        for i in range(num_stacks):
            crate = line[i*4 + 1]
            if crate != " ":
                stacks[i].append(crate)

    return stacks


def parse_instructions(instructions_input):
    lines = [l for l in instructions_input.split("\n") if l]

    instructions = []

    for line in lines:
        r = re.search(INSTR_REGEX, line)
        instructions.append((int(r.group(1)), int(r.group(2)) - 1, int(r.group(3)) - 1))

    return instructions


# Part 1:
stacks = parse_crates(ip[0])
instr = parse_instructions(ip[1])

# Perform all instructions
for num, source, dest in instr:
    for _ in range(num):
        crate = stacks[source].pop()
        stacks[dest].append(crate)

# Take the top crate of each stack and stick together
pt1 = "".join([s.pop() for s in stacks])
print(f"Part 1: {pt1}")

# Part 2:
# Re-create the input
stacks = parse_crates(ip[0])
instr = parse_instructions(ip[1])


# Perform all instructions
for num, source, dest in instr:
    tmp = []
    for _ in range(num):
        crate = stacks[source].pop()
        tmp.append(crate)
    for _ in range(num):
        crate = tmp.pop()
        stacks[dest].append(crate)

# Take the top crate of each stack and stick together
pt2 = "".join([s.pop() for s in stacks])
print(f"Part 2: {pt2}")