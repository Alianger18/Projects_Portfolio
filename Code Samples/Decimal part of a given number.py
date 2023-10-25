import math
def decimal_part(value):
    frac,whole = math.modf(value)
    while frac==0 :
        return "INTEGER"
    else:
        f='%.2f'%frac
        print(f)