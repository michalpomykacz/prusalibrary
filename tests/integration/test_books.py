import pytest
import requests

from app.library.models import Book


@pytest.mark.integration
@pytest.mark.django_db()
class TestBooks:

    @pytest.mark.skip
    def test_book_list(self, live_server, books_in_db: list[Book]):
        response = requests.get(f"{live_server.url}/api/v1/books")
        assert response.status_code == 200

    # TODO to be done
