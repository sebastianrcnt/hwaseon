import datetime

day1 = datetime.date(2020, 1, 1)
day2 = datetime.date(2021, 1, 1)

print(day1.strftime("%Y%m%d"))
print(day2.isoformat())