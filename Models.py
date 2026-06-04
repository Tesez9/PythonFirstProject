from pydantic import BaseModel, Field


class BookCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=100,
        description="Название книги (от 1 до 100 символов)",
    )
    author: str = Field(
        min_length=1,
        max_length=100,
        description="Автор книги (от 1 до 100 символов)",
    )