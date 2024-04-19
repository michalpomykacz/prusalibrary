import pytest

from app.library.models import Book, Borrowing


@pytest.mark.component
@pytest.mark.django_db()
class TestBookManager:

    def test_get_book_avg_borrowing_time(
        self, books_with_borrowing_history: list[Book]
    ):
        avg_borrowing_time = Borrowing.objects.book_avg_borrowing_time(
            books_with_borrowing_history[0].id
        )

        assert avg_borrowing_time == 6

    def test_get_book_avg_borrowing_time_no_history(self):
        book = Book.objects.create(isbn="123456789", title="Test Book")

        avg_borrowing_time = Borrowing.objects.book_avg_borrowing_time(book.id)

        assert avg_borrowing_time == 0

    def test_is_book_borrowed(self):
        book = Book.objects.create(isbn="123456789", title="Test Book")
        book.borrowing_set.create(borrow_dt="2024-01-01")

        assert Borrowing.objects.is_book_borrowed(book.id)

    def test_is_book_not_borrowed(self):
        book = Book.objects.create(isbn="123456789", title="Test Book")

        assert not Borrowing.objects.is_book_borrowed(book.id)
