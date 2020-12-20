import sys
import re
from functools import reduce, lru_cache
from operator import mul

NUMBER_PATTERN = re.compile(r'\d+')

def split_lines(lines):
    return [line.strip() for line in lines.split('\n')]

def parse_tile(tile_blob):
    lines = split_lines(tile_blob)
    tile_id = int(NUMBER_PATTERN.search(lines[0]).group(0))
    grid = [list(line) for line in lines[1:]]
    return tile_id, grid

def parse_tiles(filename):
    f = open(filename)
    tiles = f.read().split('\n\n')
    return {tile_id: grid for tile_id, grid in map(parse_tile, tiles)}

@lru_cache(maxsize=None)
def clockwise_edges_by_id(tile_id):
    top = ''.join(TILES[tile_id][0])
    bottom = ''.join(TILES[tile_id][-1][::-1])
    right = ''.join([line[-1] for line in TILES[tile_id]])
    left = ''.join([line[0] for line in TILES[tile_id][::-1]])
    return {top, right, bottom, left}

@lru_cache(maxsize=None)
def trigwise_edges_by_id(tile_id):
    top = ''.join(TILES[tile_id][0][::-1])
    bottom = ''.join(TILES[tile_id][-1])
    right = ''.join([line[-1] for line in TILES[tile_id][::-1]])
    left = ''.join([line[0] for line in TILES[tile_id]])
    return {top, right, bottom, left}

@lru_cache(maxsize=None)
def all_edges_by_id(tile_id):
    return trigwise_edges_by_id(tile_id) | clockwise_edges_by_id(tile_id)

def set_union(sets):
    return reduce(lambda a, b : a | b, sets)

file = './day20/input'
TILES = parse_tiles(file)

# Part 1
corner_tiles = []
for tile_id in TILES.keys():
    other_tiles_edges = set_union([all_edges_by_id(id) for id in TILES.keys() if id != tile_id])
    unmatched = clockwise_edges_by_id(tile_id) - other_tiles_edges
    if len(unmatched) == 2:
        corner_tiles.append(tile_id)
print(reduce(mul, corner_tiles))
