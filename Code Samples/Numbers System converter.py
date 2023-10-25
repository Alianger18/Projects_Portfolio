class  Nsc() :
    def __init__(self) : 
        return None
    def to_binary(value) : 
        # accepts an integer and converts it to its binary representation.
        base = [0,1]
        b = len(base)
        repr = [0,0,0,0,0,0,0,0]
        temp = 0
        for i in range(-7,1) : 
            if value - 2**(-i) > 0 :
                repr[i+7] = 1
            else : 
                pass
        final_repr = ''
        for j in range(len(repr)) : 
            final_repr += str(repr[j])
        return final_repr
    def to_octal(value) :
        # accepts an integer and converts it to its octal representation.
        a = str(oct(value))
        b = list(a)
        del b[0:2]
        if len(b) == 2 :
            b.insert(0, '0')
        else : 
            pass
        final_repr = ''
        for element in b :
            final_repr += element
        return final_repr
    def to_decimal(value) :
        # accepts an integer and converts it to its decimal representation.
        return value
    def to_hexadecimal(value) :
        # accepts an integer and converts it to its hexadecimal representation.
        a = str(hex(value))
        b = list(a)
        del b[0:2]
        if len(b) == 2 :
            b.insert(0, '0')
        else : 
            pass
        final_repr = ''
        for element in b :
            final_repr += element
        return final_repr