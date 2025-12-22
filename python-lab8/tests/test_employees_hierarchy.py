"""Тесты для Части 2: Тестирование наследования и абстрактных классов."""

import pytest
from abc import ABC
from src.core.abstract_employee import AbstractEmployee
from src.core.employee import Employee
from src.employees.manager import Manager
from src.employees.developer import Developer
from src.employees.salesperson import Salesperson
from src.factories.employee_factory import EmployeeFactoryMethod


class TestAbstractEmployee:
    """Тесты для абстрактного класса AbstractEmployee."""
    
    def test_cannot_create_abstract_employee(self):
        """Тест невозможности создания экземпляра AbstractEmployee."""
        # Assert
        with pytest.raises(TypeError):
            AbstractEmployee()


class TestManager:
    """Тесты для класса Manager."""
    
    def test_manager_salary_calculation(self):
        """Тест расчета зарплаты менеджера с учетом бонуса."""
        # Arrange
        manager = Manager(1, "John", "Management", 5000, 1000)
        
        # Act
        salary = manager.calculate_salary()
        
        # Assert
        assert salary == 6000  # 5000 + 1000
    
    def test_manager_get_info_includes_bonus(self):
        """Тест метода get_info - должен включать информацию о бонусе."""
        # Arrange
        manager = Manager(1, "John", "Management", 5000, 1000)
        
        # Act
        info = manager.get_info()
        
        # Assert
        assert "бонус: 1000" in info
        assert "итоговая зарплата: 6000" in info
    
    def test_manager_bonus_setter_validation(self):
        """Тест сеттера бонуса с валидацией."""
        # Arrange
        manager = Manager(1, "John", "Management", 5000, 1000)
        
        # Act & Assert
        manager.bonus = 2000
        assert manager.bonus == 2000
        
        with pytest.raises(ValueError):
            manager.bonus = -500


class TestDeveloper:
    """Тесты для класса Developer."""
    
    @pytest.mark.parametrize("level,expected_salary", [
        ("junior", 5000),    # 5000 * 1.0
        ("middle", 7500),    # 5000 * 1.5
        ("senior", 10000)    # 5000 * 2.0
    ])
    def test_developer_salary_by_level(self, level, expected_salary):
        """Параметризованный тест расчета зарплаты по уровням."""
        # Arrange
        dev = Developer(1, "Alice", "DEV", 5000, ["Python"], level)
        
        # Act & Assert
        assert dev.calculate_salary() == expected_salary
    
    def test_developer_add_skill(self):
        """Тест метода add_skill."""
        # Arrange
        dev = Developer(1, "Alice", "DEV", 5000, ["Python"], "middle")
        
        # Act
        dev.add_skill("Java")
        
        # Assert
        assert "Java" in dev.tech_stack
        assert len(dev.tech_stack) == 2
    
    def test_developer_add_duplicate_skill(self):
        """Тест добавления дублирующегося навыка."""
        # Arrange
        dev = Developer(1, "Alice", "DEV", 5000, ["Python"], "middle")
        
        # Act
        dev.add_skill("Python")  # Дубликат
        
        # Assert
        assert dev.tech_stack.count("Python") == 1
    
    def test_developer_get_info_includes_tech_stack(self):
        """Тест метода get_info - должен включать стек технологий."""
        # Arrange
        dev = Developer(1, "Alice", "DEV", 5000, ["Python", "Java"], "senior")
        
        # Act
        info = dev.get_info()
        
        # Assert
        assert "Python" in info
        assert "Java" in info
        assert "senior" in info
    
    def test_developer_invalid_seniority_level(self):
        """Тест валидации уровня seniority."""
        # Assert
        with pytest.raises(ValueError):
            Developer(1, "Alice", "DEV", 5000, ["Python"], "invalid_level")
    
    def test_developer_skills_iteration(self):
        """Тест итерации по стеку технологий."""
        # Arrange
        dev = Developer(1, "John", "DEV", 5000, ["Python", "Java", "SQL"], "senior")
        
        # Act
        skills = []
        for skill in dev:
            skills.append(skill)
        
        # Assert
        assert skills == ["Python", "Java", "SQL"]


