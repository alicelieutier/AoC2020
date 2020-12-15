import sys

def starting_numbers_from_file(filename):
    f = open(filename)
    return [int(number) for number in f.read().strip().split(',')]

def print_number_at_turns(turns, starting_numbers):
    last_turn_spoken = {n: index + 1 for index, n in enumerate(starting_numbers[:-1])}
    last_spoken = starting_numbers[-1]
    turn = len(starting_numbers)

    for turn_to_print in sorted(turns):
        while turn < turn_to_print:
            last_time_spoken = last_turn_spoken.get(last_spoken, None)
            spoken = 0 if last_time_spoken is None else (turn - last_time_spoken)
            last_turn_spoken[last_spoken] = turn
            turn += 1
            last_spoken = spoken
        print(turn, spoken)

# change the input here
file = './day15/input'
starting_numbers = starting_numbers_from_file(file)

# Parts 1 and 2
print_number_at_turns((2020, 30000000), starting_numbers)