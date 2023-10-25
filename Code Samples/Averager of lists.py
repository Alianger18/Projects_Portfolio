from random import randint
def avg(list) : 
    sum = 0
    for element in list : 
        sum += element
    return sum // 2

lista = [randint(1,100) for i in range(25) if i > 0 ]
print(lista)
print(avg(lista))

print("new" "line")