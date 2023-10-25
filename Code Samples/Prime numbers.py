def prime_numbers(x,y) : 
    temp = [i for i in range(x,y+1) if i > 0 ]
    prime_numbers = []
    for element in temp :
        temporary = []
        for k in range(2,element+1) : 
            if element % k == 0 :
                temporary.append(k)
            else :
                pass
        if len(temporary) == 1 :
            prime_numbers.append(element)
        temporary.clear
    return prime_numbers

print(prime_numbers(1,23))