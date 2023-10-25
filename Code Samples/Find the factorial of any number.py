import random
number = random.randint(1,10000)
for i in range(2, number + 1) :
    if number % i == 0 :
        factorial = i
        print('The factorial of ' + str(number) + ' is ' + str(i))
        break