import datetime
import zoneinfo

import pytest

from app.library.models import Book
from app.library.serializers import BookBorrowingSerializer, BookReturnSerializer


@pytest.mark.component
@pytest.mark.django_db()
class TestBorrowingSerializer:

    def test_create_book_borrowing(self):
        book = Book.objects.create(
            isbn="123456789", title="Test Book", is_available=True
        )

        serializer = BookBorrowingSerializer(
            data={"book": book.id, "borrow_dt": "2024-01-01"}
        )

        assert serializer.is_valid()
        assert serializer.validated_data == {
            "book": book,
            "borrow_dt": datetime.datetime(
                2024, 1, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="UTC")
            ),
        }

    def test_create_book_borrowing_book_not_exists(self):
        serializer = BookBorrowingSerializer(
            data={"book": 1, "borrow_dt": "2024-01-01"}
        )

        assert not serializer.is_valid()
        assert 'Invalid pk "1" - object does not exist.' in str(serializer.errors)

    def test_create_book_borrowing_not_available(self):
        book = Book.objects.create(
            isbn="123456789", title="Test Book", is_available=False
        )

        serializer = BookBorrowingSerializer(
            data={"book": book.id, "borrow_dt": "2024-01-01"}
        )

        assert not serializer.is_valid()
        assert "Book is not available." in str(serializer.errors)


@pytest.mark.component
@pytest.mark.django_db()
class TestBorrowingUpdateSerializer:

    def test_update_book_borrowing(self):
        book = Book.objects.create(
            isbn="123456789", title="Test Book", is_available=False
        )
        book.borrowing_set.create(borrow_dt="2024-01-01")

        serializer = BookReturnSerializer(
            data={"book": book.id, "return_dt": "2024-01-01"}
        )

        assert serializer.is_valid()
        assert serializer.validated_data == {
            "book": book,
            "return_dt": datetime.datetime(
                2024, 1, 1, 0, 0, tzinfo=zoneinfo.ZoneInfo(key="UTC")
            ),
        }

    def test_update_book_borrowing_not_borrowed(self):
        book = Book.objects.create(
            isbn="123456789", title="Test Book", is_available=False
        )
        book.borrowing_set.create(borrow_dt="2024-01-01", return_dt="2024-01-02")

        serializer = BookReturnSerializer(
            data={"book": book.id, "return_dt": "2024-01-03"}
        )

        assert not serializer.is_valid()
        assert "Book is not borrowed." in str(serializer.errors)
