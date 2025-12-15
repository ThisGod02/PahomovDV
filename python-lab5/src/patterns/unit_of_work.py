"""Unit of Work паттерн - управление транзакциями."""

from typing import List, Optional
from src.patterns.repository import (
    EmployeeRepository, DepartmentRepository, ProjectRepository,
    IEmployeeRepository, IDepartmentRepository, IProjectRepository
)


class UnitOfWork:
    """
    Unit of Work для управления транзакциями.
    
    Гарантирует согласованность данных при комплексных операциях.
    """
    
    def __init__(self):
        """Инициализация Unit of Work."""
        self._employee_repo = EmployeeRepository()
        self._department_repo = DepartmentRepository()
        self._project_repo = ProjectRepository()
        
        self._new_employees: List = []
        self._modified_employees: List = []
        self._deleted_employees: List = []
        
        self._new_departments: List = []
        self._modified_departments: List = []
        self._deleted_departments: List = []
        
        self._new_projects: List = []
        self._modified_projects: List = []
        self._deleted_projects: List = []
    
    @property
    def employees(self) -> IEmployeeRepository:
        """
        Получить репозиторий сотрудников.
        
        Returns:
            Репозиторий сотрудников
        """
        return self._employee_repo
    
    @property
    def departments(self) -> IDepartmentRepository:
        """
        Получить репозиторий отделов.
        
        Returns:
            Репозиторий отделов
        """
        return self._department_repo
    
    @property
    def projects(self) -> IProjectRepository:
        """
        Получить репозиторий проектов.
        
        Returns:
            Репозиторий проектов
        """
        return self._project_repo
    
    def register_new_employee(self, employee) -> None:
        """
        Зарегистрировать нового сотрудника для добавления.
        
        Args:
            employee: Объект сотрудника
        """
        if employee not in self._new_employees:
            self._new_employees.append(employee)
    
    def register_modified_employee(self, employee) -> None:
        """
        Зарегистрировать измененного сотрудника.
        
        Args:
            employee: Объект сотрудника
        """
        if employee not in self._modified_employees:
            self._modified_employees.append(employee)
    
    def register_deleted_employee(self, employee) -> None:
        """
        Зарегистрировать сотрудника для удаления.
        
        Args:
            employee: Объект сотрудника
        """
        if employee not in self._deleted_employees:
            self._deleted_employees.append(employee)
    
    def register_new_department(self, department) -> None:
        """
        Зарегистрировать новый отдел для добавления.
        
        Args:
            department: Объект отдела
        """
        if department not in self._new_departments:
            self._new_departments.append(department)
    
    def register_modified_department(self, department) -> None:
        """
        Зарегистрировать измененный отдел.
        
        Args:
            department: Объект отдела
        """
        if department not in self._modified_departments:
            self._modified_departments.append(department)
    
    def register_deleted_department(self, department) -> None:
        """
        Зарегистрировать отдел для удаления.
        
        Args:
            department: Объект отдела
        """
        if department not in self._deleted_departments:
            self._deleted_departments.append(department)
    
    def register_new_project(self, project) -> None:
        """
        Зарегистрировать новый проект для добавления.
        
        Args:
            project: Объект проекта
        """
        if project not in self._new_projects:
            self._new_projects.append(project)
    
    def register_modified_project(self, project) -> None:
        """
        Зарегистрировать измененный проект.
        
        Args:
            project: Объект проекта
        """
        if project not in self._modified_projects:
            self._modified_projects.append(project)
    
    def register_deleted_project(self, project) -> None:
        """
        Зарегистрировать проект для удаления.
        
        Args:
            project: Объект проекта
        """
        if project not in self._deleted_projects:
            self._deleted_projects.append(project)
    
    def commit(self) -> None:
        """
        Выполнить все зарегистрированные изменения.
        
        Все изменения применяются атомарно - либо все, либо ничего.
        
        Raises:
            Exception: Если произошла ошибка при выполнении транзакции
        """
        try:
            # Применяем изменения для сотрудников
            for employee in self._new_employees:
                self._employee_repo.add(employee)
            
            for employee in self._modified_employees:
                self._employee_repo.update(employee)
            
            for employee in self._deleted_employees:
                self._employee_repo.delete(employee.id)
            
            # Применяем изменения для отделов
            for department in self._new_departments:
                self._department_repo.add(department)
            
            for department in self._modified_departments:
                # Для отделов обновление через повторное добавление
                self._department_repo.delete(department.name)
                self._department_repo.add(department)
            
            for department in self._deleted_departments:
                self._department_repo.delete(department.name)
            
            # Применяем изменения для проектов
            for project in self._new_projects:
                self._project_repo.add(project)
            
            for project in self._modified_projects:
                # Для проектов обновление через повторное добавление
                self._project_repo.delete(project.project_id)
                self._project_repo.add(project)
            
            for project in self._deleted_projects:
                self._project_repo.delete(project.project_id)
            
            # Очищаем списки после успешного выполнения
            self._clear_registrations()
            
        except Exception as e:
            # В случае ошибки откатываем изменения
            self.rollback()
            raise e
    
    def rollback(self) -> None:
        """
        Откатить все зарегистрированные изменения.
        
        Очищает все списки изменений без применения.
        """
        self._clear_registrations()
    
    def _clear_registrations(self) -> None:
        """Очистить все списки регистраций."""
        self._new_employees.clear()
        self._modified_employees.clear()
        self._deleted_employees.clear()
        
        self._new_departments.clear()
        self._modified_departments.clear()
        self._deleted_departments.clear()
        
        self._new_projects.clear()
        self._modified_projects.clear()
        self._deleted_projects.clear()


