### **Лабораторная работа №8: Тестирование программного обеспечения**

**Тема:** Тестирование системы учета сотрудников на основе принципов ООП и патернов.

**Цель работы:** Освоить основы модульного тестирования, научиться писать unit-тесты для классов и методов, использовать фреймворк `pytest`, применять техники изоляции зависимостей с помощью моков и стабов.

**Стек технологий:**
- **Язык программирования:** Python 3.x
- **Фреймворк для тестирования:** `pytest`
- **Библиотека для моков:** `unittest.mock`
- **Инструменты:** Любая IDE (PyCharm, VSCode), Git.

---

### **Часть 1: Тестирование инкапсуляции и базового класса `Employee`**

**Цель:** Написать модульные тесты для класса `Employee`, проверяющие корректность инкапсуляции, валидации данных и работы методов.

**Задание:**

1. **Подготовка окружения:**
   - Установите `pytest`, если он не установлен:
     ```bash
     pip install pytest
     ```
   - Создайте файл `test_employee.py` для написания тестов.

2. **Тестирование конструктора и свойств:**
   - Напишите тест, который проверяет, что объект класса `Employee` корректно инициализируется с валидными данными.
   - Напишите тесты, которые проверяют, что сеттеры:
     - Вызывают исключение `ValueError` при попытке установки отрицательного значения для `id` или `base_salary`.
     - Вызывают исключение `ValueError` при попытке установки пустой строки для `name`.

3. **Тестирование методов:**
   - Напишите тест для метода `__str__`, который проверяет, что строковое представление объекта соответствует ожидаемому формату.
   - Напишите тест для метода `calculate_salary`, который проверяет, что зарплата обычного сотрудника равна базовой зарплате.

4. **Пример теста:**
   ```python
   import pytest
   from employee import Employee

   class TestEmployee:
       def test_employee_creation_valid_data(self):
           # Arrange
           emp = Employee(1, "Alice", "IT", 5000)

           # Assert
           assert emp.id == 1
           assert emp.name == "Alice"
           assert emp.department == "IT"
           assert emp.base_salary == 5000

       def test_employee_invalid_id_raises_error(self):
           # Assert
           with pytest.raises(ValueError):
               Employee(-1, "Alice", "IT", 5000)

       def test_employee_calculate_salary(self):
           # Arrange
           emp = Employee(1, "Alice", "IT", 5000)

           # Act
           salary = emp.calculate_salary()

           # Assert
           assert salary == 5000

       def test_employee_str_representation(self):
           # Arrange
           emp = Employee(1, "Alice", "IT", 5000)

           # Act
           result = str(emp)

           # Assert
           expected = "Сотрудник [id: 1, имя: Alice, отдел: IT, базовая зарплата: 5000]"
           assert result == expected
   ```

5. **Запуск тестов:**
   - Запустите тесты с помощью команды:
     ```bash
     pytest -v
     ```
   - Убедитесь, что все тесты проходят.

**Критерии оценки:**
- **Удовлетворительно:** Написаны тесты для конструктора и методов класса `Employee`.
- **Хорошо:** Добавлены тесты для проверки валидации данных в сеттерах.
- **Отлично:** Тесты покрывают все методы класса, включая крайние случаи, и используют параметризацию для проверки различных сценариев.

---

### **Часть 2: Тестирование наследования и абстрактных классов**

**Цель:** Написать модульные тесты для иерархии классов сотрудников, проверяющие корректность наследования, реализацию абстрактных методов и полиморфное поведение.

**Задание:**

1. **Тестирование абстрактного класса:**
   - Создайте файл `test_employees_hierarchy.py`
   - Напишите тесты, проверяющие, что:
     - Нельзя создать экземпляр `AbstractEmployee`
     - Классы-наследники корректно реализуют абстрактные методы
     - Вызов абстрактных методов у наследников работает корректно

2. **Тестирование класса Manager:**
   - Проверьте расчет зарплаты с учетом бонуса
   - Проверьте метод `get_info` на наличие информации о бонусе
   - Протестируйте сеттер для бонуса с валидацией

