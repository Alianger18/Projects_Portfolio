class Employee() :
    def __init__(self, full_name, age=None, salary=None, dept=None) :
        i = full_name.index(" ")
        self.first_name = full_name[:i]
        self.last_name = full_name[i+1:]
        self.age = int(age)
        self.salary = int(salary)
        self.dept = dept

print(Employee('Ali Barir', 21, 5500, 'D.FORMATION').age)