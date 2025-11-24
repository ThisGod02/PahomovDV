"""Демонстрация всех паттернов проектирования."""

from src.database.connection import DatabaseConnection
from src.factories.employee_factory import (
    ManagerFactory, DeveloperFactory, SalespersonFactory
)
from src.factories.company_factory import TechCompanyFactory, SalesCompanyFactory
from src.patterns.builder import EmployeeBuilder
from src.patterns.adapter import ExternalSalaryService, SalaryCalculatorAdapter
from src.patterns.decorator import BonusDecorator, TrainingDecorator, PerformanceDecorator
from src.patterns.facade import CompanyFacade
from src.patterns.observer import NotificationSystem, ObservableEmployee
from src.patterns.strategy import (
    PerformanceBonusStrategy, SeniorityBonusStrategy, ProjectBonusStrategy, BonusContext
)
from src.patterns.command import HireEmployeeCommand, FireEmployeeCommand, UpdateSalaryCommand, CommandInvoker
from src.patterns.repository import EmployeeRepository
from src.patterns.unit_of_work import UnitOfWork
from src.patterns.specification import (
    SalarySpecification, DepartmentSpecification, SkillSpecification, SpecificationRepository
)
from src.employees.developer import Developer
from src.employees.manager import Manager
from src.core.company import Company


def demonstrate_singleton():
    """Демонстрация Singleton паттерна."""
    print("\n=== 1. Singleton (Одиночка) ===")
    
    # Получаем экземпляры
    db1 = DatabaseConnection.get_instance()
    db2 = DatabaseConnection.get_instance()
    
    # Проверяем, что это один и тот же объект
    print(f"db1 is db2: {db1 is db2}")
    print(f"ID db1: {id(db1)}")
    print(f"ID db2: {id(db2)}")
    
    # Получаем подключение
    conn1 = db1.get_connection(":memory:")
    print("Подключение к БД создано успешно")


def demonstrate_factory_method():
    """Демонстрация Factory Method паттерна."""
    print("\n=== 2. Factory Method (Фабричный метод) ===")
    
    # Используем конкретные фабрики
    manager_factory = ManagerFactory()
    developer_factory = DeveloperFactory()
    salesperson_factory = SalespersonFactory()
    
    manager = manager_factory.create_employee(
        id=1, name="Алиса", department="MANAGEMENT", base_salary=70000, bonus=20000
    )
    developer = developer_factory.create_employee(
        id=2, name="Боб", department="DEV", base_salary=50000,
        tech_stack=["Python", "Java"], seniority_level="senior"
    )
    salesperson = salesperson_factory.create_employee(
        id=3, name="Чарли", department="SALES", base_salary=40000,
        commission_rate=0.15, sales_volume=100000
    )
    
    print(f"Менеджер: {manager.get_info()}")
    print(f"Разработчик: {developer.get_info()}")
    print(f"Продавец: {salesperson.get_info()}")


def demonstrate_abstract_factory():
    """Демонстрация Abstract Factory паттерна."""
    print("\n=== 3. Abstract Factory (Абстрактная фабрика) ===")
    
    # Создаем IT-компанию
    tech_factory = TechCompanyFactory()
    tech_company = tech_factory.create_company("TechCorp")
    print(f"Создана IT-компания: {tech_company}")
    print(f"Отделы: {[d.name for d in tech_company.get_departments()]}")
    print(f"Проекты: {[p.name for p in tech_company.get_projects()]}")
    
    # Создаем торговую компанию
    sales_factory = SalesCompanyFactory()
    sales_company = sales_factory.create_company("SalesCorp")
    print(f"\nСоздана торговая компания: {sales_company}")
    print(f"Отделы: {[d.name for d in sales_company.get_departments()]}")
    print(f"Проекты: {[p.name for p in sales_company.get_projects()]}")


def demonstrate_builder():
    """Демонстрация Builder паттерна."""
    print("\n=== 4. Builder (Строитель) ===")
    
    # Создаем разработчика через Builder
    developer = (EmployeeBuilder()
                .set_id(101)
                .set_name("John Doe")
                .set_department("DEV")
                .set_base_salary(5000)
                .set_type("developer")
                .set_skills(["Python", "Java"])
                .set_seniority("senior")
                .build())
    
    print(f"Разработчик через Builder: {developer.get_info()}")
    
    # Создаем менеджера через Builder
    manager = (EmployeeBuilder()
              .set_id(102)
              .set_name("Jane Smith")
              .set_department("MANAGEMENT")
              .set_base_salary(7000)
              .set_type("manager")
              .set_bonus(2000)
              .build())
    
    print(f"Менеджер через Builder: {manager.get_info()}")


