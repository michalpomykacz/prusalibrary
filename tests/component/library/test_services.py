import datetime

import pytest

from app.library.exceptions import LibraryError
from app.library.models import Book
from app.library.services import borrow_book, return_book


@pytest.mark.component
@pytest.mark.django_db()
class TestServices:

    def test_borrow_book(self, available_book):

        borrow_book(available_book, datetime.datetime(2024, 1, 1, 0, 0))
        available_book.refresh_from_db()

        assert available_book.borrowing_count == 1
        assert not available_book.is_available
        assert available_book.avg_borrowing_time == 0

    def test_book_cannot_be_borrowed_twice_at_time(self, available_book):
        borrow_book(available_book, datetime.datetime(2024, 1, 1, 0, 0))
        with pytest.raises(LibraryError) as e:
            borrow_book(available_book, datetime.datetime(2024, 1, 1, 0, 0))

        assert str(e.value) == "The book has been borrowed in the meantime."

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
