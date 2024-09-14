import numpy as np

n = int(input('Enter your 1st number:'))
m = int(input('Enter your 2nd number:'))

red = np.sum(np.array([i for i in range(n, m+1)]))
print(red)
