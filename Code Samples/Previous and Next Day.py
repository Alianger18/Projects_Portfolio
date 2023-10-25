import datetime
def calculate_dates(input_date):
    Months=['00',1,2,4,5,6,7,8,9,10,11,12]
    Days=['00',31,28,31,30,31,30,31,31,30,31,30,31]
    Datos = datetime.datetime.strptime(str(input_date), "%Y-%m-%d")
    Day=Datos.day
    Month=Datos.month
    Year=Datos.year
    if Year%4==0:
        Days[2]=29
    input_date=datetime.date(Year,Month,Day)
    dmin=Day-1
    mmin=Month
    ymin=Year
    dmax=Day+1
    mmax=Month
    ymax=Year
    if Days[Month]<dmax:
        dmax=dmax-Days[Month]
        mmax=mmax+1
        if mmax>12:
            ymax=ymax+1
            mmax=mmax-12
    if dmin==0:
        dmin=Days[Month-1]
        if dmin=='00':
            dmin=31
        mmin-=1
        if mmin<=0:
            mmin=12
            ymin-=1
    prev_date=datetime.date(ymin,mmin,dmin)
    next_date=datetime.date(ymax,mmax,dmax)
    return (prev_date,input_date,next_date)