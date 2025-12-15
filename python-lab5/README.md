# Лабораторная работа №5: Применение паттернов проектирования

## Описание

Данная лабораторная работа представляет собой комплексный рефакторинг системы учета сотрудников из ЛР №3 с применением 13+ паттернов проектирования.

## Структура проекта

```
python-lab5/
├── src/                          # Исходный код системы
│   ├── core/                     # Основные классы системы
│   ├── employees/                # Классы сотрудников
│   ├── factories/                # Фабрики (Factory Method, Abstract Factory)
│   ├── patterns/                 # Реализации паттернов проектирования
│   │   ├── singleton.py         # Singleton
│   │   ├── builder.py           # Builder
│   │   ├── adapter.py           # Adapter
│   │   ├── decorator.py         # Decorator
│   │   ├── facade.py            # Facade
│   │   ├── observer.py          # Observer
│   │   ├── strategy.py          # Strategy
│   │   ├── command.py           # Command
│   │   ├── repository.py        # Repository
│   │   ├── unit_of_work.py      # Unit of Work
│   │   └── specification.py     # Specification
│   ├── database/                 # Работа с базой данных
│   └── utils/                    # Вспомогательные модули
├── examples/                     # Примеры использования
│   └── demo_patterns.py         # Демонстрация всех паттернов
├── tests/                        # Тесты
└── Отчёт.md                      # Отчёт по лабораторной работе
```

## Реализованные паттерны

### Порождающие паттерны
1. **Singleton** - `DatabaseConnection` для управления подключением к БД
2. **Factory Method** - Рефакторинг `EmployeeFactory` с абстрактными и конкретными фабриками
3. **Abstract Factory** - `TechCompanyFactory` и `SalesCompanyFactory` для создания компаний
4. **Builder** - `EmployeeBuilder` для пошагового создания сотрудников

### Структурные паттерны
5. **Adapter** - `SalaryCalculatorAdapter` для интеграции внешней системы расчета зарплат
6. **Decorator** - `BonusDecorator`, `TrainingDecorator`, `PerformanceDecorator` для добавления функциональности
7. **Facade** - `CompanyFacade` для упрощения работы с компанией

### Поведенческие паттерны
8. **Observer** - `NotificationSystem` для уведомлений об изменениях
9. **Strategy** - Стратегии расчета бонусов (`PerformanceBonusStrategy`, `SeniorityBonusStrategy`, `ProjectBonusStrategy`)
10. **Command** - Команды для операций (`HireEmployeeCommand`, `FireEmployeeCommand`, `UpdateSalaryCommand`)

### Комбинированные паттерны
11. **Repository** - Репозитории для работы с данными (`EmployeeRepository`, `DepartmentRepository`, `ProjectRepository`)
12. **Unit of Work** - Управление транзакциями
13. **Specification** - Спецификации для фильтрации сотрудников

## Запуск демонстрации

```bash
python examples/demo_patterns.py
```

## Требования

- Python 3.8+
- Стандартная библиотека Python

## Автор

Пахомов Давид Вадимович
Группа: ПИН-Б-О-24-2


