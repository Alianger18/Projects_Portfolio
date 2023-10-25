import datetime
def add_to_date(input_date):
    Months=[0,1,2,4,5,6,7,8,9,10,11,12]
    Days=[0,31,28,31,30,31,30,31,31,30,31,30,31]
    Datos = datetime.datetime.strptime(str(input_date), "%Y-%m-%d")
    Year=Datos.year ; Month=Datos.month ; Day=Datos.day ;
    Ymin = 0 ; Mmin = 0 ; Dmin = 0 ; 
    if Year % 4 == 0:
        Days[2] = 29
    if Month == 1 :
        if Day - 5 > 0 : 
            Dmin = Day - 5
            Mmin = Month
            Ymin = Year 
        else :
            Dmin = 31 + Day - 5 
            Mmin = 12 
            Ymin = Year - 1
    else : 
        if Day - 5 > 0 : 
            Dmin = Day - 5
            Mmin = Month
            Ymin = Year 
        else :
            Dmin = Days[Month-1] + Day - 5 
            Mmin = Month - 1
            Ymin = Year
    next_date=datetime.date.replace(input_date,Ymin,Mmin,Dmin)
    return next_date