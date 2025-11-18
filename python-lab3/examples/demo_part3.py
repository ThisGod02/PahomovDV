"""Демонстрация части 4.3: Полиморфизм и магические методы."""

import sys
import os
from functools import cmp_to_key

# Добавляем корневую директорию проекта в путь
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.core.employee import Employee
from src.core.department import Department
from src.employees.manager import Manager
from src.employees.developer import Developer
from src.employees.salesperson import Salesperson
from src.utils.comparators import compare_by_name, compare_by_salary, compare_by_department_and_name


def main():
    print("=" * 60)
    print("Демонстрация части 4.3: Полиморфизм и магические методы")
    print("=" * 60)
    
    # Создание сотрудников
    print("\n1. Создание сотрудников:")
    emp1 = Employee(1, "Анна", "IT", 50000.0)
    emp2 = Manager(2, "Борис", "MANAGEMENT", 70000.0, 20000.0)
    emp3 = Developer(3, "Виктор", "DEV", 50000.0, ["Python", "Java"], "senior")
    emp4 = Salesperson(4, "Галина", "SALES", 40000.0, 0.1, 80000.0)
    
    # Создание отдела
    print("\n2. Создание и заполнение отдела:")
    dept = Department("Разработка")
    dept.add_employee(emp1)
    dept.add_employee(emp2)
    dept.add_employee(emp3)
    dept.add_employee(emp4)
    print(f"   {dept}")
    print(f"   Количество сотрудников: {len(dept)}")
    
    # Полиморфизм в расчете зарплат
    print("\n3. Полиморфизм в расчете общей зарплаты:")
    total = dept.calculate_total_salary()
    print(f"   Общая зарплата отдела: {total}")
    
    # Статистика по типам сотрудников
    print("\n4. Статистика по типам сотрудников:")
    counts = dept.get_employee_count()
    for emp_type, count in counts.items():
        print(f"   {emp_type}: {count}")
    
    # Магические методы для сотрудников
    print("\n5. Магические методы для сотрудников:")
    print(f"   emp1 == emp2: {emp1 == emp2}")
    print(f"   emp1 == emp1: {emp1 == emp1}")
    print(f"   emp1 < emp2 (по зарплате): {emp1 < emp2}")
    print(f"   emp1 + emp2 (сумма зарплат): {emp1 + emp2}")
    
    # Суммирование через sum()
    print("\n6. Суммирование зарплат через sum():")
    employees = [emp1, emp2, emp3, emp4]
    total_salary = sum(employees)
    print(f"   Сумма зарплат через sum(): {total_salary}")
    
    # Магические методы для отдела
    print("\n7. Магические методы для отдела:")
    print(f"   Количество сотрудников (len): {len(dept)}")
    print(f"   Первый сотрудник (dept[0]): {dept[0].name}")
    print(f"   emp1 in dept: {emp1 in dept}")
    print(f"   emp1 not in dept: {emp1 not in dept}")
    
    # Итерация по отделу
    print("\n8. Итерация по отделу:")
    print("   Сотрудники в отделе:")
    for emp in dept:
        print(f"      - {emp.name} ({emp.__class__.__name__})")
    
    # Итерация по стеку технологий разработчика
    print("\n9. Итерация по стеку технологий разработчика:")
    print(f"   Технологии {emp3.name}:")
    for skill in emp3:
        print(f"      - {skill}")
    
    # Сортировка сотрудников
    print("\n10. Сортировка сотрудников:")
    print("    По имени:")
    sorted_by_name = sorted(employees, key=lambda e: e.name)
    for emp in sorted_by_name:
        print(f"       {emp.name}")
    
    print("    По зарплате:")
    sorted_by_salary = sorted(employees, key=lambda e: e.calculate_salary(), reverse=True)
    for emp in sorted_by_salary:
        print(f"       {emp.name}: {emp.calculate_salary()}")
    
    print("    По отделу и имени (через компаратор):")
    sorted_by_dept_name = sorted(employees, key=cmp_to_key(compare_by_department_and_name))
    for emp in sorted_by_dept_name:
        print(f"       {emp.department} - {emp.name}")
    
    # Сериализация и десериализация
    print("\n11. Сериализация и десериализация:")
    filename = "data/json/department_demo.json"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    dept.save_to_file(filename)
    print(f"    Отдел сохранен в {filename}")
    
    loaded_dept = Department.load_from_file(filename)
    print(f"    Отдел загружен: {loaded_dept}")
    print(f"    Количество сотрудников в загруженном отделе: {len(loaded_dept)}")
    
    # Поиск сотрудника
    print("\n12. Поиск сотрудника по ID:")
    found = dept.find_employee_by_id(3)
    if found:
        print(f"    Найден: {found.get_info()}")
    
    print("\n" + "=" * 60)
    print("Демонстрация завершена!")
    print("=" * 60)


if __name__ == "__main__":
    main()

