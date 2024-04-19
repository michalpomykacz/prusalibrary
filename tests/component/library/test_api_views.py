import datetime
import zoneinfo

import pytest
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from app.library import api_views
from app.library.models import Book


@pytest.mark.component
@pytest.mark.django_db()
class TestLibraryAPIView:

    def test_get_books(self, api_rf: APIRequestFactory, books_in_db: list[Book]):
        request = api_rf.get(reverse("library:books"))
        response = api_views.BookList.as_view()(request)

        assert response.status_code == 200
        assert response.data == [
            {
                "id": 1,
                "isbn": "439023483",
                "title": "The Hunger Games",
                "is_available": True,
                "original_publication_year": 2008,
                "avg_borrowing_time": 12000,
                "borrowing_count": 0,
                "authors": [{"name": "Suzanne Collins"}],
            },
            {
                "id": 2,
                "isbn": "439554934",
                "title": "Harry Potter and the Philosopher's Stone",
                "is_available": False,
                "original_publication_year": 1997,
                "avg_borrowing_time": 21000,
                "borrowing_count": 0,
                "authors": [{"name": "J.K. Rowling"}, {"name": "Mary GrandPré"}],
            },
        ]

    def test_get_filtered_books(
        self, api_rf: APIRequestFactory, books_in_db: list[Book]
    ):
        request = api_rf.get(reverse("library:books"), {"title": "Harry"})
        response = api_views.BookList.as_view()(request)

        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data.pop()["isbn"] == "439554934"

    def test_get_book_detail(self, api_rf: APIRequestFactory, books_in_db: list[Book]):
        searched_book = books_in_db[0]
        request = api_rf.get(reverse("library:book", kwargs={"pk": searched_book.pk}))
        response = api_views.BookDetail.as_view()(request, pk=searched_book.pk)

        assert response.status_code == 200
        assert response.data["isbn"] == "439023483"

    def test_borrow_book(self, api_rf: APIRequestFactory, mocker):
        book = Book.objects.create(
            isbn="439023483",
            is_available=True,
        )
        request = api_rf.post(
            reverse("library:book_borrowing"),
            {"borrow_dt": "2024-01-01", "book": book.pk},
            format="json",
        )
        mocked_borrow_book = mocker.patch.object(api_views, "borrow_book")
        response = api_views.BookBorrowing.as_view()(request)

        assert response.status_code == 201
        mocked_borrow_book.assert_called_with(
            book=book,
            borrow_dt=datetime.datetime(
                2024, 1, 1, tzinfo=zoneinfo.ZoneInfo(key="UTC")
            ),
        )

    def test_return_book(self, api_rf: APIRequestFactory, mocker):
        book = Book.objects.create(
            isbn="439023483",
            is_available=False,
        )
        book.borrowing_set.create(borrow_dt="2024-01-01")
        request = api_rf.post(
            reverse("library:book_return"),
            {"return_dt": "2024-01-10", "book": book.pk},
            format="json",
        )
        mocked_return_book = mocker.patch.object(api_views, "return_book")
        response = api_views.BookReturn.as_view()(request)

        assert response.status_code == 200
        mocked_return_book.assert_called_with(
            book=book,
            return_dt=datetime.datetime(
                2024, 1, 10, tzinfo=zoneinfo.ZoneInfo(key="UTC")
            ),
        )
