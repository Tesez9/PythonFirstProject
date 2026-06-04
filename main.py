from typing import Annotated
from fastapi import FastAPI, HTTPException, status, Query, Cookie
from Models import BookCreate

app = FastAPI(title="Books API")

books_db = [
    {
        "id": 1,
        "title": "Harry",
        "author": "author1"
    }
]


@app.get("/books/search", status_code=status.HTTP_200_OK)
def search_books(
    title: Annotated[
        str | None,
        Query(
            min_length=3,
            max_length=50,
            description="Введите часть названия книги для поиска",
        )
    ] = None
):
    if not title:
        return []
    found_books = [book for book in books_db if title.lower() in book["title"].lower()]
    return found_books


@app.get("/books", status_code=status.HTTP_200_OK)
def get_all_books(
    # Параметр куки
    session_token: Annotated[
        str | None,
        Cookie(description="Токен пользователя")
    ] = None
):
    if session_token:
        print(f"--> Токен пользователя: {session_token}")
    else:
        print("--> Токена нет")
    return books_db


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
def get_book_by_id(book_id: int):
    for book in books_db:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@app.post("/books", status_code=status.HTTP_201_CREATED)
def create_book(book_data: BookCreate):
    new_id = 1 if not books_db else max(b["id"] for b in books_db) + 1
    new_book = {
        "id": new_id,
        **book_data.model_dump()
    }
    books_db.append(new_book)
    return new_book

@app.put("/books/{book_id}", status_code=status.HTTP_200_OK)
def update_book(book_id: int, book_data: BookCreate):
    for book in books_db:
        if book["id"] == book_id:
            book["title"] = book_data.title
            book["author"] = book_data.author
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@app.delete("/books/{book_id}", status_code=status.HTTP_200_OK)
def delete_book(book_id: int):
    for i, book in enumerate(books_db):
        if book["id"] == book_id:
            books_db.pop(i)
            return {"message": "Book deleted"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")