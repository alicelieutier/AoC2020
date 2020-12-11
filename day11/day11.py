import sys
# import re
from functools import reduce
# from collections import deque
from itertools import count

def parse_seats(filename):
    f = open(filename)
    return [list(line.strip()) for line in f.readlines()]

def is_empty(map, i, j):
    return map[i][j] != '#'

def is_occupied(map, i, j):
    return map[i][j] == '#'

def is_within_bounds(map, i, j):
    return i >= 0 and i < len(map) and j >= 0 and j < len(map[i])

def memoize_skip_first_arg(fun):
    memo = {}
    def helper(skipped, x, y):
        if (x, y) not in memo:            
            memo[(x, y)] = fun(skipped, x, y)
        return memo[(x, y)]
    return helper

def is_seat(map, i, j):
    return map[i][j] != '.'

@memoize_skip_first_arg
def adjacent_seats(map, x, y):
    nine_adjacent_coords = {(i, j) for i in range(x-1, x+2) for j in range(y-1, y+2)}
    seats_only = {(i, j) for (i, j) in nine_adjacent_coords if is_within_bounds(map, i, j) and is_seat(map, i, j)}
    return seats_only - {(x, y)}

def next_visible_seat(map, x, y, direction):
    dx, dy = direction
    gen_seats_in_direction = (coord for coord in  zip(count(x + dx, dx), count(y + dy, dy)))
    for (i, j) in gen_seats_in_direction:
        if not is_within_bounds(map, i, j):
            return None
        if is_seat(map, i, j):
            return (i, j)

@memoize_skip_first_arg
def visible_seats(map, x, y):
    directions = {(i, j) for i in range(-1, 2) for j in range(-1, 2)} - {(0, 0)}
    visible_seats = {next_visible_seat(map, x, y, direction) for direction in directions} - { None }
    return visible_seats

def four_or_more(array):
    return len([i for i in array if i == True]) >= 4

def five_or_more(array):
    return len([i for i in array if i == True]) >= 5

def adjacent_cell_rule(map, i, j):
    moves = {
        '.': '.',
        'L': '#' if all([is_empty(map, x, y) for (x,y) in adjacent_seats(map, i, j)]) else 'L',
        '#': 'L' if four_or_more([is_occupied(map, x, y) for (x,y) in adjacent_seats(map, i, j)]) else '#'
    }
    return moves[map[i][j]]

def visible_cell_rule(map, i, j):
    moves = {
        '.': '.',
        'L': '#' if all([is_empty(map, x, y) for (x,y) in visible_seats(map, i, j)]) else 'L',
        '#': 'L' if five_or_more([is_occupied(map, x, y) for (x,y) in visible_seats(map, i, j)]) else '#'
    }
    return moves[map[i][j]]

def check_adjacent_seat_tick(initial_map):
    return [[adjacent_cell_rule(initial_map, i, j) for j in range(len(initial_map[i]))] for i in range(len(initial_map)) ]

def check_visible_seat_tick(initial_map):
    return [[visible_cell_rule(initial_map, i, j) for j in range(len(initial_map[i]))] for i in range(len(initial_map)) ]

def count_occupied(map):
    flattened = (map[i][j] for i in range(len(map)) for j in range(len(map[i])))
    def aux(acc, seat):
        return acc + 1 if seat == '#' else acc
    return reduce(aux, flattened, 0)

def pretty_print(map):
    print('\n'.join([''.join(line) for line in map]))

def find_stable_state(map, tick):
    count = 0
    new_map = tick(map)
    new_count = count_occupied(new_map)
    while new_count != count:
        new_map = tick(new_map)
        count, new_count = new_count, count_occupied(new_map)
    return count

# change the input here
file = './day11/input'
seats = parse_seats(file)

# part 1
print(find_stable_state(seats, check_adjacent_seat_tick))

# part 2
print(find_stable_state(seats, check_visible_seat_tick))