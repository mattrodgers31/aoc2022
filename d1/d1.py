#! /usr/bin/python

with open("input.txt", "r") as f:
    elves = f.read().split("\n\n")

elf_calories = []

for elf in elves:
    food_items = elf.split("\n")
    if '' in food_items:
        food_items.remove('')
    calories =  sum([int(food) for food in food_items])
    elf_calories.append(calories)

elf_calories.sort()

print(f"Part 1: {elf_calories[-1]}")
print(f"Part 2: {sum(elf_calories[-3:])}")
