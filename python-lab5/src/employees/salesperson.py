"""Класс Salesperson (Продавец)."""

from src.core.employee import Employee


class Salesperson(Employee):
    """
    Класс для представления продавца.
    
    Продавец получает базовую зарплату плюс комиссию от объема продаж.
    """
    
    def __init__(self, id: int, name: str, department: str, base_salary: float,
                 commission_rate: float, sales_volume: float):
        """
        Инициализация продавца.
        
        Args:
            id: Уникальный идентификатор
            name: Имя продавца
            department: Отдел
            base_salary: Базовая зарплата
            commission_rate: Процент комиссии (например, 0.1 для 10%)
            sales_volume: Объем продаж
        """
        super().__init__(id, name, department, base_salary)
        self.__commission_rate = commission_rate
        self.__sales_volume = sales_volume
        self._validate_commission_rate(commission_rate)
        self._validate_sales_volume(sales_volume)
    
    def _validate_commission_rate(self, value: float) -> None:
        """Валидация процента комиссии."""
        if not isinstance(value, (int, float)) or value < 0 or value > 1:
            raise ValueError(
                f"Процент комиссии должен быть числом от 0 до 1, получено: {value}"
            )
    
    def _validate_sales_volume(self, value: float) -> None:
        """Валидация объема продаж."""
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError(
                f"Объем продаж должен быть неотрицательным числом, получено: {value}"
            )
    
    @property
    def commission_rate(self) -> float:
        """Получить процент комиссии."""
        return self.__commission_rate
    
    @commission_rate.setter
    def commission_rate(self, value: float) -> None:
        """Установить процент комиссии."""
        self._validate_commission_rate(value)
        self.__commission_rate = float(value)
    
    @property
    def sales_volume(self) -> float:
        """Получить объем продаж."""
        return self.__sales_volume
    
    @sales_volume.setter
    def sales_volume(self, value: float) -> None:
        """Установить объем продаж."""
        self._validate_sales_volume(value)
        self.__sales_volume = float(value)
    
    def update_sales(self, new_sales: float) -> None:
        """
        Добавить сумму к текущему объему продаж.
        
        Args:
            new_sales: Новая сумма продаж для добавления
        """
        if not isinstance(new_sales, (int, float)) or new_sales < 0:
            raise ValueError(
                f"Новая сумма продаж должна быть неотрицательным числом, получено: {new_sales}"
            )
        self.__sales_volume += new_sales
    
    def calculate_salary(self) -> float:
        """
        Рассчитать итоговую заработную плату продавца.
        
        Returns:
            Базовая зарплата + (объем продаж * процент комиссии)
        """
        return self.base_salary + (self.__sales_volume * self.__commission_rate)
    
    def get_info(self) -> str:
        """
        Получить полную информацию о продавце.
        
        Returns:
            Строка с полной информацией
        """
        return (f"Продавец [id: {self.id}, имя: {self.name}, отдел: {self.department}, "
                f"базовая зарплата: {self.base_salary}, процент комиссии: {self.__commission_rate}, "
                f"объем продаж: {self.__sales_volume}, итоговая зарплата: {self.calculate_salary()}]")
    
    def to_dict(self) -> dict:
        """
        Сериализация продавца в словарь.
        
        Returns:
            Словарь с данными продавца
        """
        base_dict = super().to_dict()
        base_dict["type"] = "Salesperson"
        base_dict["commission_rate"] = self.__commission_rate
        base_dict["sales_volume"] = self.__sales_volume
        return base_dict
    
    @classmethod
    def from_dict(cls, data: dict):
        """
        Создание объекта продавца из словаря.
        
        Args:
            data: Словарь с данными продавца
        
        Returns:
            Объект Salesperson
        """
        return cls(
            id=data["id"],
            name=data["name"],
            department=data["department"],
            base_salary=data["base_salary"],
            commission_rate=data.get("commission_rate", 0),
            sales_volume=data.get("sales_volume", 0)
        )

