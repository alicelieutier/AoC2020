import sys
import re
from functools import reduce

def parse_instructions(filename):
    f = open(filename)
    return [parse_instruction(line.strip()) for line in f.readlines()]

LINE_PATTERN = re.compile(r'(?P<action>[NEWSLRF])(?P<value>\d+)')
def parse_instruction(line):
    match = LINE_PATTERN.search(line)
    action, value = match.group('action'), int(match.group('value'))
    return (action, value)

RIGHT_TURN = ['N', 'E', 'S', 'W']
def calculate_new_facing_direction(initial_direction, action, value):
    if action not in {'L', 'R'}:
        return initial_direction
    angle = value if action == 'R' else 360 - value
    offset = RIGHT_TURN.index(initial_direction)
    quarter_turns = angle // 90
    return RIGHT_TURN[(offset + quarter_turns) % 4]

NS_EW_VALUES = {
    'N': lambda ns, ew, value : (ns + value, ew),
    'S': lambda ns, ew, value : (ns - value, ew),
    'E': lambda ns, ew, value : (ns, ew + value),
    'W': lambda ns, ew, value : (ns, ew - value),
    'L': lambda ns, ew, _ : (ns, ew),
    'R': lambda ns, ew, _ : (ns, ew),
}
def run_intructions(instructions):
    def aux(acc, instruction):
        ns, ew, facing = acc
        action, value = instruction
        if action == 'F':
            action = facing
        ns, ew = NS_EW_VALUES[action](ns, ew, value)
        return ns, ew, calculate_new_facing_direction(facing, action, value)
    return reduce(aux, instructions, (0, 0, 'E'))


def simple_sine(angle): return [0, 1, 0, -1][angle // 90 % 4]
def simple_cosine(angle): return [1, 0, -1, 0][angle // 90 % 4]

def coords_after_rotation(ship_coords, waypoint_coords, action, value):
    # 𝑥′=(𝑥−𝑝)cos(𝜃)−(𝑦−𝑞)sin(𝜃)+𝑝
    # 𝑦′=(𝑥−𝑝)sin(𝜃)+(𝑦−𝑞)cos(𝜃)+𝑞
    p, q = ship_coords
    x, y = waypoint_coords
    theta = value if action == 'L' else 360 - value
    new_x = (x - p)*simple_cosine(theta) - (y - q)*simple_sine(theta) + p
    new_y = (x - p)*simple_sine(theta) + (y - q)*simple_cosine(theta) + q
    return ship_coords, (new_x, new_y)

def coords_after_move_forward(ship_coords, waypoint_coords, value):
    sx, sy = ship_coords
    wx, wy = waypoint_coords
    move_x, move_y = value * (wx - sx), value * (wy - sy)
    return (sx + move_x, sy + move_y), (wx + move_x, wy + move_y)

ABSOLUTE_MOVE = {
    'N': lambda x, y, value : (x, y + value),
    'S': lambda x, y, value : (x, y - value),
    'E': lambda x, y, value : (x + value, y),
    'W': lambda x, y, value : (x - value, y),
}
def coords_after_waypoint_move(ship_coords, waypoint_coords, action, value):
    wx, wy = waypoint_coords
    new_x, new_y = ABSOLUTE_MOVE[action](wx, wy, value)
    return ship_coords, (new_x, new_y)

def run_part2_instructions(instructions):
    def aux(acc, instruction):
        ship_coords, waypoint_coords = acc
        action, value = instruction
        if action == 'F':
            return coords_after_move_forward(ship_coords, waypoint_coords, value)
        if action in {'L', 'R'}:
            return coords_after_rotation(ship_coords, waypoint_coords, action, value)
        return coords_after_waypoint_move(ship_coords, waypoint_coords, action, value) 
    return reduce(aux, instructions, ((0, 0), (10, 1)))

# change the input here
file = './day12/input'
instructions = parse_instructions(file)

# Part 1
final_ns, final_ew, _ = run_intructions(instructions)
print(abs(final_ns) + abs(final_ew))

# Part 2
(x, y), _ = run_part2_instructions(instructions)
print(abs(x) + abs(y))

# Tests
# Part 1
assert(calculate_new_facing_direction('N', 'R', 90) == 'E')
assert(calculate_new_facing_direction('N', 'R', 180) == 'S')
assert(calculate_new_facing_direction('S', 'R', 270) == 'E')
assert(calculate_new_facing_direction('E', 'L', 180) == 'W')
assert(calculate_new_facing_direction('W', 'L', 90) == 'S')
assert(calculate_new_facing_direction('E', 'N', 23) == 'E')
assert(calculate_new_facing_direction('W', 'E', 6) == 'W')

# Part 2
assert(simple_sine(270) == -1)
assert(simple_cosine(270) == 0)
assert(simple_sine(360) == 0)
assert(simple_cosine(360) == 1)

assert(coords_after_rotation((1, 1), (3, 2), 'L', 90) == ((1, 1), (0, 3)))
assert(coords_after_rotation((1, 1), (3, 2), 'L', 180) == ((1, 1), (-1, 0)))
assert(coords_after_rotation((2, 1), (-1, 0), 'R', 90) == ((2, 1), (1, 4)))
assert(coords_after_rotation((2, 1), (-1, 0), 'R', 180) == ((2, 1), (5, 2)))

assert(coords_after_move_forward((2, 2), (3, 4), 3) == ((5, 8), (6, 10)))
assert(coords_after_waypoint_move((2, 4), (4, 5),'W', 5) == ((2, 4), (-1, 5)))