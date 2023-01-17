"""
import datetime
import calendar

# Get the current date
now = datetime.datetime.now()

weekday_name = now.strftime("%A")


def is_holiday(today):
    if today == 'Saturday' or today == 'Sunday':
        print("Today is a holiday!")
    else:
        print("Today is not a holiday.")


# which day is holiday? => take in the list of holiday
def get_current_month_count():
    # Get the number of days in the current month
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    return days_in_month  # amount of holidays and normal days

print(weekday_name)
print(get_current_month_count())
"""
import calendar
import numpy as np


def days_in_month(year, month):
    return calendar.monthrange(year, month)[1]


def weekend_days(year, month):
    # calendar.Calendar() creates list of all week days within specific month
    cal = calendar.Calendar()

    return [day for day in cal.itermonthdays(year, month) if day and calendar.weekday(year, month, day) >= 5]


def create_list(number_of_nurse, days_in_month):
    # create list which has shape like (number_of_nurse,days_in_month ,3)
    # 3 is for 3 shifts
    # 0 is for day off
    # 1 is for day on
    # 2 is for weekend
    return np.zeros((number_of_nurse, days_in_month, 3))


print(create_list(3, days_in_month(2023, 1)))
