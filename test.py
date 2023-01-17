
"""
shift_requests = [[[0, 0, 1], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 1],  # <-- first nurse has 7 day of shift, and 3 shifts to be selected for each day
                   [0, 1, 0], [0, 0, 1]],

                  [[0, 0, 0], [0, 0, 0], [0, 1, 0], [0, 1, 0], [1, 0, 0],
                   [0, 0, 0], [0, 0, 1]],

                  [[0, 1, 0], [0, 1, 0], [0, 0, 0], [1, 0, 0], [0, 0, 0],
                   [0, 1, 0], [0, 0, 0]],

                  [[0, 0, 1], [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 0],
                   [1, 0, 0], [0, 0, 0]],

                  [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 0, 0], [1, 0, 0],  # <-- fifth nurse
                   [0, 1, 0], [0, 0, 0]]]

# [0,0,0] means this day the nurse doesn't have any shift

# [1,0,0] means this day the nurse have early shift => 08.00 - 16.00
# [0,1,0] means this day the nurse have mid-day shift => 16.00 - 24.00
# [0,0,1] means this day the nurse have late-day shift => 24.00 - 08.00


print(str('the number of all nurses ') +  str(len(shift_requests)))  # <-- the number of all nurses
print(str('the number of all days ') + str(len(shift_requests[0])))  # <-- the number of all days
print(str('the number of all shifts of a day ') + str(len(shift_requests[0][0])))  # <-- the number of all shifts of a day
"""
