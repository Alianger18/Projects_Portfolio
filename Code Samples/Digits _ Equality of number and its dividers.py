def factors(x):
    list_1=[]
    for i in range(1,10000):
        if x%i==0 and x!=i:
            list_1.append(i)
        else:
            continue
    else:
        pass
    return list_1

def sum_pos_divisor(num):
    listo=factors(num)
    fullsum=0
    b=0
    for item in listo:
        fullsum+=listo[b]
        b+=1
    if fullsum==num:
        return("True")
    else:
        return("False")
