import sys
import re

def parse_instructions(filename):
    f = open(filename)
    return [parse_instruction(line.strip()) for line in f.readlines()]

# eg: mem[8] = 11
MEM_PATTERN = re.compile(r'mem\[(?P<address>\d+)\] = (?P<value>\d+)')
# eg: mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
MASK_PATTERN = re.compile(r'mask = (?P<mask>[01X]{36})')

def parse_instruction(line):
    match = MEM_PATTERN.search(line)
    if match is None:
        match = MASK_PATTERN.search(line)
        return {'type': 'mask', 'mask': match.group('mask')}
    return {'type': 'mem', 'address': int(match.group('address')), 'value': int(match.group('value'))}

def one_mask(mask, value):
    one_mask = int(mask.replace('X','0'), 2)
    return value | one_mask

def zero_mask(mask, value):
    zero_mask = int(mask.replace('X','1'), 2)
    return value & zero_mask

def masked_v1(mask, value):
    return one_mask(mask, zero_mask(mask, value))

def run_instructions_v1(instructions):
    mem = {}
    mask = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    for instruction in instructions:
        if instruction['type'] == 'mask':
            mask = instruction['mask']
        else:
            mem[instruction['address']] = masked_v1(mask, instruction['value'])
    return mem

def find_all_with_index(string, character):
    position = string.find(character)
    while position > -1:
        yield position
        position = string.find(character, position + 1)

def permutations_0_1(length):
    for i in range(2 ** length):
        yield format(i, '0{}b'.format(length))

def gen_floating_bits_addresses(mask, address):
    address_array = list(format(address, '036b'))
    X_positions = list(find_all_with_index(mask, 'X'))
    for permutation in permutations_0_1(len(X_positions)):
        for character, index in zip(permutation, X_positions):
            address_array[index] = character
        yield int(''.join(address_array), 2)

def get_address_generator(mask):
    def gen_masked_addresses(address):
        address = one_mask(mask, address)
        for address in gen_floating_bits_addresses(mask, address):
            yield address 
    return gen_masked_addresses

def run_instructions_v2(instructions):
    mem = {}
    address_generator = lambda address : [address]
    for instruction in instructions:
        if instruction['type'] == 'mask':
            address_generator = get_address_generator(instruction['mask'])
        else:
            for address in address_generator(instruction['address']):
                mem[address] = instruction['value']
    return mem

# change the input here
file = './day14/input'
instructions = parse_instructions(file)

# Part 1
final_state = run_instructions_v1(instructions)
print(sum(final_state.values()))

# Parts 2
final_state = run_instructions_v2(instructions)
print(sum(final_state.values()))