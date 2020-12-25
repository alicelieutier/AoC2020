import sys
from functools import reduce
from collections import Counter

def parse_directions(filename):
    f = open(filename)
    return [parse_line(line.strip()) for line in f.readlines()]

def parse_line(line):
    directions = []
    index = 0
    while index < len(line):
        if line[index] in 'ns':
            directions.append(line[index] + line[index+1])
            index += 2
        else:
            directions.append(line[index])
            index += 1
    return directions

def neighbors(tile):
    e, nw = tile
    return {
        (e, nw + 1),
        (e + 1, nw + 1),
        (e + 1, nw),
        (e, nw - 1),
        (e - 1, nw - 1),
        (e - 1, nw),
    }

def zero_or_more_than_two(iterable):
    count = iterable.count(True)
    return count == 0 or count > 2

def exactly_two(iterable):
    return iterable.count(True) == 2

def tiles_to_process(black_tiles):
    return black_tiles | reduce(lambda a, b : a | b, [neighbors(tile) for tile in black_tiles])

def tick(black_tiles):
    new_black_tiles = set()
    for tile in tiles_to_process(black_tiles):
        if ((tile in black_tiles and not zero_or_more_than_two([neighbor in black_tiles for neighbor in neighbors(tile)])) or
            (tile not in black_tiles and exactly_two([neighbor in black_tiles for neighbor in neighbors(tile)]))):
           new_black_tiles.add(tile)
    return new_black_tiles

# change the input here
file = './day24/input'
directions = parse_directions(file)

# Part 1
black_tiles = set()
for itinerary in directions:
    c = Counter(itinerary)
    # normalizing coordinates to be expressed in east/north_west coordinates
    east = c['e'] - c['w'] + c['ne'] - c['sw']
    north_west = c['nw'] - c['se'] + c['ne'] - c['sw']
    # flip
    black_tiles ^= {(east, north_west)}

print(len(black_tiles))

# Part 2
for _ in range(100):
    black_tiles = tick(black_tiles)

print(len(black_tiles))