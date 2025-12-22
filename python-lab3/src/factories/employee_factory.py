"""Фабрика для создания сотрудников."""

from typing import Dict, Any
from src.core.abstract_employee import AbstractEmployee
from src.core.employee import Employee
from src.employees.manager import Manager
from src.employees.developer import Developer
from src.employees.salesperson import Salesperson


class EmployeeFactory:
    """
    Фабрика для создания объектов сотрудников.
    
    Реализует паттерн Factory Method.
    """
    
    @staticmethod
    def create_employee(emp_type: str, **kwargs) -> AbstractEmployee:
        """
        Создать сотрудника указанного типа.
        
        Args:
            emp_type: Тип сотрудника ("manager", "developer", "salesperson", "employee")
            **kwargs: Параметры для создания сотрудника
        
        Returns:
            Объект сотрудника соответствующего типа
        
        Raises:
            ValueError: Если указан неверный тип сотрудника
        """
        emp_type = emp_type.lower()
        
        if emp_type == "employee":
            return Employee(
                id=kwargs.get("id"),
                name=kwargs.get("name"),
                department=kwargs.get("department"),
                base_salary=kwargs.get("base_salary")
            )
        elif emp_type == "manager":
            return Manager(
                id=kwargs.get("id"),
                name=kwargs.get("name"),
                department=kwargs.get("department"),
                base_salary=kwargs.get("base_salary"),
                bonus=kwargs.get("bonus")
            )
        elif emp_type == "developer":
            return Developer(
                id=kwargs.get("id"),
                name=kwargs.get("name"),
                department=kwargs.get("department"),
                base_salary=kwargs.get("base_salary"),
                tech_stack=kwargs.get("tech_stack", []),
                seniority_level=kwargs.get("seniority_level")
            )
        elif emp_type == "salesperson":
            return Salesperson(
                id=kwargs.get("id"),
                name=kwargs.get("name"),
                department=kwargs.get("department"),
                base_salary=kwargs.get("base_salary"),
                commission_rate=kwargs.get("commission_rate"),
                sales_volume=kwargs.get("sales_volume", 0.0)
            )
        else:
            raise ValueError(
                f"Неизвестный тип сотрудника: {emp_type}. "
                f"Доступные типы: employee, manager, developer, salesperson"
            )





