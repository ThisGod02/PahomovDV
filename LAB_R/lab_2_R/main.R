# Задание 2 – Написать программу вычисляющую площадь неправильного
# многоугольника. Многоугольник на плоскости задается целочисленными координатами своих
# N вершин в декартовой системе. Стороны многоугольника не соприкасаются (за исключением
# соседних - в вершинах) и не пересекаются. Программа в первой строке должна принимать
# число N – количество вершин многоугольника, в последующих N строках – координаты
# соответствующих вершин (вершины задаются в последовательности против часовой стрелки).
# На выход программа должна выдавать площадь фигуры.
# Программа должна быть выполнена в виде блок-схемы и на ЯВУ.

erors <- 0

while(erors < 3){
  cat("Введите название искомой фигуры (круг, треугольник, квадрат, прямоугольник)\n")

  vvod <- readline()

  if (erors == 3){
    cat ("Ну ты и дурак конечно...\n")
    break
  }

  if (vvod == "круг"){
    cat("Введите радиус круга: \n")
    circle_radius <- as.numeric(readline())
    circle_area <- pi * circle_radius * circle_radius
    cat("ПЛощадь круга: ", circle_area, "\n")
  }
  else if(vvod == "квадрат"){
    cat("Длина стороны квадрата: \n")
    square_side <- as.numeric(readline())
    square_area <- square_side * square_side
    cat("Площадь квадрата:", square_area)
  }
  else if(vvod == "треугольник"){
    cat ("Введите стороны треугольника: \n")
    triangle_a <- as.numeric(readline())
    triangle_b <- as.numeric(readline())
    triangle_c <- as.numeric(readline())
    triangle_p <- (triangle_a + triangle_b + triangle_c) / 2
    triangle_area <- (triangle_p * (triangle_p - triangle_a) * (triangle_p - triangle_b) * (triangle_p - triangle_c)) ** 1/2
    cat ("Площадь треугольника: ", triangle_area)
  }
  else if(vvod == "прямоугольника"){
    cat("Первая сторона прямоугольника: \n")
    rectangle_side1 <- as.numeric(readline())
    cat("Вторая сторона прямоугольника: \n")
    rectangle_side2 <- as.numeric(readline())
    rectangle_area <- rectangle_side1 * rectangle_side2
    cat("Площадь прямоугольника:\n", rectangle_area)
  }
  else if (vvod != "круг"){
    cat("eblan\n")
    erors <- erors + 1
  }
}