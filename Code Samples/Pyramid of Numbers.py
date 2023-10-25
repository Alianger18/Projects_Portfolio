# Pyramid Of numbers 
l = [ i for i in range(1,10) if i > 0]
a = ''
for i in range(len(l)) :
    a += (str(l[i]) + ' ')
    print(a)