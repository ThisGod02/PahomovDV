"""Specification паттерн - спецификации для фильтрации сотрудников."""

from abc import ABC, abstractmethod
from typing import List
from src.core.abstract_employee import AbstractEmployee


class Specification(ABC):
    """Абстрактная спецификация."""
    
    @abstractmethod
    def is_satisfied_by(self, employee: AbstractEmployee) -> bool:
        """Проверить, удовлетворяет ли сотрудник спецификации."""
        pass
    
    def __and__(self, other: 'Specification') -> 'AndSpecification':
        """Комбинировать спецификации через AND."""
        return AndSpecification(self, other)
    
    def __or__(self, other: 'Specification') -> 'OrSpecification':
        """Комбинировать спецификации через OR."""
        return OrSpecification(self, other)
    
    def __invert__(self) -> 'NotSpecification':
        """Инвертировать спецификацию (NOT)."""
        return NotSpecification(self)


class AndSpecification(Specification):
    """Спецификация AND (логическое И)."""
    
    def __init__(self, spec1: Specification, spec2: Specification):
        """Инициализация AND-спецификации."""
        self._spec1 = spec1
        self._spec2 = spec2
    
    def is_satisfied_by(self, employee: AbstractEmployee) -> bool:
        """Проверить, удовлетворяет ли сотрудник обеим спецификациям."""
        return self._spec1.is_satisfied_by(employee) and self._spec2.is_satisfied_by(employee)


class OrSpecification(Specification):
    """Спецификация OR (логическое ИЛИ)."""
    
    def __init__(self, spec1: Specification, spec2: Specification):
        """Инициализация OR-спецификации."""
        self._spec1 = spec1
        self._spec2 = spec2
    
    def is_satisfied_by(self, employee: AbstractEmployee) -> bool:
        """Проверить, удовлетворяет ли сотрудник хотя бы одной спецификации."""
        return self._spec1.is_satisfied_by(employee) or self._spec2.is_satisfied_by(employee)


class NotSpecification(Specification):
    """Спецификация NOT (логическое НЕ)."""
    
    def __init__(self, spec: Specification):
        """Инициализация NOT-спецификации."""
        self._spec = spec
    
    def is_satisfied_by(self, employee: AbstractEmployee) -> bool:
        """Проверить, не удовлетворяет ли сотрудник спецификации."""
        return not self._spec.is_satisfied_by(employee)


class SalarySpecification(Specification):
    """Спецификация для фильтрации по зарплате."""
    
    def __init__(self, min_salary: float = 0, max_salary: float = float('inf')):
        """Инициализация спецификации зарплаты."""
        self._min_salary = min_salary
        self._max_salary = max_salary
    
    def is_satisfied_by(self, employee: AbstractEmployee) -> bool:
        """Проверить, находится ли зарплата в диапазоне."""
        salary = employee.calculate_salary()
        return self._min_salary <= salary <= self._max_salary


class DepartmentSpecification(Specification):
    """Спецификация для фильтрации по отделу."""
    
    def __init__(self, department: str):
        """Инициализация спецификации отдела."""
        self._department = department
    
    def is_satisfied_by(self, employee: AbstractEmployee) -> bool:
        """Проверить, принадлежит ли сотрудник отделу."""
        return employee.department == self._department


class SpecificationRepository:
    """Репозиторий с поддержкой спецификаций."""
    
    def __init__(self, employees: List[AbstractEmployee]):
        """Инициализация репозитория."""
        self._employees = employees
    
    def find_by_specification(self, spec: Specification) -> List[AbstractEmployee]:
        """Найти сотрудников по спецификации."""
        return [emp for emp in self._employees if spec.is_satisfied_by(emp)]


