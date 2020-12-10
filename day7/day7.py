import sys
import re
# from collections import deque

def parse_rules(filename):
    f = open(filename)
    return [parse_rule(rule) for rule in f.readlines()]

def parse_rule(rule):
  out_colour, contained_bags = rule.strip().split(' bags contain ')
  insides = [] if contained_bags == 'no other bags.' else parse_contained_bags(contained_bags)
  return (out_colour, insides)

COLOUR_PATTERN = re.compile(r'(\d+) ([a-z ]+) bag')
def parse_contained_bags(insides):
    return [(int(nb), colour) for (nb, colour) in COLOUR_PATTERN.findall(insides)]

# change the input here
file = './day7/input'
rules = parse_rules(file)

# part 1
# parent traversal
parent_graph = {}

for out_colour, insides in rules:
    parent_graph.setdefault(out_colour, [])
    for _, in_colour in insides:
        parent_graph.setdefault(in_colour, [])
        parent_graph[in_colour].append(out_colour)

ancestors = set(parent_graph['shiny gold'])
queue = parent_graph['shiny gold']

while len(queue) > 0:
    node = queue.pop()
    parents = parent_graph[node]
    ancestors.update(parents)
    queue.extend(parents)

print(len(ancestors))

# part 2
# children traversal
tree = {}
for out_colour, insides in rules:
    tree[out_colour] = []
    for nb, colour in insides:
        tree[out_colour].extend([colour for _ in range(nb)]) 

children = 0
queue = tree['shiny gold']

while len(queue) > 0:
    node = queue.pop()
    children += 1
    queue.extend(tree[node])

print(children)