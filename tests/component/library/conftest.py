import pytest

from app.library.models import Book


@pytest.fixture
def available_book():
    return Book.objects.create(
        isbn="439023483",
        title="The Hunger Games",
        is_available=True,
    )
