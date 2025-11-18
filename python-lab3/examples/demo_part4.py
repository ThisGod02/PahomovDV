"""Демонстрация части 4.4: Композиция и агрегация."""

import sys
import os

# Добавляем корневую директорию проекта в путь
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.core.company import Company
from src.core.department import Department
from src.core.project import Project
from src.employees.manager import Manager
from src.employees.developer import Developer
from src.employees.salesperson import Salesperson
from src.utils.exceptions import (
    EmployeeNotFoundError, DepartmentNotFoundError, ProjectNotFoundError,
    InvalidStatusError, DuplicateIdError
)


def main():
    print("=" * 60)
    print("Демонстрация части 4.4: Композиция и агрегация")
    print("=" * 60)
    
    # Создание компании
    print("\n1. Создание компании:")
    company = Company("TechInnovations")
    print(f"   {company}")
    
    # Создание отделов
    print("\n2. Создание отделов:")
    dev_department = Department("Development")
    sales_department = Department("Sales")
    
    company.add_department(dev_department)
    company.add_department(sales_department)
    print(f"   Отделы созданы и добавлены в компанию")
    print(f"   Количество отделов: {len(company.get_departments())}")
    
    # Создание сотрудников
    print("\n3. Создание сотрудников:")
    manager = Manager(1, "Алиса Джонсон", "DEV", 70000.0, 20000.0)
    developer = Developer(2, "Боб Смит", "DEV", 50000.0, 
                         ["Python", "SQL", "Docker"], "senior")
    salesperson = Salesperson(3, "Чарли Браун", "SAL", 40000.0, 0.15, 50000.0)
    
    dev_department.add_employee(manager)
    dev_department.add_employee(developer)
    sales_department.add_employee(salesperson)
    
    print(f"   Сотрудники созданы и добавлены в отделы")
    print(f"   Сотрудников в отделе Development: {len(dev_department)}")
    print(f"   Сотрудников в отделе Sales: {len(sales_department)}")
    
    # Создание проектов
    print("\n4. Создание проектов:")
    ai_project = Project(101, "AI Platform", "Разработка AI системы", 
                        "2024-12-31", "active")
    web_project = Project(102, "Web Portal", "Создание веб-портала", 
                          "2024-09-30", "planning")
    
    company.add_project(ai_project)
    company.add_project(web_project)
    print(f"   Проекты созданы и добавлены в компанию")
    print(f"   Количество проектов: {len(company.get_projects())}")
    
    # Формирование команд проектов (композиция)
    print("\n5. Формирование команд проектов (композиция):")
    ai_project.add_team_member(developer)
    ai_project.add_team_member(manager)
    web_project.add_team_member(developer)
    
    print(f"   Команда проекта '{ai_project.name}': {ai_project.get_team_size()} человек")
    print(f"   Команда проекта '{web_project.name}': {web_project.get_team_size()} человек")
    print(f"   Бюджет команды AI Platform: {ai_project.calculate_total_salary()}")
    
    # Информация о проектах
    print("\n6. Информация о проектах:")
    for proj in company.get_projects():
        print(f"   {proj.get_project_info()}")
    
    # Финансовые показатели
    print("\n7. Финансовые показатели компании:")
    total_cost = company.calculate_total_monthly_cost()
    print(f"   Общие месячные затраты на зарплаты: {total_cost}")
    
    # Статистика по отделам
    print("\n8. Статистика по отделам:")
    stats = company.get_department_stats()
    for dept_name, dept_stats in stats.items():
        print(f"   {dept_name}:")
        print(f"      Сотрудников: {dept_stats['employee_count']}")
        print(f"      Общая зарплата: {dept_stats['total_salary']}")
        print(f"      Типы сотрудников: {dept_stats['employee_types']}")
    
    # Анализ бюджетов проектов
    print("\n9. Анализ бюджетов проектов:")
    budget_analysis = company.get_project_budget_analysis()
    print(f"   Всего проектов: {budget_analysis['total_projects']}")
    print(f"   Общий бюджет: {budget_analysis['total_budget']}")
    print(f"   По статусам:")
    for status, info in budget_analysis['by_status'].items():
        print(f"      {status}: {info['count']} проектов, бюджет: {info['total_budget']}")
    
    # Поиск перегруженных сотрудников
    print("\n10. Поиск перегруженных сотрудников:")
    overloaded = company.find_overloaded_employees()
    if overloaded:
        for emp in overloaded:
            print(f"    {emp.name} участвует в нескольких проектах")
    else:
        print("    Перегруженных сотрудников не найдено")
    
    # Назначение сотрудника на проект
    print("\n11. Назначение сотрудника на проект:")
    # Менеджер уже в команде AI Platform, попробуем добавить продавца на новый проект
    # Сначала создадим новый проект
    marketing_project = Project(103, "Marketing Campaign", "Маркетинговая кампания", 
                               "2024-11-30", "planning")
    company.add_project(marketing_project)
    # Теперь назначим продавца на маркетинговый проект
    company.assign_employee_to_project(3, 103)  # Продавец на маркетинговый проект
    print(f"    Продавец назначен на проект Marketing Campaign")
    print(f"    Команда проекта Marketing Campaign: {marketing_project.get_team_size()} человек")
    
    # Проверка доступности сотрудника
    print("\n12. Проверка доступности сотрудников:")
    for emp_id in [1, 2, 3]:
        available = company.check_employee_availability(emp_id)
        emp = company.find_employee_by_id(emp_id)
        print(f"    {emp.name if emp else 'Не найден'}: {'Доступен' if available else 'Перегружен'}")
    
    # Валидация и обработка ошибок
    print("\n13. Демонстрация валидации и обработки ошибок:")
    
    try:
        invalid_project = Project(101, "Test", "Test", "2024-12-31", "invalid_status")
    except InvalidStatusError as e:
        print(f"    Ошибка при создании проекта с невалидным статусом: {e}")
    
    try:
        company.add_project(Project(101, "Duplicate", "Test", "2024-12-31", "planning"))
    except DuplicateIdError as e:
        print(f"    Ошибка при добавлении проекта с дублирующимся ID: {e}")
    
    try:
        company.remove_department("Development")
    except ValueError as e:
        print(f"    Ошибка при удалении отдела с сотрудниками: {e}")
    
    # Сериализация компании
    print("\n14. Сериализация компании:")
    json_filename = "data/json/company_demo.json"
    os.makedirs(os.path.dirname(json_filename), exist_ok=True)
    company.save_to_json(json_filename)
    print(f"    Компания сохранена в {json_filename}")
    
    # Экспорт отчетов
    print("\n15. Экспорт отчетов:")
    csv_employees = "data/csv/employees_report.csv"
    csv_projects = "data/csv/projects_report.csv"
    os.makedirs(os.path.dirname(csv_employees), exist_ok=True)
    
    company.export_employees_csv(csv_employees)
    company.export_projects_csv(csv_projects)
    print(f"    Отчет по сотрудникам сохранен в {csv_employees}")
    print(f"    Отчет по проектам сохранен в {csv_projects}")
    
    # Загрузка компании из файла
    print("\n16. Загрузка компании из файла:")
    loaded_company = Company.load_from_json(json_filename)
    print(f"    Компания загружена: {loaded_company}")
    print(f"    Отделов: {len(loaded_company.get_departments())}")
    print(f"    Проектов: {len(loaded_company.get_projects())}")
    
    # Перенос сотрудника между отделами
    print("\n17. Перенос сотрудника между отделами:")
    try:
        company.transfer_employee(2, "Development", "Sales")
        print(f"    Сотрудник перенесен из Development в Sales")
        print(f"    Сотрудников в Development: {len(dev_department)}")
        print(f"    Сотрудников в Sales: {len(sales_department)}")
    except Exception as e:
        print(f"    Ошибка при переносе: {e}")
    
    print("\n" + "=" * 60)
    print("Демонстрация завершена!")
    print("=" * 60)


if __name__ == "__main__":
    main()

