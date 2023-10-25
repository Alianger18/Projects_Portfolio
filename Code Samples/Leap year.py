import datetime
def leap_year(input_date):
    datem = datetime.datetime.strptime(str(input_date), "%Y-%m-%d")
    if datem.year%4==0:
        return 'Leap Year'
    else:
        return 'Non Leap Year'
print(leap_year('2021-3-3'))