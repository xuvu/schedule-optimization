from ortools.constraint_solver import pywrapcp

# Define the number of nurses, shifts, and days in the schedule
num_nurses = 10
num_shifts = 3  # morning, afternoon, night
num_days = 31
working_days = list(range(num_days))

# Create a solver and a decision builder
solver = pywrapcp.Solver("Nurse schedule")

# Create variables to represent each shift for each nurse and each day
shifts = [[[solver.IntVar(0, num_nurses - 1, "shift(%i,%i,%i)" % (n, s, d))
            for d in range(num_days)]
           for s in range(num_shifts)]
          for n in range(num_nurses)]

db = solver.Phase([shifts[n][s][d] for n in range(num_nurses) for s in range(num_shifts) for d in range(num_days)],
                  solver.INT_VAR_SIMPLE,
                  solver.INT_VALUE_SIMPLE)

# Ensure that each nurse works the same number of shifts for each shift type
for n in range(num_nurses):
    for s in range(num_shifts):
        solver.Add(solver.Sum([shifts[n][s][d] for d in range(num_days) if d not in working_days]) == int((num_days - len(working_days))/num_shifts))
        solver.Add(solver.Sum([shifts[n][s][d] for d in working_days]) == int(len(working_days)/num_shifts))

# Ensure that no morning shifts are scheduled on working days
for n in range(num_nurses):
    for d in range(num_days):
        if d % 7 < 5:
            solver.Add(shifts[n][0][d] == -1)


# Ensure that each nurse works at most two shifts within 4 days
for n in range(num_nurses):
    for d in range(num_days):
        if d < num_days - 3:
            solver.Add(solver.Sum([shifts[n][s][d + i] for i in range(4) for s in range(num_shifts)]) <= 2)

# Set a shift request for a specific nurse
nurse = 2
shift = 1
day = 15
solver.Add(shifts[nurse][shift][day] == nurse)

# Find a solution
solution = solver.Assignment()
solution.Add([shifts[n][s][d] for n in range(num_nurses)
              for s in range(num_shifts)
              for d in range(num_days)])
solver.NewSearch(db)


if solver.NextSolution():
    for n in range(num_nurses):
        print("Nurse", n)
        for d in range(num_days):
            print("Day", d, ":", end=" ")
            for s in range(num_shifts):
                if shifts[n][s][d].Value() == n:
                    print(s, end=" ")
            print()
        print()