3. **Тестирование класса Developer:**
   - Проверьте расчет зарплаты с учетом уровня seniority
   - Протестируйте метод `add_skill`
   - Проверьте корректность работы с стеком технологий
   - Убедитесь, что метод `get_info` включает информацию о технологиях и уровне

4. **Тестирование класса Salesperson:**
   - Проверьте расчет зарплаты с учетом комиссии
   - Протестируйте метод `update_sales`
   - Убедитесь, что метод `get_info` включает информацию о комиссии и объеме продаж

5. **Пример теста для Manager:**
   ```python
   import pytest
   from employee import Manager, Developer, Salesperson

   class TestManager:
       def test_manager_salary_calculation(self):
           # Arrange
           manager = Manager(1, "John", "Management", 5000, 1000)
           
           # Act
           salary = manager.calculate_salary()
           
           # Assert
           assert salary == 6000

       def test_manager_get_info_includes_bonus(self):
           # Arrange
           manager = Manager(1, "John", "Management", 5000, 1000)
           
           # Act
           info = manager.get_info()
           
           # Assert
           assert "бонус: 1000" in info
           assert "итоговая зарплата: 6000" in info
   ```

6. **Тестирование фабрики сотрудников:**
   - Напишите тесты для `EmployeeFactory`
   - Проверьте создание сотрудников разных типов
   - Убедитесь, что передаваемые параметры корректно обрабатываются

7. **Параметризованные тесты:**
   - Используйте `@pytest.mark.parametrize` для тестирования разных сценариев расчета зарплат
   - Пример для Developer:
   ```python
   @pytest.mark.parametrize("level,expected_salary", [
       ("junior", 5000),
       ("middle", 7500),
       ("senior", 10000)
   ])
   def test_developer_salary_by_level(self, level, expected_salary):
       # Arrange
       dev = Developer(1, "Alice", "DEV", 5000, ["Python"], level)
       
       # Act & Assert
       assert dev.calculate_salary() == expected_salary
   ```

8. **Тестирование полиморфного поведения:**
   - Создайте тест, который демонстрирует работу с коллекцией разных типов сотрудников
   - Проверьте, что для каждого типа вызывается правильная реализация `calculate_salary`

**Критерии оценки:**
- **Удовлетворительно:** Написаны тесты для основных классов наследников
- **Хорошо:** Добавлены тесты для фабрики и параметризованные тесты
- **Отлично:** Полное покрытие тестами всей иерархии классов, включая крайние случаи и проверку полиморфного поведения

---

### **Часть 3: Тестирование полиморфизма и магических методов**

**Цель:** Написать комплексные тесты для проверки полиморфного поведения, перегрузки операторов и магических методов в системе учета сотрудников.

**Задание:**

1. **Тестирование класса Department:**
   - Создайте файл `test_department.py`
   - Напишите тесты для методов:
     - `add_employee`, `remove_employee`, `get_employees`
     - `calculate_total_salary` (полиморфное поведение)
     - `get_employee_count` (статистика по типам сотрудников)
     - `find_employee_by_id`

2. **Тестирование магических методов сотрудников:**
   - Проверьте корректность работы операторов сравнения:
   ```python
   def test_employee_equality(self):
       emp1 = Employee(1, "John", "IT", 5000)
       emp2 = Employee(1, "Jane", "HR", 4000)
       emp3 = Employee(2, "Bob", "IT", 5000)
       
       assert emp1 == emp2  # одинаковый ID
       assert emp1 != emp3  # разный ID
   ```

   - Проверьте операторы сравнения по зарплате:
   ```python
   def test_employee_salary_comparison(self):
       emp1 = Employee(1, "John", "IT", 5000)
       emp2 = Employee(2, "Jane", "HR", 6000)
       
       assert emp1 < emp2
       assert emp2 > emp1
   ```

   - Протестируйте сложение зарплат:
   ```python
   def test_employee_addition(self):
       emp1 = Employee(1, "John", "IT", 5000)
       emp2 = Employee(2, "Jane", "HR", 6000)
       
       assert emp1 + emp2 == 11000
   ```

