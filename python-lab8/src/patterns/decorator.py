"""Decorator паттерн - декораторы для сотрудников."""

from src.core.abstract_employee import AbstractEmployee


class EmployeeDecorator(AbstractEmployee):
    """Базовый декоратор для сотрудников."""
    
    def __init__(self, employee: AbstractEmployee):
        """Инициализация декоратора."""
        self._employee = employee
    
    @property
    def id(self) -> int:
        """Получить ID сотрудника."""
        return self._employee.id
    
    @property
    def name(self) -> str:
        """Получить имя сотрудника."""
        return self._employee.name
    
    @property
    def department(self) -> str:
        """Получить отдел сотрудника."""
        return self._employee.department
    
    @property
    def base_salary(self) -> float:
        """Получить базовую зарплату сотрудника."""
        return self._employee.base_salary
    
    def calculate_salary(self) -> float:
        """Рассчитать зарплату (базовая реализация)."""
        return self._employee.calculate_salary()
    
    def get_info(self) -> str:
        """Получить информацию о сотруднике."""
        return self._employee.get_info()


class BonusDecorator(EmployeeDecorator):
    """Декоратор для добавления бонуса к зарплате."""
    
    def __init__(self, employee: AbstractEmployee, bonus_amount: float):
        """Инициализация декоратора бонуса."""
        super().__init__(employee)
        if bonus_amount < 0:
            raise ValueError("Бонус не может быть отрицательным")
        self._bonus_amount = bonus_amount
    
    def calculate_salary(self) -> float:
        """Рассчитать зарплату с учетом бонуса."""
        return self._employee.calculate_salary() + self._bonus_amount
    
    def get_info(self) -> str:
        """Получить информацию о сотруднике с бонусом."""
        base_info = self._employee.get_info()
        return f"{base_info} [Бонус: {self._bonus_amount}]"


