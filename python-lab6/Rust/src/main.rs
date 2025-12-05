// main.rs
mod ownership;
mod iterators_closures;
mod pattern_matching;
mod error_handling;
mod functional_data_structures;

fn main() {
    println!("=== Rust Функциональное Программирование ===\n");
    
    // Базовые операции и система владения
    ownership::main();
    println!();
    
    // Итераторы и замыкания
    iterators_closures::demonstrate_iterators();
    println!();
    
    // Pattern matching
    pattern_matching::demonstrate_pattern_matching();
    println!();
    
    // Обработка ошибок
    error_handling::demonstrate_error_handling();
    println!();
    
    // Функциональные структуры данных
    functional_data_structures::demonstrate_functional_structures();
    println!();
    
    // Дополнительные демонстрации
    println!("=== Дополнительные примеры ===");
    
    // Генератор Фибоначчи
    let fib = functional_data_structures::Fibonacci::new();
    let first_10: Vec<u64> = fib.take(10).collect();
    println!("Первые 10 чисел Фибоначчи: {:?}", first_10);
    
    // Анализ продуктов
    let products = vec![
        iterators_closures::Product::new(1, "iPhone", 999.99, "electronics", true),
        iterators_closures::Product::new(2, "MacBook", 1999.99, "electronics", false),
        iterators_closures::Product::new(3, "T-shirt", 29.99, "clothing", true),
        iterators_closures::Product::new(4, "Jeans", 79.99, "clothing", true),
        iterators_closures::Product::new(5, "Book", 15.99, "education", false),
    ];
    
    let (avg_price, available_count, expensive) = iterators_closures::analyze_products(&products);
    println!("\nАнализ продуктов:");
    println!("  Средняя цена: {:.2}", avg_price);
    println!("  Доступных: {}", available_count);
    println!("  Дорогих (>100): {}", expensive.len());
}

