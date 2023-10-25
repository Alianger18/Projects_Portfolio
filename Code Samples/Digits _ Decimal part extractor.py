import math

def decimal_part(value):
    frac,whole = math.modf(value)
    while frac==0 :
        return "INTEGER"
    else:
      #The 2f thing below is how much number you need in your decimal part.
      #The approximative evaluation is applied, 0,9338 is 0,934 is 0,93 and so on.
      f='%.2f'%frac
      print(f)
