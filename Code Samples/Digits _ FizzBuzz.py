def fizzbuzz(i):
    if i%3==0 and i%5==0:
        print("FizzBuzz")
    elif i%3==0:
        print("Fizz")
    elif i%5==0:
        print("Buzz")
    else:
        print(i)

f=0
while f<100 :
    fizzbuzz(f)
    f+=1
else:
    pass
