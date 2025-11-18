"""Демонстрация части 4.2: Наследование и абстракция."""

import sys
import os

# Добавляем корневую директорию проекта в путь
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.core.employee import Employee
from src.employees.manager import Manager
from src.employees.developer import Developer
from src.employees.salesperson import Salesperson
from src.factories.employee_factory import EmployeeFactory


def main():
    print("=" * 60)
    print("Демонстрация части 4.2: Наследование и абстракция")
    print("=" * 60)
    
    # Создание сотрудников разных типов
    print("\n1. Создание сотрудников разных типов:")
    employee = Employee(1, "Обычный Сотрудник", "ADMIN", 30000.0)
    manager = Manager(2, "Алиса Менеджер", "MANAGEMENT", 70000.0, 20000.0)
    developer = Developer(3, "Боб Разработчик", "DEV", 50000.0, 
                         ["Python", "Java", "SQL"], "senior")
    salesperson = Salesperson(4, "Чарли Продавец", "SALES", 40000.0, 0.15, 100000.0)
    
    print(f"   {employee.get_info()}")
    print(f"   {manager.get_info()}")
    print(f"   {developer.get_info()}")
    print(f"   {salesperson.get_info()}")
    
    # Демонстрация расчета зарплат
    print("\n2. Расчет итоговых зарплат:")
    print(f"   Обычный сотрудник: {employee.calculate_salary()}")
    print(f"   Менеджер: {manager.calculate_salary()}")
    print(f"   Разработчик (senior): {developer.calculate_salary()}")
    print(f"   Продавец: {salesperson.calculate_salary()}")
    
    # Демонстрация работы с Developer
    print("\n3. Работа с разработчиком:")
    print(f"   Стек технологий: {developer.tech_stack}")
    developer.add_skill("Docker")
    print(f"   После добавления Docker: {developer.tech_stack}")
    print(f"   Итерация по стеку технологий:")
    for skill in developer:
        print(f"      - {skill}")
    
    # Демонстрация работы с Salesperson
    print("\n4. Работа с продавцом:")
    print(f"   Объем продаж до обновления: {salesperson.sales_volume}")
    salesperson.update_sales(50000.0)
    print(f"   Объем продаж после обновления: {salesperson.sales_volume}")
    print(f"   Новая зарплата: {salesperson.calculate_salary()}")
    
    # Демонстрация фабрики
    print("\n5. Демонстрация фабрики сотрудников:")
    emp1 = EmployeeFactory.create_employee(
        "manager",
        id=10,
        name="Фабричный Менеджер",
        department="MANAGEMENT",
        base_salary=60000.0,
        bonus=15000.0
    )
    emp2 = EmployeeFactory.create_employee(
        "developer",
        id=11,
        name="Фабричный Разработчик",
        department="DEV",
        base_salary=45000.0,
        tech_stack=["Python", "JavaScript"],
        seniority_level="middle"
    )
    print(f"   {emp1.get_info()}")
    print(f"   {emp2.get_info()}")
    
    # Демонстрация полиморфизма в коллекции
    print("\n6. Полиморфизм в коллекции:")
    employees_list = [employee, manager, developer, salesperson, emp1, emp2]
    print("   Информация о всех сотрудниках:")
    for emp in employees_list:
        print(f"      {emp.get_info()}")
    
    total_salary = sum(emp.calculate_salary() for emp in employees_list)
    print(f"\n   Общая сумма зарплат всех сотрудников: {total_salary}")
    
    print("\n" + "=" * 60)
    print("Демонстрация завершена!")
    print("=" * 60)


if __name__ == "__main__":
    main()

