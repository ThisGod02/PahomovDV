"""Базовый класс Employee с инкапсуляцией данных."""

from src.core.abstract_employee import AbstractEmployee


class Employee(AbstractEmployee):
    """
    Базовый класс для представления сотрудника компании.
    
    Реализует инкапсуляцию через приватные атрибуты и свойства.
    """
    
    def __init__(self, id: int, name: str, department: str, base_salary: float):
        """
        Инициализация сотрудника.
        
        Args:
            id: Уникальный идентификатор сотрудника
            name: Имя сотрудника
            department: Отдел сотрудника
            base_salary: Базовая зарплата
        """
        self.__id = id
        self.__name = name
        self.__department = department
        self.__base_salary = base_salary
        
        # Валидация при инициализации
        self._validate_id(id)
        self._validate_name(name)
        self._validate_base_salary(base_salary)
    
    def _validate_id(self, value: int) -> None:
        """Валидация ID."""
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"ID должен быть положительным целым числом, получено: {value}")
    
    def _validate_name(self, value: str) -> None:
        """Валидация имени."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Имя не должно быть пустой строкой, получено: '{value}'")
    
    def _validate_base_salary(self, value: float) -> None:
        """Валидация базовой зарплаты."""
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError(f"Базовая зарплата должна быть неотрицательным числом, получено: {value}")
    
    @property
    def id(self) -> int:
        """Получить ID сотрудника."""
        return self.__id
    
    @id.setter
    def id(self, value: int) -> None:
        """Установить ID сотрудника."""
        self._validate_id(value)
        self.__id = value
    
    @property
    def name(self) -> str:
        """Получить имя сотрудника."""
        return self.__name
    
    @name.setter
    def name(self, value: str) -> None:
        """Установить имя сотрудника."""
        self._validate_name(value)
        self.__name = value
    
    @property
    def department(self) -> str:
        """Получить отдел сотрудника."""
        return self.__department
    
    @department.setter
    def department(self, value: str) -> None:
        """Установить отдел сотрудника."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Отдел не должен быть пустой строкой, получено: '{value}'")
        self.__department = value
    
    @property
    def base_salary(self) -> float:
        """Получить базовую зарплату сотрудника."""
        return self.__base_salary
    
    @base_salary.setter
    def base_salary(self, value: float) -> None:
        """Установить базовую зарплату сотрудника."""
        self._validate_base_salary(value)
        self.__base_salary = float(value)
    
    def calculate_salary(self) -> float:
        """
        Рассчитать итоговую заработную плату.
        
        Для обычного сотрудника итоговая зарплата равна базовой.
        
        Returns:
            Итоговая зарплата сотрудника
        """
        return self.__base_salary
    
    def get_info(self) -> str:
        """
        Получить полную информацию о сотруднике.
        
        Returns:
            Строка с полной информацией о сотруднике
        """
        return (f"{self.__str__()}, итоговая зарплата: {self.calculate_salary()}")
    
    def __eq__(self, other) -> bool:
        """
        Сравнение сотрудников по ID.
        
        Args:
            other: Другой объект для сравнения
        
        Returns:
            True если ID совпадают, False иначе
        """
        if not isinstance(other, Employee):
            return NotImplemented
        return self.__id == other.id
    
    def __lt__(self, other) -> bool:
        """
        Сравнение сотрудников по итоговой зарплате.
        
        Args:
            other: Другой объект для сравнения
        
        Returns:
            True если зарплата текущего сотрудника меньше
        """
        if not isinstance(other, Employee):
            return NotImplemented
        return self.calculate_salary() < other.calculate_salary()
    
    def __add__(self, other) -> float:
        """
        Сложение двух сотрудников возвращает сумму их зарплат.
        
        Args:
            other: Другой объект сотрудника
        
        Returns:
            Сумма зарплат двух сотрудников
        """
        if not isinstance(other, Employee):
            return NotImplemented
        return self.calculate_salary() + other.calculate_salary()
    
    def __radd__(self, other) -> float:
        """
        Поддержка суммирования в списке через sum().
        
        Args:
            other: Число (обычно 0 при суммировании списка)
        
        Returns:
            Зарплата сотрудника
        """
        if other == 0:
            return self.calculate_salary()
        return other + self.calculate_salary()
    
    def to_dict(self) -> dict:
        """
        Сериализация сотрудника в словарь.
        
        Returns:
            Словарь с данными сотрудника
        """
        return {
            "type": "Employee",
            "id": self.__id,
            "name": self.__name,
            "department": self.__department,
            "base_salary": self.__base_salary
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """
        Создание объекта сотрудника из словаря.
        
        Args:
            data: Словарь с данными сотрудника
        
        Returns:
            Объект Employee
        """
        return cls(
            id=data["id"],
            name=data["name"],
            department=data["department"],
            base_salary=data["base_salary"]
        )
    
    def __str__(self) -> str:
        """
        Строковое представление сотрудника.
        
        Returns:
            Строка с информацией о сотруднике
        """
        return (f"Сотрудник [id: {self.__id}, имя: {self.__name}, "
                f"отдел: {self.__department}, базовая зарплата: {self.__base_salary}]")

