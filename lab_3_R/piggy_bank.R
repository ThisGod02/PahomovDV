# Задание 3. Создайте класс копилка. Описание структуры классы выполните из своего
# понимания копилки.

Piggy_bank <- R6Class(
    "Piggy Bank",
    private = list(
        money = 0,
        unharmed = TRUE
    ),
    public = list(
        initialize = function(money){
            if(!missing(money)){
                private$money <- money
            }
        },
        put_money = function(money){
            if(private$unharmed){
                private$money <- private$money + money
                cat("Вы положили деньги в свинку копилку!\n")
            }
            else {
                cat("Свинка копилка разбита!\n")
            }
        },
        destroy_piggy = function(){
            if(private$unharmed){
                private$unharmed = FALSE
                cat("Вы разбили свинку копилку! В ней было:", private$money, "рублей!\n")
                return(private$money)
            }
            else {
                cat("Свинка копилка разбита!\n")
            }
        }
    )
)
piggy_bank1 = Piggy_bank$new()
piggy_bank1$put_money(100)
piggy_bank1$put_money(200)
piggy_bank1$destroy_piggy()