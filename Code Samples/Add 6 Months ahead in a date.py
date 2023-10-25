import datetime
def add_to_date(input_date):
    Months=[0,1,2,4,5,6,7,8,9,10,11,12]
    Days=[0,31,28,31,30,31,30,31,31,30,31,30,31]
    Datos = datetime.datetime.strptime(str(input_date), "%Y-%m-%d")
    Year=Datos.year
    Month=Datos.month
    Day=Datos.day
    if Year%4==0:
        Days[2]=29
    Days_diff=1
    Dmax=Day+1
    if Month>6:
        Mmax=(Month+6)-12
    else : 
        Mmax=Month+6
    next_date=datetime.date.replace(input_date,Year,Mmax,Dmax)
    return next_date
b=datetime.date(2021,11,15)
print(add_to_date(b))