def demonstrate_adapter():
    """Демонстрация Adapter паттерна."""
    print("\n=== 5. Adapter (Адаптер) ===")
    
    # Создаем внешний сервис
    external_service = ExternalSalaryService()
    adapter = SalaryCalculatorAdapter(external_service)
    
    # Создаем сотрудника
    developer = Developer(1, "Test Dev", "DEV", 50000, ["Python"], "senior")
    
    # Используем адаптер для расчета зарплаты
    salary = adapter.calculate_salary(developer)
    print(f"Зарплата через адаптер: {salary}")
    print(f"Зарплата напрямую: {developer.calculate_salary()}")


def demonstrate_decorator():
    """Демонстрация Decorator паттерна."""
    print("\n=== 6. Decorator (Декоратор) ===")
    
    # Создаем базового сотрудника
    developer = Developer(1, "Decorated Dev", "DEV", 50000, ["Python"], "middle")
    print(f"Исходный сотрудник: зарплата = {developer.calculate_salary()}")
    
    # Добавляем бонус
    decorated_with_bonus = BonusDecorator(developer, 5000)
    print(f"С бонусом: зарплата = {decorated_with_bonus.calculate_salary()}")
    
    # Добавляем обучение
    decorated_with_training = TrainingDecorator(decorated_with_bonus, 2000)
    decorated_with_training.add_training("Python Advanced")
    print(f"С обучением: {decorated_with_training.get_info()}")
    
    # Добавляем производительность
    decorated_with_performance = PerformanceDecorator(decorated_with_training, 1.1)
    print(f"С производительностью: зарплата = {decorated_with_performance.calculate_salary()}")


def demonstrate_facade():
    """Демонстрация Facade паттерна."""
    print("\n=== 7. Facade (Фасад) ===")
    
    # Создаем компанию
    company = Company("TestCompany")
    dept = company.get_departments()[0] if company.get_departments() else None
    if not dept:
        from src.core.department import Department
        dept = Department("Development")
        company.add_department(dept)
    
    # Создаем фасад
    facade = CompanyFacade(company)
    
    # Используем упрощенный интерфейс
    developer = Developer(1, "Facade Dev", "Development", 50000, ["Python"], "senior")
    facade.hire_employee(developer, "Development")
    
    print(f"Статистика компании: {facade.get_company_statistics()}")
    print(f"Зарплата отдела: {facade.calculate_department_salary('Development')}")


def demonstrate_observer():
    """Демонстрация Observer паттерна."""
    print("\n=== 8. Observer (Наблюдатель) ===")
    
    # Создаем систему уведомлений
    notification_system = NotificationSystem()
    
    # Создаем наблюдаемого сотрудника
    developer = Developer(1, "Observed Dev", "DEV", 50000, ["Python"], "senior")
    observable_employee = ObservableEmployee(developer)
    
    # Подписываемся на уведомления
    observable_employee.attach(notification_system)
    
    # Изменяем зарплату (должно прийти уведомление)
    print("Изменяем зарплату...")
    observable_employee.set_base_salary(60000)
    
    # Просматриваем уведомления
    notifications = notification_system.get_notifications()
    print(f"Количество уведомлений: {len(notifications)}")


def demonstrate_strategy():
    """Демонстрация Strategy паттерна."""
    print("\n=== 9. Strategy (Стратегия) ===")
    
    developer = Developer(1, "Strategy Dev", "DEV", 50000, ["Python"], "senior")
    
    # Используем разные стратегии
    performance_strategy = PerformanceBonusStrategy(0.1)
    seniority_strategy = SeniorityBonusStrategy()
    project_strategy = ProjectBonusStrategy(2000)
    
    context = BonusContext(performance_strategy)
    bonus1 = context.calculate_bonus(developer)
    print(f"Бонус по производительности: {bonus1}")
    
    context.set_strategy(seniority_strategy)
    bonus2 = context.calculate_bonus(developer)
    print(f"Бонус по стажу: {bonus2}")
    
    context.set_strategy(project_strategy)
    bonus3 = context.calculate_bonus(developer, project_count=2)
    print(f"Бонус по проектам (2 проекта): {bonus3}")