3. **Тестирование магических методов Department:**
   - Проверьте работу `__len__`, `__getitem__`, `__contains__`:
   ```python
   def test_department_magic_methods(self):
       dept = Department("IT")
       emp = Employee(1, "John", "IT", 5000)
       
       dept.add_employee(emp)
       
       assert len(dept) == 1
       assert dept[0] == emp
       assert emp in dept
   ```

4. **Тестирование итерации:**
   - Проверьте итерацию по отделу:
   ```python
   def test_department_iteration(self):
       dept = Department("IT")
       employees = [Employee(i, f"Emp{i}", "IT", 5000) for i in range(3)]
       
       for emp in employees:
           dept.add_employee(emp)
       
       count = 0
       for employee in dept:
           count += 1
       
       assert count == 3
   ```

   - Проверьте итерацию по стеку технологий разработчика:
   ```python
   def test_developer_skills_iteration(self):
       dev = Developer(1, "John", "DEV", 5000, ["Python", "Java", "SQL"], "senior")
       
       skills = []
       for skill in dev:
           skills.append(skill)
       
       assert skills == ["Python", "Java", "SQL"]
   ```

5. **Тестирование сериализации:**
   - Напишите тесты для методов `to_dict` и `from_dict`:
   ```python
   def test_employee_serialization(self):
       emp = Employee(1, "John", "IT", 5000)
       
       # Сериализация
       data = emp.to_dict()
       
       # Десериализация
       new_emp = Employee.from_dict(data)
       
       assert new_emp.id == emp.id
       assert new_emp.name == emp.name
   ```

6. **Тестирование сортировки:**
   - Проверьте различные способы сортировки сотрудников:
   ```python
   def test_employee_sorting(self):
       employees = [
           Employee(3, "Charlie", "IT", 7000),
           Employee(1, "Alice", "HR", 5000),
           Employee(2, "Bob", "IT", 6000)
       ]
       
       # Сортировка по имени
       sorted_by_name = sorted(employees, key=lambda x: x.name)
       assert sorted_by_name[0].name == "Alice"
       
       # Сортировка по зарплате
       sorted_by_salary = sorted(employees, key=lambda x: x.calculate_salary())
       assert sorted_by_salary[0].calculate_salary() == 5000
   ```

7. **Интеграционные тесты:**
   - Создайте комплексные тесты, проверяющие взаимодействие всех компонентов:
   ```python
   def test_department_integration(self):
       dept = Department("Development")
       
       manager = Manager(1, "Alice", "DEV", 7000, 2000)
       developer = Developer(2, "Bob", "DEV", 5000, ["Python"], "senior")
       
       dept.add_employee(manager)
       dept.add_employee(developer)
       
       # Проверка полиморфного расчета зарплат
       total_salary = dept.calculate_total_salary()
       expected = manager.calculate_salary() + developer.calculate_salary()
       
       assert total_salary == expected
       assert dept.get_employee_count()["Manager"] == 1
       assert dept.get_employee_count()["Developer"] == 1
   ```

**Критерии оценки:**
- **Удовлетворительно:** Написаны тесты для основных магических методов и полиморфного поведения
- **Хорошо:** Добавлены тесты для сериализации и итерации
- **Отлично:** Полное покрытие всех магических методов, включая интеграционные тесты и проверку сортировки

---

### **Часть 4: Тестирование композиции, агрегации и сложных структур**

**Цель:** Написать тесты для проверки корректности работы композиции, агрегации, валидации данных и сложных бизнес-методов в системе компании.

**Задание:**

1. **Тестирование класса Project:**
   - Создайте файл `test_project_company.py`
   - Напишите тесты для методов управления командой проекта:
   ```python
   def test_project_team_management(self):
       project = Project(1, "AI Platform", "Разработка AI системы", "2024-12-31", "planning")
       dev = Developer(1, "John", "DEV", 5000, ["Python"], "senior")
       
       project.add_team_member(dev)
       assert len(project.get_team()) == 1
       assert project.get_team_size() == 1
       
       project.remove_team_member(1)
       assert len(project.get_team()) == 0
   ```

   - Проверьте расчет суммарной зарплаты команды:
   ```python
   def test_project_total_salary(self):
       project = Project(1, "AI Platform", "Разработка AI системы", "2024-12-31", "planning")
       manager = Manager(1, "Alice", "DEV", 7000, 2000)
       developer = Developer(2, "Bob", "DEV", 5000, ["Python"], "senior")
       
       project.add_team_member(manager)
       project.add_team_member(developer)
       
       total = project.calculate_total_salary()
       expected = manager.calculate_salary() + developer.calculate_salary()
       assert total == expected
   ```

