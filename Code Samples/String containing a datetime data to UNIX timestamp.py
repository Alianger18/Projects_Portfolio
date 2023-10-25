import datetime 
def day_of_year(input_string):
    Days=['00',31,28,31,30,31,30,31,31,30,31,30,31]
    Months_num=['00', 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10, 11 , 12 ]
    Months_str=['#',
    'Jan' ,'Feb' ,'Mar' ,'Apr' ,'Mai' ,'Jun' ,
    'Jul' ,'Aug' ,'Sep' ,'Oct' ,'Nov' , 'Dec'
                ]
    c=input_string ; b=''
    l=[]
    for i in range(len(c)) : 
        l.append(c[i])
    del l[-1] ; del l[-1] 
    mn=l[0]+l[1]+l[2]
    mi=str(Months_str.index(mn))
    if len(mi) ==  1 :
        mi='0'+mi
    del l[0] ; del l[0] ; del l[0] 
    l.insert(0,mi) 
    for i in range(len(l)) :
        b+=l[i]
    Datos = datetime.datetime.strptime(b, "%m %d %Y %H:%M:%S")
    Second = Datos.second
    Minute = Datos.minute
    Hour = Datos.hour
    Day = Datos.day
    Month = Datos.month
    Year = Datos.year
    if 'PM' in input_string or 'pm' in input_string :
        Hour=Hour+12
    date=datetime.datetime(Year,Month,Day,Hour,Minute,Second)
    return datetime.datetime.timestamp(date)