def demonstrate_command():
    """Демонстрация Command паттерна."""
    print("\n=== 10. Command (Команда) ===")
    
    # Создаем компанию и отдел
    company = Company("CommandCompany")
    from src.core.department import Department
    dept = Department("Development")
    company.add_department(dept)
    
    # Создаем вызывающий объект
    invoker = CommandInvoker()
    
    # Создаем команды
    developer = Developer(1, "Command Dev", "Development", 50000, ["Python"], "senior")
    hire_command = HireEmployeeCommand(developer, company, "Development")
    
    # Выполняем команду
    print("Выполняем команду найма...")
    invoker.execute_command(hire_command)
    print(f"Сотрудников в отделе: {len(dept)}")
    
    # Отменяем команду
    print("Отменяем команду...")
    invoker.undo()
    print(f"Сотрудников в отделе после отмены: {len(dept)}")


def demonstrate_repository():
    """Демонстрация Repository паттерна."""
    print("\n=== 11. Repository (Репозиторий) ===")
    
    # Создаем репозиторий
    repo = EmployeeRepository()
    
    # Добавляем сотрудников
    developer = Developer(1, "Repo Dev", "DEV", 50000, ["Python"], "senior")
    manager = Manager(2, "Repo Manager", "MANAGEMENT", 70000, 20000)
    
    repo.add(developer)
    repo.add(manager)
    
    # Получаем всех
    all_employees = repo.get_all()
    print(f"Всего сотрудников в репозитории: {len(all_employees)}")
    
    # Получаем по ID
    found = repo.get_by_id(1)
    print(f"Найден сотрудник: {found.name if found else 'не найден'}")


def demonstrate_unit_of_work():
    """Демонстрация Unit of Work паттерна."""
    print("\n=== 12. Unit of Work ===")
    
    # Создаем Unit of Work
    uow = UnitOfWork()
    
    # Регистрируем изменения
    developer = Developer(1, "UOW Dev", "DEV", 50000, ["Python"], "senior")
    manager = Manager(2, "UOW Manager", "MANAGEMENT", 70000, 20000)
    
    uow.register_new_employee(developer)
    uow.register_new_employee(manager)
    
    # Применяем все изменения атомарно
    print("Применяем изменения...")
    uow.commit()
    
    # Проверяем результат
    all_employees = uow.employees.get_all()
    print(f"Сотрудников после commit: {len(all_employees)}")


def demonstrate_specification():
    """Демонстрация Specification паттерна."""
    print("\n=== 13. Specification (Спецификация) ===")
    
    # Создаем сотрудников
    employees = [
        Developer(1, "Dev1", "DEV", 50000, ["Python", "Java"], "senior"),
        Developer(2, "Dev2", "DEV", 40000, ["Python"], "middle"),
        Manager(3, "Manager1", "MANAGEMENT", 70000, 20000),
        Developer(4, "Dev3", "QA", 45000, ["Java"], "senior")
    ]
    
    # Создаем репозиторий со спецификациями
    spec_repo = SpecificationRepository(employees)
    
    # Простые спецификации
    high_salary_spec = SalarySpecification(min_salary=50000)
    dev_spec = DepartmentSpecification("DEV")
    python_spec = SkillSpecification(["Python"])
    
    # Комбинированные спецификации
    combined_spec = high_salary_spec & dev_spec & python_spec
    
    # Находим сотрудников
    high_paid_devs = spec_repo.find_by_specification(combined_spec)
    print(f"Высокооплачиваемые Python-разработчики в DEV: {len(high_paid_devs)}")
    for emp in high_paid_devs:
        print(f"  - {emp.name}")


def main():
    """Главная функция для демонстрации всех паттернов."""
    print("=" * 60)
    print("ДЕМОНСТРАЦИЯ ПАТТЕРНОВ ПРОЕКТИРОВАНИЯ")
    print("=" * 60)
    
    demonstrate_singleton()
    demonstrate_factory_method()
    demonstrate_abstract_factory()
    demonstrate_builder()
    demonstrate_adapter()
    demonstrate_decorator()
    demonstrate_facade()
    demonstrate_observer()
    demonstrate_strategy()
    demonstrate_command()
    demonstrate_repository()
    demonstrate_unit_of_work()
    demonstrate_specification()
    
    print("\n" + "=" * 60)
    print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("=" * 60)


if __name__ == "__main__":
    main()

