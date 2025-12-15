"""Observer паттерн - система уведомлений."""

from abc import ABC, abstractmethod
from typing import List
from src.core.abstract_employee import AbstractEmployee


class Observer(ABC):
    """
    Абстрактный наблюдатель.
    
    Определяет интерфейс для объектов, которые должны быть уведомлены
    об изменениях в системе.
    """
    
    @abstractmethod
    def update(self, event_type: str, data: dict) -> None:
        """
        Обновить наблюдателя при изменении состояния.
        
        Args:
            event_type: Тип события
            data: Данные события
        """
        pass


class Subject(ABC):
    """
    Абстрактный субъект (наблюдаемый объект).
    
    Определяет интерфейс для объектов, за которыми можно наблюдать.
    """
    
    def __init__(self):
        """Инициализация субъекта."""
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer) -> None:
        """
        Подписать наблюдателя на уведомления.
        
        Args:
            observer: Объект наблюдателя
        """
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: Observer) -> None:
        """
        Отписать наблюдателя от уведомлений.
        
        Args:
            observer: Объект наблюдателя
        """
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self, event_type: str, data: dict) -> None:
        """
        Уведомить всех наблюдателей об изменении.
        
        Args:
            event_type: Тип события
            data: Данные события
        """
        for observer in self._observers:
            observer.update(event_type, data)


class NotificationSystem(Observer):
    """
    Система уведомлений (конкретный наблюдатель).
    
    Регистрирует и обрабатывает уведомления об изменениях в системе.
    """
    
    def __init__(self):
        """Инициализация системы уведомлений."""
        self._notifications: List[dict] = []
    
    def update(self, event_type: str, data: dict) -> None:
        """
        Обработать уведомление.
        
        Args:
            event_type: Тип события
            data: Данные события
        """
        notification = {
            "event_type": event_type,
            "data": data,
            "timestamp": self._get_timestamp()
        }
        self._notifications.append(notification)
        self._process_notification(notification)
    
    def _process_notification(self, notification: dict) -> None:
        """
        Обработать уведомление (можно переопределить для логирования).
        
        Args:
            notification: Уведомление
        """
        event_type = notification["event_type"]
        data = notification["data"]
        
        if event_type == "salary_changed":
            print(f"Уведомление: Изменена зарплата сотрудника {data.get('employee_id')}")
        elif event_type == "employee_hired":
            print(f"Уведомление: Нанят сотрудник {data.get('employee_name')}")
        elif event_type == "employee_fired":
            print(f"Уведомление: Уволен сотрудник {data.get('employee_id')}")
        elif event_type == "project_status_changed":
            print(f"Уведомление: Изменен статус проекта {data.get('project_id')}")
    
    def get_notifications(self) -> List[dict]:
        """
        Получить все уведомления.
        
        Returns:
            Список уведомлений
        """
        return self._notifications.copy()
    
    def clear_notifications(self) -> None:
        """Очистить все уведомления."""
        self._notifications.clear()
    
    @staticmethod
    def _get_timestamp() -> str:
        """
        Получить текущую временную метку.
        
        Returns:
            Строка с временной меткой
        """
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class ObservableEmployee(AbstractEmployee, Subject):
    """
    Наблюдаемый сотрудник.
    
    Расширяет AbstractEmployee функциональностью Subject для уведомлений.
    """
    
    def __init__(self, employee: AbstractEmployee):
        """
        Инициализация наблюдаемого сотрудника.
        
        Args:
            employee: Базовый объект сотрудника
        """
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
        """
        Рассчитать зарплату.
        
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
    
    def set_base_salary(self, new_salary: float) -> None:
        """
        Установить новую базовую зарплату с уведомлением.
        
        Args:
            new_salary: Новая зарплата
        """
        old_salary = self._employee.base_salary
        self._employee.base_salary = new_salary
        
        # Уведомляем наблюдателей
        self.notify("salary_changed", {
            "employee_id": self.id,
            "employee_name": self.name,
            "old_salary": old_salary,
            "new_salary": new_salary
        })


class ProjectObserver(Subject):
    """
    Наблюдаемый проект.
    
    Уведомляет наблюдателей об изменениях статуса проекта.
    """
    
    def __init__(self, project):
        """
        Инициализация наблюдаемого проекта.
        
        Args:
            project: Объект проекта
        """
        super().__init__()
        self._project = project
    
    def change_status(self, new_status: str) -> None:
        """
        Изменить статус проекта с уведомлением.
        
        Args:
            new_status: Новый статус
        """
        old_status = self._project.status
        self._project.change_status(new_status)
        
        # Уведомляем наблюдателей
        self.notify("project_status_changed", {
            "project_id": self._project.project_id,
            "project_name": self._project.name,
            "old_status": old_status,
            "new_status": new_status
        })


