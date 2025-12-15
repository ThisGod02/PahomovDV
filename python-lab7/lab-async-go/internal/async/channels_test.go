package async

import (
	"context"
	"testing"
	"time"
)

func TestMergeChannels(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel()
	
	ch1 := make(chan int)
	ch2 := make(chan int)
	
	go func() {
		defer close(ch1)
		for i := 0; i < 3; i++ {
			ch1 <- i
		}
	}()
	
	go func() {
		defer close(ch2)
		for i := 3; i < 6; i++ {
			ch2 <- i
		}
	}()
	
	merged := MergeChannels(ctx, ch1, ch2)
	
	var results []int
	timeout := time.After(1 * time.Second)
	
	for {
		select {
		case val, ok := <-merged:
			if !ok {
				goto done
			}
			results = append(results, val)
		case <-timeout:
			goto done
		case <-ctx.Done():
			goto done
		}
	}
	
done:
	// Проверяем, что получили хотя бы некоторые значения
	if len(results) == 0 {
		t.Error("Expected at least some values from merged channels")
	}
}

func TestBufferedChannelProcessor(t *testing.T) {
	input := make(chan int, 5)
	
	for i := 1; i <= 5; i++ {
		input <- i
	}
	close(input)
	
	output := BufferedChannelProcessor(input, 3)
	
	expected := []int{2, 4, 6, 8, 10}
	var results []int
	
	for val := range output {
		results = append(results, val)
	}
	
	if len(results) != len(expected) {
		t.Errorf("Expected %d results, got %d", len(expected), len(results))
	}
	
	for i, val := range results {
		if val != expected[i] {
			t.Errorf("Expected %d at position %d, got %d", expected[i], i, val)
		}
	}
}

func TestChannelTimeout(t *testing.T) {
	ch := make(chan int)
	
	select {
	case <-ch:
		t.Error("Should not receive from channel")
	case <-time.After(100 * time.Millisecond):
		// Ожидаемое поведение - таймаут
	}
}

func TestProducer(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 1*time.Second)
	defer cancel()
	
	ch := Producer(ctx, 5)
	
	var results []int
	timeout := time.After(800 * time.Millisecond)
	
	for {
		select {
		case val, ok := <-ch:
			if !ok {
				goto done
			}
			results = append(results, val)
		case <-timeout:
			goto done
		case <-ctx.Done():
			goto done
		}
	}
	
done:
	if len(results) == 0 {
		t.Error("Expected at least some values from producer")
	}
}

func TestConsumer(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel()
	
	input := make(chan int)
	go func() {
		defer close(input)
		for i := 0; i < 5; i++ {
			input <- i
			time.Sleep(50 * time.Millisecond)
		}
	}()
	
	results := Consumer(ctx, input, 1*time.Second)
	
	if len(results) == 0 {
		t.Error("Expected at least some values from consumer")
	}
}

func TestConsumer_Timeout(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel()
	
	input := make(chan int)
	// Не закрываем канал, чтобы проверить таймаут
	
	results := Consumer(ctx, input, 100*time.Millisecond)
	
	// Должен вернуть пустой результат из-за таймаута
	if len(results) != 0 {
		t.Errorf("Expected empty results due to timeout, got %d", len(results))
	}
}

func BenchmarkBufferedChannelProcessor(b *testing.B) {
	input := make(chan int, 100)
	
	go func() {
		defer close(input)
		for i := 0; i < 1000; i++ {
			input <- i
		}
	}()
	
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		output := BufferedChannelProcessor(input, 10)
		for range output {
		}
	}
}

