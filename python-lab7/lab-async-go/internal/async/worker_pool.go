package async

import (
	"context"
	"sync"
	"time"
)

// Task представляет задачу для обработки воркером
type Task struct {
	ID   int
	Data interface{}
}

// Result представляет результат обработки задачи
type Result struct {
	TaskID int
	Output interface{}
	Error  error
}

// WorkerPool представляет пул воркеров для обработки задач
type WorkerPool struct {
	workersCount int
	tasks        chan Task
	results      chan Result
	wg           sync.WaitGroup
}

// NewWorkerPool создаёт новый пул воркеров
func NewWorkerPool(workers int) *WorkerPool {
	return &WorkerPool{
		workersCount: workers,
		tasks:        make(chan Task, workers*2),
		results:      make(chan Result, workers*2),
	}
}

// Start запускает воркеров для обработки задач
func (wp *WorkerPool) Start(ctx context.Context, processor func(Task) Result) {
	for i := 0; i < wp.workersCount; i++ {
		wp.wg.Add(1)
		go func(workerID int) {
			defer wp.wg.Done()
			for {
				select {
				case task, ok := <-wp.tasks:
					if !ok {
						return
					}
					result := processor(task)
					select {
					case wp.results <- result:
					case <-ctx.Done():
						return
					}
				case <-ctx.Done():
					return
				}
			}
		}(i)
	}
}

// Submit отправляет задачу в пул
func (wp *WorkerPool) Submit(task Task) {
	wp.tasks <- task
}

// GetResults возвращает канал с результатами
func (wp *WorkerPool) GetResults() <-chan Result {
	return wp.results
}

// Stop останавливает пул воркеров
func (wp *WorkerPool) Stop() {
	close(wp.tasks)
	wp.wg.Wait()
	close(wp.results)
}

// ProcessTasks обрабатывает список задач и возвращает результаты
func (wp *WorkerPool) ProcessTasks(ctx context.Context, tasks []Task, processor func(Task) Result) []Result {
	go wp.Start(ctx, processor)
	
	for _, task := range tasks {
		select {
		case wp.tasks <- task:
		case <-ctx.Done():
			return nil
		}
	}
	
	// Закрываем канал задач после отправки всех задач
	go func() {
		time.Sleep(100 * time.Millisecond) // Даём время на отправку
		close(wp.tasks)
	}()
	
	var results []Result
	for i := 0; i < len(tasks); i++ {
		select {
		case result, ok := <-wp.results:
			if !ok {
				return results
			}
			results = append(results, result)
		case <-ctx.Done():
			return results
		}
	}
	
	return results
}
