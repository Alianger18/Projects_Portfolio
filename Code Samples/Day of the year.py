import datetime
def day_of_year(input_date):
    Months=['00',1,2,4,5,6,7,8,9,10,11,12]
    Days=['00',31,28,31,30,31,30,31,31,30,31,30,31]
    Datos = datetime.datetime.strptime(str(input_date), "%Y-%m-%d")
    Day=Datos.day
    Month=Datos.month
    Year=Datos.year
    if Year%4==0:
        Days[2]=29
    day_of_the_year=Day
    for i in range(1,Month):
        day_of_the_year+=Days[i]
    return day_of_the_year