"""Decorator паттерн - декораторы для сотрудников."""

from src.core.abstract_employee import AbstractEmployee


class EmployeeDecorator(AbstractEmployee):
    """
    Базовый декоратор для сотрудников.
    
    Реализует паттерн Decorator для добавления функциональности.
    """
    
    def __init__(self, employee: AbstractEmployee):
        """
        Инициализация декоратора.
        
        Args:
            employee: Объект сотрудника для декорирования
        """
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
        """
        Рассчитать зарплату (базовая реализация).
        
        Returns:
            Зарплата сотрудника
        """
        return self._employee.calculate_salary()
    
    def get_info(self) -> str:
        """
        Получить информацию о сотруднике.
        
        Returns:
            Строка с информацией
        """
        return self._employee.get_info()


class BonusDecorator(EmployeeDecorator):
    """
    Декоратор для добавления бонуса к зарплате.
    
    Добавляет фиксированный бонус к зарплате сотрудника.
    """
    
    def __init__(self, employee: AbstractEmployee, bonus_amount: float):
        """
        Инициализация декоратора бонуса.
        
        Args:
            employee: Объект сотрудника
            bonus_amount: Размер бонуса
        """
        super().__init__(employee)
        if bonus_amount < 0:
            raise ValueError("Бонус не может быть отрицательным")
        self._bonus_amount = bonus_amount
    
    def calculate_salary(self) -> float:
        """
        Рассчитать зарплату с учетом бонуса.
        
        Returns:
            Зарплата + бонус
        """
        return self._employee.calculate_salary() + self._bonus_amount
    
    def get_info(self) -> str:
        """
        Получить информацию о сотруднике с бонусом.
        
        Returns:
            Строка с информацией
        """
        base_info = self._employee.get_info()
        return f"{base_info} [Бонус: {self._bonus_amount}]"


class TrainingDecorator(EmployeeDecorator):
    """
    Декоратор для сотрудников, проходящих обучение.
    
    Добавляет функциональность обучения и может влиять на зарплату.
    """
    
    def __init__(self, employee: AbstractEmployee, training_bonus: float = 0):
        """
        Инициализация декоратора обучения.
        
        Args:
            employee: Объект сотрудника
            training_bonus: Бонус за обучение (опционально)
        """
        super().__init__(employee)
        self._training_bonus = max(0, training_bonus)
        self._completed_trainings = []
    
    def add_training(self, training_name: str) -> None:
        """
        Добавить завершенное обучение.
        
        Args:
            training_name: Название обучения
        """
        if training_name not in self._completed_trainings:
            self._completed_trainings.append(training_name)
    
    def get_completed_trainings(self) -> list:
        """
        Получить список завершенных обучений.
        
        Returns:
            Список названий обучений
        """
        return self._completed_trainings.copy()
    
    def calculate_salary(self) -> float:
        """
        Рассчитать зарплату с учетом бонуса за обучение.
        
        Returns:
            Зарплата + бонус за обучение
        """
        base_salary = self._employee.calculate_salary()
        return base_salary + self._training_bonus
    
    def get_info(self) -> str:
        """
        Получить информацию о сотруднике с обучением.
        
        Returns:
            Строка с информацией
        """
        base_info = self._employee.get_info()
        trainings = ", ".join(self._completed_trainings) if self._completed_trainings else "нет"
        return f"{base_info} [Обучение: {trainings}, бонус за обучение: {self._training_bonus}]"


class PerformanceDecorator(EmployeeDecorator):
    """
    Декоратор для учета производительности.
    
    Добавляет процентный бонус на основе производительности.
    """
    
    def __init__(self, employee: AbstractEmployee, performance_multiplier: float):
        """
        Инициализация декоратора производительности.
        
        Args:
            employee: Объект сотрудника
            performance_multiplier: Множитель производительности (например, 1.1 для +10%)
        """
        super().__init__(employee)
        if performance_multiplier < 0:
            raise ValueError("Множитель производительности не может быть отрицательным")
        self._performance_multiplier = performance_multiplier
    
    def calculate_salary(self) -> float:
        """
        Рассчитать зарплату с учетом производительности.
        
        Returns:
            Зарплата * множитель производительности
        """
        return self._employee.calculate_salary() * self._performance_multiplier
    
    def get_info(self) -> str:
        """
        Получить информацию о сотруднике с производительностью.
        
        Returns:
            Строка с информацией
        """
        base_info = self._employee.get_info()
        multiplier_percent = (self._performance_multiplier - 1) * 100
        return f"{base_info} [Производительность: {multiplier_percent:+.1f}%]"





