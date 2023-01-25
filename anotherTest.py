from ortools.sat.python import cp_model
from itertools import product

# programmer = 8, service = 6
A = [11, 12, 13, 14, 15, 16, 17, 18]
B = [21, 22, 23, 24, 25, 26]

counts = {}
all_pairs = product(A, B)

# Creates the model.
model = cp_model.CpModel()

_pairs = {}
count = 0
for a_ in A:
    for b_ in B:
        _pairs[(a_, b_)] = model.NewBoolVar('_pairs_a%ib%i' % (a_, b_))
        count += 1
print(count)

for a_ in A:
    model.Add(sum(_pairs[(a_, b_)] for b_ in B if b_ == 21) <= 1)

model.Maximize(sum(_pairs[(a_, b_)] for a_ in A for b_ in B))

for pair in all_pairs:
    print(pair)
    for element in pair:
        if element in counts:
            counts[element] += 1
        else:
            counts[element] = 1
print(counts)
