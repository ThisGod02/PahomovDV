"""Функции-компараторы для сортировки сотрудников."""

from src.core.abstract_employee import AbstractEmployee


def compare_by_name(emp1: AbstractEmployee, emp2: AbstractEmployee) -> int:
    """
    Компаратор для сортировки по имени.
    
    Args:
        emp1: Первый сотрудник
        emp2: Второй сотрудник
    
    Returns:
        -1 если emp1 < emp2, 0 если равны, 1 если emp1 > emp2
    """
    name1 = getattr(emp1, 'name', '')
    name2 = getattr(emp2, 'name', '')
    if name1 < name2:
        return -1
    elif name1 > name2:
        return 1
    return 0


def compare_by_salary(emp1: AbstractEmployee, emp2: AbstractEmployee) -> int:
    """
    Компаратор для сортировки по зарплате.
    
    Args:
        emp1: Первый сотрудник
        emp2: Второй сотрудник
    
    Returns:
        -1 если emp1 < emp2, 0 если равны, 1 если emp1 > emp2
    """
    salary1 = emp1.calculate_salary()
    salary2 = emp2.calculate_salary()
    if salary1 < salary2:
        return -1
    elif salary1 > salary2:
        return 1
    return 0


def compare_by_department_and_name(emp1: AbstractEmployee, emp2: AbstractEmployee) -> int:
    """
    Компаратор для сортировки по отделу, затем по имени.
    
    Args:
        emp1: Первый сотрудник
        emp2: Второй сотрудник
    
    Returns:
        -1 если emp1 < emp2, 0 если равны, 1 если emp1 > emp2
    """
    dept1 = getattr(emp1, 'department', '')
    dept2 = getattr(emp2, 'department', '')
    
    if dept1 < dept2:
        return -1
    elif dept1 > dept2:
        return 1
    
    # Если отделы равны, сравниваем по имени
    return compare_by_name(emp1, emp2)





