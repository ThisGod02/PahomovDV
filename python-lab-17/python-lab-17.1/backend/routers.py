from fastapi import APIRouter, HTTPException, Depends, Query, status
from typing import List, Optional
from datetime import date, timedelta

from models import BookCreate, BookResponse, BookUpdate, BorrowRequest, BookDetailResponse, Genre
import database

router = APIRouter()

# GET /books - получение списка всех книг с фильтрацией
@router.get("/books", response_model=List[BookResponse])
async def get_books(
    genre: Optional[Genre] = Query(None, description="Фильтр по жанру"),
    author: Optional[str] = Query(None, description="Фильтр по автору"),
    available_only: bool = Query(False, description="Только доступные книги"),
    skip: int = Query(0, ge=0, description="Количество книг для пропуска"),
    limit: int = Query(10, ge=1, le=100, description="Лимит книг на странице")
):
    """
    Получить список книг с возможностью фильтрации.
    """
    filtered_books = []
    
    for book_id, book_data in database.books_db.items():
        # Фильтрация по жанру
        if genre and book_data["genre"] != genre:
            continue
            
        # Фильтрация по автору (регистронезависимый поиск)
        if author and author.lower() not in book_data["author"].lower():
            continue
            
        # Фильтрация по доступности
        if available_only and not book_data.get("available", True):
            continue
        
        filtered_books.append(database.book_to_response(book_id, book_data))
    
    # Пагинация
    return filtered_books[skip : skip + limit]

# GET /books/{book_id} - получение книги по ID
@router.get("/books/{book_id}", response_model=BookDetailResponse)
async def get_book(book_id: int):
    """
    Получить информацию о книге по её ID.
    """
    if book_id not in database.books_db:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    
    book_data = database.books_db[book_id]
    response = BookDetailResponse(
        id=book_id,
        title=book_data["title"],
        author=book_data["author"],
        genre=book_data["genre"],
        publication_year=book_data["publication_year"],
        pages=book_data["pages"],
        isbn=book_data["isbn"],
        available=book_data.get("available", True)
    )
    
    # Если книга взята, добавляем информацию о заимствовании
    if book_id in database.borrow_records:
        borrow_info = database.borrow_records[book_id]
        response.borrowed_by = borrow_info["borrower_name"]
        response.borrowed_date = borrow_info["borrowed_date"]
        response.return_date = borrow_info["return_date"]
    
    return response

# POST /books - создание новой книги
@router.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate):
    """
    Создать новую книгу в библиотеке.
    """
    # Проверка уникальности ISBN
    for b in database.books_db.values():
        if b["isbn"] == book.isbn:
            raise HTTPException(status_code=400, detail="Книга с таким ISBN уже существует")
    
    book_id = database.get_next_id()
    book_dict = book.model_dump()
    book_dict["available"] = True
    database.books_db[book_id] = book_dict
    
    return database.book_to_response(book_id, database.books_db[book_id])

# PUT /books/{book_id} - полное обновление книги
@router.put("/books/{book_id}", response_model=BookResponse)
async def update_book(book_id: int, book_update: BookUpdate):
    """
    Обновить информацию о книге.
    """
    if book_id not in database.books_db:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    
    current_data = database.books_db[book_id]
    update_data = book_update.model_dump(exclude_unset=True)
    
    # Если передается ISBN, проверьте его уникальность (кроме самой этой книги)
    if "isbn" in update_data:
        for bid, b in database.books_db.items():
            if bid != book_id and b["isbn"] == update_data["isbn"]:
                raise HTTPException(status_code=400, detail="Книга с таким ISBN уже существует")
    
    # Обновляем поля
    for key, value in update_data.items():
        current_data[key] = value
        
    database.books_db[book_id] = current_data
    return database.book_to_response(book_id, database.books_db[book_id])

# DELETE /books/{book_id} - удаление книги
@router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    """
    Удалить книгу из библиотеки.
    """
    if book_id not in database.books_db:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    
    # Если книга взята, нельзя её удалить
    if not database.books_db[book_id].get("available", True):
        raise HTTPException(status_code=400, detail="Нельзя удалить книгу, которая находится на руках")
    
    del database.books_db[book_id]
    if book_id in database.borrow_records:
        del database.borrow_records[book_id]
    
    return None

# POST /books/{book_id}/borrow - заимствование книги
@router.post("/books/{book_id}/borrow", response_model=BookDetailResponse)
async def borrow_book(book_id: int, borrow_request: BorrowRequest):
    """
    Взять книгу из библиотеки.
    """
    if book_id not in database.books_db:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    
    if not database.books_db[book_id].get("available", True):
        raise HTTPException(status_code=400, detail="Книга уже занята")
    
    # Обновляем статус
    database.books_db[book_id]["available"] = False
    
    # Создаем запись о заимствовании
    borrow_info = {
        "borrower_name": borrow_request.borrower_name,
        "borrowed_date": date.today(),
        "return_date": date.today() + timedelta(days=borrow_request.return_days)
    }
    database.borrow_records[book_id] = borrow_info
    
    # Получаем базовый ответ
    book_resp = database.book_to_response(book_id, database.books_db[book_id])
    
    # Добавляем детали детального ответа
    return BookDetailResponse(
        **book_resp.model_dump(),
        borrowed_by=borrow_info["borrower_name"],
        borrowed_date=borrow_info["borrowed_date"],
        return_date=borrow_info["return_date"]
    )

# POST /books/{book_id}/return - возврат книги
@router.post("/books/{book_id}/return", response_model=BookResponse)
async def return_book(book_id: int):
    """
    Вернуть книгу в библиотеку.
    """
    if book_id not in database.books_db:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    
    if database.books_db[book_id].get("available", True):
        raise HTTPException(status_code=400, detail="Книга уже находится в библиотеке")
    
    # Обновляем статус
    database.books_db[book_id]["available"] = True
    
    # Удаляем запись о заимствовании
    if book_id in database.borrow_records:
        del database.borrow_records[book_id]
    
    return database.book_to_response(book_id, database.books_db[book_id])

# GET /stats - статистика библиотеки
@router.get("/stats")
async def get_library_stats():
    """
    Получить статистику библиотеки.
    """
    total_books = len(database.books_db)
    available_books = sum(1 for b in database.books_db.values() if b.get("available", True))
    borrowed_books = total_books - available_books
    
    # Распределение по жанрам
    genres = {}
    for b in database.books_db.values():
        g = b["genre"]
        genres[g] = genres.get(g, 0) + 1
        
    # Самый плодовитый автор
    authors = {}
    for b in database.books_db.values():
        a = b["author"]
        authors[a] = authors.get(a, 0) + 1
    
    prolific_author = max(authors, key=authors.get) if authors else None
    
    return {
        "total_books": total_books,
        "available_books": available_books,
        "borrowed_books": borrowed_books,
        "books_by_genre": genres,
        "most_prolific_author": prolific_author
    }
