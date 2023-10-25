class Car() :
    global data_base ; data_base = {} 
    def __init__(self, model, year, type_of_car, unique_id) :
        self.model = model
        self.year = year
        self.type_of_car = type_of_car
        self.unique_id = unique_id
        data_base[model] = [year, type_of_car, unique_id]
        return None 
    def no_of_vehicles(self) : 
        no_of_objects = len(data_base.keys())
        return no_of_objects

Car("Mercedes CLA 250 AMG", "CLA 250 AMG", 1985, "Limousine", "002734162317")
Car("BMW M5 6th Series", "M5 6th Series", 1972, "Sport", "001548132819")
print(Car.nbr_objects())