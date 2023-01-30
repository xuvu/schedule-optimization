shift_per_person = 26

num_person_per_shift = 2

A = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7']
B = ['B1', 'B2', 'B3']

if len(A) == len(B):
    violation_pair = (shift_per_person / num_person_per_shift)
else:
    violation_pair = (shift_per_person / num_person_per_shift) * (len(A) - len(B))

print(violation_pair)
