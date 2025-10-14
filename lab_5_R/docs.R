# Задание 2. Используя документацию пакета purrr опишите отличия и особенности
# функций семейства map_*. Приведите примеры реализации с использование различных
# тестовых данных. Данные можно брать из пакета datasets или создав свои тестовые наборы.
# Для просмотра данных из пакета datasets выполните код library(help = "datasets")

numbers <- list(1:3, 4:6, 7:9)
mixed <- list(1, "hello", 3.14, TRUE)
df <- data.frame(a = 1:3, b = 4:6, c = 7:9)

map(numbers, ~ .x * 2)
map(numbers, length)

map_chr(numbers, ~ paste(.x, collapse = ", "))
map_chr(df, ~ paste("col", .x[1]))

map_dbl(numbers, mean)
map_dbl(df, sum)

map_int(numbers, length)
map_int(numbers, ~ .x[1])

map_lgl(numbers, ~ any(.x %% 2 == 0))
map_lgl(numbers, ~ all(.x > 0))

map_if(df, is.numeric, ~ .x * 2)
map_if(numbers, ~ length(.x) > 2, sum)

map_at(df, c("a", "c"), ~ .x * 10)
map_at(numbers, c(1, 3), ~ .x * 100)

deep_list <- list(
  list(a = 1:2, b = 3:4),
  list(c = 5:6, d = 7:8)
)
map_depth(deep_list, 2, sum)

map_vec(numbers, mean)
map_vec(numbers, length)
map_vec(numbers, ~ mean(.x) > 5)