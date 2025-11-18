"""Класс Developer (Разработчик)."""

from typing import List
from src.core.employee import Employee


class Developer(Employee):
    """
    Класс для представления разработчика.
    
    Разработчик получает базовую зарплату, умноженную на коэффициент уровня.
    """
    
    SENIORITY_COEFFICIENTS = {
        "junior": 1.0,
        "middle": 1.5,
        "senior": 2.0
    }
    
    def __init__(self, id: int, name: str, department: str, base_salary: float,
                 tech_stack: List[str], seniority_level: str):
        """
        Инициализация разработчика.
        
        Args:
            id: Уникальный идентификатор
            name: Имя разработчика
            department: Отдел
            base_salary: Базовая зарплата
            tech_stack: Список технологий
            seniority_level: Уровень (junior, middle, senior)
        """
        super().__init__(id, name, department, base_salary)
        self.__tech_stack = list(tech_stack) if tech_stack else []
        self.__seniority_level = seniority_level
        self._validate_seniority_level(seniority_level)
        self._validate_tech_stack(tech_stack)
    
    def _validate_seniority_level(self, value: str) -> None:
        """Валидация уровня seniority."""
        if value not in self.SENIORITY_COEFFICIENTS:
            raise ValueError(
                f"Уровень должен быть одним из: {list(self.SENIORITY_COEFFICIENTS.keys())}, "
                f"получено: '{value}'"
            )
    
    def _validate_tech_stack(self, value: List[str]) -> None:
        """Валидация стека технологий."""
        if not isinstance(value, list):
            raise ValueError(f"Стек технологий должен быть списком, получено: {type(value)}")
        if not all(isinstance(tech, str) and tech.strip() for tech in value):
            raise ValueError("Все технологии должны быть непустыми строками")
    
    @property
    def tech_stack(self) -> List[str]:
        """Получить стек технологий."""
        return self.__tech_stack.copy()
    
    @property
    def seniority_level(self) -> str:
        """Получить уровень seniority."""
        return self.__seniority_level
    
    @seniority_level.setter
    def seniority_level(self, value: str) -> None:
        """Установить уровень seniority."""
        self._validate_seniority_level(value)
        self.__seniority_level = value
    
    def add_skill(self, new_skill: str) -> None:
        """
        Добавить новую технологию в стек.
        
        Args:
            new_skill: Название новой технологии
        """
        if not isinstance(new_skill, str) or not new_skill.strip():
            raise ValueError(f"Технология должна быть непустой строкой, получено: '{new_skill}'")
        if new_skill not in self.__tech_stack:
            self.__tech_stack.append(new_skill)
    
    def calculate_salary(self) -> float:
        """
        Рассчитать итоговую заработную плату разработчика.
        
        Returns:
            Базовая зарплата * коэффициент уровня
        """
        coefficient = self.SENIORITY_COEFFICIENTS[self.__seniority_level]
        return self.base_salary * coefficient
    
    def get_info(self) -> str:
        """
        Получить полную информацию о разработчике.
        
        Returns:
            Строка с полной информацией
        """
        return (f"Разработчик [id: {self.id}, имя: {self.name}, отдел: {self.department}, "
                f"базовая зарплата: {self.base_salary}, уровень: {self.__seniority_level}, "
                f"стек технологий: {self.__tech_stack}, итоговая зарплата: {self.calculate_salary()}]")
    
    def __iter__(self):
        """Итерация по стеку технологий."""
        return iter(self.__tech_stack)
    
    def to_dict(self) -> dict:
        """
        Сериализация разработчика в словарь.
        
        Returns:
            Словарь с данными разработчика
        """
        base_dict = super().to_dict()
        base_dict["type"] = "Developer"
        base_dict["tech_stack"] = self.__tech_stack.copy()
        base_dict["seniority_level"] = self.__seniority_level
        return base_dict
    
    @classmethod
    def from_dict(cls, data: dict):
        """
        Создание объекта разработчика из словаря.
        
        Args:
            data: Словарь с данными разработчика
        
        Returns:
            Объект Developer
        """
        return cls(
            id=data["id"],
            name=data["name"],
            department=data["department"],
            base_salary=data["base_salary"],
            tech_stack=data.get("tech_stack", []),
            seniority_level=data.get("seniority_level", "junior")
        )

