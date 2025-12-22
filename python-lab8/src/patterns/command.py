"""Command паттерн - команды для операций с сотрудниками."""

from abc import ABC, abstractmethod
from typing import Optional
from src.core.company import Company
from src.core.department import Department
from src.core.abstract_employee import AbstractEmployee
from src.utils.exceptions import EmployeeNotFoundError, DepartmentNotFoundError


class Command(ABC):
    """Абстрактная команда."""
    
    @abstractmethod
    def execute(self) -> bool:
        """Выполнить команду."""
        pass
    
    @abstractmethod
    def undo(self) -> bool:
        """Отменить команду."""
        pass


class HireEmployeeCommand(Command):
    """Команда для найма сотрудника."""
    
    def __init__(self, employee: AbstractEmployee, company: Company, department_name: str):
        """Инициализация команды найма."""
        self._employee = employee
        self._company = company
        self._department_name = department_name
        self._executed = False
    
    def execute(self) -> bool:
        """Выполнить найм сотрудника."""
        if self._executed:
            return False
        
        department = self._find_department()
        if department is None:
            raise DepartmentNotFoundError(f"Отдел '{self._department_name}' не найден")
        
        department.add_employee(self._employee)
        self._executed = True
        return True
    
    def undo(self) -> bool:
        """Отменить найм сотрудника."""
        if not self._executed:
            return False
        
        department = self._find_department()
        if department is None:
            return False
        
        try:
            department.remove_employee(self._employee.id)
            self._executed = False
            return True
        except ValueError:
            return False
    
    def _find_department(self) -> Optional[Department]:
        """Найти отдел по названию."""
        departments = self._company.get_departments()
        return next((d for d in departments if d.name == self._department_name), None)


