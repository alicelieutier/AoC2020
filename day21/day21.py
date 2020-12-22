import sys
import re

def parse_ingredients(filename):
    f = open(filename)
    return [parse_ingredient_list(line.strip()) for line in f.readlines()]

INGREDIENTS_PATTERN = re.compile(r'([a-z ]+)')
ALLERGENS_PATTERN = re.compile(r'\(contains ([,a-z ]+)\)')
def parse_ingredient_list(line):
    ingredients = INGREDIENTS_PATTERN.match(line).group(1).strip().split(' ')
    allergens_match = ALLERGENS_PATTERN.search(line)
    allergens = allergens_match.group(1).split(', ') if allergens_match is not None else []
    return (ingredients, allergens)

def build_label_sets(all_ingredient_lists):
    label_sets = {}
    for (ingredients, allergens) in all_ingredient_lists:
        for allergen in allergens:
            default = label_sets.setdefault(allergen, set(ingredients))
            label_sets[allergen] = default & set(ingredients)
    return label_sets

# When items have a set of possible labels, simplify the sets
# until each item only has one label
# expects a structure of the shape:
# {'item1': {'label1', 'label2'}, 'item2':{'label1'}}
# and returns
# {'item1': 'label2', 'item2': 'label1'}
def simplify_labels(label_sets):
    # this algorithm will not work unless some items have only one candidate label
    min_length = min((len(candidates) for candidates in label_sets.values()))
    assert(min_length == 1)

    assigned_label_sets = {}
    max_length = max((len(candidates) for candidates in label_sets.values()))
    while max_length > 0:
        # find items with just one possible label
        assigned_label_sets.update({item: candidates.pop() for item, candidates in label_sets.items() if len(candidates) == 1})
        # remove that label from the sets of possible labels for other items
        assigned_labels = set(assigned_label_sets.values())
        for candidates in label_sets.values():
            candidates -= assigned_labels
        max_length = max((len(candidates) for candidates in label_sets.values()))
    return assigned_label_sets


# change the input here
file = './day21/input'
all_ingredient_lists = parse_ingredients(file)
label_sets = build_label_sets(all_ingredient_lists)
allergens_to_ingredient = simplify_labels(label_sets)
print(allergens_to_ingredient)

# Part 1
non_allergenic_ingredients = [ingredient for (ingredients, _) in all_ingredient_lists for ingredient in ingredients if ingredient not in allergens_to_ingredient.values()]
print(len(non_allergenic_ingredients))

# Part 2
sorted_allergens = sorted(allergens_to_ingredient.keys())
print(','.join([allergens_to_ingredient[allergen] for allergen in sorted_allergens]))

# Tests
assert(simplify_labels({'item1': {'label1', 'label2'}, 'item2':{'label1'}})=={'item1': 'label2', 'item2': 'label1'})
assert(simplify_labels({'item1': {'label1', 'label3'}, 'item2':{'label1'}, 'item3':{'label2', 'label3'}})=={'item1': 'label3', 'item2': 'label1', 'item3': 'label2'})
assert(parse_ingredient_list('mxmxvkd kfcds sqjhc nhms (contains dairy, fish)') == (['mxmxvkd', 'kfcds', 'sqjhc', 'nhms'], ['dairy', 'fish']))
assert(parse_ingredient_list('mxmxvkd (contains dairy)') == (['mxmxvkd'], ['dairy']))
assert(parse_ingredient_list('kfcds sqjhc nhms') == (['kfcds', 'sqjhc', 'nhms'], []))