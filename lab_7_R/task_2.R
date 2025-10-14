# Задание 2.
# Распараллельте фрагмент кода, представленный ниже, используя вычислительный
# кластер:
# for(iter in seq_len(50))
#  result[iter] <- mean_of_rnorm(10000)
# Для решения подгрузите функцию
# mean_of_rnorm <- function(n) {
#  random_numbers <- rnorm(n)
#  mean(random_numbers)
# }

# Определяем функцию
mean_of_rnorm <- function(n) {
  random_numbers <- rnorm(n)
  mean(random_numbers)
}

# Определяем количество ядер
ncores <- detectCores(logical = FALSE)

# Создаём кластер
cl <- makeCluster(ncores)

# Передаём функцию на все узлы
clusterExport(cl, varlist = "mean_of_rnorm")

# --- Параллельный вариант ---
system.time({
  result_parallel <- parSapply(cl, seq_len(50), function(x) mean_of_rnorm(10000))
})

# Останавливаем кластер
stopCluster(cl)

# Проверяем результат
summary(result_parallel)

# --- Последовательный вариант ---
system.time({
  result_seq <- numeric(50)
  for (iter in seq_len(50))
    result_seq[iter] <- mean_of_rnorm(10000)
})

summary(result_seq)
