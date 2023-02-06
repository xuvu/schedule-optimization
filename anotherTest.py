import math
import random

#
# total_shifts = 142
# list1 = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8']
# list2 = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6']
# min_shift = math.floor(total_shifts / (len(list1) + len(list2)))
#
#
# element_counts = {element: 0 for element in list1 + list2}
# result = []
#
# count_pair = 0
# for k in range(math.floor(total_shifts/(len(list1)) * len(list2))):
#     for b in list2:
#         for a in list1:
#             if count_pair >= total_shifts:
#                 break
#             if b != a and element_counts[b] < min_shift and element_counts[a] < min_shift:
#                 count_pair += 1
#                 element_counts[a] += 1
#                 element_counts[b] += 1
#                 result += [(a, b)]
#
# print(min_shift, count_pair)
# print(result)
# print(element_counts)
# result1 = [(a, b) for a in list1 for b in list2 if a != b]
# dup_ = math.floor(total_shifts / (len(result1) * 2))
# result1 = result1 * dup_
# # count how many times each element was picked
# element_counts = {element: 0 for element in list1 + list2}
# for a, b in result1:
#     element_counts[a] += 1
#     element_counts[b] += 1
#
# print(len(result1))
# print(result1)
# print(element_counts)


list1 = ['A1', 'A2', 'A3']

list2 = ['B1', 'B2']

# [A,A,A]
A_A_A = []
for A1 in list1:
    for A2 in list1:
        for A3 in list1:
            if A1 != A2 and A1 != A3 and A2 != A3:
                A_A_A += [(A1, A2, A3)]

print(A_A_A)

# [A,A,B]
A_A_B = []
for A1 in list1:
    for A2 in list1:
        for B1 in list2:
            if A1 != A2:
                A_A_B += [(A1, A2, B1)]

print(A_A_B)

# [A,B,B]
A_B_B = []
for A1 in list1:
    for B1 in list1:
        for B2 in list2:
            if B1 != B2:
                A_B_B += [(A1, B1, B2)]

print(A_B_B)