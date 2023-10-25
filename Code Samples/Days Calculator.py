import datetime
def date_diff():
    date1='1970-1-1'
    date2='2021-10-28'
    date_1 = datetime.datetime.strptime(str(date1), "%Y-%m-%d")
    date_2 = datetime.datetime.strptime(str(date2), "%Y-%m-%d")
    delta=datetime.datetime.__sub__(date_2,date_1)
    return delta

print(date_diff())