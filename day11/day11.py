import sys
from functools import reduce, lru_cache
from itertools import count, islice

def parse_seats(filename):
    f = open(filename)
    return [list(line.strip()) for line in f.readlines()]

# using a flattened array because why not, using this method to read i,j values
def get(map, i, j):
    return map[i * J_DIMENSION + j]

def is_within_bounds(i, j):
    return i >= 0 and i < I_DIMENSION and j >= 0 and j < J_DIMENSION

def is_seat(i, j):
    return get(FLATTENED_SEATS, i, j) != '.'

def is_empty(map, i, j):
    return get(map, i, j) != '#'

def is_occupied(map, i, j):
    return get(map, i, j) == '#'

# remember the set of adjacent seat coordinates for any given seat
@lru_cache(maxsize=None)
def adjacent_seats(x, y):
    adjacent_coords = {(i, j) for i in range(x-1, x+2) for j in range(y-1, y+2)} - {(x, y)}
    seats_only = {(i, j) for (i, j) in adjacent_coords if is_within_bounds(i, j) and is_seat(i, j)}
    return seats_only

# finds next visible seat in a direction, returns None if the edge is visible instead
def next_visible_seat(x, y, direction):
    dx, dy = direction
    gen_seats_in_direction = (coord for coord in  zip(count(x + dx, dx), count(y + dy, dy)))
    for (i, j) in gen_seats_in_direction:
        if not is_within_bounds(i, j):
            return None
        if is_seat(i, j):
            return (i, j)

EIGHT_DIRECTIONS = {(i, j) for i in range(-1, 2) for j in range(-1, 2)} - {(0, 0)}

# remember the set of visible seat coordinates for any given seat
@lru_cache(maxsize=None)
def visible_seats(x, y):
    visible_seats = {next_visible_seat(x, y, direction) for direction in EIGHT_DIRECTIONS} - { None }
    return visible_seats

def four_or_more(iterable):
    return iterable.count(True) >= 4

def five_or_more(iterable):
    return iterable.count(True) >= 5

ADJACENT_SEATS_RULES = {
    '.': lambda *args : '.',
    'L': lambda map, i, j : '#' if all([is_empty(map, x, y) for (x,y) in adjacent_seats(i, j)]) else 'L',
    '#': lambda map, i, j : 'L' if four_or_more([is_occupied(map, x, y) for (x, y) in adjacent_seats(i, j)]) else '#'
}

VISIBLE_SEATS_RULES = {
    '.': lambda *args : '.',
    'L': lambda map, i, j : '#' if all([is_empty(map, x, y) for (x,y) in visible_seats(i, j)]) else 'L',
    '#': lambda map, i, j : 'L' if five_or_more([is_occupied(map, x, y) for (x, y) in visible_seats(i, j)]) else '#'
}

# get the ticker for a given set of rules
def get_tick(rules):
    def aux(map):
        apply_rules = lambda map, i, j : rules[get(map, i, j)](map, i, j)
        # this order - for i then for j - is important, otherwise it transposes the grid everytime
        return [apply_rules(map, i, j) for i in range(I_DIMENSION) for j in range(J_DIMENSION)]
    return aux

# pretty print used for debugging
def pretty_print(map):
    print('\n'.join([''.join(islice(map, J_DIMENSION * i, J_DIMENSION * (i+1))) for i in range(I_DIMENSION)]))

# will return the number of occupied seats once stable
def find_stable_state(map, tick):
    count = 0
    new_map = tick(map)
    new_count = new_map.count('#')
    while new_count != count:
        new_map = tick(new_map)
        count, new_count = new_count, new_map.count('#')
    return count

# change the input here
file = './day11/input'
SEATS = parse_seats(file)
I_DIMENSION = len(SEATS)
J_DIMENSION = len(SEATS[0])
FLATTENED_SEATS = [SEATS[i][j] for i in range(I_DIMENSION) for j in range(J_DIMENSION)]

# part 1
print(find_stable_state(FLATTENED_SEATS, get_tick(ADJACENT_SEATS_RULES)))

# part 2
print(find_stable_state(FLATTENED_SEATS, get_tick(VISIBLE_SEATS_RULES)))