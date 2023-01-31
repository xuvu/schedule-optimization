roles = ["Programmer", "Programmer", "Programmer", "Programmer", "Programmer", "Programmer", "Programmer", "Programmer",
         "Service", "Service", "Service", "Service", "Service", "Service"]

# counts = {role: roles.count(role) for role in set(roles)}
# print(counts)
#
# min_value = max(counts.values())
# min_type = [key for key, value in counts.items() if value == min_value]
#
# print(counts[str(min_type[0])])

role_count = [f"{k}{i}" for i, k in enumerate(roles, 1) if k == 'Programmer']
print(role_count)
