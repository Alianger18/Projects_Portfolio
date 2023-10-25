def Duplicates_detecter(list) : 
    a_set = set()
    dups = []
    for i in range(len(list)) : 
        var = list[i]
        l1 = len(a_set)
        a_set.add(var)
        l2 = len(a_set)
        if l1 == l2 :
            dups.append(var)
        else : 
            pass
    return dups
