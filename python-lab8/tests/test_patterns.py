"""Тесты для Части 5: Тестирование паттернов проектирования."""

import pytest
from unittest.mock import Mock
from src.core.employee import Employee
from src.employees.manager import Manager
from src.employees.developer import Developer
from src.database.connection import DatabaseConnection
from src.patterns.singleton import DatabaseConnection as SingletonDB
from src.patterns.builder import EmployeeBuilder
from src.patterns.adapter import ExternalSalaryService, SalaryCalculatorAdapter
from src.patterns.decorator import BonusDecorator
from src.patterns.observer import ObservableEmployee, Observer
from src.patterns.strategy import PerformanceBonusStrategy, SeniorityBonusStrategy, BonusContext
from src.patterns.command import HireEmployeeCommand
from src.patterns.repository import EmployeeRepository
from src.patterns.specification import SalarySpecification, DepartmentSpecification, SpecificationRepository
from src.core.company import Company
from src.core.department import Department


class TestSingletonPattern:
    """Тесты паттерна Singleton."""
    
    def test_singleton_pattern(self):
        """Тест паттерна Singleton для DatabaseConnection."""
        # Arrange & Act
        db1 = DatabaseConnection.get_instance()
        db2 = DatabaseConnection.get_instance()
        
        # Assert
        assert db1 is db2
        assert id(db1) == id(db2)
    
    def test_singleton_reset_for_testing(self):
        """Тест сброса экземпляра для тестирования."""
        # Arrange
        db1 = DatabaseConnection.get_instance()
        db1.reset_instance()
        
        # Act
        db2 = DatabaseConnection.get_instance()
        db3 = DatabaseConnection.get_instance()
        
        # Assert
        assert db2 is db3
        assert db1 is not db2  # Новый экземпляр после reset


class TestFactoryMethodPattern:
    """Тесты паттерна Factory Method."""
    
    def test_employee_factory_method(self):
        """Тест фабрики для создания сотрудников."""
        # Arrange
        from src.factories.employee_factory import EmployeeFactoryMethod
        
        # Act & Assert
        employee = EmployeeFactoryMethod.create_employee(
            "developer",
            id=1,
            name="John",
            department="DEV",
            base_salary=5000,
            tech_stack=["Python"],
            seniority_level="middle"
        )
        
        assert isinstance(employee, Developer)
        assert employee.calculate_salary() == 7500  # 5000 * 1.5


class TestBuilderPattern:
    """Тесты паттерна Builder."""
    
    def test_employee_builder_pattern(self):
        """Тест паттерна Builder для создания сотрудников."""
        # Arrange & Act
        developer = (EmployeeBuilder()
                    .set_id(101)
                    .set_name("John Doe")
                    .set_department("DEV")
                    .set_base_salary(5000)
                    .set_type("developer")
                    .set_skills(["Python", "Java"])
                    .set_seniority("senior")
                    .build())
        
        # Assert
        assert developer.id == 101
        assert developer.name == "John Doe"
        assert isinstance(developer, Developer)
        assert developer.calculate_salary() == 10000  # 5000 * 2.0
    
    def test_employee_builder_manager(self):
        """Тест Builder для создания менеджера."""
        # Arrange & Act
        manager = (EmployeeBuilder()
                  .set_id(2)
                  .set_name("Alice")
                  .set_department("MAN")
                  .set_base_salary(7000)
                  .set_type("manager")
                  .set_bonus(2000)
                  .build())
        
        # Assert
        assert isinstance(manager, Manager)
        assert manager.calculate_salary() == 9000


class TestAdapterPattern:
    """Тесты паттерна Adapter."""
    
    def test_salary_calculator_adapter(self):
        """Тест адаптера для внешней системы расчета зарплат."""
        # Arrange
        external_service = ExternalSalaryService()
        adapter = SalaryCalculatorAdapter(external_service)
        employee = Employee(1, "John", "IT", 5000)
        
        # Act
        result = adapter.calculate_salary(employee)
        
        # Assert
        assert result == 5000  # Базовая зарплата через внешний сервис
    
    def test_adapter_with_manager(self):
        """Тест адаптера с менеджером."""
        # Arrange
        external_service = ExternalSalaryService()
        adapter = SalaryCalculatorAdapter(external_service)
        manager = Manager(1, "John", "IT", 5000, 1000)
        
        # Act
        result = adapter.calculate_salary(manager)
        
        # Assert
        assert result == 6000  # 5000 + 1000


class TestDecoratorPattern:
    """Тесты паттерна Decorator."""
    
    def test_bonus_decorator(self):
        """Тест декоратора бонуса."""
        # Arrange
        employee = Employee(1, "John", "IT", 5000)
        decorated_employee = BonusDecorator(employee, 1000)
        
        # Act
        salary = decorated_employee.calculate_salary()
        
        # Assert
        assert salary == 6000
        assert "Бонус: 1000" in decorated_employee.get_info()


class TestObserverPattern:
    """Тесты паттерна Observer."""
    
    def test_observer_pattern(self):
        """Тест паттерна Observer с моками."""
        # Arrange
        employee = Employee(1, "John", "IT", 5000)
        observable_emp = ObservableEmployee(employee)
        observer = Mock(spec=Observer)
        
        observable_emp.attach(observer)
        
        # Act
        observable_emp.set_base_salary(6000)
        
        # Assert
        observer.update.assert_called_once()
        call_args = observer.update.call_args
        assert call_args[0][0] == "salary_changed"
        assert call_args[0][1]["employee_id"] == 1
        assert call_args[0][1]["old_salary"] == 5000
        assert call_args[0][1]["new_salary"] == 6000


