
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

holiday_shift = len(weekend_days_in_month(year_, month_)) * num_shifts
working_shift = (num_shifts * num_days) - holiday_shift

min_holiday_shift_per_nurse = holiday_shift // num_nurses
min_working_shift_per_nurse = working_shift // num_nurses

if holiday_shift % nurse_num:
    max_shifts_per_nurse_holiday = min_holiday_shift_per_nurse
else:
    max_shifts_per_nurse_holiday = min_holiday_shift_per_nurse + 1

if working_shift % num_nurses == 0:
    max_working_shifts_per_nurse = min_working_shift_per_nurse
else:
    max_working_shifts_per_nurse = min_working_shift_per_nurse + 1

for n in all_nurses:
    num_shifts_worked = 0
    num_shifts_worked_holiday = 0
    for d in all_days:
        if is_holiday(d, weekend_days_in_month(year_, month_)):
            for s in all_shifts:
                num_shifts_worked += shifts[(n, d, s)]
        else:
            for s in all_shifts:
                num_shifts_worked_holiday += shifts[(n, d, s)]

    model.Add(min_working_shift_per_nurse <= num_shifts_worked)
    model.Add(num_shifts_worked <= max_working_shifts_per_nurse)

    model.Add(min_holiday_shift_per_nurse <= num_shifts_worked_holiday)
    model.Add(num_shifts_worked_holiday <= max_shifts_per_nurse_holiday)
