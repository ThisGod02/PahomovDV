# Задание 2. Создайте генератор класса Микроволновая печь. В качестве данных класс
# должен содержать сведения о мощности печи (Вт) и о состоянии дверцы (открыта или
# закрыта). Данный класс должен обладать методами открыть и закрыть дверь микроволновки,
# а также методом, отвечающим за приготовление пищи. Метод, отвечающий за приготовление
# пищи, должен вводить систему в бездействие (используется Sys.sleep) на определенное
# количество времени (которое зависит от мощности печи) и после выводить сообщение о
# готовности пищи.

Microwave <- R6Class(
  "Microwave",
  private = list(
    vt = 100,
    door_open = TRUE
  ),
  public = list(
    initialize = function(vt, door_open) {
      if(!missing(vt)) {
        private$vt <- vt
      }
      if(!missing(door_open)) {
        private$door_open <- door_open
      }
    },
    open_door = function(){
      private$door_open <- TRUE
    },
    close_door = function(){
      private$door_open<- FALSE
    },
    cook = function(){
      if(private$door_open == TRUE){
        print("Перед началом готовки закройте дверь!")
        return(NA)
      }
      cat("Время ожидания готовки:", 1000/private$vt, "\n")
      Sys.sleep(1000/private$vt)
      print("Еда готова!")
    }
  )
)
microwave1 = Microwave$new()
microwave2 = Microwave$new(
  vt = 1000,
  door_open = FALSE
)
microwave1$cook()
microwave1$close_door()
microwave1$cook()
microwave2$cook()
print(microwave1)