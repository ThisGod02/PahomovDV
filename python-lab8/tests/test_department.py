"""Тесты для Части 3: Тестирование полиморфизма и магических методов."""

import pytest
from src.core.employee import Employee
from src.core.department import Department
from src.employees.manager import Manager
from src.employees.developer import Developer
from src.employees.salesperson import Salesperson


class TestDepartment:
    """Тесты для класса Department."""
    
    def test_department_add_employee(self):
        """Тест добавления сотрудника в отдел."""
        # Arrange
        dept = Department("IT")
        emp = Employee(1, "John", "IT", 5000)
        
        # Act
        dept.add_employee(emp)
        
        # Assert
        assert len(dept) == 1
        assert emp in dept
    
    def test_department_remove_employee(self):
        """Тест удаления сотрудника из отдела."""
        # Arrange
        dept = Department("IT")
        emp = Employee(1, "John", "IT", 5000)
        dept.add_employee(emp)
        
        # Act
        dept.remove_employee(1)
        
        # Assert
        assert len(dept) == 0
    
    def test_department_get_employees(self):
        """Тест получения списка сотрудников."""
        # Arrange
        dept = Department("IT")
        emp1 = Employee(1, "John", "IT", 5000)
        emp2 = Employee(2, "Jane", "IT", 6000)
        dept.add_employee(emp1)
        dept.add_employee(emp2)
        
        # Act
        employees = dept.get_employees()
        
        # Assert
        assert len(employees) == 2
        assert employees[0].id == 1
        assert employees[1].id == 2
    
    def test_department_calculate_total_salary_polymorphic(self):
        """Тест полиморфного расчета общей зарплаты."""
        # Arrange
        dept = Department("Development")
        manager = Manager(1, "Alice", "DEV", 7000, 2000)
        developer = Developer(2, "Bob", "DEV", 5000, ["Python"], "senior")
        salesperson = Salesperson(3, "Charlie", "SAL", 4000, 0.15, 50000)
        
        dept.add_employee(manager)
        dept.add_employee(developer)
        dept.add_employee(salesperson)
        
        # Act
        total = dept.calculate_total_salary()
        
        # Assert
        expected = manager.calculate_salary() + developer.calculate_salary() + salesperson.calculate_salary()
        assert total == expected
    
    def test_department_get_employee_count(self):
        """Тест статистики по типам сотрудников."""
        # Arrange
        dept = Department("Development")
        manager = Manager(1, "Alice", "DEV", 7000, 2000)
        developer1 = Developer(2, "Bob", "DEV", 5000, ["Python"], "senior")
        developer2 = Developer(3, "Charlie", "DEV", 5000, ["Java"], "middle")
        
        dept.add_employee(manager)
        dept.add_employee(developer1)
        dept.add_employee(developer2)
        
        # Act
        counts = dept.get_employee_count()
        
        # Assert
        assert counts["Manager"] == 1
        assert counts["Developer"] == 2
    
    def test_department_find_employee_by_id(self):
        """Тест поиска сотрудника по ID."""
        # Arrange
        dept = Department("IT")
        emp = Employee(1, "John", "IT", 5000)
        dept.add_employee(emp)
        
        # Act
        found = dept.find_employee_by_id(1)
        
        # Assert
        assert found is not None
        assert found.id == 1
        assert found.name == "John"
    
    def test_department_find_employee_by_id_not_found(self):
        """Тест поиска несуществующего сотрудника."""
        # Arrange
        dept = Department("IT")
        
        # Act
        found = dept.find_employee_by_id(999)
        
        # Assert
        assert found is None


class TestEmployeeMagicMethods:
    """Тесты магических методов Employee."""
    
    def test_employee_equality(self):
        """Тест оператора равенства (__eq__)."""
        # Arrange
        emp1 = Employee(1, "John", "IT", 5000)
        emp2 = Employee(1, "Jane", "HR", 4000)  # Тот же ID
        emp3 = Employee(2, "Bob", "IT", 5000)    # Другой ID
        
        # Assert
        assert emp1 == emp2  # одинаковый ID
        assert emp1 != emp3  # разный ID
    
    def test_employee_salary_comparison(self):
        """Тест операторов сравнения по зарплате."""
        # Arrange
        emp1 = Employee(1, "John", "IT", 5000)
        emp2 = Employee(2, "Jane", "HR", 6000)
        
        # Assert
        assert emp1 < emp2
        assert emp2 > emp1
        assert emp1 <= emp2
        assert emp2 >= emp1
    
    def test_employee_addition(self):
        """Тест сложения зарплат (__add__)."""
        # Arrange
        emp1 = Employee(1, "John", "IT", 5000)
        emp2 = Employee(2, "Jane", "HR", 6000)
        
        # Act
        result = emp1 + emp2
        
        # Assert
        assert result == 11000
    
    def test_employee_radd(self):
        """Тест правого сложения для sum()."""
        # Arrange
        employees = [
            Employee(1, "John", "IT", 5000),
            Employee(2, "Jane", "HR", 6000),
            Employee(3, "Bob", "IT", 7000)
        ]
        
        # Act
        total = sum(employees)
        
        # Assert
        assert total == 18000


