import sys
import re
from math import isqrt
from functools import reduce, lru_cache
from itertools import cycle

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
    return [Tile(tile_id, grid) for tile_id, grid in map(parse_tile, tiles)]

def set_union(sets):
    return reduce(lambda a, b : a | b, sets)

class Tile:
    def __init__(self, id, grid):
        self.id = id
        self.grid = grid

    def __str__(self):
        return '\n'.join([
            str(self.id),
            '\n'.join([''.join([str(el) for el in line]) for line in self.grid])
        ])
    
    def rotate_quater_turn_right(self):
        self.grid = tuple([tuple([line[i] for line in self.grid[::-1]]) for i in range(len(self.grid[0]))])

    def flip_horizontally(self):
        self.grid = tuple(tuple(line[::-1]) for line in self.grid)

    EDGES = {
        'top': lambda grid: ''.join(grid[0]),
        'bottom': lambda grid: ''.join(grid[-1][::-1]),
        'right': lambda grid: ''.join([line[-1] for line in grid]),
        'left': lambda grid: ''.join([line[0] for line in grid[::-1]]),
    }

    def edge(self, side='top', direction='clockwise'):
        result = self.EDGES[side](self.grid)
        return result if direction == 'clockwise' else ''.join(result[::-1])

    def all_edges(self):
        return set([self.edge(side, direction) for side in self.EDGES.keys() for direction in ['clockwise', 'trig']])

    def all_clockwise_edges(self):
        return set([self.edge(side) for side in self.EDGES.keys()])

    def intersection(self, other):
        if self.match(other):
            return list(self.all_edges() & other.all_edges())
        return None

    def match(self, other):
        return len(self.all_edges() & other.all_edges()) == 2

    def rotate_flip(self):
        while True:
            for _ in range(4):
                self.rotate_quater_turn_right()
                yield
            self.flip_horizontally()

