
def dict_sort(input_dict):
    ct=input_dict
    kies=list(ct.keys())
    dic_listed=[]
    for i in range(len(kies)):
        y=kies[i]
        x=[ct[y],y]
        dic_listed.append(x)
    sorted_list=sorted(dic_listed)
    output_dict={}
    for j in range(len(sorted_list)):
        x=sorted_list[j][1]
        y=sorted_list[j][0]
        output_dict[x]=y
    return output_dict

a = {'ali':2, 'karima':1, 'mouad':3, 'nabil':4}
A=dict_sort(a)
print(A)