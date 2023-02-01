"""Nurse scheduling problem with shift requests."""
import math

from ortools.sat.python import cp_model
import calendar
import numpy as np
from datetime import date

name_of_person = ['ภูวเนตร',
                  'ราเชนทร์',
                  'พลกฤต',
                  'ชานนท์',
                  'ปรมะ',
                  'สัญญา',
                  'วินัย',
                  'รณยุทธ',
                  'วัฒพงษ์',
                  'ราเชน',
                  'นฤชิต',
                  'จีรวัฒน์',
                  'สุเมธร์',
                  'นที'
                  ]


# Get the name of a nurse
def map_name_person(n):
    return name_of_person[n]


# Get name of type of a nurse
def name_of_type_nurse(n):
    return roles[n]


def get_days_in_year(year):
    days_in_year = [i for i in range(1, 366)]
    return days_in_year


def get_weekend_days_in_year(year):
    weekend_days = []
    normal_day = 1
    for month in range(1, 13):
        for day in range(1, calendar.monthrange(year, month)[1] + 1):
            current_date = date(year, month, day)
            if current_date.weekday() in [5, 6]:
                weekend_days.append(normal_day)
            normal_day += 1
    return weekend_days


def create_list(number_of_nurse, days_in_month):
    # create list which has shape like (number_of_nurse,days_in_month ,3)
    # 3 is for 3 shifts
    # 0 is for day off
    # 1 is for day on
    # 2 is for weekend
    return np.zeros((number_of_nurse, days_in_month, 3))


def get_max_diff_type(A, B, total_shifts):
    if A > B:
        list1 = A
        list2 = B
    else:
        list1 = B
        list2 = A

    min_shift = math.floor(total_shifts / (len(list1) + len(list2)))

    element_counts = {element: 0 for element in list1 + list2}
    result = []

    count_pair = 0
    for k in range(math.floor(total_shifts / (len(list1)) * len(list2))):
        for b in list2:
            for a in list1:
                if count_pair >= total_shifts:
                    break
                if b != a and element_counts[b] < min_shift and element_counts[a] < min_shift:
                    count_pair += 1
                    element_counts[a] += 1
                    element_counts[b] += 1
                    result += [(a, b)]
    return count_pair


# Define the types of nurses
types = ["Programmer", "Service"]
all_types = range(len(types))

# (EASY) (FINISH)
# no morning shift in working day => good

# (EASY) (FINISH)
# holiday can have all three shifts => good

# (FINISH)
# Each shift has 2 person

# (MEDIUM)
# 2 person per shift
# programmer + service => programmer + programmer => service + service

# (HARD)
# (1,2) same => (1,2) different => (0,1) same => good

# (HARD)
# night to morning is forbidden (0,2) in a day (can but shouldn't) => good

# (HARD)
# morning to night is forbidden (2,0) in a day (forbidden) => good

# special holiday

# special hospital
# afternoon to night (1,2) the highest priority with same person => (1,2) different person
# (0,1) if (1,2) can't happen

# Type of nurses

# programmer = 8, service = 6
roles = ["Programmer", "Programmer", "Programmer", "Programmer", "Programmer", "Programmer", "Programmer", "Programmer",
         "Service", "Service", "Service", "Service", "Service", "Service"]

year_ = 2023
month_ = 1


# Define the type of nurse for each nurse
def type_of_nurse(n):
    return types.index(roles[n])