class TestStrategyPattern:
    """Тесты паттерна Strategy."""
    
    def test_bonus_strategy_pattern(self):
        """Тест паттерна Strategy для расчета бонусов."""
        # Arrange
        employee = Employee(1, "John", "IT", 5000)
        performance_strategy = PerformanceBonusStrategy(performance_multiplier=0.1)
        seniority_strategy = SeniorityBonusStrategy()
        
        context = BonusContext(performance_strategy)
        
        # Act & Assert
        bonus1 = context.calculate_bonus(employee)
        assert bonus1 == 500  # 5000 * 0.1
        
        # Смена стратегии
        context.set_strategy(seniority_strategy)
        developer = Developer(1, "John", "IT", 5000, ["Python"], "senior")
        bonus2 = context.calculate_bonus(developer)
        assert bonus2 == 15000  # Бонус для senior


class TestCommandPattern:
    """Тесты паттерна Command."""
    
    def test_command_pattern_with_undo(self):
        """Тест паттерна Command с отменой."""
        # Arrange
        employee = Employee(1, "John", "IT", 5000)
        company = Company("TestCorp")
        dept = Department("IT")
        company.add_department(dept)
        
        hire_command = HireEmployeeCommand(employee, company, "IT")
        
        # Act - Выполнение
        hire_command.execute()
        assert employee in company.get_all_employees()
        
        # Act - Отмена
        hire_command.undo()
        assert employee not in company.get_all_employees()


class TestRepositoryPattern:
    """Тесты паттерна Repository."""
    
    def test_employee_repository(self):
        """Тест репозитория сотрудников."""
        # Arrange
        repo = EmployeeRepository()
        employee = Employee(1, "John", "IT", 5000)
        
        # Act
        repo.add(employee)
        found = repo.find_by_id(1)
        
        # Assert
        assert found is not None
        assert found.name == "John"
    
    def test_repository_error_handling(self):
        """Тест обработки ошибок в репозитории."""
        # Arrange
        repo = EmployeeRepository()
        
        # Act & Assert
        with pytest.raises(ValueError):
            repo.find_by_id(999)  # Несуществующий ID (через get_by_id)
        
        # Проверка через find_by_id (возвращает None)
        assert repo.find_by_id(999) is None


class TestSpecificationPattern:
    """Тесты паттерна Specification."""
    
    def test_specification_pattern(self):
        """Тест паттерна Specification."""
        # Arrange
        employees = [
            Employee(1, "John", "IT", 5000),
            Employee(2, "Jane", "HR", 6000),
            Employee(3, "Bob", "IT", 7000)
        ]
        
        repo = SpecificationRepository(employees)
        
        # Act
        high_salary_spec = SalarySpecification(min_salary=5500)
        it_spec = DepartmentSpecification("IT")
        combined_spec = high_salary_spec & it_spec
        
        result = repo.find_by_specification(combined_spec)
        
        # Assert
        assert len(result) == 1
        assert result[0].name == "Bob"
    
    def test_specification_or(self):
        """Тест спецификации OR."""
        # Arrange
        employees = [
            Employee(1, "John", "IT", 5000),
            Employee(2, "Jane", "HR", 6000),
            Employee(3, "Bob", "IT", 7000)
        ]
        
        repo = SpecificationRepository(employees)
        
        # Act
        it_spec = DepartmentSpecification("IT")
        hr_spec = DepartmentSpecification("HR")
        combined_spec = it_spec | hr_spec
        
        result = repo.find_by_specification(combined_spec)
        
        # Assert
        assert len(result) == 3  # Все сотрудники из IT или HR


class TestComplexPatternInteraction:
    """Интеграционные тесты взаимодействия паттернов."""
    
    def test_complex_pattern_interaction(self):
        """Тест взаимодействия нескольких паттернов."""
        # 1. Singleton для БД
        db = DatabaseConnection.get_instance()
        db2 = DatabaseConnection.get_instance()
        assert db is db2
        
        # 2. Factory для создания сотрудников
        from src.factories.employee_factory import EmployeeFactoryMethod
        developer = EmployeeFactoryMethod.create_employee(
            "developer",
            id=1, name="John", department="DEV", base_salary=5000,
            tech_stack=["Python"], seniority_level="senior"
        )
        assert isinstance(developer, Developer)
        
        # 3. Builder для сложной конфигурации
        manager = (EmployeeBuilder()
                  .set_id(2)
                  .set_name("Alice")
                  .set_department("MAN")
                  .set_base_salary(7000)
                  .set_type("manager")
                  .set_bonus(2000)
                  .build())
        assert isinstance(manager, Manager)
        
        # 4. Repository для сохранения
        repo = EmployeeRepository()
        repo.add(developer)
        repo.add(manager)
        
        # 5. Specification для поиска
        spec = SalarySpecification(min_salary=6000)
        high_earners = [emp for emp in repo.get_all() if spec.is_satisfied_by(emp)]
        
        # Assert
        assert len(high_earners) == 1
        assert high_earners[0].name == "Alice"
    
    def test_notification_system_with_mocks(self):
        """Тест системы уведомлений с моками."""
        # Arrange
        employee = Employee(1, "John", "IT", 5000)
        observable_emp = ObservableEmployee(employee)
        mock_notifier = Mock()
        observable_emp.attach(mock_notifier)
        
        # Act
        observable_emp.set_base_salary(6000)
        
        # Assert
        mock_notifier.update.assert_called_once()


