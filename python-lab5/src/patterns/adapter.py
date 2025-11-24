"""Adapter паттерн - адаптер для внешней системы расчета зарплат."""

from typing import Protocol
from src.core.abstract_employee import AbstractEmployee


class ExternalSalaryCalculator(Protocol):
    """
    Протокол для внешней системы расчета зарплат.
    
    Представляет интерфейс сторонней библиотеки.
    """
    
    def compute_payment(self, employee_data: dict) -> float:
        """
        Вычислить зарплату (внешний интерфейс).
        
        Args:
            employee_data: Словарь с данными сотрудника
        
        Returns:
            Рассчитанная зарплата
        """
        ...


class ExternalSalaryService:
    """
    Имитация внешней системы расчета зарплат.
    
    Использует другой интерфейс, несовместимый с нашей системой.
    """
    
    def compute_payment(self, employee_data: dict) -> float:
        """
        Вычислить зарплату через внешний сервис.
        
        Args:
            employee_data: Словарь с данными сотрудника
        
        Returns:
            Рассчитанная зарплата
        """
        base_salary = employee_data.get("base_salary", 0)
        bonus = employee_data.get("bonus", 0)
        multiplier = employee_data.get("multiplier", 1.0)
        commission = employee_data.get("commission", 0)
        
        return (base_salary * multiplier) + bonus + commission


class SalaryCalculatorAdapter:
    """
    Адаптер для интеграции внешней системы расчета зарплат.
    
    Адаптирует интерфейс внешней библиотеки к интерфейсу нашей системы.
    """
    
    def __init__(self, external_calculator: ExternalSalaryCalculator):
        """
        Инициализация адаптера.
        
        Args:
            external_calculator: Экземпляр внешней системы расчета
        """
        self._external_calculator = external_calculator
    
    def calculate_salary(self, employee: AbstractEmployee) -> float:
        """
        Рассчитать зарплату сотрудника через внешнюю систему.
        
        Адаптирует наш интерфейс AbstractEmployee к интерфейсу внешней системы.
        
        Args:
            employee: Объект сотрудника
        
        Returns:
            Рассчитанная зарплата
        """
        # Преобразуем наш объект в формат, ожидаемый внешней системой
        employee_data = self._convert_to_external_format(employee)
        
        # Вызываем внешний метод
        return self._external_calculator.compute_payment(employee_data)
    
    def _convert_to_external_format(self, employee: AbstractEmployee) -> dict:
        """
        Преобразовать объект сотрудника в формат внешней системы.
        
        Args:
            employee: Объект сотрудника
        
        Returns:
            Словарь с данными в формате внешней системы
        """
        data = {
            "base_salary": employee.base_salary,
            "bonus": 0,
            "multiplier": 1.0,
            "commission": 0
        }
        
        # Обрабатываем разные типы сотрудников
        if hasattr(employee, 'bonus'):
            data["bonus"] = employee.bonus
        
        if hasattr(employee, 'seniority_level'):
            # Преобразуем уровень в множитель
            multipliers = {"junior": 1.0, "middle": 1.5, "senior": 2.0}
            data["multiplier"] = multipliers.get(employee.seniority_level, 1.0)
        
        if hasattr(employee, 'commission_rate') and hasattr(employee, 'sales_volume'):
            data["commission"] = employee.sales_volume * employee.commission_rate
        
        return data

