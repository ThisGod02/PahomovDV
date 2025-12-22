"""Repository паттерн - репозитории для работы с данными."""

from abc import ABC, abstractmethod
from typing import List, Optional
from src.core.abstract_employee import AbstractEmployee


class IEmployeeRepository(ABC):
    """Интерфейс репозитория сотрудников."""
    
    @abstractmethod
    def add(self, employee: AbstractEmployee) -> None:
        """Добавить сотрудника."""
        pass
    
    @abstractmethod
    def get_by_id(self, employee_id: int) -> Optional[AbstractEmployee]:
        """Получить сотрудника по ID."""
        pass
    
    @abstractmethod
    def get_all(self) -> List[AbstractEmployee]:
        """Получить всех сотрудников."""
        pass
    
    @abstractmethod
    def update(self, employee: AbstractEmployee) -> None:
        """Обновить сотрудника."""
        pass
    
    @abstractmethod
    def delete(self, employee_id: int) -> None:
        """Удалить сотрудника."""
        pass


class EmployeeRepository(IEmployeeRepository):
    """Репозиторий сотрудников."""
    
    def __init__(self):
        """Инициализация репозитория."""
        self._employees: dict[int, AbstractEmployee] = {}
    
    def add(self, employee: AbstractEmployee) -> None:
        """Добавить сотрудника."""
        if employee.id in self._employees:
            raise ValueError(f"Сотрудник с ID {employee.id} уже существует")
        self._employees[employee.id] = employee
    
    def get_by_id(self, employee_id: int) -> Optional[AbstractEmployee]:
        """Получить сотрудника по ID."""
        return self._employees.get(employee_id)
    
    def get_all(self) -> List[AbstractEmployee]:
        """Получить всех сотрудников."""
        return list(self._employees.values())
    
    def update(self, employee: AbstractEmployee) -> None:
        """Обновить сотрудника."""
        if employee.id not in self._employees:
            raise ValueError(f"Сотрудник с ID {employee.id} не найден")
        self._employees[employee.id] = employee
    
    def delete(self, employee_id: int) -> None:
        """Удалить сотрудника."""
        if employee_id not in self._employees:
            raise ValueError(f"Сотрудник с ID {employee_id} не найден")
        del self._employees[employee_id]
    
    def find_by_id(self, employee_id: int) -> Optional[AbstractEmployee]:
        """Найти сотрудника по ID (алиас для get_by_id)."""
        return self.get_by_id(employee_id)


