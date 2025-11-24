"""Specification паттерн - спецификации для фильтрации сотрудников."""

from abc import ABC, abstractmethod
from typing import List
from src.core.abstract_employee import AbstractEmployee


class Specification(ABC):
    """
    Абстрактная спецификация.
    
    Определяет интерфейс для проверки соответствия объектов условиям.
    """
    
    @abstractmethod
    def is_satisfied_by(self, employee: AbstractEmployee) -> bool:
        """
        Проверить, удовлетворяет ли сотрудник спецификации.
        
        Args:
            employee: Объект сотрудника
        
        Returns:
            True если сотрудник удовлетворяет условию
        """
        pass
    
    def __and__(self, other: 'Specification') -> 'AndSpecification':
        """
        Комбинировать спецификации через AND.
        
        Args:
            other: Другая спецификация
        
        Returns:
            Комбинированная спецификация
        """
        return AndSpecification(self, other)
    
    def __or__(self, other: 'Specification') -> 'OrSpecification':
        """
        Комбинировать спецификации через OR.
        
        Args:
            other: Другая спецификация
        
        Returns:
            Комбинированная спецификация
        """
        return OrSpecification(self, other)
    
    def __invert__(self) -> 'NotSpecification':
        """
        Инвертировать спецификацию (NOT).
        
        Returns:
            Инвертированная спецификация
        """
        return NotSpecification(self)


class AndSpecification(Specification):
    """
    Спецификация AND (логическое И).
    
    Объединяет две спецификации через логическое И.
    """
    
    def __init__(self, spec1: Specification, spec2: Specification):
        """
        Инициализация AND-спецификации.
        
        Args:
            spec1: Первая спецификация
            spec2: Вторая спецификация
        """
        self._spec1 = spec1
        self._spec2 = spec2
    
    def is_satisfied_by(self, employee: AbstractEmployee) -> bool:
        """
        Проверить, удовлетворяет ли сотрудник обеим спецификациям.
        
        Args:
            employee: Объект сотрудника
        
        Returns:
            True если сотрудник удовлетворяет обеим спецификациям
        """
        return self._spec1.is_satisfied_by(employee) and self._spec2.is_satisfied_by(employee)


class OrSpecification(Specification):
    """
    Спецификация OR (логическое ИЛИ).
    
    Объединяет две спецификации через логическое ИЛИ.
    """
    
    def __init__(self, spec1: Specification, spec2: Specification):
        """
        Инициализация OR-спецификации.
        
        Args:
            spec1: Первая спецификация
            spec2: Вторая спецификация
        """
        self._spec1 = spec1
        self._spec2 = spec2
    
    def is_satisfied_by(self, employee: AbstractEmployee) -> bool:
        """
        Проверить, удовлетворяет ли сотрудник хотя бы одной спецификации.
        
        Args:
            employee: Объект сотрудника
        
        Returns:
            True если сотрудник удовлетворяет хотя бы одной спецификации
        """
        return self._spec1.is_satisfied_by(employee) or self._spec2.is_satisfied_by(employee)


class NotSpecification(Specification):
    """
    Спецификация NOT (логическое НЕ).
    
    Инвертирует результат другой спецификации.
    """
    
    def __init__(self, spec: Specification):
        """
        Инициализация NOT-спецификации.
        
        Args:
            spec: Спецификация для инверсии
        """
        self._spec = spec
    
    def is_satisfied_by(self, employee: AbstractEmployee) -> bool:
        """
        Проверить, не удовлетворяет ли сотрудник спецификации.
        
        Args:
            employee: Объект сотрудника
        
        Returns:
            True если сотрудник НЕ удовлетворяет спецификации
        """
        return not self._spec.is_satisfied_by(employee)


class SalarySpecification(Specification):
    """
    Спецификация для фильтрации по зарплате.
    
    Проверяет, находится ли зарплата сотрудника в заданном диапазоне.
    """
    
    def __init__(self, min_salary: float = 0, max_salary: float = float('inf')):
        """
        Инициализация спецификации зарплаты.
        
        Args:
            min_salary: Минимальная зарплата
            max_salary: Максимальная зарплата
        """
        self._min_salary = min_salary
        self._max_salary = max_salary
    
    def is_satisfied_by(self, employee: AbstractEmployee) -> bool:
        """
        Проверить, находится ли зарплата в диапазоне.
        
        Args:
            employee: Объект сотрудника
        
        Returns:
            True если зарплата в диапазоне
        """
        salary = employee.calculate_salary()
        return self._min_salary <= salary <= self._max_salary


class DepartmentSpecification(Specification):
    """
    Спецификация для фильтрации по отделу.
    
    Проверяет, принадлежит ли сотрудник указанному отделу.
    """
    
    def __init__(self, department: str):
        """
        Инициализация спецификации отдела.
        
        Args:
            department: Название отдела
        """
        self._department = department
    
    def is_satisfied_by(self, employee: AbstractEmployee) -> bool:
        """
        Проверить, принадлежит ли сотрудник отделу.
        
        Args:
            employee: Объект сотрудника
        
        Returns:
            True если сотрудник в указанном отделе
        """
        return employee.department == self._department


class SkillSpecification(Specification):
    """
    Спецификация для фильтрации по навыкам.
    
    Проверяет, имеет ли разработчик указанные навыки.
    """
    
    def __init__(self, required_skills: List[str]):
        """
        Инициализация спецификации навыков.
        
        Args:
            required_skills: Список требуемых навыков
        """
        self._required_skills = set(required_skills)
    
    def is_satisfied_by(self, employee: AbstractEmployee) -> bool:
        """
        Проверить, имеет ли сотрудник требуемые навыки.
        
        Args:
            employee: Объект сотрудника
        
        Returns:
            True если сотрудник имеет все требуемые навыки
        """
        if not hasattr(employee, 'tech_stack'):
            return False
        
        employee_skills = set(employee.tech_stack)
        return self._required_skills.issubset(employee_skills)


class EmployeeTypeSpecification(Specification):
    """
    Спецификация для фильтрации по типу сотрудника.
    
    Проверяет, является ли сотрудник указанным типом.
    """
    
    def __init__(self, employee_type: type):
        """
        Инициализация спецификации типа.
        
        Args:
            employee_type: Класс типа сотрудника
        """
        self._employee_type = employee_type
    
    def is_satisfied_by(self, employee: AbstractEmployee) -> bool:
        """
        Проверить, является ли сотрудник указанным типом.
        
        Args:
            employee: Объект сотрудника
        
        Returns:
            True если сотрудник является указанным типом
        """
        return isinstance(employee, self._employee_type)


class SpecificationRepository:
    """
    Репозиторий с поддержкой спецификаций.
    
    Позволяет находить объекты по спецификациям.
    """
    
    def __init__(self, employees: List[AbstractEmployee]):
        """
        Инициализация репозитория.
        
        Args:
            employees: Список сотрудников
        """
        self._employees = employees
    
    def find_by_specification(self, spec: Specification) -> List[AbstractEmployee]:
        """
        Найти сотрудников по спецификации.
        
        Args:
            spec: Спецификация для фильтрации
        
        Returns:
            Список сотрудников, удовлетворяющих спецификации
        """
        return [emp for emp in self._employees if spec.is_satisfied_by(emp)]

