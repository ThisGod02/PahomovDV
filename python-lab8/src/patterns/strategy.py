"""Strategy паттерн - стратегии расчета бонусов."""

from abc import ABC, abstractmethod
from src.core.abstract_employee import AbstractEmployee


class BonusStrategy(ABC):
    """Абстрактная стратегия расчета бонусов."""
    
    @abstractmethod
    def calculate_bonus(self, employee: AbstractEmployee) -> float:
        """Рассчитать бонус для сотрудника."""
        pass


class PerformanceBonusStrategy(BonusStrategy):
    """Стратегия расчета бонуса на основе производительности."""
    
    def __init__(self, performance_multiplier: float = 0.1):
        """Инициализация стратегии."""
        if performance_multiplier < 0 or performance_multiplier > 1:
            raise ValueError("Множитель производительности должен быть от 0 до 1")
        self._multiplier = performance_multiplier
    
    def calculate_bonus(self, employee: AbstractEmployee) -> float:
        """Рассчитать бонус на основе производительности."""
        return employee.base_salary * self._multiplier


class SeniorityBonusStrategy(BonusStrategy):
    """Стратегия расчета бонуса на основе стажа."""
    
    SENIORITY_BONUSES = {
        "junior": 0.0,
        "middle": 5000.0,
        "senior": 15000.0
    }
    
    def calculate_bonus(self, employee: AbstractEmployee) -> float:
        """Рассчитать бонус на основе стажа."""
        if hasattr(employee, 'seniority_level'):
            return self.SENIORITY_BONUSES.get(employee.seniority_level, 0.0)
        return 0.0


class BonusContext:
    """Контекст для использования стратегий расчета бонусов."""
    
    def __init__(self, strategy: BonusStrategy):
        """Инициализация контекста."""
        self._strategy = strategy
    
    def set_strategy(self, strategy: BonusStrategy) -> None:
        """Установить новую стратегию."""
        self._strategy = strategy
    
    def calculate_bonus(self, employee: AbstractEmployee) -> float:
        """Рассчитать бонус используя текущую стратегию."""
        return self._strategy.calculate_bonus(employee)


