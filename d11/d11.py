#! /usr/bin/python

import sys
from operator import mul, add
from collections import deque
from math import floor, prod


with open(sys.argv[1], "r") as f:
    ip = f.read().strip().split("\n\n")


def divs(a, b):
    return 0 == a % b


OPERATORS = {"*": mul, "+": add}
TESTS = {"divisible": divs}


class Monkey():
    def __init__(self, items, operation, test, on_true, on_false) -> None:
        self.items = deque(items)
        self.operation = operation
        self.test = test
        self.on_true = on_true
        self.on_false = on_false
        self.inspection_count = 0

    def __repr__(self):
        return (f"Items: {self.items}\n"
                f"Operation: new = old {self.operation[0]} {self.operation[1]}\n"
                f"Test: {self.test[0]} by {self.test[1]}\n"
                f"On True: throw to {self.on_true}\n"
                f"On False: throw to {self.on_false}\n"
                f"Inspection count: {self.inspection_count}")

    @classmethod
    def from_str(cls, string):
        lines = string.split("\n")
        items = [int(item.strip(",")) for item in lines[1].split()[2:]]
        op = OPERATORS[lines[2].split()[4]]
        op_val = lines[2].split()[5]
        test = TESTS[lines[3].split()[1]]
        test_val = int(lines[3].split()[3])
        on_true = int(lines[4].split()[5])
        on_false = int(lines[5].split()[5])
        return cls(items, (op, op_val), (test, test_val), on_true, on_false)

    def throw_to(self, item):
        self.items.append(item)

    def take_turn(self, monkeylist, pt2):
        for _ in range(len(self.items)):
            # Get item
            item = self.items.popleft()

            # Perform operation
            if self.operation[1] == "old":
                item = self.operation[0](item, item)
            else:
                item = self.operation[0](item, int(self.operation[1]))

            if pt2:
                # If we keep only the value mod N, where N is the product of all divisors,
                # then the maths still works but we avoid having to deal with enormous numbers
                item = item % divisor_product
            else:
                # Reduce worry level
                item = floor(item / 3)
            
            # Perform test
            test = self.test[0](item, self.test[1])
            
            # Apply result of test
            if test:
                monkeylist[self.on_true].throw_to(item)
            else:
                monkeylist[self.on_false].throw_to(item)

            # Increment inspection count
            self.inspection_count += 1
        

# Part 1
monkeys = [Monkey.from_str(s) for s in ip]

ROUNDS = 20
for _ in range(ROUNDS):
    for m in monkeys:
        m.take_turn(monkeys, False)

inspection_counts = sorted([m.inspection_count for m in monkeys])
print(f"Part 1: {inspection_counts[-1] * inspection_counts[-2]}")


# Part 2
monkeys = [Monkey.from_str(s) for s in ip]
divisor_product = prod([m.test[1] for m in monkeys])

ROUNDS = 10000
for _ in range(ROUNDS):
    for m in monkeys:
        m.take_turn(monkeys, True)

inspection_counts = sorted([m.inspection_count for m in monkeys])
print(f"Part 2: {inspection_counts[-1] * inspection_counts[-2]}")