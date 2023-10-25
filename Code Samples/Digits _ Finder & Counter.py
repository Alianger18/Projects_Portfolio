def digits_counter(string):
    count=0
    a=0
    x=string
    list_1=["0","1","2","3","4","5","6","7","8","9"]
    while a<len(x):
        if x[a] in list_1:
            #We look for only the number.
            count+=1
            a+=1
        else:
            a+=1
    print(count)

def digits_finder(string):
    count=0
    a=0
    x=string
    list_1=["0","1","2","3","4","5","6","7","8","9"]
    used_digits=[]
    while a<len(x):
        if x[a] in list_1:
            #The kicker here is the digit found in the string is added by identity to a list printed at the issue.
            used_digits.append(x[a])
            count+=1
            a+=1
        else:
            a+=1
    print(used_digits)
