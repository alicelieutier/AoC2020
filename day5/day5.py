import sys

def id_from_code(code):
    key = {'F': 0, 'B': 1, 'L': 0, 'R': 1}
    translate = lambda letter : str(key[letter])
    binary_string = ''.join(map(translate, code))
    return int(binary_string, 2)

def ids_from_file(filename):
    f = open(filename)
    return [id_from_code(line.strip()) for line in f.readlines()]

def find_missing(sequential_nbs):
    i = 0
    check = sorted(sequential_nbs)
    while check[i] + 1 == check[i+1]:
        i += 1
    return check[i] + 1

file = './day5/input'
ids = ids_from_file(file)

# part 1
print(max(ids))

# part 2
print(find_missing(ids))