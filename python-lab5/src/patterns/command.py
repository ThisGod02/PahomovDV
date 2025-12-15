"""Command паттерн - команды для операций с сотрудниками."""

from abc import ABC, abstractmethod
from typing import Optional
from src.core.company import Company
from src.core.department import Department
from src.core.abstract_employee import AbstractEmployee
from src.utils.exceptions import EmployeeNotFoundError, DepartmentNotFoundError


class Command(ABC):
    """
    Абстрактная команда.
    
    Определяет интерфейс для выполнения и отмены операций.
    """
    
    @abstractmethod
    def execute(self) -> bool:
        """
        Выполнить команду.
        
        Returns:
            True если выполнение успешно
        """
        pass
    
    @abstractmethod
    def undo(self) -> bool:
        """
        Отменить команду.
        
        Returns:
            True если отмена успешна
        """
        pass


class HireEmployeeCommand(Command):
    """
    Команда для найма сотрудника.
    
    Реализует операцию найма с возможностью отмены.
    """
    
    def __init__(self, employee: AbstractEmployee, company: Company, department_name: str):
        """
        Инициализация команды найма.
        
        Args:
            employee: Объект сотрудника
            company: Объект компании
            department_name: Название отдела
        """
        self._employee = employee
        self._company = company
        self._department_name = department_name
        self._executed = False
    
    def execute(self) -> bool:
        """
        Выполнить найм сотрудника.
        
        Returns:
            True если найм успешен
        """
        if self._executed:
            return False
        
        department = self._find_department()
        if department is None:
            raise DepartmentNotFoundError(f"Отдел '{self._department_name}' не найден")
        
        department.add_employee(self._employee)
        self._executed = True
        return True
    
    def undo(self) -> bool:
        """
        Отменить найм сотрудника.
        
        Returns:
            True если отмена успешна
        """
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


class FireEmployeeCommand(Command):
    """
    Команда для увольнения сотрудника.
    
    Реализует операцию увольнения с возможностью отмены.
    """
    
    def __init__(self, employee_id: int, company: Company, department_name: str):
        """
        Инициализация команды увольнения.
        
        Args:
            employee_id: ID сотрудника
            company: Объект компании
            department_name: Название отдела
        """
        self._employee_id = employee_id
        self._company = company
        self._department_name = department_name
        self._employee: Optional[AbstractEmployee] = None
        self._executed = False
    
    def execute(self) -> bool:
        """
        Выполнить увольнение сотрудника.
        
        Returns:
            True если увольнение успешно
        """
        if self._executed:
            return False
        
        department = self._find_department()
        if department is None:
            raise DepartmentNotFoundError(f"Отдел '{self._department_name}' не найден")
        
        self._employee = department.find_employee_by_id(self._employee_id)
        if self._employee is None:
            raise EmployeeNotFoundError(f"Сотрудник с ID {self._employee_id} не найден")
        
        department.remove_employee(self._employee_id)
        self._executed = True
        return True
    
    def undo(self) -> bool:
        """
        Отменить увольнение (вернуть сотрудника).
        
        Returns:
            True если отмена успешна
        """
        if not self._executed or self._employee is None:
            return False
        
        department = self._find_department()
        if department is None:
            return False
        
        try:
            department.add_employee(self._employee)
            self._executed = False
            return True
        except ValueError:
            return False
    
    def _find_department(self) -> Optional[Department]:
        """Найти отдел по названию."""
        departments = self._company.get_departments()
        return next((d for d in departments if d.name == self._department_name), None)


class UpdateSalaryCommand(Command):
    """
    Команда для обновления зарплаты сотрудника.
    
    Реализует операцию изменения зарплаты с возможностью отмены.
    """
    
    def __init__(self, employee_id: int, company: Company, new_salary: float):
        """
        Инициализация команды обновления зарплаты.
        
        Args:
            employee_id: ID сотрудника
            company: Объект компании
            new_salary: Новая зарплата
        """
        self._employee_id = employee_id
        self._company = company
        self._new_salary = new_salary
        self._old_salary: Optional[float] = None
        self._employee: Optional[AbstractEmployee] = None
        self._executed = False
    
    def execute(self) -> bool:
        """
        Выполнить обновление зарплаты.
        
        Returns:
            True если обновление успешно
        """
        if self._executed:
            return False
        
        self._employee = self._company.find_employee_by_id(self._employee_id)
        if self._employee is None:
            raise EmployeeNotFoundError(f"Сотрудник с ID {self._employee_id} не найден")
        
        self._old_salary = self._employee.base_salary
        self._employee.base_salary = self._new_salary
        self._executed = True
        return True
    
    def undo(self) -> bool:
        """
        Отменить обновление зарплаты.
        
        Returns:
            True если отмена успешна
        """
        if not self._executed or self._employee is None or self._old_salary is None:
            return False
        
        self._employee.base_salary = self._old_salary
        self._executed = False
        return True


class CommandInvoker:
    """
    Вызывающий объект для команд.
    
    Управляет выполнением и отменой команд, поддерживает историю.
    """
    
    def __init__(self):
        """Инициализация вызывающего объекта."""
        self._history: list[Command] = []
        self._current_index = -1
    
    def execute_command(self, command: Command) -> bool:
        """
        Выполнить команду.
        
        Args:
            command: Команда для выполнения
        
        Returns:
            True если выполнение успешно
        """
        if command.execute():
            # Удаляем команды после текущей позиции (если есть)
            self._history = self._history[:self._current_index + 1]
            self._history.append(command)
            self._current_index = len(self._history) - 1
            return True
        return False
    
    def undo(self) -> bool:
        """
        Отменить последнюю команду.
        
        Returns:
            True если отмена успешна
        """
        if self._current_index < 0:
            return False
        
        command = self._history[self._current_index]
        if command.undo():
            self._current_index -= 1
            return True
        return False
    
    def redo(self) -> bool:
        """
        Повторить последнюю отмененную команду.
        
        Returns:
            True если повтор успешен
        """
        if self._current_index >= len(self._history) - 1:
            return False
        
        self._current_index += 1
        command = self._history[self._current_index]
        return command.execute()
    
    def clear_history(self) -> None:
        """Очистить историю команд."""
        self._history.clear()
        self._current_index = -1


