"""Тесты для Части 4: Тестирование композиции, агрегации и сложных структур."""

import pytest
import os
import tempfile
from src.core.employee import Employee
from src.core.department import Department
from src.core.company import Company
from src.core.project import Project
from src.employees.manager import Manager
from src.employees.developer import Developer
from src.employees.salesperson import Salesperson
from src.utils.exceptions import (
    DuplicateIdError, InvalidStatusError, EmployeeNotFoundError,
    DepartmentNotFoundError, ProjectNotFoundError
)


class TestProject:
    """Тесты для класса Project."""
    
    def test_project_team_management(self):
        """Тест управления командой проекта."""
        # Arrange
        project = Project(1, "AI Platform", "Разработка AI системы", "2024-12-31", "planning")
        dev = Developer(1, "John", "DEV", 5000, ["Python"], "senior")
        
        # Act
        project.add_team_member(dev)
        
        # Assert
        assert len(project.get_team()) == 1
        assert project.get_team_size() == 1
        
        # Act - Удаление
        project.remove_team_member(1)
        
        # Assert
        assert len(project.get_team()) == 0
    
    def test_project_total_salary(self):
        """Тест расчета суммарной зарплаты команды."""
        # Arrange
        project = Project(1, "AI Platform", "Разработка AI системы", "2024-12-31", "planning")
        manager = Manager(1, "Alice", "DEV", 7000, 2000)
        developer = Developer(2, "Bob", "DEV", 5000, ["Python"], "senior")
        
        project.add_team_member(manager)
        project.add_team_member(developer)
        
        # Act
        total = project.calculate_total_salary()
        
        # Assert
        expected = manager.calculate_salary() + developer.calculate_salary()
        assert total == expected
    
    def test_project_invalid_status_raises_error(self):
        """Тест валидации статусов проектов."""
        # Assert
        with pytest.raises(InvalidStatusError):
            Project(1, "Test", "Test", "2024-12-31", "invalid")
        
        # Валидные статусы
        valid_statuses = ["planning", "active", "completed", "cancelled"]
        for status in valid_statuses:
            project = Project(1, "Test", "Test", "2024-12-31", status)
            assert project.status == status


class TestCompany:
    """Тесты для класса Company."""
    
    def test_company_department_management(self):
        """Тест управления отделами компании."""
        # Arrange
        company = Company("TechCorp")
        dept = Department("Development")
        
        # Act
        company.add_department(dept)
        
        # Assert
        assert len(company.get_departments()) == 1
        
        # Act - Удаление
        company.remove_department("Development")
        
        # Assert
        assert len(company.get_departments()) == 0
    
    def test_company_find_employee(self):
        """Тест поиска сотрудников по ID в компании."""
        # Arrange
        company = Company("TechCorp")
        dept = Department("Development")
        emp = Employee(1, "John", "DEV", 5000)
        
        dept.add_employee(emp)
        company.add_department(dept)
        
        # Act
        found = company.find_employee_by_id(1)
        
        # Assert
        assert found is not None
        assert found.name == "John"
    
    def test_company_cannot_delete_department_with_employees(self):
        """Тест ограничения при удалении отдела с сотрудниками."""
        # Arrange
        company = Company("TechCorp")
        dept = Department("Development")
        emp = Employee(1, "John", "DEV", 5000)
        
        dept.add_employee(emp)
        company.add_department(dept)
        
        # Assert
        with pytest.raises(ValueError, match="Нельзя удалить отдел"):
            company.remove_department("Development")
    
    def test_company_duplicate_employee_id_raises_error(self):
        """Тест генерации исключения при дублировании ID сотрудника."""
        # Arrange
        company = Company("TechCorp")
        dept = Department("Development")
        emp1 = Employee(1, "John", "DEV", 5000)
        emp2 = Employee(1, "Jane", "DEV", 6000)  # Тот же ID
        
        dept.add_employee(emp1)
        company.add_department(dept)
        
        # Assert
        with pytest.raises(ValueError, match="уже находится в отделе"):
            dept.add_employee(emp2)
    
    def test_company_get_all_employees(self):
        """Тест получения всех сотрудников компании."""
        # Arrange
        company = Company("TechCorp")
        dept1 = Department("Development")
        dept2 = Department("Sales")
        
        emp1 = Employee(1, "John", "DEV", 5000)
        emp2 = Employee(2, "Jane", "SAL", 6000)
        
        dept1.add_employee(emp1)
        dept2.add_employee(emp2)
        
        company.add_department(dept1)
        company.add_department(dept2)
        
        # Act
        all_employees = company.get_all_employees()
        
        # Assert
        assert len(all_employees) == 2
    
    def test_company_calculate_total_monthly_cost(self):
        """Тест расчета общих месячных затрат."""
        # Arrange
        company = Company("TechCorp")
        dept = Department("Development")
        
        manager = Manager(1, "Alice", "DEV", 7000, 2000)
        developer = Developer(2, "Bob", "DEV", 5000, ["Python"], "senior")
        
        dept.add_employee(manager)
        dept.add_employee(developer)
        company.add_department(dept)
        
        # Act
        total_cost = company.calculate_total_monthly_cost()
        
        # Assert
        expected = manager.calculate_salary() + developer.calculate_salary()
        assert total_cost == expected


