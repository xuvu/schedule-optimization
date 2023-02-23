from ortools.sat.python import cp_model
import numpy as np

num_nurses = 5
num_days = 7
num_shifts = 3

# The objective is to minimize the standard deviation of total shifts for each nurse.
model = cp_model.CpModel()

# Creates shift variables.
shifts = {}
for j in range(num_nurses):
    for i in range(num_days):
        for k in range(num_shifts):
            shifts[(j, i, k)] = model.NewBoolVar('shift_j%i_d%i_s%i' % (j, i, k))

# Each shift is assigned to exactly one nurse.
for i in range(num_days):
    for k in range(num_shifts):
        model.Add(sum(shifts[(j, i, k)] for j in range(num_nurses)) == 1)

# Each nurse works at most one shift per day.
for j in range(num_nurses):
    for i in range(num_days):
        model.Add(sum(shifts[(j, i, k)] for k in range(num_shifts)) <= 1)

# Each nurse works at least two consecutive shifts before taking a rest.
for j in range(num_nurses):
    for i in range(num_days - 2):
        model.Add(sum(shifts[(j, i + d, k)] for d in range(3) for k in range(num_shifts)) >= 2).OnlyEnforceIf(shifts[(j, i, 0)])

# Create the total shift variable for each nurse.
total_shifts = [model.NewIntVar(0, num_days, f'total_shifts_n{j}') for j in range(num_nurses)]
for j in range(num_nurses):
    model.Add(total_shifts[j] == sum(shifts[(j, i, k)] for i in range(num_days) for k in range(num_shifts)))

# Minimize the standard deviation of total shifts for each nurse.
avg_total_shifts = np.mean(list(range(num_days))) * num_shifts
standard_deviations = []
for j in range(num_nurses):
    deviation = model.NewIntVar(0, num_days, f'std_dev_n{j}')
    model.Add(deviation == (total_shifts[j] - avg_total_shifts) * (total_shifts[j] - avg_total_shifts))
    standard_deviations.append(deviation)
model.Minimize(sum(standard_deviations))

# Solve the model.
solver = cp_model.CpSolver()
status = solver.Solve(model)

# Print the results.
if status == cp_model.OPTIMAL:
    for j in range(num_nurses):
        print('Nurse', j)
        for i in range(num_days):
            for k in range(num_shifts):
                if solver.Value(shifts[(j, i, k)]) == 1:
                    print(f"Day {i}: Shift {k}")
        print(f"Total Shifts: {solver.Value(total_shifts[j])}")
else:
    print('No solution found.')
