"""Nurse scheduling problem with shift requests."""
from ortools.sat.python import cp_model
import calendar
import numpy as np
import math

year_ = 2023
month_ = 1
nurse_num = 11


def amount_of_days_in_month(year, month):
    return calendar.monthrange(year, month)[1]


def weekend_days_in_month(year, month):
    cal = calendar.Calendar()
    weekend_days = [day for day in cal.itermonthdays(year, month) if day and calendar.weekday(year, month, day) >= 5]
    return weekend_days


def create_list(number_of_nurse, days_in_month):
    # create list which has shape like (number_of_nurse,days_in_month ,3)
    # 3 is for 3 shifts
    # 0 is for day off
    # 1 is for day on
    # 2 is for weekend
    return np.zeros((number_of_nurse, days_in_month, 3))


def is_holiday(d, list_of_holiday):
    if d in list_of_holiday:
        return True
    else:
        return False


# Define the types of nurses
types = ["Type1", "Type2"]
all_types = range(len(types))

roles = ["Type1", "Type1", "Type2", "Type1", "Type2", "Type1", "Type2", "Type1", "Type2", "Type2","Type2"]


# Define the type of nurse for each nurse
def type_of_nurse(n):
    return types.index(roles[n])


def main():
    # This program tries to find an optimal assignment of nurses to shifts
    # (3 shifts per day, for 7 days), subject to some constraints (see below).
    # Each nurse can request to be assigned to specific shifts.
    # The optimal assignment maximizes the number of fulfilled shift requests

    num_nurses = nurse_num
    num_shifts = 3
    total_day = amount_of_days_in_month(year_, month_)
    all_nurses = range(num_nurses)
    all_shifts = range(num_shifts)
    all_days = range(total_day)

    # shift_requests[0][0][0] means first nurse, first day, first shift shift_requests[1][2][1] would mean that the
    # second nurse wants to work on the third day of the week on the second shift of the day.

    # this variable should be generated automatically then can be modified later on
    shift_requests = create_list(nurse_num, amount_of_days_in_month(year_, month_))  # <-- demo

    # Creates the model.
    model = cp_model.CpModel()

    # Creates shift variables.
    # shifts[(n, d, s)]: nurse 'n' works shift 's' on day 'd'.

    working_days = []
    holidays = []

    for d in all_days:
        if not is_holiday(d, weekend_days_in_month(year_, month_)):
            working_days.append(d)
        else:
            holidays.append(d)

    total_working_days = len(working_days)
    total_holidays = len(holidays)

    # add the constraint which for each nurse should have equal shift

    total_morning_shifts_working_days = total_working_days
    total_afternoon_shifts_working_days = total_working_days
    total_night_shifts_working_days = total_working_days

    total_morning_shifts_holidays = total_holidays
    total_afternoon_shifts_holidays = total_holidays
    total_night_shifts_holidays = total_holidays

    shifts = {}
    for n in all_nurses:
        for d in all_days:
            for s in all_shifts:
                shifts[(n, d, s)] = model.NewBoolVar('shift_n%id%is%i' % (n, d, s))

    # Each shift is assigned to exactly one nurse in.
    for d in all_days:
        for s in all_shifts:
            model.AddExactlyOne(shifts[(n, d, s)] for n in all_nurses)

    for n in all_nurses:
        for s in all_shifts:
            for d in range(6, total_day):
                model.Add(sum(shifts[(n, d - 6 + i, s)] for i in range(6)) <= 2)

    # Each nurse works at most two shifts per day.
    for n in all_nurses:
        for d in all_days:
            shifts_per_day = sum(shifts[(n, d, s)] for s in all_shifts)
            model.Add(shifts_per_day <= 2)

    # Each day has at least one different types of nurses.
    for d in all_days:
        for type_ in all_types:
            number_of_nurses_of_type = sum(
                shifts[(n, d, s)] for n in all_nurses if type_of_nurse(n) == type_ for s in all_shifts)
            model.Add(number_of_nurses_of_type >= 1)

    # Try to distribute the shifts evenly, so that each nurse works
    # min_shifts_per_nurse shifts. If this is not possible, because the total
    # number of shifts is not divisible by the number of nurses, some nurses will
    # be assigned one more shift.
    min_shifts_per_nurse = (num_shifts * total_working_days) // num_nurses
    if num_shifts * total_working_days % num_nurses == 0:
        max_shifts_per_nurse = min_shifts_per_nurse
    else:
        max_shifts_per_nurse = min_shifts_per_nurse + 1

    min_shifts_per_nurse_h = (num_shifts * total_holidays) // num_nurses
    if num_shifts * total_holidays % num_nurses == 0:
        max_shifts_per_nurse_h = min_shifts_per_nurse_h
    else:
        max_shifts_per_nurse_h = min_shifts_per_nurse_h + 1

    # Morning shift working day
    min_morning_shift_per_nurse = total_morning_shifts_working_days // num_nurses
    min_afternoon_shift_per_nurse = total_afternoon_shifts_working_days // num_nurses
    min_night_shift_per_nurse = total_night_shifts_working_days // num_nurses
    if min_morning_shift_per_nurse == 0 and total_morning_shifts_working_days != 0:
        min_morning_shift_per_nurse = 1
        max_morning_shift_per_nurse = 1

        min_afternoon_shift_per_nurse = 1
        max_afternoon_shift_per_nurse = 1

        min_night_shift_per_nurse = 1
        max_night_shift_per_nurse = 1

    elif total_morning_shifts_working_days % num_nurses == 0:
        max_morning_shift_per_nurse = min_morning_shift_per_nurse
        max_afternoon_shift_per_nurse = min_morning_shift_per_nurse
        max_night_shift_per_nurse = min_morning_shift_per_nurse
    else:
        max_morning_shift_per_nurse = min_morning_shift_per_nurse + 1
        max_afternoon_shift_per_nurse = min_morning_shift_per_nurse + 1
        max_night_shift_per_nurse = min_morning_shift_per_nurse + 1

    # Morning shift holiday
    min_morning_shift_per_nurse_h = total_morning_shifts_holidays // num_nurses
    min_afternoon_shift_per_nurse_h = total_afternoon_shifts_holidays // num_nurses
    min_night_shift_per_nurse_h = total_night_shifts_holidays // num_nurses
    if min_morning_shift_per_nurse_h == 0 and total_morning_shifts_holidays != 0:
        min_morning_shift_per_nurse_h = 0
        max_morning_shift_per_nurse_h = 1

        min_afternoon_shift_per_nurse_h = 0
        max_afternoon_shift_per_nurse_h = 1

        min_night_shift_per_nurse_h = 0
        max_night_shift_per_nurse_h = 1

    elif total_morning_shifts_working_days % num_nurses == 0:
        max_morning_shift_per_nurse_h = min_morning_shift_per_nurse_h
        max_afternoon_shift_per_nurse_h = min_morning_shift_per_nurse_h
        max_night_shift_per_nurse_h = min_morning_shift_per_nurse_h
    else:
        max_morning_shift_per_nurse_h = min_morning_shift_per_nurse_h + 1
        max_afternoon_shift_per_nurse_h = min_morning_shift_per_nurse_h + 1
        max_night_shift_per_nurse_h = min_morning_shift_per_nurse_h + 1

    for n in all_nurses:
        num_shift_worked = 0
        num_shift_worked_h = 0

        num_shifts_morning = 0
        num_shifts_morning_h = 0

        num_shifts_afternoon = 0
        num_shifts_afternoon_h = 0

        num_shifts_night = 0
        num_shifts_night_h = 0

        for d in working_days:
            for s in all_shifts:
                num_shift_worked += shifts[(n, d, s)]

                if s == 0:
                    num_shifts_morning += shifts[(n, d, s)]
                elif s == 1:
                    num_shifts_afternoon += shifts[(n, d, s)]
                elif s == 2:
                    num_shifts_night += shifts[(n, d, s)]

        # all shifts constraint
        model.Add(min_shifts_per_nurse <= num_shift_worked)
        model.Add(num_shift_worked <= max_shifts_per_nurse)

        # morning shifts constraint
        model.Add(min_morning_shift_per_nurse <= num_shifts_morning)
        model.Add(num_shifts_morning <= max_morning_shift_per_nurse)

        # afternoon shifts constraint
        model.Add(min_afternoon_shift_per_nurse <= num_shifts_afternoon)
        model.Add(num_shifts_afternoon <= max_afternoon_shift_per_nurse)

        # night shifts constraint
        model.Add(min_night_shift_per_nurse <= num_shifts_night)
        model.Add(num_shifts_night <= max_night_shift_per_nurse)

        for d in holidays:
            for s in all_shifts:
                num_shift_worked_h += shifts[(n, d, s)]
                if s == 0:
                    num_shifts_morning_h += shifts[(n, d, s)]
                elif s == 1:
                    num_shifts_afternoon_h += shifts[(n, d, s)]
                elif s == 2:
                    num_shifts_night_h += shifts[(n, d, s)]

        # all shifts constraint
        model.Add(min_shifts_per_nurse_h <= num_shift_worked_h)
        model.Add(num_shift_worked_h <= max_shifts_per_nurse_h)

        # morning shifts constraint
        model.Add(min_morning_shift_per_nurse_h <= num_shifts_morning_h)
        model.Add(num_shifts_morning_h <= max_morning_shift_per_nurse_h)

        # afternoon shifts constraint
        model.Add(min_afternoon_shift_per_nurse_h <= num_shifts_afternoon_h)
        model.Add(num_shifts_afternoon_h <= max_afternoon_shift_per_nurse_h)

        # night shifts constraint
        model.Add(min_night_shift_per_nurse_h <= num_shifts_night_h)
        model.Add(num_shifts_night_h <= max_night_shift_per_nurse_h)

    # pylint: disable=g-complex-comprehension
    model.Maximize(
        sum(shift_requests[n][d][s] * shifts[(n, d, s)] for n in all_nurses
            for d in all_days for s in all_shifts))

    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        print('Solution:')
        for d in all_days:
            print('Day', d)
            for n in all_nurses:
                for s in all_shifts:
                    if solver.Value(shifts[(n, d, s)]) == 1:
                        if shift_requests[n][d][s] == 1:
                            print('Nurse', type_of_nurse(n), n, 'works shift', s, '(requested).')
                        else:
                            print('Nurse', type_of_nurse(n), n, 'works shift', s,
                                  '(not requested).')
            print()
        print(f'Number of shift requests met = {solver.ObjectiveValue()}',
              f'(out of {num_nurses * min_shifts_per_nurse})')
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

                if is_holiday(d, weekend_days_in_month(year_, month_)):
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

        print('nurse', n, ' has ', num_shifts_worked, 'normal day', num_shifts_holi, 'holiday',
              num_shifts_worked + num_shifts_holi, 'total day')
        # Print the results

    for n in all_nurses:
        print("Nurse ", n, " morning_shifts: ", solver.Value(morning_shifts[n]), " afternoon_shifts: ",
              solver.Value(afternoon_shifts[n]), " night_shifts: ", solver.Value(night_shifts[n]))
        print("Nurse ", n, " morning_shifts_holiday: ", solver.Value(morning_shifts_h[n]), " afternoon_shifts_holiday: ",
              solver.Value(afternoon_shifts_h[n]), " night_shifts_holiday: ", solver.Value(night_shifts_h[n]))
        print('---')


if __name__ == '__main__':
    main()
