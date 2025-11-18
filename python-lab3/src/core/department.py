"""Класс Department (Отдел) для управления сотрудниками."""

import json
from typing import List, Optional, Dict
from src.core.abstract_employee import AbstractEmployee


class Department:
    """
    Класс для представления отдела компании.
    
    Управляет коллекцией сотрудников с поддержкой полиморфизма.
    """
    
    def __init__(self, name: str):
        """
        Инициализация отдела.
        
        Args:
            name: Название отдела
        """
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"Название отдела не должно быть пустой строкой, получено: '{name}'")
        self.__name = name
        self.__employees: List[AbstractEmployee] = []
    
    @property
    def name(self) -> str:
        """Получить название отдела."""
        return self.__name
    
    @name.setter
    def name(self, value: str) -> None:
        """Установить название отдела."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Название отдела не должно быть пустой строкой, получено: '{value}'")
        self.__name = value
    
    def add_employee(self, employee: AbstractEmployee) -> None:
        """
        Добавить сотрудника в отдел.
        
        Args:
            employee: Объект сотрудника
        """
        if not isinstance(employee, AbstractEmployee):
            raise TypeError(f"Сотрудник должен быть экземпляром AbstractEmployee, получено: {type(employee)}")
        if employee in self.__employees:
            raise ValueError(f"Сотрудник с ID {employee.id} уже находится в отделе")
        self.__employees.append(employee)
    
    def remove_employee(self, employee_id: int) -> None:
        """
        Удалить сотрудника по ID.
        
        Args:
            employee_id: ID сотрудника для удаления
        
        Raises:
            ValueError: Если сотрудник не найден
        """
        employee = self.find_employee_by_id(employee_id)
        if employee is None:
            raise ValueError(f"Сотрудник с ID {employee_id} не найден в отделе")
        self.__employees.remove(employee)
    
    def get_employees(self) -> List[AbstractEmployee]:
        """
        Получить список всех сотрудников отдела.
        
        Returns:
            Список сотрудников
        """
        return self.__employees.copy()
    
    def calculate_total_salary(self) -> float:
        """
        Вычислить общую зарплату всех сотрудников отдела.
        
        Демонстрирует полиморфизм - метод работает с разными типами сотрудников.
        
        Returns:
            Сумма зарплат всех сотрудников
        """
        return sum(emp.calculate_salary() for emp in self.__employees)
    
    def get_employee_count(self) -> Dict[str, int]:
        """
        Получить количество сотрудников каждого типа.
        
        Returns:
            Словарь с количеством сотрудников по типам
        """
        counts: Dict[str, int] = {}
        for emp in self.__employees:
            emp_type = emp.__class__.__name__
            counts[emp_type] = counts.get(emp_type, 0) + 1
        return counts
    
    def find_employee_by_id(self, employee_id: int) -> Optional[AbstractEmployee]:
        """
        Найти сотрудника по ID.
        
        Args:
            employee_id: ID сотрудника
        
        Returns:
            Объект сотрудника или None если не найден
        """
        for emp in self.__employees:
            if hasattr(emp, 'id') and emp.id == employee_id:
                return emp
        return None
    
    def __len__(self) -> int:
        """
        Возвращает количество сотрудников в отделе.
        
        Returns:
            Количество сотрудников
        """
        return len(self.__employees)
    
    def __getitem__(self, key) -> AbstractEmployee:
        """
        Доступ к сотруднику по индексу.
        
        Args:
            key: Индекс сотрудника
        
        Returns:
            Объект сотрудника
        
        Raises:
            IndexError: Если индекс вне диапазона
        """
        return self.__employees[key]
    
    def __contains__(self, employee: AbstractEmployee) -> bool:
        """
        Проверка принадлежности сотрудника отделу.
        
        Args:
            employee: Объект сотрудника
        
        Returns:
            True если сотрудник в отделе, False иначе
        """
        return employee in self.__employees
    
    def __iter__(self):
        """
        Итерация по сотрудникам отдела.
        
        Returns:
            Итератор по списку сотрудников
        """
        return iter(self.__employees)
    
    def save_to_file(self, filename: str) -> None:
        """
        Сохранить всех сотрудников отдела в JSON файл.
        
        Args:
            filename: Имя файла для сохранения
        """
        data = {
            "name": self.__name,
            "employees": [self._employee_to_dict(emp) for emp in self.__employees]
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    @classmethod
    def load_from_file(cls, filename: str) -> 'Department':
        """
        Загрузить отдел из JSON файла.
        
        Args:
            filename: Имя файла для загрузки
        
        Returns:
            Объект Department
        """
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return cls.load_from_file_dict(data)
    
    @classmethod
    def load_from_file_dict(cls, data: dict) -> 'Department':
        """
        Загрузить отдел из словаря.
        
        Args:
            data: Словарь с данными отдела
        
        Returns:
            Объект Department
        """
        dept = cls(data["name"])
        for emp_data in data.get("employees", []):
            employee = cls._employee_from_dict(emp_data)
            dept.add_employee(employee)
        return dept
    
    @staticmethod
    def _employee_to_dict(employee: AbstractEmployee) -> dict:
        """Преобразовать сотрудника в словарь для сериализации."""
        if hasattr(employee, 'to_dict'):
            return employee.to_dict()
        # Fallback для случаев, когда метод to_dict не реализован
        return {
            "type": employee.__class__.__name__,
            "id": getattr(employee, 'id', None),
            "name": getattr(employee, 'name', None),
            "department": getattr(employee, 'department', None),
            "base_salary": getattr(employee, 'base_salary', None)
        }
    
    @staticmethod
    def _employee_from_dict(data: dict) -> AbstractEmployee:
        """Создать объект сотрудника из словаря."""
        from src.core.employee import Employee
        from src.employees.manager import Manager
        from src.employees.developer import Developer
        from src.employees.salesperson import Salesperson
        
        emp_type = data.get("type", "Employee")
        
        if emp_type == "Manager":
            return Manager(
                id=data["id"],
                name=data["name"],
                department=data["department"],
                base_salary=data["base_salary"],
                bonus=data.get("bonus", 0)
            )
        elif emp_type == "Developer":
            return Developer(
                id=data["id"],
                name=data["name"],
                department=data["department"],
                base_salary=data["base_salary"],
                tech_stack=data.get("tech_stack", []),
                seniority_level=data.get("seniority_level", "junior")
            )
        elif emp_type == "Salesperson":
            return Salesperson(
                id=data["id"],
                name=data["name"],
                department=data["department"],
                base_salary=data["base_salary"],
                commission_rate=data.get("commission_rate", 0),
                sales_volume=data.get("sales_volume", 0)
            )
        else:
            return Employee.from_dict(data)
    
    def __str__(self) -> str:
        """
        Строковое представление отдела.
        
        Returns:
            Строка с информацией об отделе
        """
        return f"Отдел '{self.__name}' (сотрудников: {len(self.__employees)})"

