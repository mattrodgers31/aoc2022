#! /usr/bin/python

import sys


with open(sys.argv[1], "r") as f:
    commands = [c.strip() for c in f.read().strip().split("$ ") if c]


class File():
    def __init__(self, name, parent, size) -> None:
        self.name = name
        self.parent = parent
        self.size = size

    def get_size(self):
        return self.size

    def get_path(self) -> str:
        if self.parent:
            return f"{self.parent.get_path()}/{self.name}"
        return self.name

    def __repr__(self) -> str:
        return f"{self.name} (file, size={self.size})"


class Directory():
    def __init__(self, name, parent, depth) -> None:
        self.name = name
        self.parent = parent
        self.depth = depth
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def get_size(self):
        return sum([c.get_size() for c in self.children])

    def get_path(self) -> str:
        if self.parent:
            return f"{self.parent.get_path()}/{self.name}"
        return ""

    def __repr__(self) -> str:
        indent = " " * self.depth * 2
        return f"{self.name} (dir, size={self.get_size()})" + "".join([f"\n{indent}{child}" for child in self.children])


# Assert we always start from directory "/"
assert(commands[0] == "cd /")
current = Directory("/", None, 1)
root = current

# Construct directory structure
for c in commands[1:]:
    if c[0:2] == "cd":
        loc = c[3:]
        if loc == "..":
            current = current.parent
        else:
            path = loc.split("/")
            for p in path:
                for i, ch in enumerate(current.children):
                    if ch.name == p:
                        current = current.children[i]
                        break
                    if i == len(current.children) - 1:
                        assert(0) # Did not find match
    elif c[0:2] == "ls":
        items = c.split("\n")
        for item in items[1:]:
            size, name = item.split()
            if size == "dir":
                current.add_child(Directory(name, current, current.depth + 1))
            else:
                current.add_child(File(name, current, int(size)))
    else:
        assert(0)

print(f"File structure: ")
print(root)
print("")

# Part 1
# Traverse directory structure and sum size of directories that have a size <= 100000
def traverse_dir_sizes(dir: Directory, record: dict):
    cur_size = dir.get_size()
    record[dir.get_path()] = cur_size

    for c in dir.children:
        if isinstance(c, Directory):
            traverse_dir_sizes(c, record)

directories = {}
traverse_dir_sizes(root, directories)

pt1 = 0
for dir, size in directories.items():
    if size <= 100000:
        pt1 += size

print(f"Part 1: {pt1}")

# Part 2
# Find the smallest directory we can delete which frees up enough space
total_space = 70000000
required_space = 30000000
size_to_delete = root.get_size() + required_space - total_space

pt2 = total_space # Start with a numer larger than root size
for dir, size in directories.items():
    if size >= size_to_delete: # Find directories big enough to free up required space
        if size < pt2: # Choose the smallest one
            pt2 = size

print(f"Part 2: {pt2}")