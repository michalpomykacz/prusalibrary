import datetime

import pytest

from app.library.models import Book
from app.library.services import borrow_book, return_book


@pytest.mark.component
@pytest.mark.django_db()
class TestServices:

    def test_borrow_book(self):
        book = Book.objects.create(
            isbn="439023483",
            is_available=True,
        )

        borrow_book(book, datetime.datetime(2024, 1, 1, 0, 0))
        book.refresh_from_db()

        assert book.borrowing_count == 1
        assert not book.is_available
        assert book.avg_borrowing_time == 0

    def test_return_book(self):
        book = Book.objects.create(
            isbn="439023483",
            borrowing_count=1,
            is_available=False,
        )
        book.borrowing_set.create(borrow_dt=datetime.datetime(2024, 1, 1, 0, 0))

        return_book(book, datetime.datetime(2024, 1, 10, 0, 0))
        book.refresh_from_db()

        assert book.borrowing_count == 1
        assert book.is_available
        assert book.avg_borrowing_time == 9
