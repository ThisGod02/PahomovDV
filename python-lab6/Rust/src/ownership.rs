// Базовые функции
pub fn square(x: i32) -> i32 {
    x * x
}

pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

// Функции высшего порядка
pub fn apply_function<F>(f: F, x: i32) -> i32 
where 
    F: Fn(i32) -> i32,
{
    f(x)
}

// Демонстрация системы владения
pub fn demonstrate_ownership() {
    println!("=== Система владения ===");
    
    let s1 = String::from("hello");
    let s2 = s1; // Перемещение владения, s1 больше не валидна
    // println!("{}", s1); // Ошибка компиляции!
    println!("s2 = {}", s2);
    
    // Клонирование для глубокого копирования
    let s3 = s2.clone();
    println!("s2 = {}, s3 = {}", s2, s3);
    
    // Заимствование (borrowing)
    let len = calculate_length(&s3);
    println!("Длина '{}' = {}", s3, len);
    
    // Изменяемое заимствование
    let mut s4 = String::from("hello");
    modify_string(&mut s4);
    println!("После модификации: {}", s4);
}

fn calculate_length(s: &String) -> usize {
    s.len()
}

fn modify_string(s: &mut String) {
    s.push_str(", world!");
}

// Каррирование
pub fn multiply(a: i32) -> impl Fn(i32) -> i32 {
    move |b| a * b
}

pub fn main() {
    println!("Квадрат 5: {}", square(5));
    println!("Сложение 3 и 4: {}", add(3, 4));
    println!("Применение функции: {}", apply_function(square, 3));
    
    let double = multiply(2);
    println!("Удвоение 7: {}", double(7));
    
    demonstrate_ownership();
}

