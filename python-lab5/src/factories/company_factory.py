"""Abstract Factory паттерн - фабрики для создания компаний."""

from abc import ABC, abstractmethod
from typing import List
from src.core.company import Company
from src.core.department import Department
from src.core.project import Project
from src.core.abstract_employee import AbstractEmployee
from src.factories.employee_factory import (
    EmployeeFactory, ManagerFactory, DeveloperFactory, SalespersonFactory
)


class CompanyFactory(ABC):
    """
    Абстрактная фабрика для создания компаний (Abstract Factory паттерн).
    
    Каждая конкретная фабрика создает согласованный набор объектов:
    специфических сотрудников, отделов, проектов.
    """
    
    @abstractmethod
    def create_company(self, name: str) -> Company:
        """
        Создать компанию.
        
        Args:
            name: Название компании
        
        Returns:
            Объект Company
        """
        pass
    
    @abstractmethod
    def create_department(self, name: str) -> Department:
        """
        Создать отдел.
        
        Args:
            name: Название отдела
        
        Returns:
            Объект Department
        """
        pass
    
    @abstractmethod
    def create_project(self, project_id: int, name: str, description: str, 
                      deadline: str) -> Project:
        """
        Создать проект.
        
        Args:
            project_id: ID проекта
            name: Название проекта
            description: Описание проекта
            deadline: Срок выполнения
        
        Returns:
            Объект Project
        """
        pass
    
    @abstractmethod
    def create_employee_factory(self) -> EmployeeFactory:
        """
        Создать фабрику сотрудников.
        
        Returns:
            Фабрика сотрудников
        """
        pass


class TechCompanyFactory(CompanyFactory):
    """
    Фабрика для создания IT-компаний.
    
    Создает компании с техническими отделами и проектами.
    """
    
    def create_company(self, name: str) -> Company:
        """Создать IT-компанию."""
        company = Company(name)
        
        # Создаем технические отделы
        dev_dept = self.create_department("Development")
        qa_dept = self.create_department("QA")
        company.add_department(dev_dept)
        company.add_department(qa_dept)
        
        # Создаем типичные IT-проекты
        web_project = self.create_project(
            project_id=1,
            name="Web Platform",
            description="Разработка веб-платформы",
            deadline="2024-12-31"
        )
        api_project = self.create_project(
            project_id=2,
            name="API Service",
            description="Разработка API сервиса",
            deadline="2024-11-30"
        )
        company.add_project(web_project)
        company.add_project(api_project)
        
        return company
    
    def create_department(self, name: str) -> Department:
        """Создать технический отдел."""
        return Department(name)
    
    def create_project(self, project_id: int, name: str, description: str, 
                      deadline: str) -> Project:
        """Создать технический проект."""
        return Project(project_id, name, description, deadline, status="planning")
    
    def create_employee_factory(self) -> EmployeeFactory:
        """Создать фабрику разработчиков."""
        return DeveloperFactory()


class SalesCompanyFactory(CompanyFactory):
    """
    Фабрика для создания торговых компаний.
    
    Создает компании с отделами продаж и торговыми проектами.
    """
    
    def create_company(self, name: str) -> Company:
        """Создать торговую компанию."""
        company = Company(name)
        
        # Создаем отделы продаж
        sales_dept = self.create_department("Sales")
        marketing_dept = self.create_department("Marketing")
        company.add_department(sales_dept)
        company.add_department(marketing_dept)
        
        # Создаем торговые проекты
        campaign_project = self.create_project(
            project_id=1,
            name="Marketing Campaign",
            description="Маркетинговая кампания",
            deadline="2024-10-31"
        )
        expansion_project = self.create_project(
            project_id=2,
            name="Market Expansion",
            description="Расширение рынка",
            deadline="2024-12-31"
        )
        company.add_project(campaign_project)
        company.add_project(expansion_project)
        
        return company
    
    def create_department(self, name: str) -> Department:
        """Создать отдел продаж."""
        return Department(name)
    
    def create_project(self, project_id: int, name: str, description: str, 
                      deadline: str) -> Project:
        """Создать торговый проект."""
        return Project(project_id, name, description, deadline, status="planning")
    
    def create_employee_factory(self) -> EmployeeFactory:
        """Создать фабрику продавцов."""
        return SalespersonFactory()