2. **Тестирование класса Company:**
   - Проверьте методы управления отделами и проектами:
   ```python
   def test_company_department_management(self):
       company = Company("TechCorp")
       dept = Department("Development")
       
       company.add_department(dept)
       assert len(company.get_departments()) == 1
       
       company.remove_department("Development")
       assert len(company.get_departments()) == 0
   ```

   - Протестируйте поиск сотрудников по ID:
   ```python
   def test_company_find_employee(self):
       company = Company("TechCorp")
       dept = Department("Development")
       emp = Employee(1, "John", "DEV", 5000)
       
       dept.add_employee(emp)
       company.add_department(dept)
       
       found = company.find_employee_by_id(1)
       assert found is not None
       assert found.name == "John"
   ```

3. **Тестирование кастомных исключений:**
   - Проверьте генерацию исключений в различных сценариях:
   ```python
   def test_duplicate_employee_id_raises_error(self):
       company = Company("TechCorp")
       dept = Department("Development")
       emp1 = Employee(1, "John", "DEV", 5000)
       emp2 = Employee(1, "Jane", "DEV", 6000)  # Тот же ID
       
       dept.add_employee(emp1)
       company.add_department(dept)
       
       with pytest.raises(DuplicateIdError):
           dept.add_employee(emp2)
   ```

4. **Тестирование валидации данных:**
   - Проверьте валидацию статусов проектов:
   ```python
   @pytest.mark.parametrize("invalid_status", ["invalid", "done", "in_progress"])
   def test_project_invalid_status_raises_error(self, invalid_status):
       with pytest.raises(InvalidStatusError):
           Project(1, "Test", "Test", "2024-12-31", invalid_status)
   ```

5. **Тестирование управления зависимостями:**
   - Проверьте ограничения при удалении:
   ```python
   def test_cannot_delete_department_with_employees(self):
       company = Company("TechCorp")
       dept = Department("Development")
       emp = Employee(1, "John", "DEV", 5000)
       
       dept.add_employee(emp)
       company.add_department(dept)
       
       with pytest.raises(ValueError, match="Cannot delete department with employees"):
           company.remove_department("Development")
   ```

6. **Тестирование сериализации компании:**
   - Проверьте полный цикл сохранения/загрузки:
   ```python
   def test_company_serialization_roundtrip(self):
       # Создание тестовой компании
       company = Company("TechCorp")
       dept = Department("Development")
       emp = Employee(1, "John", "DEV", 5000)
       
       dept.add_employee(emp)
       company.add_department(dept)
       
       # Сохранение и загрузка
       company.save_to_json("test_company.json")
       loaded_company = Company.load_from_json("test_company.json")
       
       assert loaded_company.name == "TechCorp"
       assert len(loaded_company.get_departments()) == 1
   ```

7. **Тестирование бизнес-методов:**
   - Проверьте анализ данных компании:
   ```python
   def test_department_statistics(self):
       company = create_test_company()  # Вспомогательная функция
       stats = company.get_department_stats()
       
       assert "Development" in stats
       assert stats["Development"]["employee_count"] == 3
       assert stats["Development"]["total_salary"] > 0
   ```

   - Проверьте поиск перегруженных сотрудников:
   ```python
   def test_find_overloaded_employees(self):
       company = create_test_company()
       overloaded = company.find_overloaded_employees()
       
       # Проверяем, что сотрудник участвует в нескольких проектах
       assert any(len(emp.get_projects()) > 2 for emp in overloaded)
   ```

