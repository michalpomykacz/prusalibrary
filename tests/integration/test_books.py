import pytest
import requests
from pytest_django.live_server_helper import LiveServer

from app.library.models import Book


@pytest.mark.integration
@pytest.mark.django_db()
class TestBooksAPI:

    def test_book_list(self, live_server: LiveServer, books_in_db: list[Book]):
        response = requests.get(
            f"{live_server.url}/api/v1/books?avg_borrowing_time__gte=13000"
        )
        assert response.status_code == 200
        assert response.json() == [
            {
                "id": 2,
                "isbn": "439554934",
                "title": "Harry Potter and the Philosopher's Stone",
                "is_available": False,
                "original_publication_year": 1997,
                "avg_borrowing_time": 21000,
                "borrowing_count": 0,
                "authors": [{"name": "J.K. Rowling"}, {"name": "Mary GrandPré"}],
            }
        ]

    def test_book_detail(self, live_server: LiveServer, books_in_db: list[Book]):
        book = books_in_db[0]
        response = requests.get(f"{live_server.url}/api/v1/books/{book.id}")
        assert response.status_code == 200
        assert response.json() == {
            "id": book.id,
            "isbn": "439023483",
            "title": "The Hunger Games",
            "is_available": True,
            "original_publication_year": 2008,
            "avg_borrowing_time": 12000,
            "borrowing_count": 0,
            "authors": [{"name": "Suzanne Collins"}],
        }
