"""Builder паттерн - пошаговое создание сотрудников."""

from typing import List, Optional
from src.core.abstract_employee import AbstractEmployee
from src.core.employee import Employee
from src.employees.manager import Manager
from src.employees.developer import Developer
from src.employees.salesperson import Salesperson


class EmployeeBuilder:
    """
    Builder для пошагового создания сложных объектов сотрудников.
    
    Реализует fluent-интерфейс для удобного создания объектов.
    """
    
    def __init__(self):
        """Инициализация билдера."""
        self._id: Optional[int] = None
        self._name: Optional[str] = None
        self._department: Optional[str] = None
        self._base_salary: Optional[float] = None
        self._employee_type: Optional[str] = None
        
        # Параметры для Manager
        self._bonus: Optional[float] = None
        
        # Параметры для Developer
        self._tech_stack: Optional[List[str]] = None
        self._seniority_level: Optional[str] = None
        
        # Параметры для Salesperson
        self._commission_rate: Optional[float] = None
        self._sales_volume: Optional[float] = None
    
    def set_id(self, id: int) -> 'EmployeeBuilder':
        """
        Установить ID сотрудника.
        
        Args:
            id: ID сотрудника
        
        Returns:
            self для цепочки вызовов
        """
        self._id = id
        return self
    
    def set_name(self, name: str) -> 'EmployeeBuilder':
        """
        Установить имя сотрудника.
        
        Args:
            name: Имя сотрудника
        
        Returns:
            self для цепочки вызовов
        """
        self._name = name
        return self
    
    def set_department(self, department: str) -> 'EmployeeBuilder':
        """
        Установить отдел сотрудника.
        
        Args:
            department: Отдел
        
        Returns:
            self для цепочки вызовов
        """
        self._department = department
        return self
    
    def set_base_salary(self, base_salary: float) -> 'EmployeeBuilder':
        """
        Установить базовую зарплату.
        
        Args:
            base_salary: Базовая зарплата
        
        Returns:
            self для цепочки вызовов
        """
        self._base_salary = base_salary
        return self
    
    def set_type(self, employee_type: str) -> 'EmployeeBuilder':
        """
        Установить тип сотрудника.
        
        Args:
            employee_type: Тип ("employee", "manager", "developer", "salesperson")
        
        Returns:
            self для цепочки вызовов
        """
        self._employee_type = employee_type.lower()
        return self
    
    def set_bonus(self, bonus: float) -> 'EmployeeBuilder':
        """
        Установить бонус (для Manager).
        
        Args:
            bonus: Бонус
        
        Returns:
            self для цепочки вызовов
        """
        self._bonus = bonus
        return self
    
    def set_skills(self, tech_stack: List[str]) -> 'EmployeeBuilder':
        """
        Установить стек технологий (для Developer).
        
        Args:
            tech_stack: Список технологий
        
        Returns:
            self для цепочки вызовов
        """
        self._tech_stack = tech_stack
        return self
    
    def set_seniority(self, seniority_level: str) -> 'EmployeeBuilder':
        """
        Установить уровень seniority (для Developer).
        
        Args:
            seniority_level: Уровень ("junior", "middle", "senior")
        
        Returns:
            self для цепочки вызовов
        """
        self._seniority_level = seniority_level
        return self
    
    def set_commission_rate(self, commission_rate: float) -> 'EmployeeBuilder':
        """
        Установить процент комиссии (для Salesperson).
        
        Args:
            commission_rate: Процент комиссии
        
        Returns:
            self для цепочки вызовов
        """
        self._commission_rate = commission_rate
        return self
    
    def set_sales_volume(self, sales_volume: float) -> 'EmployeeBuilder':
        """
        Установить объем продаж (для Salesperson).
        
        Args:
            sales_volume: Объем продаж
        
        Returns:
            self для цепочки вызовов
        """
        self._sales_volume = sales_volume
        return self
    
    def build(self) -> AbstractEmployee:
        """
        Построить объект сотрудника.
        
        Returns:
            Объект сотрудника
        
        Raises:
            ValueError: Если не хватает обязательных параметров
        """
        # Проверка обязательных параметров
        if self._id is None:
            raise ValueError("ID сотрудника обязателен")
        if self._name is None:
            raise ValueError("Имя сотрудника обязательно")
        if self._department is None:
            raise ValueError("Отдел сотрудника обязателен")
        if self._base_salary is None:
            raise ValueError("Базовая зарплата обязательна")
        
        employee_type = self._employee_type or "employee"
        
        if employee_type == "manager":
            if self._bonus is None:
                raise ValueError("Бонус обязателен для менеджера")
            return Manager(
                id=self._id,
                name=self._name,
                department=self._department,
                base_salary=self._base_salary,
                bonus=self._bonus
            )
        elif employee_type == "developer":
            if self._tech_stack is None:
                self._tech_stack = []
            if self._seniority_level is None:
                self._seniority_level = "junior"
            return Developer(
                id=self._id,
                name=self._name,
                department=self._department,
                base_salary=self._base_salary,
                tech_stack=self._tech_stack,
                seniority_level=self._seniority_level
            )
        elif employee_type == "salesperson":
            if self._commission_rate is None:
                self._commission_rate = 0.0
            if self._sales_volume is None:
                self._sales_volume = 0.0
            return Salesperson(
                id=self._id,
                name=self._name,
                department=self._department,
                base_salary=self._base_salary,
                commission_rate=self._commission_rate,
                sales_volume=self._sales_volume
            )
        else:
            # Обычный сотрудник
            return Employee(
                id=self._id,
                name=self._name,
                department=self._department,
                base_salary=self._base_salary
            )

