import csv 

with open('input.txt', 'r') as csvfile : 
    file = csv.reader(csvfile, delimiter = ',')
    f = ''
    for row in csvfile :
        f += row

def read_text_file(word) : 
    count = 0
    for i in range(len(f)) :
            l = len(word)
            if f[i] == word[0] : 
                if l == 1 and f[i+1] == ' ' :
                    count += 1
                elif f[i:i+l] == word[:] : 
                    count += 1
    return(count)