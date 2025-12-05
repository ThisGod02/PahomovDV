use std::rc::Rc;

// Функциональный список
#[derive(Debug, Clone)]
pub enum List<T> {
    Empty,
    Cons(T, Rc<List<T>>),
}

impl<T> List<T> {
    pub fn new() -> Self {
        List::Empty
    }
    
    pub fn prepend(&self, elem: T) -> Self {
        List::Cons(elem, Rc::new(self.clone()))
    }
    
    pub fn head(&self) -> Option<&T> {
        match self {
            List::Cons(head, _) => Some(head),
            List::Empty => None,
        }
    }
    
    pub fn tail(&self) -> Option<&List<T>> {
        match self {
            List::Cons(_, tail) => Some(tail),
            List::Empty => None,
        }
    }
    
    pub fn iter(&self) -> ListIter<T> {
        ListIter { current: self }
    }
}

// Итератор для функционального списка
pub struct ListIter<'a, T> {
    current: &'a List<T>,
}

impl<'a, T> Iterator for ListIter<'a, T> {
    type Item = &'a T;
    
    fn next(&mut self) -> Option<Self::Item> {
        match self.current {
            List::Cons(head, tail) => {
                self.current = tail;
                Some(head)
            }
            List::Empty => None,
        }
    }
}

pub fn demonstrate_functional_structures() {
    println!("\n=== Функциональные структуры данных ===");
    
    // Создание списка в функциональном стиле
    let list = List::new()
        .prepend(3)
        .prepend(2)
        .prepend(1);
    
    println!("Функциональный список: {:?}", list);
    
    // Итерация по списку
    println!("Элементы списка:");
    for elem in list.iter() {
        println!("- {}", elem);
    }
    
    // Голова и хвост
    if let Some(head) = list.head() {
        println!("Голова списка: {}", head);
    }
    
    if let Some(tail) = list.tail() {
        println!("Хвост списка: {:?}", tail);
    }
}

// Неизменяемая структура данных
#[derive(Debug, Clone)]
pub struct ImmutablePoint {
    x: f64,
    y: f64,
}

impl ImmutablePoint {
    pub fn new(x: f64, y: f64) -> Self {
        ImmutablePoint { x, y }
    }
    
    // Вместо мутации возвращаем новую структуру
    pub fn translate(&self, dx: f64, dy: f64) -> Self {
        ImmutablePoint {
            x: self.x + dx,
            y: self.y + dy,
        }
    }
    
    pub fn distance(&self, other: &ImmutablePoint) -> f64 {
        ((self.x - other.x).powi(2) + (self.y - other.y).powi(2)).sqrt()
    }
}

// Практическое задание 3: Генератор чисел Фибоначчи
pub struct Fibonacci {
    current: u64,
    next: u64,
}

impl Fibonacci {
    pub fn new() -> Self {
        Fibonacci { current: 0, next: 1 }
    }
}

impl Iterator for Fibonacci {
    type Item = u64;
    
    fn next(&mut self) -> Option<Self::Item> {
        let result = self.current;
        let new_next = self.current.checked_add(self.next)?;
        self.current = self.next;
        self.next = new_next;
        Some(result)
    }
}

pub fn main() {
    demonstrate_functional_structures();
    
    // Демонстрация неизменяемой точки
    let point1 = ImmutablePoint::new(0.0, 0.0);
    let point2 = point1.translate(3.0, 4.0);
    
    println!("Расстояние между {:?} и {:?} = {:.2}", point1, point2, point1.distance(&point2));
    
    // Демонстрация генератора Фибоначчи
    println!("\n=== Генератор чисел Фибоначчи ===");
    let fib = Fibonacci::new();
    let first_10: Vec<u64> = fib.take(10).collect();
    println!("Первые 10 чисел Фибоначчи: {:?}", first_10);
}

