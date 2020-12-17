import sys
from functools import reduce, lru_cache

def parse_live_cells(filename):
    f = open(filename)
    grid = [list(line.strip()) for line in f.readlines()]
    return {(i, j, 0) for i in range(len(grid)) for j in range(len(grid[0])) if grid[i][j] == '#'}

def parse_live_cells_4D(filename):
    f = open(filename)
    grid = [list(line.strip()) for line in f.readlines()]
    return {(i, j, 0, 0) for i in range(len(grid)) for j in range(len(grid[0])) if grid[i][j] == '#'}

@lru_cache(maxsize=None)
def neighbors(cell):
    x, y, z = cell
    return {(i, j, k) for i in range(x-1, x+2) for j in range(y-1, y+2) for k in range(z-1, z+2)} - {cell}

@lru_cache(maxsize=None)
def neighbors_4D(cell):
    x, y, z, w = cell
    return {(i, j, k, l) for i in range(x-1, x+2) for j in range(y-1, y+2) for k in range(z-1, z+2) for l in range(w-1, w+2)} - {cell}

def two_or_three(iterable):
    count = iterable.count(True)
    return count == 2 or count == 3

def three(iterable):
    return iterable.count(True) == 3

def cells_to_process(live_cells):
    return live_cells | reduce(lambda a, b : a | b, [neighbors(cell) for cell in live_cells])

def cells_to_process_4D(live_cells):
    return live_cells | reduce(lambda a, b : a | b, [neighbors_4D(cell) for cell in live_cells])

# If a cube is active and exactly 2 or 3 of its neighbors are also active,
# the cube remains active. Otherwise, the cube becomes inactive.
# If a cube is inactive but exactly 3 of its neighbors are active,
# the cube becomes active. Otherwise, the cube remains inactive.
def tick(live_cells):
    new_live_cells = set()
    for cell in cells_to_process(live_cells):
        if (cell in live_cells and two_or_three([neighbor in live_cells for neighbor in neighbors(cell)]) or
            cell not in live_cells and three([neighbor in live_cells for neighbor in neighbors(cell)])):
            new_live_cells.add(cell)
    return new_live_cells

def tick_4D(live_cells):
    new_live_cells = set()
    for cell in cells_to_process_4D(live_cells):
        if (cell in live_cells and two_or_three([neighbor in live_cells for neighbor in neighbors_4D(cell)]) or
            cell not in live_cells and three([neighbor in live_cells for neighbor in neighbors_4D(cell)])):
            new_live_cells.add(cell)
    return new_live_cells

# change the input here
file = './day17/input'

# Part 1
live_cells = parse_live_cells(file)
for i in range(6):
    live_cells = tick(live_cells)
print(len(live_cells))

# Part 2
live_cells = parse_live_cells_4D(file)
for i in range(6):
    live_cells = tick_4D(live_cells)
print(len(live_cells))
