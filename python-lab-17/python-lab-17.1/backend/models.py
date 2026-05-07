from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Genre(str, Enum):
    FICTION = "fiction"
    NON_FICTION = "non_fiction"
    SCIENCE = "science"
    FANTASY = "fantasy"
    MYSTERY = "mystery"
    BIOGRAPHY = "biography"


class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Book title")
    author: str = Field(..., min_length=1, max_length=100, description="Book author")
    genre: Genre = Field(..., description="Book genre")
    publication_year: int = Field(..., ge=1000, le=date.today().year, description="Publication year")
    pages: int = Field(..., gt=0, description="Page count")
    isbn: str = Field(..., pattern=r"^\d{13}$", description="ISBN with 13 digits")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "War and Peace",
                "author": "Leo Tolstoy",
                "genre": "fiction",
                "publication_year": 1869,
                "pages": 1225,
                "isbn": "9781234567897",
            }
        }
    )


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    genre: Optional[Genre] = None
    publication_year: Optional[int] = Field(None, ge=1000, le=date.today().year)
    pages: Optional[int] = Field(None, gt=0)
    isbn: Optional[str] = Field(None, pattern=r"^\d{13}$")


class BookResponse(BookCreate):
    id: int
    available: bool = True

    model_config = ConfigDict(from_attributes=True)


class BookDetailResponse(BookResponse):
    borrowed_by: Optional[str] = None
    borrowed_date: Optional[date] = None
    return_date: Optional[date] = None


class BorrowRequest(BaseModel):
    borrower_name: str = Field(..., min_length=1, max_length=100)
    return_days: int = Field(7, ge=1, le=30, description="Return period in days")
