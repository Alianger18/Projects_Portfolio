a = "There's a boo and loo and even sometimes yoo hoo."
result = []
for i in range(len(a)) :
    try : 
        part = a[i:i+3]
        if a[i+1:i+3] == 'oo' :
            result.append(part)
        else : 
            pass
    except : 
        IndexError
print(result)

# ------------------------------------ Another Solution -------------------------------

import re
resultado = re.findall('.oo', a)
print(resultado)