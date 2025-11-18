"""Класс Manager (Менеджер)."""

from src.core.employee import Employee


class Manager(Employee):
    """
    Класс для представления менеджера.
    
    Менеджер получает базовую зарплату плюс бонус.
    """
    
    def __init__(self, id: int, name: str, department: str, base_salary: float, bonus: float):
        """
        Инициализация менеджера.
        
        Args:
            id: Уникальный идентификатор
            name: Имя менеджера
            department: Отдел
            base_salary: Базовая зарплата
            bonus: Бонус менеджера
        """
        super().__init__(id, name, department, base_salary)
        self.__bonus = bonus
        self._validate_bonus(bonus)
    
    def _validate_bonus(self, value: float) -> None:
        """Валидация бонуса."""
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError(f"Бонус должен быть неотрицательным числом, получено: {value}")
    
    @property
    def bonus(self) -> float:
        """Получить бонус менеджера."""
        return self.__bonus
    
    @bonus.setter
    def bonus(self, value: float) -> None:
        """Установить бонус менеджера."""
        self._validate_bonus(value)
        self.__bonus = float(value)
    
    def calculate_salary(self) -> float:
        """
        Рассчитать итоговую заработную плату менеджера.
        
        Returns:
            Базовая зарплата + бонус
        """
        return self.base_salary + self.__bonus
    
    def get_info(self) -> str:
        """
        Получить полную информацию о менеджере.
        
        Returns:
            Строка с полной информацией
        """
        return (f"Менеджер [id: {self.id}, имя: {self.name}, отдел: {self.department}, "
                f"базовая зарплата: {self.base_salary}, бонус: {self.__bonus}, "
                f"итоговая зарплата: {self.calculate_salary()}]")
    
    def to_dict(self) -> dict:
        """
        Сериализация менеджера в словарь.
        
        Returns:
            Словарь с данными менеджера
        """
        base_dict = super().to_dict()
        base_dict["type"] = "Manager"
        base_dict["bonus"] = self.__bonus
        return base_dict
    
    @classmethod
    def from_dict(cls, data: dict):
        """
        Создание объекта менеджера из словаря.
        
        Args:
            data: Словарь с данными менеджера
        
        Returns:
            Объект Manager
        """
        return cls(
            id=data["id"],
            name=data["name"],
            department=data["department"],
            base_salary=data["base_salary"],
            bonus=data.get("bonus", 0)
        )