8. **Интеграционные тесты сложных сценариев:**
   - Создайте комплексный тест по примеру из задания:
   ```python
   def test_complex_company_structure(self):
       company = Company("TechInnovations")
       
       # Создание отделов
       dev_department = Department("Development")
       sales_department = Department("Sales")
       
       # Создание сотрудников
       manager = Manager(1, "Alice Johnson", "DEV", 7000, 2000)
       developer = Developer(2, "Bob Smith", "DEV", 5000, ["Python", "SQL"], "senior")
       salesperson = Salesperson(3, "Charlie Brown", "SAL", 4000, 0.15, 50000)
       
       # Добавление в отделы
       dev_department.add_employee(manager)
       dev_department.add_employee(developer)
       sales_department.add_employee(salesperson)
       
       # Добавление отделов в компанию
       company.add_department(dev_department)
       company.add_department(sales_department)
       
       # Проверки
       assert company.calculate_total_monthly_cost() > 0
       assert len(company.get_all_employees()) == 3
   ```

**Критерии оценки:**
- **Удовлетворительно:** Написаны тесты для основных методов Project и Company
- **Хорошо:** Добавлены тесты для валидации и кастомных исключений
- **Отлично:** Полное покрытие всех бизнес-методов, включая интеграционные тесты сложных сценариев и проверку сериализации

---

### **Часть 5: Тестирование паттернов проектирования**

**Цель:** Написать тесты для проверки корректной работы различных паттернов проектирования, примененных в системе учета сотрудников.

**Задание:**

1. **Тестирование порождающих паттернов:**
   - Создайте файл `test_patterns.py`

   **Singleton:**
   ```python
   def test_singleton_pattern():
       # Arrange & Act
       db1 = DatabaseConnection.get_instance()
       db2 = DatabaseConnection.get_instance()
       
       # Assert
       assert db1 is db2
       assert id(db1) == id(db2)
   ```

   **Factory Method:**
   ```python
   def test_employee_factory_method():
       # Arrange
       factory = EmployeeFactory()
       
       # Act & Assert
       employee = factory.create_employee("developer", 
                                         id=1, 
                                         name="John", 
                                         department="DEV",
                                         base_salary=5000,
                                         skills=["Python"],
                                         seniority_level="middle")
       
       assert isinstance(employee, Developer)
       assert employee.calculate_salary() == 7500  # 5000 * 1.5
   ```

   **Builder:**
   ```python
   def test_employee_builder_pattern():
       # Arrange & Act
       developer = (EmployeeBuilder()
                   .set_id(101)
                   .set_name("John Doe")
                   .set_department("DEV")
                   .set_base_salary(5000)
                   .set_skills(["Python", "Java"])
                   .set_seniority("senior")
                   .build())
       
       # Assert
       assert developer.id == 101
       assert developer.name == "John Doe"
       assert isinstance(developer, Developer)
       assert developer.calculate_salary() == 10000  # 5000 * 2.0
   ```

2. **Тестирование структурных паттернов:**

   **Adapter:**
   ```python
   def test_salary_calculator_adapter():
       # Arrange
       external_service = ExternalSalaryService()
       adapter = SalaryCalculatorAdapter(external_service)
       employee = Employee(1, "John", "IT", 5000)
       
       # Act
       result = adapter.calculate_salary(employee)
       
       # Assert
       assert result == 5000  # или другая логика адаптера
   ```

   **Decorator:**
   ```python
   def test_bonus_decorator():
       # Arrange
       employee = Employee(1, "John", "IT", 5000)
       decorated_employee = BonusDecorator(employee, 1000)
       
       # Act
       salary = decorated_employee.calculate_salary()
       
       # Assert
       assert salary == 6000
       assert "бонус: 1000" in decorated_employee.get_info()
   ```

3. **Тестирование поведенческих паттернов:**

   **Observer:**
   ```python
   def test_observer_pattern():
       # Arrange
       employee = Employee(1, "John", "IT", 5000)
       observer = Mock()
       employee.add_observer(observer)
       
       # Act
       employee.base_salary = 6000
       
       # Assert
       observer.update.assert_called_once_with(employee, "salary_changed")
   ```

   **Strategy:**
   ```python
   def test_bonus_strategy_pattern():
       # Arrange
       employee = Employee(1, "John", "IT", 5000)
       performance_strategy = PerformanceBonusStrategy()
       seniority_strategy = SeniorityBonusStrategy()
       
       # Act & Assert
       employee.set_bonus_strategy(performance_strategy)
       assert employee.calculate_bonus() == 1000  # логика performance
       
       employee.set_bonus_strategy(seniority_strategy)
       assert employee.calculate_bonus() == 1500  # логика seniority
   ```

   **Command:**
   ```python
   def test_command_pattern_with_undo():
       # Arrange
       employee = Employee(1, "John", "IT", 5000)
       company = Company("TestCorp")
       hire_command = HireEmployeeCommand(employee, company)
       
       # Act & Assert
       hire_command.execute()
       assert employee in company.get_all_employees()
       
       hire_command.undo()
       assert employee not in company.get_all_employees()
   ```

