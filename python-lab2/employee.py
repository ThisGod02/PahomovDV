class Employee:
    def __init__(self):
        self.__id = 0
        self.__name = "German Sparrow"
        self.__department = "IT"
        self.__base_salary = 100000
    
    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self, new_id):
        if new_id > 0:
            self.__id = new_id
        else:
            raise ValueError

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, new_name):
        if new_name != "":
            self.__name = new_name
        else:
            raise ValueError
    
    @property
    def department(self):
        return self.__department
    @department.setter
    def department(self, new_department):
        if new_department != "":
            self.__department = new_department
        else:
            raise ValueError

    @property
    def base_salary(self):
        return self.__base_salary
    @base_salary.setter
    def base_salary(self, new_salary):
        if new_salary > 0:
            self.__base_salary = new_salary
        else:
            raise ValueError

    def __str__(self):
        return f"Сотрудник [id: {self.id}, имя: {self.name}, департамент: {self.department}, базовый оклад: {self.base_salary}]"
    
if __name__ ==  "__main__":
    first = Employee()
    print(first.__str__())
    first.id = 1
    first.name = "John"
    first.department = "HR"
    first.base_salary = 200000
    print(first.__str__())