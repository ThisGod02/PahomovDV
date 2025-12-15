package server

import (
	"context"
	"fmt"
	"net/http"
	"sync/atomic"
	"time"
)

// Server представляет HTTP сервер с поддержкой конкурентных запросов
type Server struct {
	router      *http.ServeMux
	requestCount int64
	server      *http.Server
}

// NewServer создаёт новый HTTP сервер
func NewServer(addr string) *Server {
	s := &Server{
		router: http.NewServeMux(),
	}
	
	s.setupRoutes()
	
	s.server = &http.Server{
		Addr:    addr,
		Handler: s.router,
	}
	
	return s
}

// setupRoutes настраивает маршруты сервера
func (s *Server) setupRoutes() {
	s.router.HandleFunc("/", s.handleRoot)
	s.router.HandleFunc("/health", s.handleHealth)
	s.router.HandleFunc("/stats", s.handleStats)
}

// handleRoot обрабатывает корневой запрос
func (s *Server) handleRoot(w http.ResponseWriter, r *http.Request) {
	count := atomic.AddInt64(&s.requestCount, 1)
	time.Sleep(50 * time.Millisecond) // Имитация обработки
	fmt.Fprintf(w, "Hello! Request count: %d\n", atomic.LoadInt64(&s.requestCount))
}

// handleHealth обрабатывает запрос проверки здоровья сервера
func (s *Server) handleHealth(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	w.Write([]byte("OK"))
}

// handleStats обрабатывает запрос статистики
func (s *Server) handleStats(w http.ResponseWriter, r *http.Request) {
	count := atomic.LoadInt64(&s.requestCount)
	fmt.Fprintf(w, "Total requests: %d", count)
}

// Start запускает сервер
func (s *Server) Start() error {
	return s.server.ListenAndServe()
}

// Stop останавливает сервер с graceful shutdown
func (s *Server) Stop(ctx context.Context) error {
	return s.server.Shutdown(ctx)
}

// GetRequestCount возвращает количество обработанных запросов
func (s *Server) GetRequestCount() int64 {
	return atomic.LoadInt64(&s.requestCount)
}
