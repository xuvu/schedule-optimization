k = range(6, 10)
for d in k:
    print(d)  # 6 7 8 9
    ss = sum(d + i for i in range(6))  # (6 + 0)+ (6+1) + (6+2) + (6+3) + (6+4) + (6+5)
    print(ss)
