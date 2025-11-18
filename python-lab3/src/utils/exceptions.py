"""Кастомные исключения для системы учета сотрудников."""


class EmployeeNotFoundError(Exception):
    """Исключение при отсутствии сотрудника."""
    pass


class DepartmentNotFoundError(Exception):
    """Исключение при отсутствии отдела."""
    pass


class ProjectNotFoundError(Exception):
    """Исключение при отсутствии проекта."""
    pass


class InvalidStatusError(Exception):
    """Исключение при невалидном статусе."""
    pass


class DuplicateIdError(Exception):
    """Исключение при дублировании ID."""
    pass

