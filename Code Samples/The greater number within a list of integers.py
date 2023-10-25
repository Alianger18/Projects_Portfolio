from random import randint
ran = [randint(1,1000) for i in range(20) if i > 0]
ran = sorted(ran, reverse=False)
print(ran[-1])