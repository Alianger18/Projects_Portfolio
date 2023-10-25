a = 45298319
a = str(a)
l = ''
for i in range(1,len(a)+1) : 
    l += a[-i]
print(l)