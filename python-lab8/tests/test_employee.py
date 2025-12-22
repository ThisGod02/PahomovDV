"""Тесты для Части 1: Тестирование инкапсуляции и базового класса Employee."""

import pytest
from src.core.employee import Employee


class TestEmployee:
    """Тесты для класса Employee."""
    
    def test_employee_creation_valid_data(self):
        """Тест создания Employee с валидными данными."""
        # Arrange
        emp = Employee(1, "Alice", "IT", 5000)
        
        # Assert
        assert emp.id == 1
        assert emp.name == "Alice"
        assert emp.department == "IT"
        assert emp.base_salary == 5000
    
    def test_employee_invalid_id_raises_error(self):
        """Тест валидации ID - отрицательное значение."""
        # Assert
        with pytest.raises(ValueError, match="ID должен быть положительным"):
            Employee(-1, "Alice", "IT", 5000)
        
        with pytest.raises(ValueError, match="ID должен быть положительным"):
            Employee(0, "Alice", "IT", 5000)
    
    def test_employee_invalid_base_salary_raises_error(self):
        """Тест валидации базовой зарплаты - отрицательное значение."""
        # Assert
        with pytest.raises(ValueError, match="Базовая зарплата должна быть неотрицательным"):
            Employee(1, "Alice", "IT", -1000)
    
    def test_employee_empty_name_raises_error(self):
        """Тест валидации имени - пустая строка."""
        # Assert
        with pytest.raises(ValueError, match="Имя не должно быть пустой строкой"):
            Employee(1, "", "IT", 5000)
        
        with pytest.raises(ValueError, match="Имя не должно быть пустой строкой"):
            Employee(1, "   ", "IT", 5000)
    
    def test_employee_calculate_salary(self):
        """Тест метода calculate_salary - должен возвращать base_salary."""
        # Arrange
        emp = Employee(1, "Alice", "IT", 5000)
        
        # Act
        salary = emp.calculate_salary()
        
        # Assert
        assert salary == 5000
    
    def test_employee_str_representation(self):
        """Тест метода __str__ - проверка формата строки."""
        # Arrange
        emp = Employee(1, "Alice", "IT", 5000)
        
        # Act
        result = str(emp)
        
        # Assert
        expected = "Сотрудник [id: 1, имя: Alice, отдел: IT, базовая зарплата: 5000]"
        assert result == expected
    
    def test_employee_id_setter_validation(self):
        """Тест сеттера ID с валидацией."""
        # Arrange
        emp = Employee(1, "Alice", "IT", 5000)
        
        # Act & Assert
        emp.id = 2
        assert emp.id == 2
        
        with pytest.raises(ValueError):
            emp.id = -1
        
        with pytest.raises(ValueError):
            emp.id = 0
    
    def test_employee_name_setter_validation(self):
        """Тест сеттера имени с валидацией."""
        # Arrange
        emp = Employee(1, "Alice", "IT", 5000)
        
        # Act & Assert
        emp.name = "Bob"
        assert emp.name == "Bob"
        
        with pytest.raises(ValueError):
            emp.name = ""
        
        with pytest.raises(ValueError):
            emp.name = "   "
    
    def test_employee_base_salary_setter_validation(self):
        """Тест сеттера базовой зарплаты с валидацией."""
        # Arrange
        emp = Employee(1, "Alice", "IT", 5000)
        
        # Act & Assert
        emp.base_salary = 6000
        assert emp.base_salary == 6000
        
        with pytest.raises(ValueError):
            emp.base_salary = -1000
    
    def test_employee_department_setter_validation(self):
        """Тест сеттера отдела с валидацией."""
        # Arrange
        emp = Employee(1, "Alice", "IT", 5000)
        
        # Act & Assert
        emp.department = "HR"
        assert emp.department == "HR"
        
        with pytest.raises(ValueError):
            emp.department = ""
        
        with pytest.raises(ValueError):
            emp.department = "   "
    
    def test_employee_get_info(self):
        """Тест метода get_info."""
        # Arrange
        emp = Employee(1, "Alice", "IT", 5000)
        
        # Act
        info = emp.get_info()
        
        # Assert
        assert "Alice" in info
        assert "5000" in info
        assert "итоговая зарплата" in info


