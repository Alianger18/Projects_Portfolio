class Person():
    def __init__(self,name,age) :
        self.name = name
        self.age = age
    def compare(self,other) :
        b = "older than me."
        a = "the same age as me."
        y = "younger than me."
        if other.age > self.age :
            resp = str(other.name) + ' is ' + b 
            return resp
        elif self.age == other.age :
            resp = str(other.name) + ' is ' + a 
            return resp
        else :
            resp = str(other.name) + ' is ' + y
            return resp