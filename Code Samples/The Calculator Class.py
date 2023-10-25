class Calculator :
    def __init__(self,x,y) :
        self.x = x
        self.y = y
    def add(self) :
        value_add = self.x + self.y
        return self.x , self.y , value_add
    def sub(self) : 
        value_sub = self.x - self.y
        return self.x , self.y , value_sub
    def mul(self) : 
        value_mul = self.x * self.y
        return self.x , self.y , value_mul
    def div(self) : 
        try :
            value_div = self.x / self.y
        except self.y == 0 :
            raise ZeroDivisionError
        value_div = round(value_div)
        return self.x , self.y , value_div