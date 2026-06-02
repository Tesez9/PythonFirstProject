from fastapi import FastAPI

app = FastAPI()
books = []

@app.get("/books")
async def get_books():
    return books

@app.get("/books/search")
async def search_books(title: str):
    result = []
    for book in books:
        if title.lower() in book["title"].lower():
            result.append(book)
    return result

@app.get("/books/{book_id}")
async def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    return {"message": "Book not found"}

@app.post("/books")
async def create_book(title: str, author: str):
    book = {
        "id": len(books) + 1,
        "title": title,
        "author": author
    }
    books.append(book)
    return book

@app.put("/books/{book_id}")
async def update_book(book_id: int, title: str, author: str):
    for book in books:
        if book["id"] == book_id:
            book["title"] = title
            book["author"] = author
            return book
    return {"message": "Book not found"}

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return {"message": "Book deleted"}
    return {"message": "Book not found"}