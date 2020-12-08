import sys
import re
from itertools import count

def parse_instructions(filename):
    f = open(filename)
    return [parse_instruction(line.strip(), index) for line, index in zip(f.readlines(), count())]

LINE_PATTERN = re.compile(r'^(?P<instruction>\w{3}) (?P<argument>[-+]\d+)$')
def parse_instruction(line, index):
    match = LINE_PATTERN.search(line)
    instruction, argument = match.group('instruction'), int(match.group('argument'))
    return index, instruction, argument

def execute(instructions):
    current_index = 0
    acc = 0
    while True:
        if current_index >= len(instructions):
            yield acc, 0, 'end', 0
            return
        index, instruction, argument = instructions[current_index]
        yield acc, index, instruction, argument
        acc, current_index = execute_one_instruction(acc, index, instruction, argument)

def execute_one_instruction(acc, index, instruction, argument):
    acc = acc + argument if instruction == 'acc' else acc
    next_index = index + argument if instruction == 'jmp' else index + 1
    return acc, next_index

def terminate(instructions):
    execution = execute(instructions)
    seen = set()
    for step in execution:
        acc, index, instruction, _ = step
        if instruction == 'end':
            return (True, acc)
        if index in seen:
            return (False, acc)
        seen.add(index)

# change the input here
file = './day8/input'
instructions = parse_instructions(file)

# part 1
print(terminate(instructions)[1])

# part 2
instructions_copy = instructions[:]
for index, instruction, argument in instructions_copy:
    if instruction == 'nop':
        instructions[index] = (index, 'jmp', argument)
    elif instruction == 'jmp':
        instructions[index] = (index, 'nop', argument)
    does_terminate, acc = terminate(instructions)
    if does_terminate:
        print(acc)

    instructions[index] = (index, instruction, argument)