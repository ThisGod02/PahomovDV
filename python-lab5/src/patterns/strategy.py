"""Strategy паттерн - стратегии расчета бонусов."""

from abc import ABC, abstractmethod
from src.core.abstract_employee import AbstractEmployee


class BonusStrategy(ABC):
    """
    Абстрактная стратегия расчета бонусов.
    
    Определяет интерфейс для различных алгоритмов расчета бонусов.
    """
    
    @abstractmethod
    def calculate_bonus(self, employee: AbstractEmployee) -> float:
        """
        Рассчитать бонус для сотрудника.
        
        Args:
            employee: Объект сотрудника
        
        Returns:
            Размер бонуса
        """
        pass


class PerformanceBonusStrategy(BonusStrategy):
    """
    Стратегия расчета бонуса на основе производительности.
    
    Бонус зависит от базовой зарплаты и уровня производительности.
    """
    
    def __init__(self, performance_multiplier: float = 0.1):
        """
        Инициализация стратегии.
        
        Args:
            performance_multiplier: Множитель производительности (по умолчанию 10%)
        """
        if performance_multiplier < 0 or performance_multiplier > 1:
            raise ValueError("Множитель производительности должен быть от 0 до 1")
        self._multiplier = performance_multiplier
    
    def calculate_bonus(self, employee: AbstractEmployee) -> float:
        """
        Рассчитать бонус на основе производительности.
        
        Args:
            employee: Объект сотрудника
        
        Returns:
            Размер бонуса
        """
        return employee.base_salary * self._multiplier


class SeniorityBonusStrategy(BonusStrategy):
    """
    Стратегия расчета бонуса на основе стажа.
    
    Бонус зависит от уровня seniority сотрудника.
    """
    
    SENIORITY_BONUSES = {
        "junior": 0.0,
        "middle": 5000.0,
        "senior": 15000.0
    }
    
    def calculate_bonus(self, employee: AbstractEmployee) -> float:
        """
        Рассчитать бонус на основе стажа.
        
        Args:
            employee: Объект сотрудника
        
        Returns:
            Размер бонуса
        """
        if hasattr(employee, 'seniority_level'):
            return self.SENIORITY_BONUSES.get(employee.seniority_level, 0.0)
        return 0.0


class ProjectBonusStrategy(BonusStrategy):
    """
    Стратегия расчета бонуса на основе участия в проектах.
    
    Бонус зависит от количества проектов, в которых участвует сотрудник.
    """
    
    def __init__(self, bonus_per_project: float = 2000.0):
        """
        Инициализация стратегии.
        
        Args:
            bonus_per_project: Бонус за каждый проект
        """
        if bonus_per_project < 0:
            raise ValueError("Бонус за проект не может быть отрицательным")
        self._bonus_per_project = bonus_per_project
    
    def calculate_bonus(self, employee: AbstractEmployee, project_count: int = 0) -> float:
        """
        Рассчитать бонус на основе количества проектов.
        
        Args:
            employee: Объект сотрудника
            project_count: Количество проектов (по умолчанию 0)
        
        Returns:
            Размер бонуса
        """
        return project_count * self._bonus_per_project


class FixedBonusStrategy(BonusStrategy):
    """
    Стратегия фиксированного бонуса.
    
    Всегда возвращает фиксированную сумму.
    """
    
    def __init__(self, fixed_amount: float):
        """
        Инициализация стратегии.
        
        Args:
            fixed_amount: Фиксированная сумма бонуса
        """
        if fixed_amount < 0:
            raise ValueError("Фиксированный бонус не может быть отрицательным")
        self._fixed_amount = fixed_amount
    
    def calculate_bonus(self, employee: AbstractEmployee) -> float:
        """
        Рассчитать фиксированный бонус.
        
        Args:
            employee: Объект сотрудника
        
        Returns:
            Фиксированный бонус
        """
        return self._fixed_amount


class BonusContext:
    """
    Контекст для использования стратегий расчета бонусов.
    
    Позволяет динамически менять стратегию расчета.
    """
    
    def __init__(self, strategy: BonusStrategy):
        """
        Инициализация контекста.
        
        Args:
            strategy: Стратегия расчета бонусов
        """
        self._strategy = strategy
    
    def set_strategy(self, strategy: BonusStrategy) -> None:
        """
        Установить новую стратегию.
        
        Args:
            strategy: Новая стратегия расчета бонусов
        """
        self._strategy = strategy
    
    def calculate_bonus(self, employee: AbstractEmployee, **kwargs) -> float:
        """
        Рассчитать бонус используя текущую стратегию.
        
        Args:
            employee: Объект сотрудника
            **kwargs: Дополнительные параметры для стратегии
        
        Returns:
            Размер бонуса
        """
        # Для ProjectBonusStrategy нужен project_count
        if isinstance(self._strategy, ProjectBonusStrategy):
            project_count = kwargs.get('project_count', 0)
            return self._strategy.calculate_bonus(employee, project_count)
        else:
            return self._strategy.calculate_bonus(employee)





