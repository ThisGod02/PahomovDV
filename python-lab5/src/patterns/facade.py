"""Facade паттерн - упрощенный интерфейс для работы с компанией."""

from typing import List, Optional
from src.core.company import Company
from src.core.department import Department
from src.core.project import Project
from src.core.abstract_employee import AbstractEmployee
from src.utils.exceptions import EmployeeNotFoundError, DepartmentNotFoundError


class CompanyFacade:
    """
    Фасад для упрощения работы со сложной системой компании.
    
    Предоставляет упрощенный интерфейс для основных операций:
    найм, увольнение, расчет зарплат, управление проектами.
    """
    
    def __init__(self, company: Company):
        """
        Инициализация фасада.
        
        Args:
            company: Объект компании
        """
        self._company = company
    
    def hire_employee(self, employee: AbstractEmployee, department_name: str) -> bool:
        """
        Нанять сотрудника в отдел.
        
        Args:
            employee: Объект сотрудника
            department_name: Название отдела
        
        Returns:
            True если найм успешен
        
        Raises:
            DepartmentNotFoundError: Если отдел не найден
        """
        department = self._find_department(department_name)
        if department is None:
            raise DepartmentNotFoundError(f"Отдел '{department_name}' не найден")
        
        department.add_employee(employee)
        return True
    
    def fire_employee(self, employee_id: int, department_name: str) -> bool:
        """
        Уволить сотрудника из отдела.
        
        Args:
            employee_id: ID сотрудника
            department_name: Название отдела
        
        Returns:
            True если увольнение успешно
        
        Raises:
            DepartmentNotFoundError: Если отдел не найден
            EmployeeNotFoundError: Если сотрудник не найден
        """
        department = self._find_department(department_name)
        if department is None:
            raise DepartmentNotFoundError(f"Отдел '{department_name}' не найден")
        
        employee = department.find_employee_by_id(employee_id)
        if employee is None:
            raise EmployeeNotFoundError(f"Сотрудник с ID {employee_id} не найден")
        
        department.remove_employee(employee_id)
        return True
    
    def calculate_total_salaries(self) -> float:
        """
        Рассчитать общие затраты на зарплаты.
        
        Returns:
            Сумма всех зарплат в компании
        """
        return self._company.calculate_total_monthly_cost()
    
    def calculate_department_salary(self, department_name: str) -> float:
        """
        Рассчитать зарплаты в отделе.
        
        Args:
            department_name: Название отдела
        
        Returns:
            Сумма зарплат в отделе
        
        Raises:
            DepartmentNotFoundError: Если отдел не найден
        """
        department = self._find_department(department_name)
        if department is None:
            raise DepartmentNotFoundError(f"Отдел '{department_name}' не найден")
        
        return department.calculate_total_salary()
    
    def assign_employee_to_project(self, employee_id: int, project_id: int) -> bool:
        """
        Назначить сотрудника на проект.
        
        Args:
            employee_id: ID сотрудника
            project_id: ID проекта
        
        Returns:
            True если назначение успешно
        """
        return self._company.assign_employee_to_project(employee_id, project_id)
    
    def get_employee_info(self, employee_id: int) -> Optional[str]:
        """
        Получить информацию о сотруднике.
        
        Args:
            employee_id: ID сотрудника
        
        Returns:
            Строка с информацией или None если не найден
        """
        employee = self._company.find_employee_by_id(employee_id)
        if employee is None:
            return None
        return employee.get_info()
    
    def get_company_statistics(self) -> dict:
        """
        Получить статистику по компании.
        
        Returns:
            Словарь со статистикой
        """
        return {
            "total_employees": len(self._company.get_all_employees()),
            "total_departments": len(self._company.get_departments()),
            "total_projects": len(self._company.get_projects()),
            "total_monthly_cost": self._company.calculate_total_monthly_cost(),
            "department_stats": self._company.get_department_stats(),
            "project_analysis": self._company.get_project_budget_analysis()
        }
    
    def get_department_employees(self, department_name: str) -> List[AbstractEmployee]:
        """
        Получить список сотрудников отдела.
        
        Args:
            department_name: Название отдела
        
        Returns:
            Список сотрудников
        
        Raises:
            DepartmentNotFoundError: Если отдел не найден
        """
        department = self._find_department(department_name)
        if department is None:
            raise DepartmentNotFoundError(f"Отдел '{department_name}' не найден")
        
        return department.get_employees()
    
    def get_project_team(self, project_id: int) -> List[AbstractEmployee]:
        """
        Получить команду проекта.
        
        Args:
            project_id: ID проекта
        
        Returns:
            Список сотрудников команды
        
        Raises:
            ValueError: Если проект не найден
        """
        projects = self._company.get_projects()
        project = next((p for p in projects if p.project_id == project_id), None)
        if project is None:
            raise ValueError(f"Проект с ID {project_id} не найден")
        
        return project.get_team()
    
    def _find_department(self, name: str) -> Optional[Department]:
        """
        Найти отдел по названию.
        
        Args:
            name: Название отдела
        
        Returns:
            Объект отдела или None
        """
        departments = self._company.get_departments()
        return next((d for d in departments if d.name == name), None)


