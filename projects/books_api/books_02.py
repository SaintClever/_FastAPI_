from fastapi import FastAPI, Body
from pydantic import BaseModel

# The three biggest are:
# .dict() function is now renamed to .model_dump()
# schema_extra function within a Config class is now renamed to json_schema_extra
# Optional variables need a =None example: id: Optional[int] = None


app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    id: int
    title: str
    author: str
    description: str
    rating: int


BOOKS = [
    Book(1, "Computer Science Pro", "codingwithroby", "A very nice book!", 5),
    Book(2, "Be Fast with FastAPI", "codingwithroby", "A great book!", 5),
    Book(3, "Master Endpoints", "codingwithroby", "A awesome book!", 5),
    Book(4, "HP1", "Author 1", "Book Description", 2),
    Book(5, "HP2", "Author 2", "Book Description", 3),
    Book(6, "HP3", "Author 3", "Book Description", 1),
]


@app.get("/")
async def read_all_books():
    return BOOKS


@app.post("/create-book")
# Assign an BookRequest to book_request
async def create_book(book_request: BookRequest):
    # dump the information of book_request into Book, which key/values of BookRequest: id=0 title='string' author='string' description='string' rating=0
    new_book = Book(**book_request.model_dump())
    BOOKS.append(new_book)
