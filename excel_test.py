num_shifts = 3
all_day = range(1, 32)

for d in all_day:
    current_shift = range((num_shifts * (d - 1)) + 1, (num_shifts * d)+1)
    print(current_shift[0])
    print(current_shift[1])
    print(current_shift[2])
    # 1 2 3
