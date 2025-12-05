module Higher_Order where
-- Применение функции к каждому элементу
map' :: (a -> b) -> [a] -> [b]
map' _ [] = []
map' f (x:xs) = f x : map' f xs

-- Фильтрация списка
filter' :: (a -> Bool) -> [a] -> [a]
filter' _ [] = []
filter' p (x:xs)
    | p x       = x : filter' p xs
    | otherwise = filter' p xs

-- Свертка (fold)
myFoldl' :: (b -> a -> b) -> b -> [a] -> b
myFoldl' _ acc []     = acc
myFoldl' f acc (x:xs) = myFoldl' f (f acc x) xs

-- Композиция функций
compose :: (b -> c) -> (a -> b) -> a -> c
compose f g x = f (g x)