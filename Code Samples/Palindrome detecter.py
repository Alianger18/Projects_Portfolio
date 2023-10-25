def palindrome_detecter(string) : 
    s = string 
    s_rev = ''
    for i in range(1,len(s)+1) : 
        s_rev += s[-i]
    if s == s_rev :
        return s + ' is a palidrome.'
    else : 
        return s + ' is not a palidrome.'

print(palindrome_detecter('adba'))