def count_num_digits(input_string):
    count=0
    a=0
    x=input_string
    list_1=["0","1","2","3","4","5","6","7","8","9"]
    while a<len(x):
        if x[a] in list_1:
            #We look for only the number.
            count+=1
            a+=1
        else:
            a+=1
    return count