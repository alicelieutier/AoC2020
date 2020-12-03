import sys
import itertools
from functools import reduce

def parse_lines(filename):
    f = open(filename)
    return [line.strip() for line in f.readlines()]

def has_tree(lines, index_right, index_down):
    modulo = len(lines[0])
    return lines[index_down][index_right % modulo] == '#'

def count_trees(lines, slope):
    down, right = slope
    positions_down = range(0, len(lines), down)
    positions_right = itertools.count(start=0, step=right)
    def aux(acc, position):
        down, right = position
        return acc + 1 if has_tree(lines, right, down) else acc
    return reduce(aux, zip(positions_down, positions_right), 0)

# change the input here
file = './day3/input'
lines = parse_lines(file)

# part 1
print(count_trees(lines, (1,3)))

# part 2
slopes = [(1,1), (1,3), (1,5), (1,7), (2,1)]
def aux(acc, slope):
    return acc * count_trees(lines, slope)
total_product = reduce(aux, slopes, 1)
print(total_product)
