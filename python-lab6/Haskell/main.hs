module Main where

import Basics
import Recursion
import Patterns
import Higher_Order
import Types

countEven :: [Int] -> Int
countEven xs =  length' (filter' even xs)

positiveSquares :: [Int] -> [Int]
positiveSquares xs = map' square (filter' even xs)

pass :: Ord a => [a] -> ([a], Bool)
pass (x:y:xs)
    | x > y     = let (rest, swapped) = pass (x:xs)
                  in  (y : rest, True)
    | otherwise = let (rest, swapped) = pass (y:xs)
                  in  (x : rest, swapped)
pass xs = (xs, False)

bubbleSort :: Ord a => [a] -> [a]
bubbleSort xs =
    case pass xs of
        (ys, False) -> ys
        (ys, True)  -> bubbleSort ys

main :: IO ()
main = do
    putStrLn "=== Демонстрация работы функций ==="
    
    -- Базовые функции
    print $ square 5
    print $ grade 85
    
    -- Рекурсия
    print $ factorial 5
    print $ sumList [1, 2, 3, 4, 5]
    
    -- Pattern matching
    print $ addVectors (1, 2) (3, 4)
    
    -- Функции высшего порядка
    print $ map' square [1, 2, 3, 4]
    print $ filter' even [1, 2, 3, 4, 5, 6]
    
    -- Алгебраические типы
    print $ distance (Point 0 0) (Point 3 4)
    print $ isWeekend Saturday

    print $ countEven [1, 2, 3, 4]
    print $ positiveSquares [1, 2, 3, 4]
    print $ bubbleSort [1, 5, 3, 4, 2, 8, 6, 7]