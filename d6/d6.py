#! /usr/bin/python

import sys


with open(sys.argv[1], "r") as f:
    ip = f.read().strip()


class PacketParser():
    def __init__(self, num_distinct) -> None:
        self.count = 0
        self.num_distinct = num_distinct
        self.last_chars = []

    def add_char(self, char) -> int:
        # Track number of characters processed
        self.count += 1

        # Ensure no more than 4 items in list (of last four characters)
        if len(self.last_chars) == self.num_distinct:
            del self.last_chars[0]

        # Add current character to queue
        self.last_chars.append(char)

        if len(set(self.last_chars)) == self.num_distinct:
            # Got 4 unique characters, done
            return True, self.count

        return False, self.count


# Part 1
p = PacketParser(4)
for char in ip:
    done, count = p.add_char(char)
    if done:
        print(f"Part 1: {count}")
        break


# Part 2
p = PacketParser(14)
for char in ip:
    done, count = p.add_char(char)
    if done:
        print(f"Part 2: {count}")
        break
