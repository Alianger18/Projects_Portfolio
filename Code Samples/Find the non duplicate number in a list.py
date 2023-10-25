# My Solutoion
l = [1,9,8,7,3,6,4,6,5,4,6,3,7,2,2,1,9]
result = []
for i in range(1,len(l)+1) :
    try :
        a = l[-i]
        del l[-i] 
        if a in l :
            pass
        else : 
            result.append(a)
    except : 
        IndexError
print(result)
# Solution of Corry 
numbers = [1, 1, 2, 2, 3, 3, 4, 5, 5]
count = {}
for i in numbers:
    if i not in count:
        count[i] = 1
    else:
        count[i] += 1
for key, value in count.items():
    if value == 1:
        print(key)