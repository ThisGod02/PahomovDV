package async

import (
	"context"
	"time"
)

// MergeChannels объединяет несколько каналов в один
func MergeChannels(ctx context.Context, chs ...<-chan int) <-chan int {
	out := make(chan int)
	
	for _, ch := range chs {
		go func(c <-chan int) {
			defer func() {
				// Закрываем out только когда все горутины завершены
				// Это упрощённая версия, в реальности нужен более сложный механизм
			}()
			for {
				select {
				case val, ok := <-c:
					if !ok {
						return
					}
					select {
					case out <- val:
					case <-ctx.Done():
						return
					}
				case <-ctx.Done():
					return
				}
			}
		}(ch)
	}
	
	return out
}

// BufferedChannelProcessor обрабатывает значения из входного канала
// и отправляет результаты в выходной буферизованный канал
func BufferedChannelProcessor(input <-chan int, bufferSize int) <-chan int {
	output := make(chan int, bufferSize)
	
	go func() {
		defer close(output)
		for val := range input {
			output <- val * 2 // Простая обработка: умножение на 2
		}
	}()
	
	return output
}

// Producer создаёт канал и отправляет в него значения
func Producer(ctx context.Context, count int) <-chan int {
	out := make(chan int)
	go func() {
		defer close(out)
		for i := 0; i < count; i++ {
			select {
			case out <- i:
			case <-ctx.Done():
				return
			}
			time.Sleep(100 * time.Millisecond)
		}
	}()
	return out
}

// Consumer обрабатывает значения из канала с таймаутом
func Consumer(ctx context.Context, input <-chan int, timeout time.Duration) []int {
	var results []int
	timeoutChan := time.After(timeout)
	
	for {
		select {
		case val, ok := <-input:
			if !ok {
				return results
			}
			results = append(results, val)
		case <-timeoutChan:
			return results
		case <-ctx.Done():
			return results
		}
	}
}
