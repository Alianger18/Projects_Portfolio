def Binary_search(list, element) :
    first = 0
    last = len(list) - 1
    found = False
    while first <= last and not found :
        mid = (first + last) // 2
        if list[mid] == element : 
            found = True 
        else : 
            if element < list[mid] : 
                last = mid - 1
            else :
                first = mid + 1
    if found == True :
        return "It's found."
    else : 
        return "Nop, we don't have such item." 

a = [87,357,59,3,4,85,7,6,3,5]

print(Binary_search(a, 85))