class TestSalesperson:
    """Тесты для класса Salesperson."""
    
    def test_salesperson_salary_calculation(self):
        """Тест расчета зарплаты продавца с учетом комиссии."""
        # Arrange
        salesperson = Salesperson(3, "Charlie", "SAL", 4000, 0.15, 50000)
        
        # Act
        salary = salesperson.calculate_salary()
        
        # Assert
        assert salary == 11500  # 4000 + (50000 * 0.15)
    
    def test_salesperson_update_sales(self):
        """Тест метода update_sales."""
        # Arrange
        salesperson = Salesperson(3, "Charlie", "SAL", 4000, 0.15, 50000)
        
        # Act
        salesperson.update_sales(10000)
        
        # Assert
        assert salesperson.sales_volume == 60000
        assert salesperson.calculate_salary() == 13000  # 4000 + (60000 * 0.15)
    
    def test_salesperson_get_info_includes_commission(self):
        """Тест метода get_info - должен включать информацию о комиссии."""
        # Arrange
        salesperson = Salesperson(3, "Charlie", "SAL", 4000, 0.15, 50000)
        
        # Act
        info = salesperson.get_info()
        
        # Assert
        assert "процент комиссии: 0.15" in info
        assert "объем продаж: 50000" in info
    
    def test_salesperson_invalid_commission_rate(self):
        """Тест валидации процента комиссии."""
        # Assert
        with pytest.raises(ValueError):
            Salesperson(3, "Charlie", "SAL", 4000, 1.5, 50000)  # > 1
        
        with pytest.raises(ValueError):
            Salesperson(3, "Charlie", "SAL", 4000, -0.1, 50000)  # < 0


class TestEmployeeFactory:
    """Тесты для EmployeeFactory."""
    
    def test_employee_factory_method(self):
        """Тест фабрики для создания сотрудников разных типов."""
        # Arrange
        factory = EmployeeFactoryMethod
        
        # Act & Assert
        employee = factory.create_employee("employee", id=1, name="John", 
                                          department="IT", base_salary=5000)
        assert isinstance(employee, Employee)
        
        manager = factory.create_employee("manager", id=2, name="Alice",
                                         department="MAN", base_salary=7000, bonus=2000)
        assert isinstance(manager, Manager)
        assert manager.calculate_salary() == 9000
        
        developer = factory.create_employee("developer", id=3, name="Bob",
                                           department="DEV", base_salary=5000,
                                           tech_stack=["Python"], seniority_level="senior")
        assert isinstance(developer, Developer)
        assert developer.calculate_salary() == 10000
    
    def test_employee_factory_invalid_type(self):
        """Тест фабрики с неверным типом сотрудника."""
        # Assert
        with pytest.raises(ValueError):
            EmployeeFactoryMethod.create_employee("invalid_type", id=1, name="Test",
                                                  department="IT", base_salary=5000)


class TestPolymorphicBehavior:
    """Тесты полиморфного поведения."""
    
    def test_polymorphic_behavior(self):
        """Тест полиморфного поведения - коллекция разных типов сотрудников."""
        # Arrange
        employees = [
            Employee(1, "Alice", "IT", 5000),
            Manager(2, "Bob", "MAN", 7000, 2000),
            Developer(3, "Charlie", "DEV", 5000, ["Python"], "senior"),
            Salesperson(4, "David", "SAL", 4000, 0.15, 50000)
        ]
        
        # Act
        total_salary = sum(emp.calculate_salary() for emp in employees)
        
        # Assert
        expected = 5000 + 9000 + 10000 + 11500  # 35500
        assert total_salary == expected
        
        # Проверка, что для каждого типа вызывается правильная реализация
        assert employees[0].calculate_salary() == 5000
        assert employees[1].calculate_salary() == 9000
        assert employees[2].calculate_salary() == 10000
        assert employees[3].calculate_salary() == 11500


