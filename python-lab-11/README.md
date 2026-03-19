# Лабораторная работа №11: Бэкенд-разработка (API)

Данная лабораторная работа посвящена изучению основ серверной разработки на Python (FastAPI) и Node.js (Express).

## Структура проекта

- `book_api/`: REST API для управления библиотекой книг (FastAPI).
- `task-api/`: REST API для управления задачами (Express).

## Инструкции по запуску

### Часть 1: FastAPI (Библиотека книг)
```bash
cd book_api
# Создание и активация виртуального окружения
python -m venv venv
venv\Scripts\activate  # Для Windows
# Установка зависимостей
pip install -r requirements.txt
# Запуск сервера
python main.py
```

### Часть 2: Express (Менеджер задач)
```bash
cd task-api
npm install
# Запуск в режиме разработки
npm run dev
```
