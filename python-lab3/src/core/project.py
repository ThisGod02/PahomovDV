"""Класс Project (Проект) с композицией сотрудников."""

from datetime import datetime
from typing import List, Optional
from src.core.abstract_employee import AbstractEmployee
from src.utils.exceptions import InvalidStatusError


class Project:
    """
    Класс для представления проекта компании.
    
    Использует композицию для управления командой проекта.
    """
    
    VALID_STATUSES = ["planning", "active", "completed", "cancelled"]
    
    def __init__(self, project_id: int, name: str, description: str, 
                 deadline: str, status: str = "planning"):
        """
        Инициализация проекта.
        
        Args:
            project_id: Уникальный идентификатор проекта
            name: Название проекта
            description: Описание проекта
            deadline: Срок выполнения (строка в формате "YYYY-MM-DD")
            status: Статус проекта
        
        Raises:
            ValueError: При невалидных данных
            InvalidStatusError: При невалидном статусе
        """
        self._validate_project_id(project_id)
        self._validate_name(name)
        self._validate_deadline(deadline)
        self._validate_status(status)
        
        self.__project_id = project_id
        self.__name = name
        self.__description = description
        self.__deadline = datetime.strptime(deadline, "%Y-%m-%d")
        self.__status = status
        self.__team: List[AbstractEmployee] = []  # Композиция
    
    def _validate_project_id(self, value: int) -> None:
        """Валидация ID проекта."""
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"ID проекта должен быть положительным целым числом, получено: {value}")
    
    def _validate_name(self, value: str) -> None:
        """Валидация названия проекта."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Название проекта не должно быть пустой строкой, получено: '{value}'")
    
    def _validate_deadline(self, value: str) -> None:
        """Валидация срока выполнения."""
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Срок выполнения должен быть в формате YYYY-MM-DD, получено: '{value}'")
    
    def _validate_status(self, value: str) -> None:
        """Валидация статуса проекта."""
        if value not in self.VALID_STATUSES:
            raise InvalidStatusError(
                f"Статус должен быть одним из: {self.VALID_STATUSES}, получено: '{value}'"
            )
    
    @property
    def project_id(self) -> int:
        """Получить ID проекта."""
        return self.__project_id
    
    @property
    def name(self) -> str:
        """Получить название проекта."""
        return self.__name
    
    @property
    def description(self) -> str:
        """Получить описание проекта."""
        return self.__description
    
    @property
    def deadline(self) -> datetime:
        """Получить срок выполнения проекта."""
        return self.__deadline
    
    @property
    def status(self) -> str:
        """Получить статус проекта."""
        return self.__status
    
    def add_team_member(self, employee: AbstractEmployee) -> None:
        """
        Добавить сотрудника в проект.
        
        Args:
            employee: Объект сотрудника
        
        Raises:
            ValueError: Если сотрудник уже в команде
        """
        if not isinstance(employee, AbstractEmployee):
            raise TypeError(f"Сотрудник должен быть экземпляром AbstractEmployee, получено: {type(employee)}")
        if employee in self.__team:
            raise ValueError(f"Сотрудник с ID {employee.id} уже в команде проекта")
        self.__team.append(employee)
    
    def remove_team_member(self, employee_id: int) -> None:
        """
        Удалить сотрудника по ID.
        
        Args:
            employee_id: ID сотрудника
        
        Raises:
            ValueError: Если сотрудник не найден
        """
        employee = self.find_team_member(employee_id)
        if employee is None:
            raise ValueError(f"Сотрудник с ID {employee_id} не найден в команде проекта")
        self.__team.remove(employee)
    
    def get_team(self) -> List[AbstractEmployee]:
        """
        Получить список команды проекта.
        
        Returns:
            Список сотрудников команды
        """
        return self.__team.copy()
    
    def get_team_size(self) -> int:
        """
        Получить размер команды.
        
        Returns:
            Количество сотрудников в команде
        """
        return len(self.__team)
    
    def calculate_total_salary(self) -> float:
        """
        Рассчитать суммарную зарплату команды.
        
        Returns:
            Сумма зарплат всех членов команды
        """
        return sum(emp.calculate_salary() for emp in self.__team)
    
    def get_project_info(self) -> str:
        """
        Получить полную информацию о проекте.
        
        Returns:
            Строка с полной информацией
        """
        return (f"Проект [ID: {self.__project_id}, название: {self.__name}, "
                f"описание: {self.__description}, срок: {self.__deadline.strftime('%Y-%m-%d')}, "
                f"статус: {self.__status}, размер команды: {len(self.__team)}, "
                f"бюджет команды: {self.calculate_total_salary()}]")
    
    def change_status(self, new_status: str) -> None:
        """
        Изменить статус проекта.
        
        Args:
            new_status: Новый статус
        
        Raises:
            InvalidStatusError: Если статус невалиден
        """
        self._validate_status(new_status)
        self.__status = new_status
    
    def find_team_member(self, employee_id: int) -> Optional[AbstractEmployee]:
        """
        Найти члена команды по ID.
        
        Args:
            employee_id: ID сотрудника
        
        Returns:
            Объект сотрудника или None
        """
        for emp in self.__team:
            if hasattr(emp, 'id') and emp.id == employee_id:
                return emp
        return None
    
    def to_dict(self) -> dict:
        """
        Сериализация проекта в словарь.
        
        Returns:
            Словарь с данными проекта
        """
        return {
            "project_id": self.__project_id,
            "name": self.__name,
            "description": self.__description,
            "deadline": self.__deadline.strftime("%Y-%m-%d"),
            "status": self.__status,
            "team": [self._employee_to_dict(emp) for emp in self.__team]
        }
    
    @staticmethod
    def _employee_to_dict(employee: AbstractEmployee) -> dict:
        """Преобразовать сотрудника в словарь."""
        if hasattr(employee, 'to_dict'):
            return employee.to_dict()
        return {"id": getattr(employee, 'id', None)}
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Project':
        """
        Создать проект из словаря.
        
        Args:
            data: Словарь с данными проекта
        
        Returns:
            Объект Project
        """
        project = cls(
            project_id=data["project_id"],
            name=data["name"],
            description=data["description"],
            deadline=data["deadline"],
            status=data.get("status", "planning")
        )
        # Команда будет добавлена позже через add_team_member
        return project
    
    def __str__(self) -> str:
        """Строковое представление проекта."""
        return f"Проект '{self.__name}' (ID: {self.__project_id}, статус: {self.__status})"


