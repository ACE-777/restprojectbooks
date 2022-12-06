import random
import secrets

import uvicorn
from fastapi import FastAPI

books = {}
reviews = {}

app = FastAPI()
app.type = "00"


class Review():
    def __init__(self, name="Name", bookID=0):
        self.name = name
        self.hateoas = {"books": {"href": "/books/" + str(bookID)}}

    def getJSON(self):
        return {"name": self.name, "hateoas": self.hateoas}


class Book():
    def __init__(self, name="Name"):
        self.name = name
        self.reviews = []
        self.hateoas = {"reviews": {"href": "/reviews"}}

    def addReview(self, index):
        self.reviews.append(index)

    def getJSON(self):
        return {"name": self.name, "reviews": self.reviews, "hateoas": self.hateoas}


def generateBooks():
    for i in range(10):
        indexBook = len(books)
        book = Book(secrets.token_hex(16))
        for k in range(random.randint(0, 10)):
            review = Review(secrets.token_hex(16), indexBook)
            index = len(reviews)
            reviews[index] = review
            book.addReview(index)
        books[indexBook] = book.getJSON()


@app.get("/")
def read_root():
    return {"hateoas": {"book": {"href": "/books"}, "reviews": {"href": "/reviews"}}}


@app.get("/books")
def return_all_books(start: int = 0, limit: int = 0):
    global books

    if limit == 0:
        return books
    else:
        result = {}
        keys = list(books.keys())

        for i in range(start, start + limit + 1):
            key = keys[i]
            result[i] = books.get(key)

        return result


@app.get("/reviews")
def return_all_books(start: int = 0, limit: int = 0):
    global reviews

    if limit == 0:
        return reviews
    else:
        result = {}
        keys = list(reviews.keys())

        for i in range(start, start + limit + 1):
            key = keys[i]
            result[i] = reviews.get(key)

        return result


@app.get("/books/{book_id}")
def read_item(book_id: int):
    return books.get(book_id)


@app.get("/reviews/{book_review_id}")
def return_unic_review(book_review_id: int):
    return reviews.get(book_review_id)


def start():
    uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="info")


generateBooks()

if __name__ == '__main__':
    start()
    print("Something is not quite right")
