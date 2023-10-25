import csv 

with open('input.csv', 'r') as csvfile:
    read = csv.reader(csvfile)
    v = []
    for row in read:
        a = list(row)
        v.append(a)
    k = v[0]
    del v[0]
    
def read_csv():
    my_dict = dict()
    for i in range(len(k)) :
        my_dict[k[i]] = [v[i][0] , v[i][1], v[i][2]]
    print(my_dict.keys())