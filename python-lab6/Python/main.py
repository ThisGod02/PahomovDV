# main.py
from functions_as_objects import square, apply_function, create_multiplier
from lambda_closures import create_counter
from higher_order import students, numbers, analyze_students
from functools import reduce
from comprehensions_generators import fibonacci_generator, prime_generator
from decorators import greet, timer, repeat, logger


def main():
    print("=== Демонстрация функционального программирования в Python ===")
    
    # Функции как объекты
    print("\n1. Функции как объекты:")
    print(f"apply_function(square, 5) = {apply_function(square, 5)}")
    
    # Lambda и замыкания
    print("\n2. Lambda и замыкания:")
    counter = create_counter()
    print(f"Счетчик: {counter()}, {counter()}, {counter()}")
    
    # Функции высшего порядка
    print("\n3. Функции высшего порядка:")
    product = reduce(lambda x, y: x * y, numbers)
    print(f"Произведение чисел: {product}")
    
    # Генераторы и включения
    print("\n4. Генераторы и включения:")
    even_squares = [x * x for x in numbers if x % 2 == 0]
    print(f"Четные квадраты: {even_squares}")
    
    # Декораторы
    print("\n5. Декораторы:")
    greet("Мария")
    
    # Дополнительные демонстрации
    print("\n6. Анализ студентов:")
    analysis = analyze_students(students)
    print(f"Средний балл: {analysis['average_grade']:.2f}")
    print(f"Отличники: {[s['name'] for s in analysis['excellent_students']]}")
    
    print("\n7. Генератор простых чисел (первые 5):")
    prime_gen = prime_generator()
    primes = [next(prime_gen) for _ in range(5)]
    print(primes)


if __name__ == "__main__":
    main()

