from datetime import datetime
import itertools

import pytest
from rest_framework.test import APIRequestFactory

from app.library.models import Book, Borrowing


@pytest.fixture
def api_rf() -> APIRequestFactory:
    return APIRequestFactory()


@pytest.fixture
def books_with_borrowing_history(books_in_db: list[Book]) -> list[Book]:

    history = (
        (datetime(2024, 1, 1, 0, 0), datetime(2024, 1, 2)),
        (datetime(2024, 1, 2, 0, 0), datetime(2024, 1, 15)),
        (datetime(2024, 1, 15, 0, 0), datetime(2024, 1, 20)),
    )

    borrowings = []

    for book, dates in itertools.product(books_in_db, history):
        borrowings.append(Borrowing(book=book, borrow_dt=dates[0], return_dt=dates[1]))

    Borrowing.objects.bulk_create(borrowings)

    return books_in_db
