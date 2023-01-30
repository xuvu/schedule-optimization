from collections import Counter

'''
list1 = ['A1', 'A2', 'A3']
list2 = ['B1', 'B2']
counts_list1 = Counter(list1 * 10)
counts_list2 = Counter(list2 * 10)

# Counting the number of occurrences of all elements
counts = counts_list1 + counts_list2

# Counting the minimum number of occurrences
min_count = min(counts.values())

# Create a new list of pairings where each element is paired
# the same number of times as the minimum number of occurrences
even_pairings = []
for element1, count1 in counts_list1.items():
    for element2, count2 in counts_list2.items():
        even_pairings += [(element1, element2)] * min_count

print(even_pairings)

counts = {'A1': 0, 'A2': 0, 'A3': 0, 'B1': 0, 'B2': 0}

for pair in even_pairings:
    for element in pair:
        counts[element] += 1
print(counts)
'''

import itertools

list1 = ['A1', 'A2', 'A3']
list2 = ['B1', 'B2']

# The list includes all elements within the same set
same_a = list(itertools.product(list1, repeat=2))

same_a = [(x, y) for x in list2 for y in list2 if x != y]

# The list includes all elements within the same set
same_b = list(itertools.product(list1, repeat=2))

same_b = [(x, y) for x in list1 for y in list1 if x != y]

diff_pair = list(itertools.product(list1, list2))

print(same_a)
print(same_b)
print(diff_pair)
