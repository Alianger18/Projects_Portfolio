def empty_lister(list) : 
    v = 1
    l1 = list
    l1.append(v)
    if len(l1) == 1 :
        return "it's an empty list"
    else :
        return "it's an already filled list"