class TestCompanySerialization:
    """Тесты сериализации Company."""
    
    def test_company_serialization_roundtrip(self):
        """Тест полного цикла сохранения/загрузки компании."""
        # Arrange
        company = Company("TechCorp")
        dept = Department("Development")
        emp = Employee(1, "John", "DEV", 5000)
        
        dept.add_employee(emp)
        company.add_department(dept)
        
        # Act - Сохранение и загрузка
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            filename = f.name
        
        try:
            company.save_to_json(filename)
            loaded_company = Company.load_from_json(filename)
            
            # Assert
            assert loaded_company.name == "TechCorp"
            assert len(loaded_company.get_departments()) == 1
            assert len(loaded_company.get_all_employees()) == 1
        finally:
            if os.path.exists(filename):
                os.remove(filename)


class TestCompanyBusinessMethods:
    """Тесты бизнес-методов Company."""
    
    def test_company_department_statistics(self):
        """Тест статистики по отделам."""
        # Arrange
        company = Company("TechCorp")
        dept = Department("Development")
        
        manager = Manager(1, "Alice", "DEV", 7000, 2000)
        developer1 = Developer(2, "Bob", "DEV", 5000, ["Python"], "senior")
        developer2 = Developer(3, "Charlie", "DEV", 5000, ["Java"], "middle")
        
        dept.add_employee(manager)
        dept.add_employee(developer1)
        dept.add_employee(developer2)
        company.add_department(dept)
        
        # Act
        stats = company.get_department_stats()
        
        # Assert
        assert "Development" in stats
        assert stats["Development"]["employee_count"] == 3
        assert stats["Development"]["total_salary"] > 0
        assert stats["Development"]["employee_types"]["Manager"] == 1
        assert stats["Development"]["employee_types"]["Developer"] == 2
    
    def test_company_find_overloaded_employees(self):
        """Тест поиска перегруженных сотрудников."""
        # Arrange
        company = Company("TechCorp")
        dept = Department("Development")
        developer = Developer(1, "Bob", "DEV", 5000, ["Python"], "senior")
        
        dept.add_employee(developer)
        company.add_department(dept)
        
        project1 = Project(1, "Project 1", "Description 1", "2024-12-31", "active")
        project2 = Project(2, "Project 2", "Description 2", "2024-12-31", "active")
        project3 = Project(3, "Project 3", "Description 3", "2024-12-31", "active")
        
        company.add_project(project1)
        company.add_project(project2)
        company.add_project(project3)
        
        # Назначаем сотрудника на несколько проектов
        company.assign_employee_to_project(1, 1)
        company.assign_employee_to_project(1, 2)
        company.assign_employee_to_project(1, 3)
        
        # Act
        overloaded = company.find_overloaded_employees()
        
        # Assert
        assert len(overloaded) == 1
        assert overloaded[0].id == 1


class TestComplexCompanyStructure:
    """Интеграционные тесты сложных сценариев."""
    
    def test_complex_company_structure(self):
        """Комплексный тест структуры компании."""
        # Arrange
        company = Company("TechInnovations")
        
        # Создание отделов
        dev_department = Department("Development")
        sales_department = Department("Sales")
        
        # Создание сотрудников
        manager = Manager(1, "Alice Johnson", "DEV", 7000, 2000)
        developer = Developer(2, "Bob Smith", "DEV", 5000, ["Python", "SQL"], "senior")
        salesperson = Salesperson(3, "Charlie Brown", "SAL", 4000, 0.15, 50000)
        
        # Добавление в отделы
        dev_department.add_employee(manager)
        dev_department.add_employee(developer)
        sales_department.add_employee(salesperson)
        
        # Добавление отделов в компанию
        company.add_department(dev_department)
        company.add_department(sales_department)
        
        # Act & Assert
        assert company.calculate_total_monthly_cost() > 0
        assert len(company.get_all_employees()) == 3
        
        # Проверка поиска сотрудников
        found_employee = company.find_employee_by_id(2)
        assert found_employee is not None
        assert found_employee.name == "Bob Smith"
    
    def test_company_project_management(self):
        """Тест управления проектами в компании."""
        # Arrange
        company = Company("TechCorp")
        dept = Department("Development")
        developer = Developer(1, "Bob", "DEV", 5000, ["Python"], "senior")
        
        dept.add_employee(developer)
        company.add_department(dept)
        
        project = Project(1, "AI Project", "AI Development", "2024-12-31", "planning")
        company.add_project(project)
        
        # Act
        company.assign_employee_to_project(1, 1)
        
        # Assert
        assert project.get_team_size() == 1
        assert project.calculate_total_salary() == developer.calculate_salary()
    
    def test_company_duplicate_project_id(self):
        """Тест дублирования ID проекта."""
        # Arrange
        company = Company("TechCorp")
        project1 = Project(1, "Project 1", "Description 1", "2024-12-31", "planning")
        project2 = Project(1, "Project 2", "Description 2", "2024-12-31", "planning")  # Тот же ID
        
        company.add_project(project1)
        
        # Assert
        with pytest.raises(DuplicateIdError):
            company.add_project(project2)
    
    def test_company_cannot_delete_project_with_team(self):
        """Тест ограничения при удалении проекта с командой."""
        # Arrange
        company = Company("TechCorp")
        dept = Department("Development")
        developer = Developer(1, "Bob", "DEV", 5000, ["Python"], "senior")
        
        dept.add_employee(developer)
        company.add_department(dept)
        
        project = Project(1, "AI Project", "AI Development", "2024-12-31", "planning")
        company.add_project(project)
        company.assign_employee_to_project(1, 1)
        
        # Assert
        with pytest.raises(ValueError, match="Нельзя удалить проект"):
            company.remove_project(1)


