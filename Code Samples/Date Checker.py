import datetime
def check_date(Year,Month,Day):
    Months=[0,1,2,4,5,6,7,8,9,10,11,12]
    Days=[0,31,28,31,30,31,30,31,31,30,31,30,31]
    if Year % 4 == 0:
            Days[2] = 29
    if 10000 > Year > 0 and 13 > Month > 0 and 32 > Day > 0 :
        if Month == 2 :
            if Day > Days[2] :
                return False
            else :
                return True
        else : 
            return False
    else : 
        return False

print(check_date(2021,2,29))