"""Observer паттерн - система уведомлений."""

from abc import ABC, abstractmethod
from typing import List
from src.core.abstract_employee import AbstractEmployee


class Observer(ABC):
    """Абстрактный наблюдатель."""
    
    @abstractmethod
    def update(self, event_type: str, data: dict) -> None:
        """Обновить наблюдателя при изменении состояния."""
        pass


class Subject(ABC):
    """Абстрактный субъект (наблюдаемый объект)."""
    
    def __init__(self):
        """Инициализация субъекта."""
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer) -> None:
        """Подписать наблюдателя на уведомления."""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: Observer) -> None:
        """Отписать наблюдателя от уведомлений."""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self, event_type: str, data: dict) -> None:
        """Уведомить всех наблюдателей об изменении."""
        for observer in self._observers:
            observer.update(event_type, data)


class ObservableEmployee(AbstractEmployee, Subject):
    """Наблюдаемый сотрудник."""
    
    def __init__(self, employee: AbstractEmployee):
        """Инициализация наблюдаемого сотрудника."""
        Subject.__init__(self)
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
        """Рассчитать зарплату."""
        return self._employee.calculate_salary()
    
    def get_info(self) -> str:
        """Получить информацию о сотруднике."""
        return self._employee.get_info()
    
    def set_base_salary(self, new_salary: float) -> None:
        """Установить новую базовую зарплату с уведомлением."""
        old_salary = self._employee.base_salary
        self._employee.base_salary = new_salary
        
        # Уведомляем наблюдателей
        self.notify("salary_changed", {
            "employee_id": self.id,
            "employee_name": self.name,
            "old_salary": old_salary,
            "new_salary": new_salary
        })


