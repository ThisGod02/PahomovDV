# Задание 1.
# Используя заранее подготовленные функции визуализируйте сведения о наиболее
# часто встречающихся словах из книг Джейн Остин по буквам английского алфавита. Книги,
# необходимые для анализа, находятся в пакете janeaustenr. Также для работы потребуется пакет
# stringr. После установки пакетов добавьте следующие функции:
# extract_words <- function(book_name) {
#  text <- subset(austen_books(), book == book_name)$text
#  str_extract_all(text, boundary("word")) %>% unlist %>% tolower
# }
# janeausten_words <- function() {
#  books <- austen_books()$book %>% unique %>% as.character
#  words <- sapply(books, extract_words) %>% unlist
#  words
# }
# max_frequency <- function(letter, words, min_length = 1) {
#  w <- select_words(letter, words = words, min_length = min_length)
#  frequency <- table(w)
#  frequency[which.max(frequency)]
# }
# select_words <- function(letter, words, min_length = 1) {
#  min_length_words <- words[nchar(words) >= min_length]
#  grep(paste0("^", letter), min_length_words, value = TRUE)
# }
# Рисунок 5 – Функции необходимые для решения задания
# Для решения задачи необходимо с помощью функции janeausten_words() создать новый
# объект – вектор слов. Далее, используя одну из функций семейства apply, и заранее созданную
# функцию max_frequency создать именованный вектор, содержащий значение максимально
# встречающих слов английского алфавита, длиной не менее 5 букв.
# Полезной для работы будет использование встроенной переменной letters, содержащей
# строчные буквы английского алфавита. Для визуализации используйте функцию barplot() c
# аргументом las = 2. В случае полностью правильного выполнения задания будет представлен
# график как на рисунке 6. 

extract_words <- function(book_name) {
  text <- subset(austen_books(), book == book_name)$text
  str_extract_all(text, boundary("word")) %>% unlist() %>% tolower()
}

janeausten_words <- function() {
  books <- austen_books()$book %>% unique() %>% as.character()
  words <- sapply(books, extract_words) %>% unlist()
  words
}

select_words <- function(letter, words, min_length = 1) {
  min_length_words <- words[nchar(words) >= min_length]
  grep(paste0("^", letter), min_length_words, value = TRUE)
}

max_frequency <- function(letter, words, min_length = 1) {
  w <- select_words(letter, words = words, min_length = min_length)
  frequency <- table(w)
  if (length(frequency) == 0) return(NA)
  frequency[which.max(frequency)]
}

# Создаём вектор всех слов
words <- janeausten_words()

# Находим наиболее частые слова по буквам
freqs <- sapply(letters, max_frequency, words = words, min_length = 5)

# Строим график
barplot(freqs, las = 2, main = "Наиболее частые слова по буквам (>=5 букв)",
        ylab = "Частота", xlab = "Буквы алфавита", col = "lightblue")

