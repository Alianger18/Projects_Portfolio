def duplicate_remover(input_dict):
    ct=input_dict
    kies=list(ct.keys())
    dic_listed=[]
    for i in range(len(kies)):
        y=kies[i]
        x=[ct[y],y]
        dic_listed.append(x)
    sorted_list=sorted(dic_listed)
    sorted_list.append(['index', 'reasons only'])
    fin=[]
    for j in range(0,len(sorted_list)-1):
        x=sorted_list[j][0]
        y=sorted_list[j+1][0]
        if x==y:
            pass
        else:
            fin.append(sorted_list[j])
    almost=[]
    for k in range(len(fin)):
        x=fin[k][1]
        y=fin[k][0]
        a=[x,y]
        almost.append(a)
    almost=sorted(almost)
    output_dict={}
    for l in range(len(almost)):
        y=almost[l][1]
        x=almost[l][0]
        output_dict[x]=y
    return output_dict

input_di = {'Box1':'Apple', 'Box2':'Mango',
            'Box3':'Orange', 'Box4':'Apple',
            'Box5':'Orange', 'Box6':'Orange',
            'Box7':'Strawberry','Box8':'Apple'
            }
print(duplicate_remover(input_di))