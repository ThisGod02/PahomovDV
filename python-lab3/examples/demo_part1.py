"""Демонстрация части 4.1: Инкапсуляция."""

import sys
import os

# Добавляем корневую директорию проекта в путь
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.core.employee import Employee


def main():
    print("=" * 60)
    print("Демонстрация части 4.1: Инкапсуляция")
    print("=" * 60)
    
    # Создание объектов Employee
    print("\n1. Создание сотрудников:")
    emp1 = Employee(1, "Иван Иванов", "IT", 50000.0)
    emp2 = Employee(2, "Мария Петрова", "HR", 45000.0)
    print(f"   {emp1}")
    print(f"   {emp2}")
    
    # Демонстрация работы с свойствами
    print("\n2. Работа с свойствами (геттеры):")
    print(f"   ID сотрудника 1: {emp1.id}")
    print(f"   Имя сотрудника 1: {emp1.name}")
    print(f"   Отдел сотрудника 1: {emp1.department}")
    print(f"   Базовая зарплата сотрудника 1: {emp1.base_salary}")
    
    # Изменение через сеттеры
    print("\n3. Изменение через сеттеры:")
    emp1.name = "Иван Петров"
    emp1.base_salary = 55000.0
    print(f"   Обновленный сотрудник 1: {emp1}")
    
    # Демонстрация валидации
    print("\n4. Демонстрация валидации:")
    try:
        emp3 = Employee(-1, "Тест", "IT", 10000)  # Невалидный ID
    except ValueError as e:
        print(f"   Ошибка при создании с невалидным ID: {e}")
    
    try:
        emp1.id = -5  # Невалидный ID через сеттер
    except ValueError as e:
        print(f"   Ошибка при установке невалидного ID: {e}")
    
    try:
        emp1.name = ""  # Пустое имя
    except ValueError as e:
        print(f"   Ошибка при установке пустого имени: {e}")
    
    try:
        emp1.base_salary = -1000  # Отрицательная зарплата
    except ValueError as e:
        print(f"   Ошибка при установке отрицательной зарплаты: {e}")
    
    print("\n" + "=" * 60)
    print("Демонстрация завершена!")
    print("=" * 60)


if __name__ == "__main__":
    main()

