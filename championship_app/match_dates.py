
import datetime

def days_after(base, n):
    base_date = datetime.datetime.strptime(base, "%Y-%m-%d")
    end_date = base_date + datetime.timedelta(days=n)
    #print(base, end_date)
    return end_date.strftime("%Y-%m-%d")

def matchdays_of_round(base, round):
    return (days_after(base, round*7), days_after(base, round*7 +3))

# src = [
#   '2023-09-12',
#   '2023-09-30',
#   '2023-12-30'
# ]
# 
# for d in src:
#   print(d, days_after(d, 3))

season_start = '2023-10-01'
num_of_teams = 4
for i in range(0, (num_of_teams -1) * 2):
    print(i, matchdays_of_round(season_start, i))
