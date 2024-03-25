from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

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
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


# We use the bookRequest for a put or post becase the user in posting or puting information / createding or updating data
class BookRequest(BaseModel):
    id: Optional[int] = Field(default=None, description="id is not needed")
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1000, lt=3000)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "A new book",
                "author": "codingwithroby",
                "description": "A new description of a book",
                "rating": 5,
                "published_date": 2012,
            }
        }


BOOKS = [
    Book(1, "Computer Science Pro", "codingwithroby", "A very nice book!", 5, 1881),
    Book(2, "Be Fast with FastAPI", "codingwithroby", "A great book!", 5, 1912),
    Book(3, "Master Endpoints", "codingwithroby", "A awesome book!", 5, 1996),
    Book(4, "HP1", "Author 1", "Book Description", 2, 2024),
    Book(5, "HP2", "Author 2", "Book Description", 3, 2015),
    Book(6, "HP3", "Author 3", "Book Description", 1, 1996),
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}")
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Item not found")


@app.get("/books/")
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []

    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


# A query param has a trailing forward slash /
# @app.get("/books/publication/")


# A query param doesn't have a forward slach
# @app.get("/books/publication/{book_published_date}")


# A query param with a path has a slash
# @app.get("/books/publication/{book_published_date}/")
@app.get("/books/publish/")
async def read_book_by_publish_date(book_published_date: int = Query(gt=1000, lt=3000)):
    books_to_return = []

    for book in BOOKS:
        if book_published_date == book.published_date:
            books_to_return.append(book)

    return books_to_return


# Because we're creating data we need to use the BookRequest Scheme / blueprint. It's our body. Goes through scheme first
@app.post("/create-book")
# Assign an BookRequest to book_request
async def create_book(book_request: BookRequest):
    # dump the information of book_request into Book, which key/values of BookRequest: id=0 title='string' author='string' description='string' rating=0
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    # if len(BOOKS) > 0:
    #     book.id = BOOKS[-1].id + 1
    # else:
    #     book.id = 1

    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


# Because we're updating data we need to use the BookRequest Scheme / blueprint. It's our body. Goes through scheme first
@app.put("/books/update_book")
async def update_book(book: BookRequest):
    book_changed = False

    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True

    if not book_changed:
        raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/books/{book_id}")
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False

    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break

    if not book_changed:
        raise HTTPException(status_code=404, detail="Item not found")