def main():
    # This program tries to find an optimal assignment of nurses to shifts
    # (3 shifts per day, for 7 days), subject to some constraints (see below).
    # Each nurse can request to be assigned to specific shifts.
    # The optimal assignment maximizes the number of fulfilled shift requests

    global total_min, total_max
    num_nurses = len(roles)
    all_nurses = range(num_nurses)
    all_days = get_days_in_year(2023)

    all_weekends = get_weekend_days_in_year(2023)
    all_working_days = set(all_days) - set(all_weekends)

    total_working_days = len(all_working_days)
    total_holidays = len(all_weekends)

    # shift_requests[0][0][0] means first nurse, first day, first shift shift_requests[1][2][1] would mean that the
    # second nurse wants to work on the third day of the week on the second shift of the day.

    # this variable should be generated automatically then can be modified later on
    shift_requests = create_list(num_nurses, len(all_days))  # <-- demo

    # Creates the model.
    model = cp_model.CpModel()

    # Creates shift variables.
    # Shifts[(n, d, s)]: nurse 'n' works shift 's' on day 'd'.
    shifts = {}
    num_shifts = 3
    all_shifts = range(num_shifts)  # [1,2,3]
    num_shifts = len(all_shifts)

    forbidden_shifts = [0]

    for n in all_nurses:
        for d in all_days:
            for s in all_shifts:
                shifts[(n, d, s)] = model.NewBoolVar('shift_n%id%is%i' % (n, d, s))

    """
    # Each shift is assigned to exactly one nurse in.
    for d in all_days:
        for s in all_shifts:
            model.Add(sum(shifts[(n, d, s)] for n in all_nurses) == 1)
    """

    num_of_nurse_per_shift = 2
    # Each shift is assigned to exactly 2 nurse in.
    for d in all_days:
        if d not in all_weekends:
            for s in all_shifts:
                if s not in forbidden_shifts:  # exclude morning shift
                    model.Add(sum(shifts[(n, d, s)] for n in all_nurses) == num_of_nurse_per_shift)
        else:
            for s in all_shifts:
                model.Add(sum(shifts[(n, d, s)] for n in all_nurses) == num_of_nurse_per_shift)

    # Try to distribute the shifts evenly, so that each nurse works
    # min_shifts_per_nurse shifts. If this is not possible, because the total
    # number of shifts is not divisible by the number of nurses, some nurses will
    # be assigned one more shift.

    # min-max working day
    working_shift_per_day = ((num_shifts - len(forbidden_shifts)) * num_of_nurse_per_shift)
    min_shifts_per_nurse = (working_shift_per_day * total_working_days) // num_nurses
    if working_shift_per_day * total_working_days % num_nurses == 0:
        max_shifts_per_nurse = min_shifts_per_nurse
    else:
        max_shifts_per_nurse = min_shifts_per_nurse + 1

    # min-max holiday day
    min_shifts_per_nurse_h = ((num_shifts * num_of_nurse_per_shift) * total_holidays) // num_nurses
    if (num_shifts * num_of_nurse_per_shift) * total_holidays % num_nurses == 0:
        max_shifts_per_nurse_h = min_shifts_per_nurse_h
    else:
        max_shifts_per_nurse_h = min_shifts_per_nurse_h + 1

    # All working shifts min-max variable
    # ---------------------------------------------------------------
    min_morning_shift_per_nurse = (total_working_days * num_of_nurse_per_shift) // num_nurses
    min_afternoon_shift_per_nurse = (total_working_days * num_of_nurse_per_shift) // num_nurses
    min_night_shift_per_nurse = (total_working_days * num_of_nurse_per_shift) // num_nurses
    if min_morning_shift_per_nurse == 0 and (total_working_days * num_of_nurse_per_shift) != 0:
        min_morning_shift_per_nurse = 1
        max_morning_shift_per_nurse = 1

        min_afternoon_shift_per_nurse = 1
        max_afternoon_shift_per_nurse = 1

        min_night_shift_per_nurse = 1
        max_night_shift_per_nurse = 1

    elif (total_working_days * num_of_nurse_per_shift) % num_nurses == 0:
        max_morning_shift_per_nurse = min_morning_shift_per_nurse
        max_afternoon_shift_per_nurse = min_morning_shift_per_nurse
        max_night_shift_per_nurse = min_morning_shift_per_nurse
    else:
        max_morning_shift_per_nurse = min_morning_shift_per_nurse + 1
        max_afternoon_shift_per_nurse = min_morning_shift_per_nurse + 1
        max_night_shift_per_nurse = min_morning_shift_per_nurse + 1
    # ---------------------------------------------------------------

    # All holiday shifts min-max variable
    # ---------------------------------------------------------------
    min_morning_shift_per_nurse_h = (total_holidays * num_of_nurse_per_shift) // num_nurses
    min_afternoon_shift_per_nurse_h = (total_holidays * num_of_nurse_per_shift) // num_nurses
    min_night_shift_per_nurse_h = (total_holidays * num_of_nurse_per_shift) // num_nurses
    if min_morning_shift_per_nurse_h == 0 and (total_holidays * num_of_nurse_per_shift) != 0:
        min_morning_shift_per_nurse_h = 0
        max_morning_shift_per_nurse_h = 1

        min_afternoon_shift_per_nurse_h = 0
        max_afternoon_shift_per_nurse_h = 1

        min_night_shift_per_nurse_h = 0
        max_night_shift_per_nurse_h = 1

    elif (total_holidays * num_of_nurse_per_shift) % num_nurses == 0:
        max_morning_shift_per_nurse_h = min_morning_shift_per_nurse_h
        max_afternoon_shift_per_nurse_h = min_afternoon_shift_per_nurse_h
        max_night_shift_per_nurse_h = min_night_shift_per_nurse_h
    else:
        max_morning_shift_per_nurse_h = min_morning_shift_per_nurse_h + 1
        max_afternoon_shift_per_nurse_h = min_afternoon_shift_per_nurse_h + 1
        max_night_shift_per_nurse_h = min_night_shift_per_nurse_h + 1
    # ---------------------------------------------------------------

    for n in all_nurses:
        num_shift_worked = 0
        num_shift_worked_h = 0

        num_shifts_morning = 0
        num_shifts_morning_h = 0

        num_shifts_afternoon = 0
        num_shifts_afternoon_h = 0

        num_shifts_night = 0
        num_shifts_night_h = 0

        # Distribute working day shifts
        # ---------------------------------------------------------------
        for d in all_working_days:
            for s in all_shifts:
                if s in forbidden_shifts:
                    model.Add(shifts[(n, d, s)] == 0)
                elif s == 1:
                    num_shift_worked += shifts[(n, d, s)]
                    num_shifts_afternoon += shifts[(n, d, s)]
                elif s == 2:
                    num_shift_worked += shifts[(n, d, s)]
                    num_shifts_night += shifts[(n, d, s)]

        # all shifts constraint
        # model.Add(min_shifts_per_nurse <= num_shift_worked)
        # model.Add(num_shift_worked <= max_shifts_per_nurse)

        # morning shifts constraint (Forbidden)
        # model.Add(min_morning_shift_per_nurse <= num_shifts_morning)
        # model.Add(num_shifts_morning <= max_morning_shift_per_nurse)

        # conflict between
        # minimum type within each shift
        # distribution constraint

        # soften the constraint of working day shifts
        slack = 0

        # afternoon shifts constraint
        model.Add(min_afternoon_shift_per_nurse - slack <= num_shifts_afternoon)
        model.Add(num_shifts_afternoon <= max_afternoon_shift_per_nurse + slack)

        # night shifts constraint
        model.Add(min_night_shift_per_nurse - slack <= num_shifts_night)
        model.Add(num_shifts_night <= max_night_shift_per_nurse + slack)
        # ---------------------------------------------------------------

        # Distribute holiday day shifts
        # ---------------------------------------------------------------
        for d in all_weekends:
            for s in all_shifts:
                if s == 0:
                    num_shift_worked_h += shifts[(n, d, s)]
                    num_shifts_morning_h += shifts[(n, d, s)]
                elif s == 1:
                    num_shift_worked_h += shifts[(n, d, s)]
                    num_shifts_afternoon_h += shifts[(n, d, s)]
                elif s == 2:
                    num_shift_worked_h += shifts[(n, d, s)]
                    num_shifts_night_h += shifts[(n, d, s)]

        # all shifts constraint
        # model.Add(min_shifts_per_nurse_h <= num_shift_worked_h)
        # model.Add(num_shift_worked_h <= max_shifts_per_nurse_h)

        # soften the constraint for holiday shifts
        slack_h = 0

        # morning shifts constraint
        model.Add(min_morning_shift_per_nurse_h - slack_h <= num_shifts_morning_h)
        model.Add(num_shifts_morning_h <= max_morning_shift_per_nurse_h + slack_h)

        # afternoon shifts constraint
        model.Add(min_afternoon_shift_per_nurse_h - slack_h <= num_shifts_afternoon_h)
        model.Add(num_shifts_afternoon_h <= max_afternoon_shift_per_nurse_h + slack_h)

        # night shifts constraint
        model.Add(min_night_shift_per_nurse_h - slack_h <= num_shifts_night_h)
        model.Add(num_shifts_night_h <= max_night_shift_per_nurse_h + slack_h)

        # lower bound slack
        min_total_slack = 0

        # upper bound slack
        max_total_slack = 0

        total_min = min_shifts_per_nurse + min_shifts_per_nurse_h - min_total_slack
        total_max = max_shifts_per_nurse + max_shifts_per_nurse_h + max_total_slack

        # Total shifts should be equal
        model.Add(total_min <= (num_shift_worked + num_shift_worked_h))
        model.Add((num_shift_worked + num_shift_worked_h) <= total_max)
        # ---------------------------------------------------------------

    # For each nurse shouldn't have more than 2 shifts within 4 days
    day_interval = 4
    maximum_shifts = 2
    for n in all_nurses:
        for d in all_days:  # d = 1,2,3,4,5,...,total_day, d = 1
            if (d + day_interval) < len(all_days):  # 1 + (4-1) < 31
                model.Add(sum(shifts[(n, d + i, s)] for i in range(day_interval) for s in all_shifts) <= maximum_shifts)
                # shifts[(0, 1 + 0, 0), shifts[(0, 1 + 0, 1), shifts[(0, 1 + 0, 2)
                # shifts[(0, 1 + 1, 0), shifts[(0, 1 + 1, 1), shifts[(0, 1 + 1, 2)
                # shifts[(0, 1 + 2, 0), shifts[(0, 1 + 2, 1), shifts[(0, 1 + 2, 2)
                # shifts[(0, 1 + 3, 0), shifts[(0, 1 + 3, 1), shifts[(0, 1 + 3, 2)
                # all of the shifts period the nurse can only have 2 shifts maximum

    # Each nurse works at most two shifts per day.
    maximum_each_day_shifts = 2
    for n in all_nurses:
        for d in all_days:
            shifts_per_day = sum(shifts[(n, d, s)] for s in all_shifts)
            model.Add(shifts_per_day <= maximum_each_day_shifts)

    # Nurse type priority
    type_priority = [['Type1', 'Type2'], ['Type1', 'Type1'], ['Type2', 'Type2']]

    # Prioritize shift patterns
    # for d in all_days:
    #     for n in all_nurses:
    #         model.Add(shifts[(n, d, 1)] <= shifts[(n, d, 2)])  # (1,2) same

    max_diff_pair = get_max_diff_type()
    max_diff_count = 0
    # Each shift ensure different type of nurses
    for d in all_weekends:
        for s in all_shifts:
            if max_diff_count <= max_diff_pair:
                max_diff_count += 1
                for t in all_types:
                    type_count = 0
                    for n in all_nurses:
                        if type_of_nurse(n) == t:
                            type_count += shifts[(n, d, s)]
                    model.Add(type_count <= 1)

    for d in all_working_days:
        for s in all_shifts:
            if s != 0:
                if max_diff_count <= max_diff_pair:
                    max_diff_count += 1
                    for t in all_types:
                        type_count = 0
                        for n in all_nurses:
                            if type_of_nurse(n) == t:
                                type_count += shifts[(n, d, s)]
                        model.Add(type_count <= 1)
    # total possible way of pairing ['Type1', 'Type2'] is the product of the number of people for each type
    '''
    # Each shift ensure different type of nurses
    for d in all_days:
        if d <= 50:
            for s in all_shifts:
                for t in all_types:
                    model.Add(sum(shifts[(n, d, s)] for n in all_nurses if type_of_nurse(n) == t) <= 1)
    
    # Prioritize shift patterns
    for d in all_days:
        if d <= 10:
            for n in all_nurses:
                model.Add(shifts[(n, d, 1)] <= shifts[(n, d, 2)])  # (1,2) same
                # model.Add(shifts[(n, d, 0)] + shifts[(n, d, 2)] <= 1)  # forbidden (0,2)
                # model.Add(shifts[(n, d, 2)] + shifts[(n, d, 0)] <= 1)  # forbidden (2,0)
    '''
    # pylint: disable=g-complex-comprehension
    model.Maximize(
        sum(shift_requests[n][d - 1][s] * shifts[(n, d, s)] for n in all_nurses
            for d in all_days for s in all_shifts))

    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        print('Solution:')
        for d in all_days:
            print('Day', d, d in all_weekends)
            for s in all_shifts:
                for n in all_nurses:
                    if solver.Value(shifts[(n, d, s)]) == 1:
                        if shift_requests[n][d - 1][s] == 1:
                            print(name_of_type_nurse(n), map_name_person(n), 'works shift', s,
                                  '(requested).')
                        else:
                            print(name_of_type_nurse(n), map_name_person(n), 'works shift', s,
                                  '(not requested).')
            print()
        print(f'Number of shift requests met = {solver.ObjectiveValue()}',
              f'(out of {all_shifts})')
    else:
        print('No optimal solution found !')

    # Statistics.
    print('\nStatistics')
    print('  - conflicts: %i' % solver.NumConflicts())
    print('  - branches : %i' % solver.NumBranches())
    print('  - wall time: %f s' % solver.WallTime())

    morning_shifts = {}
    afternoon_shifts = {}
    night_shifts = {}

    morning_shifts_h = {}
    afternoon_shifts_h = {}
    night_shifts_h = {}

    sum_all_shifts = 0

    for n in all_nurses:
        num_shifts_worked = 0
        num_shifts_holi = 0

        morning_shifts[n] = 0
        afternoon_shifts[n] = 0
        night_shifts[n] = 0

        morning_shifts_h[n] = 0
        afternoon_shifts_h[n] = 0
        night_shifts_h[n] = 0

        for d in all_days:
            for s in all_shifts:
                if d in all_weekends:
                    num_shifts_holi += solver.Value(shifts[(n, d, s)])
                    if s == 0:
                        morning_shifts_h[n] += solver.Value(shifts[(n, d, s)])
                    elif s == 1:
                        afternoon_shifts_h[n] += solver.Value(shifts[(n, d, s)])
                    elif s == 2:
                        night_shifts_h[n] += solver.Value(shifts[(n, d, s)])
                else:
                    num_shifts_worked += solver.Value(shifts[(n, d, s)])
                    if s == 0:
                        morning_shifts[n] += solver.Value(shifts[(n, d, s)])
                    elif s == 1:
                        afternoon_shifts[n] += solver.Value(shifts[(n, d, s)])
                    elif s == 2:
                        night_shifts[n] += solver.Value(shifts[(n, d, s)])

        print(name_of_type_nurse(n), map_name_person(n), ' has ', num_shifts_worked, 'shifts normal day',
              num_shifts_holi,
              'shifts holiday',
              num_shifts_worked + num_shifts_holi, 'total shifts')
        sum_all_shifts = sum_all_shifts + num_shifts_worked + num_shifts_holi

        # Print the results
    for n in all_nurses:
        print(map_name_person(n), " morning_shifts: ", solver.Value(morning_shifts[n]),
              " afternoon_shifts: ",
              solver.Value(afternoon_shifts[n]), " night_shifts: ", solver.Value(night_shifts[n]))
        print(map_name_person(n), " morning_shifts_h: ", solver.Value(morning_shifts_h[n]),
              " afternoon_shifts_h: ",
              solver.Value(afternoon_shifts_h[n]), " night_shifts_h: ", solver.Value(night_shifts_h[n]))
        print('---')

    print('min working shift', min_morning_shift_per_nurse, min_afternoon_shift_per_nurse, min_night_shift_per_nurse)
    print('max working shift', max_morning_shift_per_nurse, max_afternoon_shift_per_nurse, max_night_shift_per_nurse)
    print('min holiday shift', min_morning_shift_per_nurse_h, min_afternoon_shift_per_nurse_h,
          min_night_shift_per_nurse_h)
    print('max holiday shift', max_morning_shift_per_nurse_h, max_afternoon_shift_per_nurse_h,
          max_night_shift_per_nurse_h)
    print('total shifts', sum_all_shifts)
    print('sum min total shift', total_min)
    print('sum max total shift', total_max)


if __name__ == '__main__':
    main()
