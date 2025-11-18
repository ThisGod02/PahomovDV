"""Главный скрипт для запуска демонстраций всех частей лабораторной работы."""

import sys
import os

# Добавляем корневую директорию проекта в путь
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def main():
    """Главная функция для запуска всех демонстраций."""
    print("=" * 70)
    print("СИСТЕМА УЧЕТА СОТРУДНИКОВ КОМПАНИИ")
    print("Лабораторная работа 4: Реализация принципов ООП")
    print("=" * 70)
    
    print("\nДоступные демонстрации:")
    print("1. Часть 4.1: Инкапсуляция")
    print("2. Часть 4.2: Наследование и абстракция")
    print("3. Часть 4.3: Полиморфизм и магические методы")
    print("4. Часть 4.4: Композиция и агрегация")
    print("5. Запустить все демонстрации")
    print("0. Выход")
    
    while True:
        try:
            choice = input("\nВыберите демонстрацию (0-5): ").strip()
            
            if choice == "0":
                print("\nДо свидания!")
                break
            elif choice == "1":
                print("\n" + "=" * 70)
                import examples.demo_part1 as demo1_module
                demo1_module.main()
            elif choice == "2":
                print("\n" + "=" * 70)
                import examples.demo_part2 as demo2_module
                demo2_module.main()
            elif choice == "3":
                print("\n" + "=" * 70)
                import examples.demo_part3 as demo3_module
                demo3_module.main()
            elif choice == "4":
                print("\n" + "=" * 70)
                import examples.demo_part4 as demo4_module
                demo4_module.main()
            elif choice == "5":
                print("\n" + "=" * 70)
                import examples.demo_part1 as demo1_module
                demo1_module.main()
                print("\n" + "=" * 70)
                import examples.demo_part2 as demo2_module
                demo2_module.main()
                print("\n" + "=" * 70)
                import examples.demo_part3 as demo3_module
                demo3_module.main()
                print("\n" + "=" * 70)
                import examples.demo_part4 as demo4_module
                demo4_module.main()
                print("\n" + "=" * 70)
                print("Все демонстрации завершены!")
            else:
                print("Неверный выбор. Попробуйте снова.")
        except KeyboardInterrupt:
            print("\n\nПрервано пользователем. До свидания!")
            break
        except Exception as e:
            print(f"\nПроизошла ошибка: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()

