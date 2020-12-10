import sys

def parse_joltages(filename):
    f = open(filename)
    return [int(line.strip()) for line in f.readlines()]

def count_differences(sorted_numbers):
    differences = {1: 0, 2: 0, 3: 0}
    for i in range(len(sorted_numbers) - 1):
        diff = sorted_numbers[i+1] - sorted_numbers[i]
        differences[diff] += 1
    return differences

def next_reachable_nodes(from_node, set_of_all_nodes):
    return [n for n in range(from_node + 1, from_node + 4) if n in set_of_all_nodes]

# change the input here
file = './day10/input'
joltages = parse_joltages(file)
source = 0
device = max(joltages) + 3
joltages.extend([source, device])
sorted_adaptors = sorted(joltages)

# part 1
differences = count_differences(sorted_adaptors)
print(differences[1] * differences[3])

# part 2
ways_to_reach_node = {a: 0 for a in joltages}
ways_to_reach_node[source] = 1

for node in sorted_adaptors[:-1]:
    next_possible = next_reachable_nodes(node, ways_to_reach_node)
    for next_node in next_possible:
        ways_to_reach_node[next_node] += ways_to_reach_node[node]

print(ways_to_reach_node[device])