"""Singleton для подключения к базе данных SQLite."""

import sqlite3
from typing import Optional


class DatabaseConnection:
    """
    Singleton для управления подключением к базе данных SQLite.
    
    Гарантирует единственное подключение к БД в рамках приложения.
    """
    
    _instance: Optional['DatabaseConnection'] = None
    _connection: Optional[sqlite3.Connection] = None
    
    def __new__(cls):
        """
        Создание единственного экземпляра класса.
        
        Returns:
            Единственный экземпляр DatabaseConnection
        """
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Инициализация подключения (вызывается только один раз)."""
        if self._connection is None:
            self._connection = None  # Подключение будет создано при первом вызове get_connection()
    
    @classmethod
    def get_instance(cls) -> 'DatabaseConnection':
        """
        Получить единственный экземпляр класса.
        
        Returns:
            Экземпляр DatabaseConnection
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def get_connection(self, db_path: str = ":memory:") -> sqlite3.Connection:
        """
        Получить подключение к базе данных.
        
        Args:
            db_path: Путь к файлу БД (по умолчанию in-memory)
        
        Returns:
            Объект подключения к SQLite
        """
        if self._connection is None:
            self._connection = sqlite3.connect(db_path)
            self._connection.row_factory = sqlite3.Row
            # Создаем таблицы при первом подключении
            self._create_tables()
        return self._connection
    
    def close_connection(self) -> None:
        """Закрыть подключение к базе данных."""
        if self._connection is not None:
            self._connection.close()
            self._connection = None
    
    def _create_tables(self) -> None:
        """Создать необходимые таблицы в БД."""
        if self._connection is None:
            return
        
        cursor = self._connection.cursor()
        
        # Таблица сотрудников
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                base_salary REAL NOT NULL,
                employee_type TEXT NOT NULL,
                bonus REAL,
                tech_stack TEXT,
                seniority_level TEXT,
                commission_rate REAL,
                sales_volume REAL
            )
        """)
        
        # Таблица отделов
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS departments (
                name TEXT PRIMARY KEY
            )
        """)
        
        # Таблица проектов
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                project_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                deadline TEXT NOT NULL,
                status TEXT NOT NULL
            )
        """)
        
        self._connection.commit()
    
    def reset_instance(self) -> None:
        """
        Сбросить экземпляр (для тестирования).
        
        Внимание: Используется только в тестах!
        """
        if self._connection is not None:
            self._connection.close()
        self._connection = None
        DatabaseConnection._instance = None

