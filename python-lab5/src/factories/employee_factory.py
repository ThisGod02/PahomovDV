"""Factory Method паттерн - рефакторинг EmployeeFactory."""

from abc import ABC, abstractmethod
from typing import Dict, Any
from src.core.abstract_employee import AbstractEmployee
from src.core.employee import Employee
from src.employees.manager import Manager
from src.employees.developer import Developer
from src.employees.salesperson import Salesperson


class EmployeeFactory(ABC):
    """
    Абстрактная фабрика сотрудников (Factory Method паттерн).
    
    Определяет интерфейс для создания сотрудников.
    """
    
    @abstractmethod
    def create_employee(self, **kwargs) -> AbstractEmployee:
        """
        Создать сотрудника.
        
        Args:
            **kwargs: Параметры для создания сотрудника
        
        Returns:
            Объект сотрудника
        """
        pass


class ManagerFactory(EmployeeFactory):
    """Конкретная фабрика для создания менеджеров."""
    
    def create_employee(self, **kwargs) -> Manager:
        """
        Создать менеджера.
        
        Args:
            **kwargs: Параметры (id, name, department, base_salary, bonus)
        
        Returns:
            Объект Manager
        """
        return Manager(
            id=kwargs.get("id"),
            name=kwargs.get("name"),
            department=kwargs.get("department"),
            base_salary=kwargs.get("base_salary"),
            bonus=kwargs.get("bonus", 0)
        )


class DeveloperFactory(EmployeeFactory):
    """Конкретная фабрика для создания разработчиков."""
    
    def create_employee(self, **kwargs) -> Developer:
        """
        Создать разработчика.
        
        Args:
            **kwargs: Параметры (id, name, department, base_salary, tech_stack, seniority_level)
        
        Returns:
            Объект Developer
        """
        return Developer(
            id=kwargs.get("id"),
            name=kwargs.get("name"),
            department=kwargs.get("department"),
            base_salary=kwargs.get("base_salary"),
            tech_stack=kwargs.get("tech_stack", []),
            seniority_level=kwargs.get("seniority_level", "junior")
        )


class SalespersonFactory(EmployeeFactory):
    """Конкретная фабрика для создания продавцов."""
    
    def create_employee(self, **kwargs) -> Salesperson:
        """
        Создать продавца.
        
        Args:
            **kwargs: Параметры (id, name, department, base_salary, commission_rate, sales_volume)
        
        Returns:
            Объект Salesperson
        """
        return Salesperson(
            id=kwargs.get("id"),
            name=kwargs.get("name"),
            department=kwargs.get("department"),
            base_salary=kwargs.get("base_salary"),
            commission_rate=kwargs.get("commission_rate", 0),
            sales_volume=kwargs.get("sales_volume", 0)
        )


class EmployeeFactoryMethod:
    """
    Фабрика-обертка для удобного создания сотрудников (старый интерфейс).
    
    Использует конкретные фабрики для создания объектов.
    """
    
    _factories: Dict[str, EmployeeFactory] = {
        "manager": ManagerFactory(),
        "developer": DeveloperFactory(),
        "salesperson": SalespersonFactory()
    }
    
    @staticmethod
    def create_employee(emp_type: str, **kwargs) -> AbstractEmployee:
        """
        Создать сотрудника указанного типа (старый интерфейс для обратной совместимости).
        
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
        elif emp_type in EmployeeFactoryMethod._factories:
            factory = EmployeeFactoryMethod._factories[emp_type]
            return factory.create_employee(**kwargs)
        else:
            raise ValueError(
                f"Неизвестный тип сотрудника: {emp_type}. "
                f"Доступные типы: employee, manager, developer, salesperson"
            )