4. **Тестирование комбинированных паттернов:**

   **Repository Pattern:**
   ```python
   def test_employee_repository():
       # Arrange
       repo = EmployeeRepository()
       employee = Employee(1, "John", "IT", 5000)
       
       # Act
       repo.add(employee)
       found = repo.find_by_id(1)
       
       # Assert
       assert found is not None
       assert found.name == "John"
   ```

   **Specification Pattern:**
   ```python
   def test_specification_pattern():
       # Arrange
       repo = EmployeeRepository()
       employees = [
           Employee(1, "John", "IT", 5000),
           Employee(2, "Jane", "HR", 6000),
           Employee(3, "Bob", "IT", 7000)
       ]
       
       for emp in employees:
           repo.add(emp)
       
       # Act
       high_salary_spec = SalarySpecification(min_salary=5500)
       it_spec = DepartmentSpecification("IT")
       combined_spec = high_salary_spec & it_spec
       
       result = repo.find_by_specification(combined_spec)
       
       # Assert
       assert len(result) == 1
       assert result[0].name == "Bob"
   ```

5. **Интеграционные тесты паттернов:**
   ```python
   def test_complex_pattern_interaction():
       # Демонстрация взаимодействия нескольких паттернов
       
       # 1. Singleton для БД
       db = DatabaseConnection.get_instance()
       
       # 2. Factory для создания сотрудников
       factory = TechCompanyFactory()
       developer = factory.create_developer(1, "John", "DEV", 5000, ["Python"], "senior")
       
       # 3. Builder для сложной конфигурации
       manager = (EmployeeBuilder()
                 .set_id(2)
                 .set_name("Alice")
                 .set_department("MAN")
                 .set_base_salary(7000)
                 .set_bonus(2000)
                 .build())
       
       # 4. Repository для сохранения
       repo = EmployeeRepository()
       repo.add(developer)
       repo.add(manager)
       
       # 5. Specification для поиска
       spec = SalarySpecification(min_salary=6000)
       high_earners = repo.find_by_specification(spec)
       
       # Assert
       assert len(high_earners) == 1
       assert high_earners[0].name == "Alice"
   ```

6. **Mock-тестирование:**
   ```python
   def test_notification_system_with_mocks():
       # Arrange
       employee = Employee(1, "John", "IT", 5000)
       mock_notifier = Mock()
       notification_system = NotificationSystem()
       notification_system.add_notifier(mock_notifier)
       
       # Act
       employee.add_observer(notification_system)
       employee.base_salary = 6000
       
       # Assert
       mock_notifier.notify.assert_called_once()
   ```

7. **Тестирование исключительных ситуаций:**
   ```python
   def test_repository_error_handling():
       # Arrange
       repo = EmployeeRepository()
       
       # Act & Assert
       with pytest.raises(EmployeeNotFoundError):
           repo.find_by_id(999)  # Несуществующий ID
   ```

**Критерии оценки:**
- **Удовлетворительно:** Написаны тесты для 3+ паттернов с базовой функциональностью
- **Хорошо:** Добавлены тесты для 5+ паттернов с использованием mock-объектов
- **Отлично:** Полное покрытие всех паттернов, включая интеграционные тесты и проверку взаимодействия между паттернами

---

**Рекомендуемая литература:**
1. Кент Бек. «Разработка через тестирование: Практический пример».
2. Владимир Хориков. «Unit-тестирование».
3. Документация `pytest` и `unittest.mock`: https://docs.pytest.org/en/stable/