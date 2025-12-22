"""Adapter паттерн - адаптер для внешней системы расчета зарплат."""

from typing import Protocol
from src.core.abstract_employee import AbstractEmployee


class ExternalSalaryCalculator(Protocol):
    """Протокол для внешней системы расчета зарплат."""
    
    def compute_payment(self, employee_data: dict) -> float:
        """Вычислить зарплату (внешний интерфейс)."""
        ...


class ExternalSalaryService:
    """Имитация внешней системы расчета зарплат."""
    
    def compute_payment(self, employee_data: dict) -> float:
        """Вычислить зарплату через внешний сервис."""
        base_salary = employee_data.get("base_salary", 0)
        bonus = employee_data.get("bonus", 0)
        multiplier = employee_data.get("multiplier", 1.0)
        commission = employee_data.get("commission", 0)
        
        return (base_salary * multiplier) + bonus + commission


class SalaryCalculatorAdapter:
    """Адаптер для интеграции внешней системы расчета зарплат."""
    
    def __init__(self, external_calculator: ExternalSalaryCalculator):
        """Инициализация адаптера."""
        self._external_calculator = external_calculator
    
    def calculate_salary(self, employee: AbstractEmployee) -> float:
        """Рассчитать зарплату сотрудника через внешнюю систему."""
        employee_data = self._convert_to_external_format(employee)
        return self._external_calculator.compute_payment(employee_data)
    
    def _convert_to_external_format(self, employee: AbstractEmployee) -> dict:
        """Преобразовать объект сотрудника в формат внешней системы."""
        data = {
            "base_salary": employee.base_salary,
            "bonus": 0,
            "multiplier": 1.0,
            "commission": 0
        }
        
        if hasattr(employee, 'bonus'):
            data["bonus"] = employee.bonus
        
        if hasattr(employee, 'seniority_level'):
            multipliers = {"junior": 1.0, "middle": 1.5, "senior": 2.0}
            data["multiplier"] = multipliers.get(employee.seniority_level, 1.0)
        
        if hasattr(employee, 'commission_rate') and hasattr(employee, 'sales_volume'):
            data["commission"] = employee.sales_volume * employee.commission_rate
        
        return data


