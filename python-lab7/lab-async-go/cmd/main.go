package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"os/signal"
	"sync"
	"syscall"
	"time"

	"lab-async-go/internal/async"
	"lab-async-go/internal/server"
)

func main() {
	fmt.Println("=== Лабораторная работа: Асинхронное программирование в Go ===")
	
	// Демонстрация всех паттернов
	var wg sync.WaitGroup
	
	// 1. Базовые горутины
	fmt.Println("\n1. Базовые горутины:")
	demoBasicGoroutines()
	
	// 2. Каналы
	fmt.Println("\n2. Работа с каналами:")
	demoChannels()
	
	// 3. Worker Pool
	fmt.Println("\n3. Worker Pool:")
	demoWorkerPool()
	
	// 4. HTTP сервер
	fmt.Println("\n4. HTTP Сервер:")
	fmt.Println("Запуск сервера на http://localhost:8080")
	fmt.Println("Для тестирования выполните: curl http://localhost:8080/")
	
	srv := server.NewServer(":8080")
	
	// Запуск сервера в горутине
	wg.Add(1)
	go func() {
		defer wg.Done()
		if err := srv.Start(); err != nil {
			log.Printf("Server error: %v", err)
		}
	}()
	
	// Ожидание сигнала для graceful shutdown
	stop := make(chan os.Signal, 1)
	signal.Notify(stop, os.Interrupt, syscall.SIGTERM)
	
	// Демонстрация работы сервера
	time.Sleep(2 * time.Second)
	
	// Остановка сервера
	fmt.Println("\nОстановка сервера...")
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	
	if err := srv.Stop(ctx); err != nil {
		log.Printf("Server shutdown error: %v", err)
	}
	
	wg.Wait()
	fmt.Println("Демонстрация завершена")
}

func demoBasicGoroutines() {
	var wg sync.WaitGroup
	counter := &async.Counter{}
	
	for i := 0; i < 5; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			counter.Increment()
			fmt.Printf("Горутина %d увеличила счётчик\n", id)
			time.Sleep(100 * time.Millisecond)
		}(i)
	}
	
	wg.Wait()
	fmt.Printf("Итоговое значение счётчика: %d\n", counter.Value())
}

func demoChannels() {
	ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
	defer cancel()
	
	// Создаём два продюсера
	ch1 := async.Producer(ctx, 3)
	ch2 := async.Producer(ctx, 3)
	
	// Объединяем каналы
	merged := async.MergeChannels(ctx, ch1, ch2)
	
	// Обрабатываем результаты
	results := async.Consumer(ctx, merged, 2*time.Second)
	fmt.Printf("Получено значений: %v\n", results)
}

func demoWorkerPool() {
	pool := async.NewWorkerPool(3)
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	
	tasks := []async.Task{
		{ID: 1, Data: "task1"},
		{ID: 2, Data: "task2"},
		{ID: 3, Data: "task3"},
		{ID: 4, Data: "task4"},
		{ID: 5, Data: "task5"},
	}
	
	processor := func(task async.Task) async.Result {
		time.Sleep(100 * time.Millisecond)
		return async.Result{
			TaskID: task.ID,
			Output: fmt.Sprintf("%s_processed", task.Data.(string)),
		}
	}
	
	results := pool.ProcessTasks(ctx, tasks, processor)
	
	fmt.Printf("Обработано задач: %d\n", len(results))
	for _, result := range results {
		fmt.Printf("  Задача %d: %v\n", result.TaskID, result.Output)
	}
}
