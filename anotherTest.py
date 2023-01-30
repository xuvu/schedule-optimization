import math
import random

list1 = ['A1', 'A2', 'A3']
list2 = ['B1', 'B2']

result1 = [(a, b) for a in list1 for b in list2 if a != b]

print(len(result1))

total_shifts = 120
dup_ = math.floor(120/(len(result1) * 2))
final_result = result1*dup_

print(len(final_result)/len(result1))
print(final_result)

# count how many times each element was picked
element_counts = {element: 0 for element in list1 + list2}
for a, b in final_result:
    element_counts[a] += 1
    element_counts[b] += 1

print(element_counts)
