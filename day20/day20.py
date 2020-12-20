import sys
import re
# from functools import reduce, lru_cache
from collections import Counter

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

def clockwise_edges_from_grid(grid):
    top = ''.join(grid[0])
    bottom = ''.join(grid[-1][::-1])
    right = ''.join([line[-1] for line in grid])
    left = ''.join([line[0] for line in grid[::-1]])
    return (top, right, bottom, left)

def trigwise_edges_from_grid(grid):
    top = ''.join(grid[0][::-1])
    bottom = ''.join(grid[-1])
    right = ''.join([line[-1] for line in grid[::-1]])
    left = ''.join([line[0] for line in grid])
    return (top, right, bottom, left)

# change the input here
file = './day20/input'
tiles = parse_tiles(file)

clockwise_edges_by_id = {tile_id: clockwise_edges_from_grid(grid) for (tile_id, grid) in tiles.items()}

edges = {}
for tile_id, grid in tiles.items():
    for edge in clockwise_edges_from_grid(grid):
        edges[edge] = edges.setdefault(edge, set()) | {tile_id}
    for edge in trigwise_edges_from_grid(grid):
        edges[edge] = edges.setdefault(edge, set()) | {tile_id}

for tile_id in tiles.keys():
    other_edges = {t_edge for t_edge in edges if edges[t_edge] != {tile_id}}
    unmatched = [c_edge for c_edge in clockwise_edges_by_id[tile_id] if c_edge not in other_edges]
    if len(unmatched) == 2:
        print(tile_id)