class Image:
    TILE_DIM = 10
    def __init__(self, dim):
        self.grid = [[None]*dim for _ in range(dim)]
        self.dim = dim
        self.image_dim = dim * (self.TILE_DIM - 2)
        self.open_positions = set()

    def __empty_tile__(self):
        return [[' '] * self.TILE_DIM for _ in range(self.TILE_DIM)]

    def __str__(self):
        return '\n'.join(['|'.join(line) for line in self.__id_map__()])

    def print_image(self):
        print(self.image_string())

    def image_string(self):
        return '\n'.join([''.join([self.get_pixel_no_edges(i, j) for j in range(self.image_dim)]) for i in range(self.image_dim)])

    def get_pixel_no_edges(self, top, left):
        tile = self.grid[top // (self.TILE_DIM - 2)][left // (self.TILE_DIM - 2)]
        grid = tile.grid if tile is not None else self.__empty_tile__()
        return grid[(top % (self.TILE_DIM - 2)) + 1][(left % (self.TILE_DIM - 2)) + 1]

    def __id_map__(self):
        def id_or_none(t): return str(t.id) if t is not None else 'None'
        return [[id_or_none(tile) for tile in line] for line in self.grid]

    def set_tile(self, top, right, tile):
        self.grid[top][right] = tile

    def place_top_left(self, corner_tile, bottom_and_right_edges):
        self.set_tile(0, 0, corner_tile)
        transform = corner_tile.rotate_flip()
        while not(corner_tile.edge('bottom') in bottom_and_right_edges and corner_tile.edge('right') in bottom_and_right_edges):
            next(transform)
        self.open_positions |= {(0, 1), (1, 0)}

    def __is_within_bounds(self, i, j):
        return i >= 0 and i < self.dim and j >= 0 and j < self.dim

    def __get_default(self, i, j):
        return self.grid[i][j] if self.__is_within_bounds(i, j) else None
        
    def __neighbors(self, top, right):
        return {
            'left': self.__get_default(top, right - 1),
            'top': self.__get_default(top - 1, right),
            'right': self.__get_default(top, right + 1),
            'bottom': self.__get_default(top + 1, right),
        }

    def __open_neighbors(self, x, y):
        return {(i, j) for (i, j) in [(x-1,y),(x+1, y),(x, y-1),(x, y+1)] if (self.__is_within_bounds(i, j) and self.grid[i][j] == None )}

    OPPOSITE_SIDE = {
        'top': 'bottom',
        'bottom': 'top',
        'right': 'left',
        'left': 'right',
    }

    def __edges_to_match_trig(self, i, j):
        edges = {}
        for side, tile in self.__neighbors(i, j).items():
            if tile is not None:
                edges[side] = tile.edge(self.OPPOSITE_SIDE[side], 'trig')
        return edges

    def try_tile_at(self, tile, i, j):
        if any([(not tile.match(neigh)) for neigh in set(self.__neighbors(i, j).values()) - {None}]):
            return False
        transform = tile.rotate_flip()
        edges_to_match = self.__edges_to_match_trig(i, j)
        turns = 0
        while not all([tile.edge(side) == edges_to_match[side] for side in edges_to_match.keys()]):
            next(transform)
            turns += 1
            if turns > 12:
                return False
        self.set_tile(i, j, tile)
        self.open_positions -= {(i, j)}
        self.open_positions |= self.__open_neighbors(i, j)
        return True
        
    def place_tiles(self, tiles):
        while len(self.open_positions) > 0:
            i, j = self.open_positions.pop()
            for tile in tiles:
                result = self.try_tile_at(tile, i, j)
                if result == True:
                    tiles -= {tile}
                    break

file = './day20/input'
TILES = parse_tiles(file)

# Part 1
corner_tiles = set()
for current_tile in TILES:
    other_tiles_edges = set_union([tile.all_edges() for tile in TILES if tile.id != current_tile.id])
    unmatched = current_tile.all_clockwise_edges() - other_tiles_edges
    if len(unmatched) == 2:
        corner_tiles.add(current_tile)
print(reduce(lambda acc, t: acc * t.id, corner_tiles, 1))

# Part 2
# Start with a corner tile
top_left_tile = corner_tiles.pop()
tiles_to_use = set(TILES) - {top_left_tile}

edges = []
for tile in tiles_to_use:
    if top_left_tile.match(tile):
        edges.extend(top_left_tile.intersection(tile))

image = Image(isqrt(len(TILES)))
image.place_top_left(top_left_tile, edges)
image.place_tiles(tiles_to_use)

sea_monster = [
    '                  # ',
    '#    ##    ##    ###',
    ' #  #  #  #  #  #   '
]
sea_monster_coords = [(i, j) for i in range(len(sea_monster)) for j in range(len(sea_monster[0])) if sea_monster[i][j] == '#']
def sea_monster_at(grid, i, j):
    return all([grid[i+x][j+y] == '#' for x, y in sea_monster_coords])

def count_sea_monster(grid):
    return len([(i, j) for i in range(len(grid) - len(sea_monster)) for j in range(len(grid[0]) - len(sea_monster[0])) if sea_monster_at(grid, i, j)])

full_image = Tile('full image', image.image_string().split('\n'))
transform = full_image.rotate_flip()
sea_monster_count = 0
for _ in range(10):
    sea_monster_count += count_sea_monster(full_image.grid)
    next(transform)

def hash_count(grid):
    return len([(i, j) for i in range(len(grid)) for j in range(len(grid[0])) if grid[i][j] == '#'])

sea_monster_hashes = hash_count(sea_monster)
print(hash_count(full_image.grid) - sea_monster_count * sea_monster_hashes)

# Tests
t = Tile('alice', ('aab', '123', '678'))
t.rotate_quater_turn_right()
t.rotate_quater_turn_right()
t.flip_horizontally()
assert(t.edge() == '678')
assert(t.edge('left') == 'a16')
assert(t.edge('bottom', 'trig') == 'aab')
assert(t.all_edges() == {'a16', '61a', 'baa', 'aab', '678', '83b', '876', 'b38'})

g =  """.####...#####..#...###..
#####..#..#.#.####..#.#.
.#.#...#.###...#.##.##..
#.#.##.###.#.##.##.#####
..##.###.####..#.####.##
...#.#..##.##...#..#..##
#.##.#..#.#..#..##.#.#..
.###.##.....#...###.#...
#.####.#.#....##.#..#.#.
##...#..#....#..#...####
..#.##...###..#.#####..#
....#.##.#.#####....#...
..##.##.###.....#.##..#.
#...#...###..####....##.
.#.##...#.##.#.#.###...#
#.###.#..####...##..#...
#.###...#.##...#.######.
.###.###.#######..#####.
..##.#..#..#.#######.###
#.#..##.########..#..##.
#.#####..#.#...##..#....
#....##..#.#########..##
#...#.....#..##...###.##
#..###....##.#...##.##.#"""

tt = Tile('sea', g.split('\n'))
assert(count_sea_monster(tt.grid) == 2)

