"""Класс Company (Компания) с агрегацией отделов и проектов."""

import json
import csv
from typing import List, Optional, Dict
from src.core.department import Department
from src.core.project import Project
from src.core.abstract_employee import AbstractEmployee
from src.utils.exceptions import (
    EmployeeNotFoundError, DepartmentNotFoundError, ProjectNotFoundError,
    DuplicateIdError
)


class Company:
    """
    Класс для представления компании.
    
    Использует агрегацию для управления отделами и проектами.
    """
    
    def __init__(self, name: str):
        """
        Инициализация компании.
        
        Args:
            name: Название компании
        """
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"Название компании не должно быть пустой строкой, получено: '{name}'")
        self.__name = name
        self.__departments: List[Department] = []  # Агрегация
        self.__projects: List[Project] = []  # Агрегация
    
    @property
    def name(self) -> str:
        """Получить название компании."""
        return self.__name
    
    def add_department(self, department: Department) -> None:
        """
        Добавить отдел в компанию.
        
        Args:
            department: Объект отдела
        
        Raises:
            ValueError: Если отдел уже добавлен
        """
        if not isinstance(department, Department):
            raise TypeError(f"Отдел должен быть экземпляром Department, получено: {type(department)}")
        if department in self.__departments:
            raise ValueError(f"Отдел '{department.name}' уже добавлен в компанию")
        self.__departments.append(department)
    
    def remove_department(self, department_name: str) -> None:
        """
        Удалить отдел из компании.
        
        Args:
            department_name: Название отдела
        
        Raises:
            DepartmentNotFoundError: Если отдел не найден
            ValueError: Если в отделе есть сотрудники
        """
        department = self._find_department_by_name(department_name)
        if department is None:
            raise DepartmentNotFoundError(f"Отдел '{department_name}' не найден")
        if len(department) > 0:
            raise ValueError(f"Нельзя удалить отдел '{department_name}', в нем есть сотрудники")
        self.__departments.remove(department)
    
    def get_departments(self) -> List[Department]:
        """
        Получить список всех отделов.
        
        Returns:
            Список отделов
        """
        return self.__departments.copy()
    
    def add_project(self, project: Project) -> None:
        """
        Добавить проект в компанию.
        
        Args:
            project: Объект проекта
        
        Raises:
            ValueError: Если проект уже добавлен или ID дублируется
        """
        if not isinstance(project, Project):
            raise TypeError(f"Проект должен быть экземпляром Project, получено: {type(project)}")
        if project in self.__projects:
            raise ValueError(f"Проект '{project.name}' уже добавлен в компанию")
        if self._find_project_by_id(project.project_id) is not None:
            raise DuplicateIdError(f"Проект с ID {project.project_id} уже существует")
        self.__projects.append(project)
    
    def remove_project(self, project_id: int) -> None:
        """
        Удалить проект из компании.
        
        Args:
            project_id: ID проекта
        
        Raises:
            ProjectNotFoundError: Если проект не найден
            ValueError: Если над проектом работает команда
        """
        project = self._find_project_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError(f"Проект с ID {project_id} не найден")
        if project.get_team_size() > 0:
            raise ValueError(f"Нельзя удалить проект '{project.name}', над ним работает команда")
        self.__projects.remove(project)
    
    def get_projects(self) -> List[Project]:
        """
        Получить список всех проектов.
        
        Returns:
            Список проектов
        """
        return self.__projects.copy()
    
    def get_all_employees(self) -> List[AbstractEmployee]:
        """
        Получить всех сотрудников компании.
        
        Returns:
            Список всех сотрудников из всех отделов
        """
        employees = []
        for dept in self.__departments:
            employees.extend(dept.get_employees())
        return employees
    
    def find_employee_by_id(self, employee_id: int) -> Optional[AbstractEmployee]:
        """
        Найти сотрудника по ID во всей компании.
        
        Args:
            employee_id: ID сотрудника
        
        Returns:
            Объект сотрудника или None
        """
        for dept in self.__departments:
            employee = dept.find_employee_by_id(employee_id)
            if employee is not None:
                return employee
        return None
    
    def calculate_total_monthly_cost(self) -> float:
        """
        Рассчитать общие месячные затраты на зарплаты.
        
        Returns:
            Сумма зарплат всех сотрудников компании
        """
        return sum(dept.calculate_total_salary() for dept in self.__departments)
    
    def get_projects_by_status(self, status: str) -> List[Project]:
        """
        Фильтровать проекты по статусу.
        
        Args:
            status: Статус для фильтрации
        
        Returns:
            Список проектов с указанным статусом
        """
        return [proj for proj in self.__projects if proj.status == status]
    
    def _find_department_by_name(self, name: str) -> Optional[Department]:
        """Найти отдел по названию."""
        for dept in self.__departments:
            if dept.name == name:
                return dept
        return None
    
    def _find_project_by_id(self, project_id: int) -> Optional[Project]:
        """Найти проект по ID."""
        for proj in self.__projects:
            if proj.project_id == project_id:
                return proj
        return None
    
    def transfer_employee(self, employee_id: int, from_dept: str, to_dept: str) -> bool:
        """
        Перенести сотрудника между отделами.
        
        Args:
            employee_id: ID сотрудника
            from_dept: Название исходного отдела
            to_dept: Название целевого отдела
        
        Returns:
            True если перенос успешен
        
        Raises:
            DepartmentNotFoundError: Если отдел не найден
            EmployeeNotFoundError: Если сотрудник не найден
        """
        source_dept = self._find_department_by_name(from_dept)
        target_dept = self._find_department_by_name(to_dept)
        
        if source_dept is None:
            raise DepartmentNotFoundError(f"Исходный отдел '{from_dept}' не найден")
        if target_dept is None:
            raise DepartmentNotFoundError(f"Целевой отдел '{to_dept}' не найден")
        
        employee = source_dept.find_employee_by_id(employee_id)
        if employee is None:
            raise EmployeeNotFoundError(f"Сотрудник с ID {employee_id} не найден в отделе '{from_dept}'")
        
        source_dept.remove_employee(employee_id)
        target_dept.add_employee(employee)
        return True
    
    def get_department_stats(self) -> Dict:
        """
        Получить статистику по отделам.
        
        Returns:
            Словарь со статистикой
        """
        stats = {}
        for dept in self.__departments:
            stats[dept.name] = {
                "employee_count": len(dept),
                "total_salary": dept.calculate_total_salary(),
                "employee_types": dept.get_employee_count()
            }
        return stats
    
    def get_project_budget_analysis(self) -> Dict:
        """
        Получить анализ бюджетов проектов.
        
        Returns:
            Словарь с анализом бюджетов
        """
        analysis = {
            "total_projects": len(self.__projects),
            "by_status": {},
            "total_budget": 0.0
        }
        
        for proj in self.__projects:
            status = proj.status
            budget = proj.calculate_total_salary()
            
            if status not in analysis["by_status"]:
                analysis["by_status"][status] = {"count": 0, "total_budget": 0.0}
            
            analysis["by_status"][status]["count"] += 1
            analysis["by_status"][status]["total_budget"] += budget
            analysis["total_budget"] += budget
        
        return analysis
    
    def find_overloaded_employees(self) -> List[AbstractEmployee]:
        """
        Найти перегруженных сотрудников (участвующих в нескольких проектах).
        
        Returns:
            Список перегруженных сотрудников
        """
        employee_project_count = {}
        for proj in self.__projects:
            for emp in proj.get_team():
                emp_id = emp.id
                employee_project_count[emp_id] = employee_project_count.get(emp_id, 0) + 1
        
        overloaded = []
        for emp_id, count in employee_project_count.items():
            if count > 1:
                employee = self.find_employee_by_id(emp_id)
                if employee is not None:
                    overloaded.append(employee)
        
        return overloaded
    
    def assign_employee_to_project(self, employee_id: int, project_id: int) -> bool:
        """
        Назначить сотрудника на проект.
        
        Args:
            employee_id: ID сотрудника
            project_id: ID проекта
        
        Returns:
            True если назначение успешно
        
        Raises:
            EmployeeNotFoundError: Если сотрудник не найден
            ProjectNotFoundError: Если проект не найден
        """
        employee = self.find_employee_by_id(employee_id)
        if employee is None:
            raise EmployeeNotFoundError(f"Сотрудник с ID {employee_id} не найден")
        
        project = self._find_project_by_id(project_id)
        if project is None:
            raise ProjectNotFoundError(f"Проект с ID {project_id} не найден")
        
        project.add_team_member(employee)
        return True
    
    def check_employee_availability(self, employee_id: int) -> bool:
        """
        Проверить доступность сотрудника (не перегружен ли).
        
        Args:
            employee_id: ID сотрудника
        
        Returns:
            True если сотрудник доступен (участвует менее чем в 2 проектах)
        """
        project_count = sum(1 for proj in self.__projects 
                           if proj.find_team_member(employee_id) is not None)
        return project_count < 2
    
    def save_to_json(self, filename: str) -> None:
        """
        Сохранить всю компанию в JSON файл.
        
        Args:
            filename: Имя файла для сохранения
        """
        data = {
            "name": self.__name,
            "departments": [self._department_to_dict(dept) for dept in self.__departments],
            "projects": [proj.to_dict() for proj in self.__projects]
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    @classmethod
    def load_from_json(cls, filename: str) -> 'Company':
        """
        Загрузить компанию из JSON файла.
        
        Args:
            filename: Имя файла для загрузки
        
        Returns:
            Объект Company
        """
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        company = cls(data["name"])
        
        # Загружаем отделы
        for dept_data in data.get("departments", []):
            dept = Department.load_from_file_dict(dept_data)
            company.add_department(dept)
        
        # Загружаем проекты
        for proj_data in data.get("projects", []):
            project = Project.from_dict(proj_data)
            company.add_project(project)
            # Восстанавливаем команды проектов
            for emp_data in proj_data.get("team", []):
                emp_id = emp_data.get("id")
                if emp_id:
                    try:
                        company.assign_employee_to_project(emp_id, project.project_id)
                    except (EmployeeNotFoundError, ProjectNotFoundError):
                        pass  # Пропускаем если не удалось восстановить связь
        
        return company
    
    @staticmethod
    def _department_to_dict(department: Department) -> dict:
        """Преобразовать отдел в словарь."""
        from src.core.department import Department as DeptClass
        return {
            "name": department.name,
            "employees": [DeptClass._employee_to_dict(emp) for emp in department.get_employees()]
        }
    
    def export_employees_csv(self, filename: str) -> None:
        """
        Экспортировать отчет по сотрудникам в CSV.
        
        Args:
            filename: Имя файла для экспорта
        """
        employees = self.get_all_employees()
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Имя", "Отдел", "Тип", "Базовая зарплата", "Итоговая зарплата"])
            for emp in employees:
                writer.writerow([
                    emp.id,
                    emp.name,
                    emp.department,
                    emp.__class__.__name__,
                    emp.base_salary,
                    emp.calculate_salary()
                ])
    
    def export_projects_csv(self, filename: str) -> None:
        """
        Экспортировать отчет по проектам в CSV.
        
        Args:
            filename: Имя файла для экспорта
        """
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["ID проекта", "Название", "Статус", "Срок", "Размер команды", "Бюджет команды"])
            for proj in self.__projects:
                writer.writerow([
                    proj.project_id,
                    proj.name,
                    proj.status,
                    proj.deadline.strftime("%Y-%m-%d"),
                    proj.get_team_size(),
                    proj.calculate_total_salary()
                ])
    
    def __str__(self) -> str:
        """Строковое представление компании."""
        return (f"Компания '{self.__name}' "
                f"(отделов: {len(self.__departments)}, проектов: {len(self.__projects)})")

