"""Абстрактный базовый класс для сотрудников."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.employee import Employee


class AbstractEmployee(ABC):
    """
    Абстрактный базовый класс для всех типов сотрудников.
    
    Определяет общий интерфейс для работы с сотрудниками.
    """
    
    @abstractmethod
    def calculate_salary(self) -> float:
        """
        Рассчитать итоговую заработную плату.
        
        Returns:
            Итоговая зарплата сотрудника
        """
        pass
    
    @abstractmethod
    def get_info(self) -> str:
        """
        Получить полную информацию о сотруднике.
        
        Returns:
            Строка с полной информацией
        """
        pass

