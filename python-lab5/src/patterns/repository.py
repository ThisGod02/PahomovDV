"""Repository паттерн - репозитории для работы с данными."""

from abc import ABC, abstractmethod
from typing import List, Optional
from src.core.abstract_employee import AbstractEmployee
from src.core.department import Department
from src.core.project import Project


class IEmployeeRepository(ABC):
    """
    Интерфейс репозитория сотрудников.
    
    Определяет операции CRUD для сотрудников.
    """
    
    @abstractmethod
    def add(self, employee: AbstractEmployee) -> None:
        """
        Добавить сотрудника.
        
        Args:
            employee: Объект сотрудника
        """
        pass
    
    @abstractmethod
    def get_by_id(self, employee_id: int) -> Optional[AbstractEmployee]:
        """
        Получить сотрудника по ID.
        
        Args:
            employee_id: ID сотрудника
        
        Returns:
            Объект сотрудника или None
        """
        pass
    
    @abstractmethod
    def get_all(self) -> List[AbstractEmployee]:
        """
        Получить всех сотрудников.
        
        Returns:
            Список всех сотрудников
        """
        pass
    
    @abstractmethod
    def update(self, employee: AbstractEmployee) -> None:
        """
        Обновить сотрудника.
        
        Args:
            employee: Объект сотрудника
        """
        pass
    
    @abstractmethod
    def delete(self, employee_id: int) -> None:
        """
        Удалить сотрудника.
        
        Args:
            employee_id: ID сотрудника
        """
        pass


class EmployeeRepository(IEmployeeRepository):
    """
    Репозиторий сотрудников.
    
    Реализует хранение и управление сотрудниками в памяти.
    """
    
    def __init__(self):
        """Инициализация репозитория."""
        self._employees: dict[int, AbstractEmployee] = {}
    
    def add(self, employee: AbstractEmployee) -> None:
        """
        Добавить сотрудника.
        
        Args:
            employee: Объект сотрудника
        
        Raises:
            ValueError: Если сотрудник с таким ID уже существует
        """
        if employee.id in self._employees:
            raise ValueError(f"Сотрудник с ID {employee.id} уже существует")
        self._employees[employee.id] = employee
    
    def get_by_id(self, employee_id: int) -> Optional[AbstractEmployee]:
        """
        Получить сотрудника по ID.
        
        Args:
            employee_id: ID сотрудника
        
        Returns:
            Объект сотрудника или None
        """
        return self._employees.get(employee_id)
    
    def get_all(self) -> List[AbstractEmployee]:
        """
        Получить всех сотрудников.
        
        Returns:
            Список всех сотрудников
        """
        return list(self._employees.values())
    
    def update(self, employee: AbstractEmployee) -> None:
        """
        Обновить сотрудника.
        
        Args:
            employee: Объект сотрудника
        
        Raises:
            ValueError: Если сотрудник не найден
        """
        if employee.id not in self._employees:
            raise ValueError(f"Сотрудник с ID {employee.id} не найден")
        self._employees[employee.id] = employee
    
    def delete(self, employee_id: int) -> None:
        """
        Удалить сотрудника.
        
        Args:
            employee_id: ID сотрудника
        
        Raises:
            ValueError: Если сотрудник не найден
        """
        if employee_id not in self._employees:
            raise ValueError(f"Сотрудник с ID {employee_id} не найден")
        del self._employees[employee_id]


class IDepartmentRepository(ABC):
    """
    Интерфейс репозитория отделов.
    """
    
    @abstractmethod
    def add(self, department: Department) -> None:
        """Добавить отдел."""
        pass
    
    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Department]:
        """Получить отдел по названию."""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Department]:
        """Получить все отделы."""
        pass
    
    @abstractmethod
    def delete(self, name: str) -> None:
        """Удалить отдел."""
        pass


class DepartmentRepository(IDepartmentRepository):
    """
    Репозиторий отделов.
    
    Реализует хранение и управление отделами в памяти.
    """
    
    def __init__(self):
        """Инициализация репозитория."""
        self._departments: dict[str, Department] = {}
    
    def add(self, department: Department) -> None:
        """
        Добавить отдел.
        
        Args:
            department: Объект отдела
        
        Raises:
            ValueError: Если отдел с таким названием уже существует
        """
        if department.name in self._departments:
            raise ValueError(f"Отдел '{department.name}' уже существует")
        self._departments[department.name] = department
    
    def get_by_name(self, name: str) -> Optional[Department]:
        """
        Получить отдел по названию.
        
        Args:
            name: Название отдела
        
        Returns:
            Объект отдела или None
        """
        return self._departments.get(name)
    
    def get_all(self) -> List[Department]:
        """
        Получить все отделы.
        
        Returns:
            Список всех отделов
        """
        return list(self._departments.values())
    
    def delete(self, name: str) -> None:
        """
        Удалить отдел.
        
        Args:
            name: Название отдела
        
        Raises:
            ValueError: Если отдел не найден
        """
        if name not in self._departments:
            raise ValueError(f"Отдел '{name}' не найден")
        del self._departments[name]


class IProjectRepository(ABC):
    """
    Интерфейс репозитория проектов.
    """
    
    @abstractmethod
    def add(self, project: Project) -> None:
        """Добавить проект."""
        pass
    
    @abstractmethod
    def get_by_id(self, project_id: int) -> Optional[Project]:
        """Получить проект по ID."""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Project]:
        """Получить все проекты."""
        pass
    
    @abstractmethod
    def delete(self, project_id: int) -> None:
        """Удалить проект."""
        pass


class ProjectRepository(IProjectRepository):
    """
    Репозиторий проектов.
    
    Реализует хранение и управление проектами в памяти.
    """
    
    def __init__(self):
        """Инициализация репозитория."""
        self._projects: dict[int, Project] = {}
    
    def add(self, project: Project) -> None:
        """
        Добавить проект.
        
        Args:
            project: Объект проекта
        
        Raises:
            ValueError: Если проект с таким ID уже существует
        """
        if project.project_id in self._projects:
            raise ValueError(f"Проект с ID {project.project_id} уже существует")
        self._projects[project.project_id] = project
    
    def get_by_id(self, project_id: int) -> Optional[Project]:
        """
        Получить проект по ID.
        
        Args:
            project_id: ID проекта
        
        Returns:
            Объект проекта или None
        """
        return self._projects.get(project_id)
    
    def get_all(self) -> List[Project]:
        """
        Получить все проекты.
        
        Returns:
            Список всех проектов
        """
        return list(self._projects.values())
    
    def delete(self, project_id: int) -> None:
        """
        Удалить проект.
        
        Args:
            project_id: ID проекта
        
        Raises:
            ValueError: Если проект не найден
        """
        if project_id not in self._projects:
            raise ValueError(f"Проект с ID {project_id} не найден")
        del self._projects[project_id]





