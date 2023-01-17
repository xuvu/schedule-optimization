"""Nurse scheduling problem with shift requests."""
from ortools.sat.python import cp_model
import calendar
import numpy as np

year_ = 2023
month_ = 1
nurse_num = 10
role = [0, 1]  # 1 is programmer and 0 is service


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


def main():
    # This program tries to find an optimal assignment of nurses to shifts
    # (3 shifts per day, for 7 days), subject to some constraints (see below).
    # Each nurse can request to be assigned to specific shifts.
    # The optimal assignment maximizes the number of fulfilled shift requests

    num_nurses = nurse_num
    num_shifts = 3
    num_days = amount_of_days_in_month(year_, month_)
    all_nurses = range(num_nurses)
    all_shifts = range(num_shifts)
    all_days = range(num_days)

    # consider factor
    # 1. position
    # 2. holiday (2 holidays)
    # 3. normal day ex. for same person shouldn't (5 normal days)
    # 4. time period ex. same person shouldn't have consecutive period like having morning for all 31 days

    # shift_requests[0][0][0] means first nurse, first day, first shift
    # shift_requests[1][2][1] would mean that the second nurse wants to work on the third day of the week on the second shift of the day.

    # this variable should be generate automatically then can be modified later on
    shift_requests = create_list(nurse_num, amount_of_days_in_month(year_, month_))  # <-- demo
    # Creates the model.
    model = cp_model.CpModel()

    # Creates shift variables.
    # shifts[(n, d, s)]: nurse 'n' works shift 's' on day 'd'.
    shifts = {}
    for n in all_nurses:
        for d in all_days:
            for s in all_shifts:
                shifts[(n, d, s)] = model.NewBoolVar('shift_n%id%is%i' % (n, d, s))

    # Each shift is assigned to exactly one nurse in.
    for d in all_days:
        for s in all_shifts:
            model.AddExactlyOne(shifts[(n, d, s)] for n in all_nurses)

    # Each nurse works at most two shifts per day.
    for n in all_nurses:
        for d in all_days:
            shifts_per_day = sum(shifts[(n, d, s)] for s in all_shifts)
            model.Add(shifts_per_day <= 2)

    # Try to distribute the shifts evenly, so that each nurse works
    # min_shifts_per_nurse shifts. If this is not possible, because the total
    # number of shifts is not divisible by the number of nurses, some nurses will
    # be assigned one more shift.

    min_working_days_per_nurse = 5 // num_nurses
    min_holidays_per_nurse = 2 // num_nurses
    if 5 % num_nurses != 0:
        min_working_days_per_nurse += 1
    if 2 % num_nurses != 0:
        min_holidays_per_nurse += 1

    max_working_days_per_nurse = min_working_days_per_nurse
    max_holidays_per_nurse = min_holidays_per_nurse

    for n in all_nurses:
        working_days_per_nurse = 0
        holidays_per_nurse = 0
        for d in all_days:
            if is_holiday(d, weekend_days_in_month(year_, month_)):
                for s in all_shifts:
                    holidays_per_nurse += shifts[(n, d, s)]
            else:
                for s in all_shifts:
                    working_days_per_nurse += shifts[(n, d, s)]

        model.Add(min_working_days_per_nurse <= working_days_per_nurse)
        model.Add(working_days_per_nurse <= max_working_days_per_nurse)
        model.Add(min_holidays_per_nurse <= holidays_per_nurse)
        model.Add(holidays_per_nurse <= max_holidays_per_nurse)

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
                            print('Nurse', n, 'works shift', s, '(requested).',
                                  is_holiday(d, weekend_days_in_month(year_, month_)))
                        else:
                            print('Nurse', n, 'works shift', s,
                                  '(not requested).', is_holiday(d, weekend_days_in_month(year_, month_)))
            print()
        print(f'Number of shift requests met = {solver.ObjectiveValue()}',
              f'(out of {num_nurses * (min_working_days_per_nurse + min_holidays_per_nurse)})')

    else:
        print('No optimal solution found !')

    # Statistics.
    print('\nStatistics')
    print('  - conflicts: %i' % solver.NumConflicts())
    print('  - branches : %i' % solver.NumBranches())
    print('  - wall time: %f s' % solver.WallTime())

    for n in all_nurses:
        num_shifts_worked = 0
        num_shifts_holi = 0
        for d in all_days:
            for s in all_shifts:
                if is_holiday(d, weekend_days_in_month(year_, month_)):
                    num_shifts_holi += solver.Value(shifts[(n, d, s)])
                else:
                    num_shifts_worked += solver.Value(shifts[(n, d, s)])
        print('nurse', n, ' has ', num_shifts_worked, 'normal day', num_shifts_holi, 'holiday')


if __name__ == '__main__':
    main()
