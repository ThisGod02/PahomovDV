# Задание 1. Создайте дженерик, принимающий вектор, содержащий параметры фигуры
# и вычисляющий ее площадь. Для разных фигур создайте разные классы. В качестве метода по
# умолчанию дженерик должен выводить сообщение о невозможности обработки данных.

# Функции для создания геометрических фигур
create_circle <- function(radius) {
  structure(list(radius = radius), class = "circle")
}

create_rectangle <- function(length, width) {
  structure(list(length = length, width = width), class = "rectangle")
}

create_triangle <- function(base, height) {
  structure(list(base = base, height = height), class = "triangle")
}

create_square <- function(side) {
  structure(list(side = side), class = "square")
}

calculate_S <- function(x) {
  UseMethod("calculate_S")
}

calculate_S.default <- function(x) {
  cat("Неизвестный тип фигуры\n")
  return(NA)
}

calculate_S.circle <- function(x) {
  S <- pi * x$radius^2
  cat("Площадь круга с радиусом", x$radius, "=", round(S, 2), "\n")
  return(S)
}

calculate_S.rectangle <- function(x) {
  S <- x$length * x$width
  cat("Площадь прямоугольника", x$length, "x", x$width, "=", S, "\n")
  return(S)
}

calculate_S.triangle <- function(x) {
  S <- 0.5 * x$base * x$height
  cat("Площадь треугольника с основанием", x$base, "и высотой", x$height, "=", S, "\n")
  return(S)
}

calculate_S.square <- function(x) {
  S <- x$side^2
  cat("Площадь квадрата со стороной", x$side, "=", S, "\n")
  return(S)
}

circle1 <- create_circle(5)
rectangle1 <- create_rectangle(3, 8)
triangle1 <- create_triangle(3, 8)
square1 <- create_square(5)

calculate_S(circle1)
calculate_S(rectangle1)
calculate_S(triangle1)
calculate_S(square1)