# Списковые включения (list comprehensions)

# Генераторы
def fibonacci_generator(limit):
    """Генератор чисел Фибоначчи"""
    a, b = 0, 1
    count = 0
    while count < limit:
        yield a
        a, b = b, a + b
        count += 1


# Практическое задание 3: Генератор простых чисел
def prime_generator():
    """Генератор простых чисел"""
    def is_prime(n):
        """Проверка, является ли число простым"""
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        # Проверяем делители от 3 до sqrt(n)
        i = 3
        while i * i <= n:
            if n % i == 0:
                return False
            i += 2
        return True
    
    num = 2
    while True:
        if is_prime(num):
            yield num
        num += 1


if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # Данные о студентах (для словарных включений)
    students = [
        {'name': 'Alice', 'grade': 85, 'age': 20},
        {'name': 'Bob', 'grade': 92, 'age': 22},
        {'name': 'Charlie', 'grade': 78, 'age': 19},
        {'name': 'Diana', 'grade': 95, 'age': 21},
        {'name': 'Eve', 'grade': 88, 'age': 20}
    ]
    
    # Простые включения
    squares = [x * x for x in numbers]
    print(f"Квадраты: {squares}")
    
    # Включения с условием
    even_squares = [x * x for x in numbers if x % 2 == 0]
    print(f"Квадраты четных: {even_squares}")
    
    # Словарные включения
    student_dict = {student['name']: student['grade'] for student in students}
    print(f"Словарь студентов: {student_dict}")
    
    # Множества (set) включения
    unique_ages = {student['age'] for student in students}
    print(f"Уникальные возрасты: {unique_ages}")
    
    # Использование генератора
    print("Числа Фибоначчи:")
    fib_gen = fibonacci_generator(10)
    for num in fib_gen:
        print(num, end=" ")
    print()
    
    # Генераторные выражения
    squares_gen = (x * x for x in numbers)
    print(f"Генератор квадратов: {list(squares_gen)}")
    
    # Демонстрация генератора простых чисел
    print("\nПервые 10 простых чисел:")
    prime_gen = prime_generator()
    primes = [next(prime_gen) for _ in range(10)]
    print(primes)

