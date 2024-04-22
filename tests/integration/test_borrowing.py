import pytest
import requests
from pytest_django.live_server_helper import LiveServer

from app.library.models import Book


@pytest.mark.integration
@pytest.mark.django_db()
class TestBorrowingAPI:

    def test_borrow_book(self, live_server: LiveServer, available_book: Book):
        payload = {
            "book": available_book.id,
            "borrow_dt": "2024-01-01T00:00:00Z",
        }

        response = requests.post(f"{live_server.url}/api/v1/books/borrow", json=payload)
        assert response.status_code == 201

    def test_return_book(self, live_server: LiveServer, borrowed_book: Book):
        payload = {
            "book": borrowed_book.id,
            "return_dt": "2024-01-01T00:00:00Z",
        }

        response = requests.post(f"{live_server.url}/api/v1/books/return", json=payload)
        assert response.status_code == 200
