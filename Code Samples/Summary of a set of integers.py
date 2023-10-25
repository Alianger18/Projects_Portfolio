from random import randint

ran = []
for i in range(10) : 
     ran.append(randint(1,100))
print(ran)
result = 0
for j in range(len(ran)) :
    result += ran[j]
    print(result)