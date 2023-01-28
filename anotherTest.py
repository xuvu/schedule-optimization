from ortools.sat.python import cp_model
from itertools import product


def are_list_equal(up, lb, List):
    result = all(element == List[0] + up or element == List[0] - lb or element == List[0] for element in List)
    return result


# programmer = 8, service = 6
A = [11, 12, 13, 14]
B = [21, 22, 23]

counts = {}

# Creates the model.
model = cp_model.CpModel()

_pairs = {}
count = 0

for a_ in A:
    for b_ in B:
        _pairs[(a_, b_)] = model.NewBoolVar('_pairs_a%ib%i' % (a_, b_))
        count += 1
print(count)

count_A_11 = 0
count_A_12 = 0
count_A_13 = 0
count_A_14 = 0

count_B_21 = 0
count_B_22 = 0
count_B_23 = 0
count_B_24 = 0

for a_ in A:
    for b_ in B:
        if a_ == 11:
            count_A_11 += _pairs[(a_, b_)]
        if a_ == 12:
            count_A_12 += _pairs[(a_, b_)]
        if a_ == 13:
            count_A_13 += _pairs[(a_, b_)]
        if a_ == 14:
            count_A_14 += _pairs[(a_, b_)]

        if b_ == 21:
            count_B_21 += _pairs[(a_, b_)]
        if b_ == 22:
            count_B_22 += _pairs[(a_, b_)]
        if b_ == 23:
            count_B_23 += _pairs[(a_, b_)]
        if b_ == 24:
            count_B_24 += _pairs[(a_, b_)]

list_A = [count_A_11, count_A_12, count_A_13, count_A_14]
list_B = [count_B_21, count_B_22, count_B_23, count_B_24]


'''
for a_ in list_A:
    for a_inner in list_A:
        model.Add(a_ == a_inner)

for b_ in list_B:
    for b_inner in list_B:
        model.Add(b_ == b_inner)
'''


model.Maximize(sum(_pairs[(a_, b_)] for a_ in A for b_ in B))

# Creates the solver and solve.
solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.OPTIMAL:
    print('Solution:')
    count = 1
    for a_ in A:
        for b_ in B:
            if solver.Value(_pairs[(a_, b_)]) == 1:
                print(count, ':', a_, b_)
                count += 1