class TestDepartmentMagicMethods:
    """Тесты магических методов Department."""
    
    def test_department_magic_methods(self):
        """Тест магических методов Department."""
        # Arrange
        dept = Department("IT")
        emp = Employee(1, "John", "IT", 5000)
        
        dept.add_employee(emp)
        
        # Assert
        assert len(dept) == 1
        assert dept[0] == emp
        assert emp in dept
    
    def test_department_iteration(self):
        """Тест итерации по отделу."""
        # Arrange
        dept = Department("IT")
        employees = [Employee(i, f"Emp{i}", "IT", 5000) for i in range(1, 4)]
        
        for emp in employees:
            dept.add_employee(emp)
        
        # Act
        count = 0
        for employee in dept:
            count += 1
        
        # Assert
        assert count == 3
    
    def test_department_getitem_index_error(self):
        """Тест __getitem__ с неверным индексом."""
        # Arrange
        dept = Department("IT")
        
        # Assert
        with pytest.raises(IndexError):
            _ = dept[0]


class TestDeveloperSkillsIteration:
    """Тесты итерации по навыкам разработчика."""
    
    def test_developer_skills_iteration(self):
        """Тест итерации по стеку технологий разработчика."""
        # Arrange
        dev = Developer(1, "John", "DEV", 5000, ["Python", "Java", "SQL"], "senior")
        
        # Act
        skills = []
        for skill in dev:
            skills.append(skill)
        
        # Assert
        assert skills == ["Python", "Java", "SQL"]


class TestEmployeeSerialization:
    """Тесты сериализации сотрудников."""
    
    def test_employee_serialization(self):
        """Тест сериализации и десериализации Employee."""
        # Arrange
        emp = Employee(1, "John", "IT", 5000)
        
        # Act - Сериализация
        data = emp.to_dict()
        
        # Act - Десериализация
        new_emp = Employee.from_dict(data)
        
        # Assert
        assert new_emp.id == emp.id
        assert new_emp.name == emp.name
        assert new_emp.department == emp.department
        assert new_emp.base_salary == emp.base_salary
    
    def test_manager_serialization(self):
        """Тест сериализации Manager."""
        # Arrange
        manager = Manager(1, "John", "MAN", 7000, 2000)
        
        # Act
        data = manager.to_dict()
        new_manager = Manager.from_dict(data)
        
        # Assert
        assert new_manager.bonus == 2000
        assert new_manager.calculate_salary() == 9000
    
    def test_developer_serialization(self):
        """Тест сериализации Developer."""
        # Arrange
        dev = Developer(1, "John", "DEV", 5000, ["Python", "Java"], "senior")
        
        # Act
        data = dev.to_dict()
        new_dev = Developer.from_dict(data)
        
        # Assert
        assert new_dev.tech_stack == ["Python", "Java"]
        assert new_dev.seniority_level == "senior"


class TestEmployeeSorting:
    """Тесты сортировки сотрудников."""
    
    def test_employee_sorting(self):
        """Тест различных способов сортировки сотрудников."""
        # Arrange
        employees = [
            Employee(3, "Charlie", "IT", 7000),
            Employee(1, "Alice", "HR", 5000),
            Employee(2, "Bob", "IT", 6000)
        ]
        
        # Act - Сортировка по имени
        sorted_by_name = sorted(employees, key=lambda x: x.name)
        assert sorted_by_name[0].name == "Alice"
        
        # Act - Сортировка по зарплате
        sorted_by_salary = sorted(employees, key=lambda x: x.calculate_salary())
        assert sorted_by_salary[0].calculate_salary() == 5000
    
    def test_employee_sorting_using_lt(self):
        """Тест сортировки с использованием оператора <."""
        # Arrange
        employees = [
            Employee(3, "Charlie", "IT", 7000),
            Employee(1, "Alice", "HR", 5000),
            Employee(2, "Bob", "IT", 6000)
        ]
        
        # Act
        sorted_employees = sorted(employees)
        
        # Assert
        assert sorted_employees[0].calculate_salary() == 5000
        assert sorted_employees[1].calculate_salary() == 6000
        assert sorted_employees[2].calculate_salary() == 7000


class TestDepartmentIntegration:
    """Интеграционные тесты для Department."""
    
    def test_department_integration(self):
        """Комплексный интеграционный тест для Department."""
        # Arrange
        dept = Department("Development")
        
        manager = Manager(1, "Alice", "DEV", 7000, 2000)
        developer = Developer(2, "Bob", "DEV", 5000, ["Python"], "senior")
        
        dept.add_employee(manager)
        dept.add_employee(developer)
        
        # Act
        total_salary = dept.calculate_total_salary()
        expected = manager.calculate_salary() + developer.calculate_salary()
        
        # Assert
        assert total_salary == expected
        assert dept.get_employee_count()["Manager"] == 1
        assert dept.get_employee_count()["Developer"] == 1
        
        # Проверка магических методов
        assert len(dept) == 2
        assert manager in dept
        assert developer in dept
        assert dept[0] == manager
        assert dept[1] == developer


