from datetime import datetime

import pytest

from app.library.models import Book, Author, Borrowing


@pytest.fixture()
def books_in_db() -> list[Book]:

    author1 = Author.objects.create(name="Suzanne Collins")

    book1 = Book.objects.create(
        title="The Hunger Games",
        isbn="439023483",
        language_code="eng",
        original_publication_year=2008,
        avg_borrowing_time=12000,
        is_available=True,
    )
    book1.authors.add(author1)

    author2 = Author.objects.create(name="J.K. Rowling")
    author3 = Author.objects.create(name="Mary GrandPré")

    book2 = Book.objects.create(
        title="Harry Potter and the Philosopher's Stone",
        isbn="439554934",
        language_code="eng",
        original_publication_year=1997,
        avg_borrowing_time=21000,
        is_available=False,
    )
    book2.authors.add(author2, author3)

    return [book1, book2]


@pytest.fixture()
def available_book() -> Book:
    return Book.objects.create(
        isbn="439023483",
        title="The Hunger Games",
        is_available=True,
    )


@pytest.fixture
def borrowed_book() -> Book:
    book = Book.objects.create(
        isbn="439023483",
        title="The Hunger Games",
        is_available=False,
    )
    Borrowing.objects.create(book=book, borrow_dt=datetime(2024, 1, 1, 0, 0))
    return book
